package Mneme::Handoff;

use strict;
use warnings;
use bytes;
use utf8;
use JSON::PP ();
use Digest::SHA qw(sha256_hex);
use Encode qw(decode encode FB_CROAK);
use Fcntl qw(:DEFAULT :mode O_NOFOLLOW);
use File::Basename qw(dirname);
use File::Spec ();
use File::Temp ();
use Cwd qw(abs_path);
use POSIX qw(strftime);
use IO::Handle ();
use IPC::Open3 qw(open3);
use Symbol qw(gensym);
use Getopt::Long qw(GetOptionsFromArray);
use Time::Piece ();

our $VERSION = '1.0';
our $ACTIVE_LOCK_NAME = '';

use constant REPOSITORY_ROOT => '/Users/bogac/dev/forgejo/mneme';
use constant STORE_RELATIVE  => '.mneme-local/handoffs/v1';
use constant GIT_PATH        => '/Library/Developer/CommandLineTools/usr/bin/git';
use constant PERL_PATH       => '/usr/bin/perl';
use constant ENV_PATH        => '/usr/bin/env';
use constant FALSE_PATH      => '/usr/bin/false';

use constant MAX_PACKET_NUMBER => 999_999;
use constant MAX_SOURCES       => 64;
use constant MAX_REQUEST_BYTES => 262_144;
use constant MAX_SOURCE_BYTES  => 8_388_608;
use constant MAX_SOURCE_TOTAL  => 33_554_432;
use constant MAX_JSON_BYTES    => 262_144;
use constant MAX_TSV_BYTES     => 262_144;
use constant MAX_VERDICT_BYTES => 65_536;
use constant MAX_APPROVAL_BYTES => 32_768;
use constant MAX_RECEIPT_BYTES => 65_536;
use constant MAX_ROLLBACK_BYTES => 32_768;
use constant MAX_JSON_DEPTH    => 16;
use constant MAX_ARRAY_ITEMS   => 64;
use constant MAX_PATH_BYTES    => 1_024;
use constant MAX_SEGMENT_BYTES => 255;
use constant MAX_STATUS_ITEMS  => 4_096;
use constant MAX_GIT_STREAM    => 8_388_608;

our %BINARY_IDENTITIES = (
    perl => {
        path   => PERL_PATH,
        bytes  => 167_184,
        sha256 => '85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc',
    },
    env => {
        path   => ENV_PATH,
        bytes  => 167_712,
        sha256 => '2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0',
    },
    false => {
        path   => FALSE_PATH,
        bytes  => 133_184,
        sha256 => 'ccdd13063a974daa3ffcb707ac70104fb642eaf4aab3b621e816f36e2e8b59ab',
    },
    git => {
        path   => GIT_PATH,
        bytes  => 3_837_392,
        sha256 => 'a73bf622a2e470d5d57a4b1d5aef1e8680e67278018d4858a2f93825b7d595c7',
    },
);

our @SOURCE_ROLES = qw(proposal evidence governing-input supporting-record);
our @APPROVAL_GATES = qw(
    planning-review
    implementation-review
    execution-authorization
    evidence-acceptance
    commit-authorization
);
our @VERDICTS = qw(Approve Reject ChangesRequested);
our @STATES = qw(
    Invalid
    Conflict
    Stale
    RolledBack
    Rejected
    ChangesRequested
    Consumed
    Pending
);

our %EXIT_CODE = (
    success    => 0,
    usage      => 10,
    invalid    => 20,
    stale      => 21,
    conflict   => 22,
    approval   => 23,
    repository => 24,
    unsafe     => 25,
    lock       => 26,
    limit      => 27,
    runtime    => 28,
    uncertain  => 29,
    internal   => 30,
);

our $JSON = JSON::PP->new->canonical(1)->utf8(1)->allow_nonref(0)->pretty(0);
our $JSON_ATOM = JSON::PP->new->canonical(1)->utf8(1)->allow_nonref(1)->pretty(0);

sub _fail {
    my ($code, $detail) = @_;
    $code = 'E_INTERNAL' if !defined $code || $code eq '';
    $detail = '' if !defined $detail;
    $detail =~ s/[\r\n\0]/ /g;
    die "MNEME_HANDOFF:$code:$detail\n";
}

sub failure_code {
    my ($error) = @_;
    return '' if !defined $error;
    return $1 if $error =~ /MNEME_HANDOFF:([A-Z0-9_]+):/;
    return 'E_INTERNAL';
}

sub canonical_json {
    my ($value) = @_;
    _validate_json_shape($value, 0);
    return $JSON->encode($value) . "\n";
}

sub decode_canonical_json {
    my ($bytes_value, $limit) = @_;
    $limit = MAX_JSON_BYTES if !defined $limit;
    _fail('E_LIMIT_JSON', 'json exceeds byte limit') if length($bytes_value) > $limit;
    _fail('E_JSON_NUL', 'json contains NUL') if index($bytes_value, "\0") >= 0;
    _fail('E_JSON_CR', 'json contains CR') if index($bytes_value, "\r") >= 0;
    _fail('E_JSON_LF', 'json must end with one LF') if $bytes_value !~ /\A.*\n\z/s;
    _fail('E_JSON_LF', 'json contains trailing blank data') if $bytes_value =~ /\n\n\z/;

    my $payload = substr($bytes_value, 0, -1);
    my $value;
    my $ok = eval {
        $value = $JSON->decode($payload);
        1;
    };
    _fail('E_JSON_PARSE', 'invalid json') if !$ok;
    _validate_json_shape($value, 0);
    _fail('E_JSON_NONCANONICAL', 'json is not canonical')
        if canonical_json($value) ne $bytes_value;
    return $value;
}

sub _validate_json_shape {
    my ($value, $depth) = @_;
    _fail('E_LIMIT_JSON_DEPTH', 'json nesting too deep') if $depth > MAX_JSON_DEPTH;
    my $type = ref($value);
    if ($type eq 'HASH') {
        _fail('E_LIMIT_JSON_KEYS', 'too many object keys') if scalar(keys %{$value}) > MAX_ARRAY_ITEMS;
        for my $key (keys %{$value}) {
            _fail('E_JSON_KEY', 'invalid object key') if !defined($key) || $key =~ /[\r\n\0]/;
            _validate_json_shape($value->{$key}, $depth + 1);
        }
    }
    elsif ($type eq 'ARRAY') {
        _fail('E_LIMIT_JSON_ARRAY', 'too many array items') if @{$value} > MAX_ARRAY_ITEMS;
        _validate_json_shape($_, $depth + 1) for @{$value};
    }
    elsif ($type eq '') {
        if (defined $value) {
            my $atom = $JSON_ATOM->encode($value);
            _fail('E_JSON_NUMBER', 'floating-point json numbers are forbidden')
                if $atom !~ /\A"/ && $atom !~ /\A-?(?:0|[1-9][0-9]*)\z/;
        }
    }
    elsif ($type ne 'JSON::PP::Boolean') {
        _fail('E_JSON_TYPE', 'unsupported json value type');
    }
    return 1;
}

sub sha256_bytes {
    my ($value) = @_;
    return sha256_hex($value);
}

sub sha256_file {
    my ($path, $limit) = @_;
    my $bytes_value = read_bounded_file($path, $limit);
    return sha256_hex($bytes_value);
}

sub read_bounded_file {
    my ($path, $limit) = @_;
    $limit = MAX_SOURCE_BYTES if !defined $limit;
    my @st = lstat($path);
    _fail('E_UNSAFE_MISSING', 'path missing') if !@st;
    _fail('E_UNSAFE_TYPE', 'path is not regular') if !S_ISREG($st[2]);
    _fail('E_UNSAFE_LINK', 'file link count is not one') if $st[3] != 1;
    _fail('E_LIMIT_FILE', 'file exceeds byte limit') if $st[7] > $limit;
    sysopen(my $fh, $path, O_RDONLY | O_NOFOLLOW)
        or _fail('E_UNSAFE_OPEN', 'cannot open regular file');
    binmode($fh, ':raw');
    my @opened = stat($fh);
    _fail('E_FILE_RACE', 'opened file identity changed')
        if !@opened || $opened[0] != $st[0] || $opened[1] != $st[1]
        || !S_ISREG($opened[2]) || $opened[3] != 1 || $opened[7] != $st[7];
    my $content = '';
    while (1) {
        my $buffer = '';
        my $read = sysread($fh, $buffer, 65_536);
        _fail('E_FILE_READ', 'file read failed') if !defined $read;
        last if $read == 0;
        $content .= $buffer;
        _fail('E_LIMIT_FILE', 'file changed beyond byte limit') if length($content) > $limit;
    }
    close($fh) or _fail('E_FILE_CLOSE', 'file close failed');
    _fail('E_FILE_RACE', 'file size changed during read') if length($content) != $st[7];
    return $content;
}

sub _closed_keys {
    my ($record, $allowed, $required) = @_;
    _fail('E_SCHEMA_TYPE', 'record must be object') if ref($record) ne 'HASH';
    my %allowed = map { $_ => 1 } @{$allowed};
    for my $key (keys %{$record}) {
        _fail('E_SCHEMA_UNKNOWN', "unknown key $key") if !$allowed{$key};
    }
    for my $key (@{$required}) {
        _fail('E_SCHEMA_MISSING', "missing key $key") if !exists $record->{$key};
    }
    return 1;
}

sub _is_enum {
    my ($value, $allowed) = @_;
    return 0 if !_plain_scalar($value);
    return scalar grep { $value eq $_ } @{$allowed};
}

sub _plain_scalar {
    my ($value) = @_;
    return defined($value) && ref($value) eq '';
}

sub _json_string {
    my ($value) = @_;
    return 0 if !_plain_scalar($value);
    return $JSON_ATOM->encode($value) =~ /\A"/;
}

sub _json_integer {
    my ($value) = @_;
    return 0 if !_plain_scalar($value);
    return $JSON_ATOM->encode($value) =~ /\A(?:0|[1-9][0-9]*)\z/;
}

sub _nonnegative_integer {
    my ($value) = @_;
    return _plain_scalar($value) && "$value" =~ /\A(?:0|[1-9][0-9]*)\z/;
}

sub _utc_timestamp {
    my ($value) = @_;
    return _json_string($value)
        && $value =~ /\A[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\z/;
}

sub _json_false {
    my ($value) = @_;
    return ref($value) eq 'JSON::PP::Boolean' && !$value;
}

sub _json_true {
    my ($value) = @_;
    return ref($value) eq 'JSON::PP::Boolean' && $value;
}

sub _assert_owned_directory {
    my ($path, $mode, $expected_device) = @_;
    my @st = lstat($path);
    _fail('E_UNSAFE_MISSING', 'directory missing') if !@st;
    _fail('E_UNSAFE_TYPE', 'path is not directory') if !S_ISDIR($st[2]) || S_ISLNK($st[2]);
    _fail('E_UNSAFE_OWNER', 'directory owner mismatch') if $st[4] != $<;
    _fail('E_UNSAFE_MODE', 'directory mode mismatch') if defined($mode) && (($st[2] & 07777) != $mode);
    _fail('E_UNSAFE_MOUNT', 'directory crosses filesystem boundary')
        if defined($expected_device) && $st[0] != $expected_device;
    return \@st;
}

sub _read_owned_file {
    my ($path, $limit, $mode, $expected_device) = @_;
    my @st = lstat($path);
    _fail('E_UNSAFE_MISSING', 'protocol file missing') if !@st;
    _fail('E_UNSAFE_TYPE', 'protocol path is not regular') if !S_ISREG($st[2]) || S_ISLNK($st[2]);
    _fail('E_UNSAFE_LINK', 'protocol file link count is not one') if $st[3] != 1;
    _fail('E_UNSAFE_OWNER', 'protocol file owner mismatch') if $st[4] != $<;
    _fail('E_UNSAFE_MODE', 'protocol file mode mismatch') if (($st[2] & 07777) != $mode);
    _fail('E_UNSAFE_MOUNT', 'protocol file crosses filesystem boundary')
        if defined($expected_device) && $st[0] != $expected_device;
    return read_bounded_file($path, $limit);
}

sub verify_runtime_identity {
    _fail('E_RUNTIME_IDENTITY', 'real and effective user differ') if $< != $>;
    _fail('E_RUNTIME_IDENTITY', 'elevated user is forbidden') if $< == 0;
    my $real_groups = $(;
    my $effective_groups = $);
    my ($real_gid) = split(/\s+/, $real_groups);
    my ($effective_gid) = split(/\s+/, $effective_groups);
    _fail('E_RUNTIME_IDENTITY', 'real and effective group differ') if $real_gid != $effective_gid;

    for my $name (sort keys %BINARY_IDENTITIES) {
        my $expected = $BINARY_IDENTITIES{$name};
        my @st = lstat($expected->{path});
        _fail('E_RUNTIME_IDENTITY', 'required binary missing') if !@st;
        _fail('E_RUNTIME_IDENTITY', 'required binary is not a regular file')
            if !S_ISREG($st[2]) || S_ISLNK($st[2]) || $st[3] != 1;
        _fail('E_RUNTIME_IDENTITY', 'required binary ownership or mode mismatch')
            if $st[4] != 0 || (($st[2] & 07777) != 0755);
        _fail('E_RUNTIME_IDENTITY', 'required binary byte count mismatch') if $st[7] != $expected->{bytes};
        _fail('E_RUNTIME_IDENTITY', 'required binary digest mismatch')
            if sha256_file($expected->{path}, MAX_GIT_STREAM) ne $expected->{sha256};
    }
    my $implementation = abs_path(__FILE__);
    _fail('E_RUNTIME_SOURCE', 'implementation path mismatch')
        if !defined($implementation)
        || $implementation ne REPOSITORY_ROOT . '/tools/handoff/mneme-handoff.pl';
    my @source_st = lstat($implementation);
    _fail('E_RUNTIME_SOURCE', 'implementation source identity invalid')
        if !@source_st || !S_ISREG($source_st[2]) || S_ISLNK($source_st[2])
        || $source_st[3] != 1 || $source_st[4] != $< || (($source_st[2] & 07777) != 0644);
    return 1;
}

sub validate_digest {
    my ($value) = @_;
    _fail('E_DIGEST', 'digest must be lowercase sha256')
        if !_json_string($value) || $value !~ /\A[0-9a-f]{64}\z/;
    return 1;
}

sub validate_packet_number {
    my ($value) = @_;
    _fail('E_PACKET_NUMBER', 'packet number must be six digits')
        if !_json_string($value) || $value !~ /\A[0-9]{6}\z/;
    my $number = int($value);
    _fail('E_PACKET_NUMBER', 'packet number out of range')
        if $number < 1 || $number > MAX_PACKET_NUMBER;
    return $number;
}

sub validate_relative_path {
    my ($path) = @_;
    _fail('E_UNSAFE_PATH', 'path is absent') if !defined($path) || $path eq '';
    my $utf8_ok = eval {
        my $copy = $path;
        if (utf8::is_utf8($copy)) {
            encode('UTF-8', $copy, FB_CROAK);
        }
        else {
            decode('UTF-8', $copy, FB_CROAK);
        }
        1;
    };
    _fail('E_UNSAFE_PATH', 'path is not valid UTF-8') if !$utf8_ok;
    _fail('E_LIMIT_PATH', 'path too long') if length($path) > MAX_PATH_BYTES;
    _fail('E_UNSAFE_PATH', 'path contains forbidden bytes') if $path =~ /[\r\n\0]/;
    _fail('E_UNSAFE_PATH', 'absolute path forbidden') if File::Spec->file_name_is_absolute($path);
    _fail('E_UNSAFE_PATH', 'backslash forbidden') if index($path, '\\') >= 0;
    my @parts = split('/', $path, -1);
    for my $part (@parts) {
        _fail('E_UNSAFE_PATH', 'empty or dot path segment') if $part eq '' || $part eq '.' || $part eq '..';
        _fail('E_LIMIT_SEGMENT', 'path segment too long') if length($part) > MAX_SEGMENT_BYTES;
    }
    return 1;
}

sub source_path_allowed {
    my ($path) = @_;
    validate_relative_path($path);
    return 1 if $path eq 'README.md' || $path eq 'AGENTS.md' || $path eq '.gitignore';
    return 1 if $path =~ m{\A(?:docs|experiments/phase-3|tools/handoff)/};
    _fail('E_UNSAFE_SOURCE_ROOT', 'source path outside allowlist');
}

sub prohibited_path {
    my ($path) = @_;
    validate_relative_path($path);
    return 1 if $path =~ m{\A(?:\.git|\.credentials|\.mneme-secrets|\.mneme-data|\.mneme-backups|\.mneme-generated|\.mneme-tmp)(?:/|\z)};
    return 0;
}

sub assert_regular_contained {
    my ($root, $relative, $expected_mode) = @_;
    validate_relative_path($relative);
    my $root_real = abs_path($root);
    _fail('E_UNSAFE_ROOT', 'root cannot be resolved') if !defined $root_real;
    my $cursor = $root_real;
    my @parts = split('/', $relative);
    for my $index (0 .. $#parts) {
        $cursor = File::Spec->catfile($cursor, $parts[$index]);
        my @st = lstat($cursor);
        _fail('E_UNSAFE_MISSING', 'path component missing') if !@st;
        _fail('E_UNSAFE_SYMLINK', 'symlink forbidden') if S_ISLNK($st[2]);
        if ($index < $#parts) {
            _fail('E_UNSAFE_TYPE', 'intermediate component not directory') if !S_ISDIR($st[2]);
        }
        else {
            _fail('E_UNSAFE_TYPE', 'final path not regular') if !S_ISREG($st[2]);
            _fail('E_UNSAFE_LINK', 'hard-link anomaly') if $st[3] != 1;
            _fail('E_UNSAFE_OWNER', 'file owner mismatch') if $st[4] != $<;
            _fail('E_UNSAFE_MODE', 'group/world-writable source forbidden') if ($st[2] & 0022);
            if (defined $expected_mode) {
                _fail('E_UNSAFE_MODE', 'unexpected file mode') if (($st[2] & 07777) != $expected_mode);
            }
        }
    }
    my $final_real = abs_path($cursor);
    _fail('E_UNSAFE_REALPATH', 'path cannot be resolved') if !defined $final_real;
    _fail('E_UNSAFE_ESCAPE', 'path escapes root')
        if $final_real ne $root_real && index($final_real, $root_real . '/') != 0;
    return $final_real;
}

sub validate_number_sequence {
    my ($numbers) = @_;
    my %seen;
    my @sorted = sort { $a <=> $b } map { validate_packet_number($_) } @{$numbers};
    my $expected = 1;
    for my $number (@sorted) {
        _fail('E_CONFLICT_NUMBER', 'duplicate packet number') if $seen{$number}++;
        _fail('E_CONFLICT_GAP', 'unexplained packet number gap') if $number != $expected;
        $expected++;
    }
    _fail('E_LIMIT_PACKET', 'packet number exhausted') if $expected > MAX_PACKET_NUMBER;
    return sprintf('%06d', $expected);
}

sub validate_packet_entries {
    my ($entries) = @_;
    my %expected = map { $_ => 1 } qw(
        packet.json
        request.md
        sources.tsv
        repository-state.json
        packet-manifest.sha256
        transactions
        rollbacks
    );
    for my $entry (@{$entries}) {
        _fail('E_PACKET_EXTRA', 'unexpected packet entry') if !$expected{$entry};
        delete $expected{$entry};
    }
    _fail('E_PACKET_MISSING', 'packet entry missing') if keys %expected;
    return 1;
}

sub validate_store_entries {
    my ($entries) = @_;
    my %allowed = map { $_ => 1 } qw(MNEME_HANDOFF_STORE.json packets staging locks);
    for my $entry (@{$entries}) {
        _fail('E_STORE_EXTRA', 'unexpected packet-store entry') if !$allowed{$entry};
        delete $allowed{$entry};
    }
    _fail('E_STORE_MISSING', 'packet-store entry missing') if keys %allowed;
    return 1;
}

sub validate_dirty_paths {
    my ($changed, $declared) = @_;
    my %declared = map { $_ => 1 } @{$declared};
    _fail('E_LIMIT_STATUS', 'too many status entries') if @{$changed} > MAX_STATUS_ITEMS;
    for my $path (@{$changed}) {
        source_path_allowed($path);
        _fail('E_REPOSITORY_UNREPRESENTED', 'changed path is not declared') if !$declared{$path};
    }
    return 1;
}

sub canonical_sources_tsv {
    my ($rows) = @_;
    _fail('E_LIMIT_SOURCES', 'too many sources') if @{$rows} > MAX_SOURCES;
    my %seen;
    my $total = 0;
    my @normalized;
    for my $row (@{$rows}) {
        _closed_keys($row, [qw(relative_path type mode bytes sha256 role)], [qw(relative_path type mode bytes sha256 role)]);
        source_path_allowed($row->{relative_path});
        _fail('E_SOURCE_DUPLICATE', 'duplicate source path') if $seen{$row->{relative_path}}++;
        _fail('E_SOURCE_TYPE', 'source must be regular') if $row->{type} ne 'regular';
        _fail('E_SOURCE_MODE', 'invalid mode') if $row->{mode} !~ /\A0[0-7]{3}\z/;
        _fail('E_SOURCE_BYTES', 'source bytes invalid') if $row->{bytes} !~ /\A(?:0|[1-9][0-9]*)\z/;
        _fail('E_LIMIT_SOURCE', 'source file too large') if $row->{bytes} > MAX_SOURCE_BYTES;
        validate_digest($row->{sha256});
        _fail('E_SOURCE_ROLE', 'source role invalid') if !_is_enum($row->{role}, \@SOURCE_ROLES);
        $total += $row->{bytes};
        _fail('E_LIMIT_SOURCE_TOTAL', 'aggregate sources too large') if $total > MAX_SOURCE_TOTAL;
        push @normalized, $row;
    }
    @normalized = sort { $a->{relative_path} cmp $b->{relative_path} } @normalized;
    my $text = "relative_path\ttype\tmode\tbytes\tsha256\trole\n";
    for my $row (@normalized) {
        for my $field (qw(relative_path type mode bytes sha256 role)) {
            _fail('E_TSV_FIELD', 'tsv field contains delimiter') if "$row->{$field}" =~ /[\t\r\n\0]/;
        }
        $text .= join("\t", @{$row}{qw(relative_path type mode bytes sha256 role)}) . "\n";
    }
    _fail('E_LIMIT_TSV', 'sources tsv too large') if length($text) > MAX_TSV_BYTES;
    return $text;
}

sub parse_sources_tsv {
    my ($text) = @_;
    _fail('E_LIMIT_TSV', 'sources tsv too large') if length($text) > MAX_TSV_BYTES;
    _fail('E_TSV_NUL', 'sources tsv contains NUL') if index($text, "\0") >= 0;
    _fail('E_TSV_CR', 'sources tsv contains CR') if index($text, "\r") >= 0;
    _fail('E_TSV_LF', 'sources tsv must end with LF') if $text !~ /\n\z/;
    my @lines = split("\n", $text, -1);
    pop @lines if @lines && $lines[-1] eq '';
    _fail('E_TSV_HEADER', 'sources tsv header mismatch')
        if !@lines || shift(@lines) ne "relative_path\ttype\tmode\tbytes\tsha256\trole";
    _fail('E_LIMIT_SOURCES', 'too many sources') if @lines > MAX_SOURCES;
    my @rows;
    for my $line (@lines) {
        my @fields = split("\t", $line, -1);
        _fail('E_TSV_FIELDS', 'sources tsv field count') if @fields != 6;
        push @rows, {
            relative_path => $fields[0],
            type => $fields[1],
            mode => $fields[2],
            bytes => $fields[3],
            sha256 => $fields[4],
            role => $fields[5],
        };
    }
    my $canonical = canonical_sources_tsv(\@rows);
    _fail('E_TSV_NONCANONICAL', 'sources tsv is not canonical') if $canonical ne $text;
    return \@rows;
}

sub compute_packet_id {
    my ($packet, $request_sha, $sources_sha, $repository_sha) = @_;
    validate_digest($_) for ($request_sha, $sources_sha, $repository_sha);
    my %metadata = %{$packet};
    delete $metadata{packet_id};
    my $material = join("\0",
        'mneme-handoff-packet-v1',
        canonical_json(\%metadata),
        $request_sha,
        $sources_sha,
        $repository_sha,
    );
    return sha256_hex($material);
}

sub validate_packet_record {
    my ($packet, $number, $repo_root) = @_;
    my @keys = qw(
        schema_version protocol_version packet_number purpose review_question
        created_at repository_root head branch repository_state_sha256
        request_sha256 sources_sha256 prior_packet_id superseded_packet_id
        approval_gate non_authorization source_count source_bytes packet_id
    );
    _closed_keys($packet, \@keys, \@keys);
    _fail('E_PACKET_SCHEMA', 'packet schema mismatch')
        if !_json_integer($packet->{schema_version}) || $packet->{schema_version} != 1
        || !_json_integer($packet->{protocol_version}) || $packet->{protocol_version} != 1;
    validate_packet_number($packet->{packet_number});
    _fail('E_PACKET_NUMBER', 'packet directory mismatch')
        if defined($number) && $packet->{packet_number} ne $number;
    _fail('E_PACKET_PURPOSE', 'packet purpose mismatch')
        if !_json_string($packet->{purpose}) || $packet->{purpose} ne 'file-based review handoff';
    source_path_allowed($packet->{review_question});
    _fail('E_PACKET_DATE', 'packet timestamp invalid') if !_utc_timestamp($packet->{created_at});
    _fail('E_PACKET_ROOT', 'packet repository mismatch')
        if !_json_string($packet->{repository_root}) || $packet->{repository_root} ne $repo_root;
    _fail('E_PACKET_HEAD', 'packet head invalid')
        if !_json_string($packet->{head})
        || ($packet->{head} ne 'UNBORN' && $packet->{head} !~ /\A[0-9a-f]{40,64}\z/);
    _fail('E_PACKET_BRANCH', 'packet branch invalid')
        if !_json_string($packet->{branch}) || $packet->{branch} eq ''
        || length($packet->{branch}) > MAX_PATH_BYTES || $packet->{branch} =~ /[\r\n\0]/;
    validate_digest($packet->{$_}) for qw(repository_state_sha256 request_sha256 sources_sha256 packet_id);
    for my $field (qw(prior_packet_id superseded_packet_id)) {
        _fail('E_PACKET_LINEAGE', 'packet lineage identity invalid') if !_json_string($packet->{$field});
        validate_digest($packet->{$field}) if $packet->{$field} ne '';
    }
    _fail('E_PACKET_GATE', 'packet approval gate invalid')
        if !_is_enum($packet->{approval_gate}, \@APPROVAL_GATES);
    _fail('E_PACKET_AUTHORITY', 'packet non-authorization statement mismatch')
        if !_json_string($packet->{non_authorization})
        || $packet->{non_authorization} ne 'packet consumption records a handoff and never authorizes project work';
    _fail('E_PACKET_SOURCE_COUNT', 'packet source count invalid')
        if !_json_integer($packet->{source_count})
        || $packet->{source_count} < 1 || $packet->{source_count} > MAX_SOURCES;
    _fail('E_PACKET_SOURCE_BYTES', 'packet source bytes invalid')
        if !_json_integer($packet->{source_bytes}) || $packet->{source_bytes} > MAX_SOURCE_TOTAL;
    return 1;
}

sub validate_repository_record {
    my ($repository, $repo_root) = @_;
    my @keys = qw(
        schema_version repository_root git_directory head branch status_sha256
        index_sha256 worktree packet_store_excluded
    );
    _closed_keys($repository, \@keys, \@keys);
    _fail('E_REPOSITORY_SCHEMA', 'repository schema mismatch')
        if !_json_integer($repository->{schema_version}) || $repository->{schema_version} != 1;
    _fail('E_REPOSITORY_ROOT', 'repository record root mismatch')
        if !_json_string($repository->{repository_root}) || $repository->{repository_root} ne $repo_root;
    _fail('E_REPOSITORY_GITDIR', 'repository git directory invalid')
        if !_json_string($repository->{git_directory})
        || !File::Spec->file_name_is_absolute($repository->{git_directory})
        || $repository->{git_directory} =~ /[\r\n\0]/;
    _fail('E_REPOSITORY_HEAD', 'repository head invalid')
        if !_json_string($repository->{head})
        || ($repository->{head} ne 'UNBORN' && $repository->{head} !~ /\A[0-9a-f]{40,64}\z/);
    _fail('E_REPOSITORY_BRANCH', 'repository branch invalid')
        if !_json_string($repository->{branch}) || $repository->{branch} eq ''
        || length($repository->{branch}) > MAX_PATH_BYTES || $repository->{branch} =~ /[\r\n\0]/;
    validate_digest($repository->{status_sha256});
    validate_digest($repository->{index_sha256});
    _fail('E_REPOSITORY_STORE', 'packet-store exclusion must be true')
        if !_json_true($repository->{packet_store_excluded});
    _fail('E_REPOSITORY_WORKTREE', 'worktree must be bounded array')
        if ref($repository->{worktree}) ne 'ARRAY' || @{$repository->{worktree}} > MAX_SOURCES;
    my %seen;
    my $previous = '';
    for my $row (@{$repository->{worktree}}) {
        _closed_keys($row, [qw(relative_path type mode bytes sha256)], [qw(relative_path type mode bytes sha256)]);
        source_path_allowed($row->{relative_path});
        _fail('E_REPOSITORY_WORKTREE', 'duplicate worktree path') if $seen{$row->{relative_path}}++;
        _fail('E_REPOSITORY_WORKTREE', 'worktree paths not byte-sorted')
            if $previous ne '' && $previous cmp $row->{relative_path} >= 0;
        $previous = $row->{relative_path};
        _fail('E_REPOSITORY_WORKTREE', 'worktree type invalid') if $row->{type} ne 'regular';
        _fail('E_REPOSITORY_WORKTREE', 'worktree mode invalid') if $row->{mode} !~ /\A0[0-7]{3}\z/;
        _fail('E_REPOSITORY_WORKTREE', 'worktree byte count invalid')
            if !_json_integer($row->{bytes}) || $row->{bytes} > MAX_SOURCE_BYTES;
        validate_digest($row->{sha256});
    }
    return 1;
}

sub validate_lineage {
    my ($nodes) = @_;
    my %children;
    for my $id (keys %{$nodes}) {
        validate_digest($id);
        my $parent = $nodes->{$id}{prior};
        next if !defined($parent) || $parent eq '';
        validate_digest($parent);
        _fail('E_CONFLICT_LINEAGE_MISSING', 'predecessor missing') if !exists $nodes->{$parent};
        push @{$children{$parent}}, $id;
        _fail('E_CONFLICT_LINEAGE_FORK', 'lineage fork') if @{$children{$parent}} > 1;
    }
    for my $start (keys %{$nodes}) {
        my %visited;
        my $cursor = $start;
        while (defined($cursor) && $cursor ne '') {
            _fail('E_CONFLICT_LINEAGE_CYCLE', 'lineage cycle') if $visited{$cursor}++;
            $cursor = $nodes->{$cursor}{prior};
        }
    }
    return 1;
}

sub derive_state {
    my ($facts) = @_;
    return 'Invalid' if $facts->{invalid};
    return 'Conflict' if $facts->{conflict};
    return 'Stale' if $facts->{stale};
    return 'RolledBack' if $facts->{rolled_back};
    return 'Rejected' if defined($facts->{verdict}) && $facts->{verdict} eq 'Reject';
    return 'ChangesRequested' if defined($facts->{verdict}) && $facts->{verdict} eq 'ChangesRequested';
    return 'Consumed' if defined($facts->{verdict}) && $facts->{verdict} eq 'Approve' && $facts->{receipt};
    return 'Pending';
}

sub validate_verdict {
    my ($verdict) = @_;
    my @keys = qw(
        schema_version record_type status packet_number packet_id
        packet_manifest_sha256 repository_state_sha256 sources_sha256
        verdict rationale unresolved_concerns reviewer_role proposal_date
    );
    _closed_keys($verdict, \@keys, \@keys);
    _fail('E_VERDICT_SCHEMA', 'verdict schema version')
        if !_json_integer($verdict->{schema_version}) || $verdict->{schema_version} != 1;
    _fail('E_VERDICT_TYPE', 'verdict record type')
        if !_json_string($verdict->{record_type}) || $verdict->{record_type} ne 'mneme.handoff.verdict';
    _fail('E_VERDICT_STATUS', 'verdict must remain Proposed')
        if !_json_string($verdict->{status}) || $verdict->{status} ne 'Proposed';
    validate_packet_number($verdict->{packet_number});
    validate_digest($verdict->{$_}) for qw(packet_id packet_manifest_sha256 repository_state_sha256 sources_sha256);
    _fail('E_VERDICT_VALUE', 'unknown verdict') if !_is_enum($verdict->{verdict}, \@VERDICTS);
    _fail('E_VERDICT_RATIONALE', 'invalid rationale')
        if !_json_string($verdict->{rationale}) || length($verdict->{rationale}) > 16_384
        || $verdict->{rationale} =~ /\0/;
    _fail('E_VERDICT_CONCERNS', 'concerns must be array') if ref($verdict->{unresolved_concerns}) ne 'ARRAY';
    for my $concern (@{$verdict->{unresolved_concerns}}) {
        _fail('E_VERDICT_CONCERNS', 'concern must be bounded text')
            if !_json_string($concern) || length($concern) > 4_096 || $concern =~ /\0/;
    }
    _fail('E_VERDICT_ROLE', 'reviewer role invalid')
        if !_json_string($verdict->{reviewer_role}) || $verdict->{reviewer_role} eq ''
        || length($verdict->{reviewer_role}) > 256 || $verdict->{reviewer_role} =~ /[\r\n\0]/;
    _fail('E_VERDICT_DATE', 'proposal date invalid')
        if !_json_string($verdict->{proposal_date})
        || $verdict->{proposal_date} !~ /\A[0-9]{4}-[0-9]{2}-[0-9]{2}\z/;
    return 1;
}

sub validate_approval {
    my ($approval) = @_;
    my @keys = qw(
        schema_version record_type status authority packet_number packet_id
        verdict_sha256 repository_state_sha256 approval_date decision_reference
        approval_statement_sha256
    );
    _closed_keys($approval, \@keys, \@keys);
    _fail('E_APPROVAL_SCHEMA', 'approval schema version')
        if !_json_integer($approval->{schema_version}) || $approval->{schema_version} != 1;
    _fail('E_APPROVAL_TYPE', 'approval record type')
        if !_json_string($approval->{record_type}) || $approval->{record_type} ne 'mneme.handoff.user-approval';
    _fail('E_APPROVAL_STATUS', 'approval must be Accepted')
        if !_json_string($approval->{status}) || $approval->{status} ne 'Accepted';
    _fail('E_APPROVAL_AUTHORITY', 'approval authority must be user')
        if !_json_string($approval->{authority}) || $approval->{authority} ne 'user';
    validate_packet_number($approval->{packet_number});
    validate_digest($approval->{$_}) for qw(packet_id verdict_sha256 repository_state_sha256 approval_statement_sha256);
    _fail('E_APPROVAL_DATE', 'approval date invalid')
        if !_json_string($approval->{approval_date})
        || $approval->{approval_date} !~ /\A[0-9]{4}-[0-9]{2}-[0-9]{2}\z/;
    _fail('E_APPROVAL_REFERENCE', 'decision reference absent')
        if !_json_string($approval->{decision_reference}) || $approval->{decision_reference} eq ''
        || length($approval->{decision_reference}) > 4_096 || $approval->{decision_reference} =~ /\0/;
    return 1;
}

sub validate_rollback_approval {
    my ($approval) = @_;
    my @keys = qw(
        schema_version record_type status authority packet_number packet_id
        receipt_sha256 approval_date decision_reference approval_statement_sha256
    );
    _closed_keys($approval, \@keys, \@keys);
    _fail('E_APPROVAL_SCHEMA', 'rollback approval schema version')
        if !_json_integer($approval->{schema_version}) || $approval->{schema_version} != 1;
    _fail('E_APPROVAL_TYPE', 'rollback approval record type')
        if !_json_string($approval->{record_type}) || $approval->{record_type} ne 'mneme.handoff.rollback-approval';
    _fail('E_APPROVAL_STATUS', 'rollback approval must be Accepted')
        if !_json_string($approval->{status}) || $approval->{status} ne 'Accepted';
    _fail('E_APPROVAL_AUTHORITY', 'rollback approval authority must be user')
        if !_json_string($approval->{authority}) || $approval->{authority} ne 'user';
    validate_packet_number($approval->{packet_number});
    validate_digest($approval->{$_}) for qw(packet_id receipt_sha256 approval_statement_sha256);
    _fail('E_APPROVAL_DATE', 'rollback approval date invalid')
        if !_json_string($approval->{approval_date})
        || $approval->{approval_date} !~ /\A[0-9]{4}-[0-9]{2}-[0-9]{2}\z/;
    _fail('E_APPROVAL_REFERENCE', 'rollback decision reference absent')
        if !_json_string($approval->{decision_reference}) || $approval->{decision_reference} eq ''
        || length($approval->{decision_reference}) > 4_096 || $approval->{decision_reference} =~ /\0/;
    return 1;
}

sub validate_verdict_approval {
    my ($verdict, $approval, $verdict_bytes) = @_;
    validate_verdict($verdict);
    validate_approval($approval);
    my $verdict_sha = sha256_hex($verdict_bytes);
    _fail('E_APPROVAL_VERDICT_HASH', 'approval targets another verdict') if $approval->{verdict_sha256} ne $verdict_sha;
    for my $field (qw(packet_number packet_id repository_state_sha256)) {
        _fail('E_APPROVAL_MISMATCH', "approval mismatch $field") if $approval->{$field} ne $verdict->{$field};
    }
    return $verdict_sha;
}

sub validate_receipt {
    my ($receipt) = @_;
    my @keys = qw(
        schema_version record_type packet_number packet_id packet_manifest_sha256
        repository_state_sha256 sources_sha256 verdict verdict_sha256 approval_sha256
        implementation_sha256 runtime_sha256 git_sha256 consumed_at
        project_work_authorized project_work_executed
    );
    _closed_keys($receipt, \@keys, \@keys);
    _fail('E_RECEIPT_SCHEMA', 'receipt schema version')
        if !_json_integer($receipt->{schema_version}) || $receipt->{schema_version} != 1;
    _fail('E_RECEIPT_TYPE', 'receipt record type')
        if !_json_string($receipt->{record_type}) || $receipt->{record_type} ne 'mneme.handoff.receipt';
    validate_packet_number($receipt->{packet_number});
    _fail('E_RECEIPT_VERDICT', 'receipt verdict invalid') if !_is_enum($receipt->{verdict}, \@VERDICTS);
    _fail('E_RECEIPT_AUTHORITY', 'receipt cannot authorize project work')
        if !_json_false($receipt->{project_work_authorized});
    _fail('E_RECEIPT_EXECUTION', 'receipt cannot record project execution')
        if !_json_false($receipt->{project_work_executed});
    validate_digest($receipt->{$_}) for qw(
        packet_id packet_manifest_sha256 repository_state_sha256 sources_sha256
        verdict_sha256 approval_sha256 implementation_sha256 runtime_sha256 git_sha256
    );
    _fail('E_RECEIPT_DATE', 'receipt timestamp invalid') if !_utc_timestamp($receipt->{consumed_at});
    return 1;
}

sub validate_rollback {
    my ($rollback, $receipt_sha, $current_repository_sha) = @_;
    my @keys = qw(
        schema_version record_type packet_id receipt_sha256 approval_sha256
        original_repository_state_sha256 current_repository_state_sha256
        reason rollback_date
    );
    _closed_keys($rollback, \@keys, \@keys);
    _fail('E_ROLLBACK_SCHEMA', 'rollback schema version')
        if !_json_integer($rollback->{schema_version}) || $rollback->{schema_version} != 1;
    _fail('E_ROLLBACK_TYPE', 'rollback record type')
        if !_json_string($rollback->{record_type}) || $rollback->{record_type} ne 'mneme.handoff.rollback';
    validate_digest($receipt_sha);
    validate_digest($current_repository_sha);
    validate_digest($rollback->{$_}) for qw(packet_id receipt_sha256 approval_sha256 original_repository_state_sha256 current_repository_state_sha256);
    _fail('E_CONFLICT_ROLLBACK_RECEIPT', 'rollback targets another receipt') if $rollback->{receipt_sha256} ne $receipt_sha;
    _fail('E_ROLLBACK_CURRENT', 'rollback current state mismatch') if $rollback->{current_repository_state_sha256} ne $current_repository_sha;
    _fail('E_ROLLBACK_REASON', 'rollback reason invalid')
        if !_json_string($rollback->{reason}) || $rollback->{reason} eq ''
        || length($rollback->{reason}) > 4_096 || $rollback->{reason} =~ /\0/;
    _fail('E_ROLLBACK_DATE', 'rollback timestamp invalid') if !_utc_timestamp($rollback->{rollback_date});
    return 1;
}

sub render_list_line {
    my ($summary, $verbose) = @_;
    my @fields = (
        $summary->{packet_number},
        substr($summary->{packet_id}, 0, 12),
        $summary->{state},
        ($summary->{verdict} // '-'),
        $summary->{created_at},
        $summary->{head},
        $summary->{reason},
    );
    if ($verbose) {
        push @fields, $summary->{packet_id}, $summary->{repository_state_sha256};
        push @fields, @{$summary->{paths} // []};
    }
    my $line = join("\t", @fields) . "\n";
    _fail('E_LIST_CONTENT', 'list output contains forbidden content')
        if defined($summary->{request}) && index($line, $summary->{request}) >= 0;
    return $line;
}

sub _write_all {
    my ($fh, $bytes_value) = @_;
    my $offset = 0;
    while ($offset < length($bytes_value)) {
        my $written = syswrite($fh, $bytes_value, length($bytes_value) - $offset, $offset);
        _fail('E_WRITE', 'write failed') if !defined($written) || $written == 0;
        $offset += $written;
    }
    return 1;
}

sub _sync_handle {
    my ($fh) = @_;
    $fh->flush or _fail('E_SYNC_FLUSH', 'flush failed');
    $fh->sync or _fail('E_SYNC_FILE', 'sync failed');
    return 1;
}

sub _sync_directory {
    my ($path) = @_;
    sysopen(my $fh, $path, O_RDONLY | O_NOFOLLOW)
        or _fail('E_SYNC_DIR_OPEN', 'directory sync open failed');
    $fh->sync or _fail('E_SYNC_DIR', 'directory sync failed');
    close($fh) or _fail('E_SYNC_DIR_CLOSE', 'directory close failed');
    return 1;
}

sub write_exclusive_synced {
    my ($path, $bytes_value, $mode) = @_;
    sysopen(my $fh, $path, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW, $mode)
        or _fail('E_WRITE_EXCLUSIVE', 'exclusive file creation failed');
    binmode($fh, ':raw');
    chmod($mode, $path) == 1 or _fail('E_WRITE_MODE', 'file chmod failed');
    _write_all($fh, $bytes_value);
    _sync_handle($fh);
    close($fh) or _fail('E_WRITE_CLOSE', 'file close failed');
    return 1;
}

sub _fault {
    my ($callback, $point) = @_;
    return if !defined $callback;
    $callback->($point);
}

sub _validate_atomic_stage {
    my ($staging, $files) = @_;
    my $stage_st = _assert_owned_directory($staging, 0700, undef);
    opendir(my $dh, $staging) or _fail('E_WRITE_STAGE', 'cannot inspect atomic stage');
    my @entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($dh);
    closedir($dh);
    my @expected = sort keys %{$files};
    _fail('E_WRITE_STAGE', 'atomic stage entry mismatch')
        if join("\0", @entries) ne join("\0", @expected);
    for my $name (@expected) {
        my $bytes_value = _read_owned_file(
            File::Spec->catfile($staging, $name),
            length($files->{$name}), 0600, $stage_st->[0],
        );
        _fail('E_WRITE_STAGE', 'atomic stage bytes mismatch') if $bytes_value ne $files->{$name};
    }
    return 1;
}

sub atomic_publish_directory {
    my ($staging, $final, $files, $fault_callback) = @_;
    _fail('E_CONFLICT_FINAL', 'final directory exists') if lstat($final);
    mkdir($staging, 0700) or _fail('E_WRITE_STAGE', 'cannot create staging directory');
    chmod(0700, $staging) == 1 or _fail('E_WRITE_MODE', 'staging chmod failed');
    _fault($fault_callback, 'after_stage');
    for my $relative (sort keys %{$files}) {
        validate_relative_path($relative);
        _fail('E_WRITE_NESTED', 'nested atomic payload unsupported') if $relative =~ m{/};
        write_exclusive_synced(File::Spec->catfile($staging, $relative), $files->{$relative}, 0600);
    }
    _fault($fault_callback, 'after_files');
    _validate_atomic_stage($staging, $files);
    _sync_directory($staging);
    _fault($fault_callback, 'before_rename');
    rename($staging, $final) or _fail('E_WRITE_RENAME', 'atomic directory rename failed');
    _fault($fault_callback, 'after_rename');
    my $synced = eval { _sync_directory(dirname($final)); 1 };
    _fail('E_WRITE_UNCERTAIN', 'directory publication sync uncertain') if !$synced;
    return 1;
}

sub atomic_publish_file {
    my ($staging, $final, $bytes_value, $fault_callback) = @_;
    _fail('E_CONFLICT_FINAL', 'final file exists') if lstat($final);
    write_exclusive_synced($staging, $bytes_value, 0600);
    _fault($fault_callback, 'after_file');
    my @stage_st = lstat($staging);
    my $verified = _read_owned_file($staging, length($bytes_value), 0600, $stage_st[0]);
    _fail('E_WRITE_STAGE', 'atomic file stage bytes mismatch') if $verified ne $bytes_value;
    _sync_directory(dirname($staging));
    _fault($fault_callback, 'before_rename');
    rename($staging, $final) or _fail('E_WRITE_RENAME', 'atomic file rename failed');
    _fault($fault_callback, 'after_rename');
    my $synced = eval { _sync_directory(dirname($final)); 1 };
    _fail('E_WRITE_UNCERTAIN', 'file publication sync uncertain') if !$synced;
    return 1;
}

sub acquire_lock {
    my ($lock_path, $record) = @_;
    mkdir($lock_path, 0700) or _fail('E_LOCK_EXISTS', 'lock unavailable');
    chmod(0700, $lock_path) == 1 or _fail('E_LOCK_MODE', 'lock chmod failed');
    write_exclusive_synced(File::Spec->catfile($lock_path, 'owner.json'), canonical_json($record), 0600);
    _sync_directory($lock_path);
    _sync_directory(dirname($lock_path));
    return 1;
}

sub release_lock_success {
    my ($lock_path) = @_;
    my $owner = File::Spec->catfile($lock_path, 'owner.json');
    unlink($owner) == 1 or _fail('E_LOCK_RELEASE_FILE', 'cannot remove lock owner');
    rmdir($lock_path) == 1 or _fail('E_LOCK_RELEASE_DIR', 'cannot remove lock directory');
    _sync_directory(dirname($lock_path));
    return 1;
}

sub _git_environment {
    return (
        PATH                => '/usr/bin:/bin',
        LC_ALL              => 'C',
        TZ                  => 'UTC',
        GIT_CONFIG_NOSYSTEM => '1',
        GIT_CONFIG_GLOBAL   => '/dev/null',
        GIT_OPTIONAL_LOCKS  => '0',
        GIT_TERMINAL_PROMPT => '0',
        GCM_INTERACTIVE     => 'never',
        GIT_PAGER           => 'cat',
        PAGER               => 'cat',
        GIT_ASKPASS         => FALSE_PATH,
        SSH_ASKPASS         => FALSE_PATH,
        PERL5OPT            => '',
        PERL5LIB            => '',
    );
}

sub _validate_git_arguments {
    my ($subcommand, $arguments, $stdin_bytes) = @_;
    my $joined = join("\0", @{$arguments});
    if ($subcommand eq 'rev-parse') {
        my %allowed = map { $_ => 1 } ('--show-toplevel', '--absolute-git-dir', '--verify' . "\0" . 'HEAD^{commit}');
        _fail('E_GIT_ARGUMENTS', 'rev-parse arguments not allowed') if !$allowed{$joined};
        _fail('E_GIT_STDIN', 'rev-parse stdin forbidden') if length($stdin_bytes);
    }
    elsif ($subcommand eq 'symbolic-ref') {
        _fail('E_GIT_ARGUMENTS', 'symbolic-ref arguments not allowed')
            if $joined ne join("\0", '--quiet', 'HEAD') || length($stdin_bytes);
    }
    elsif ($subcommand eq 'status') {
        _fail('E_GIT_ARGUMENTS', 'status arguments not allowed')
            if $joined ne join("\0", '--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=all')
            || length($stdin_bytes);
    }
    elsif ($subcommand eq 'ls-files') {
        _fail('E_GIT_ARGUMENTS', 'ls-files arguments not allowed')
            if @{$arguments} < 4 || $arguments->[0] ne '--stage' || $arguments->[1] ne '-z' || $arguments->[2] ne '--'
            || length($stdin_bytes);
        source_path_allowed($_) for @{$arguments}[3 .. $#{$arguments}];
    }
    elsif ($subcommand eq 'check-ignore') {
        _fail('E_GIT_ARGUMENTS', 'check-ignore arguments not allowed')
            if $joined ne join("\0", '--no-index', '-z', '--stdin') || !length($stdin_bytes);
        _fail('E_GIT_STDIN', 'check-ignore input must be NUL terminated') if $stdin_bytes !~ /\0\z/;
    }
    else {
        _fail('E_GIT_SUBCOMMAND', 'git subcommand not allowed');
    }
    return 1;
}

sub run_git_raw {
    my ($repo_root, $subcommand, $arguments, $stdin_bytes) = @_;
    my %allowed = map { $_ => 1 } qw(rev-parse symbolic-ref status ls-files check-ignore);
    _fail('E_GIT_SUBCOMMAND', 'git subcommand not allowed') if !$allowed{$subcommand};
    _fail('E_GIT_ROOT', 'git root must be literal repository') if $repo_root ne REPOSITORY_ROOT;
    $stdin_bytes = '' if !defined $stdin_bytes;
    _validate_git_arguments($subcommand, $arguments, $stdin_bytes);
    my @command = (
        GIT_PATH,
        '-C', $repo_root,
        '-c', 'core.fsmonitor=false',
        '-c', 'core.untrackedCache=false',
        '-c', 'submodule.recurse=false',
        $subcommand,
        @{$arguments},
    );

    local %ENV = _git_environment();
    my ($child_in, $child_out);
    my $child_err = gensym();
    my $pid = open3($child_in, $child_out, $child_err, @command);
    binmode($child_in, ':raw');
    binmode($child_out, ':raw');
    binmode($child_err, ':raw');
    _write_all($child_in, $stdin_bytes) if length($stdin_bytes);
    close($child_in) or _fail('E_GIT_STDIN', 'git stdin close failed');

    my $stdout = '';
    my $stderr = '';
    my %streams = (
        fileno($child_out) => [$child_out, \$stdout],
        fileno($child_err) => [$child_err, \$stderr],
    );
    my $overflow = 0;
    while (keys %streams) {
        my $read_mask = '';
        vec($read_mask, $_, 1) = 1 for keys %streams;
        my $ready = $read_mask;
        my $count = select($ready, undef, undef, undef);
        _fail('E_GIT_SELECT', 'git pipe select failed') if !defined($count) || $count < 0;
        for my $fd (keys %streams) {
            next if !vec($ready, $fd, 1);
            my ($fh, $target) = @{$streams{$fd}};
            my $chunk = '';
            my $read = sysread($fh, $chunk, 65_536);
            _fail('E_GIT_READ', 'git pipe read failed') if !defined $read;
            if ($read == 0) {
                close($fh);
                delete $streams{$fd};
                next;
            }
            if (length(${$target}) + $read > MAX_GIT_STREAM) {
                $overflow = 1;
            }
            elsif (!$overflow) {
                ${$target} .= $chunk;
            }
        }
    }
    waitpid($pid, 0);
    my $status = $? >> 8;
    _fail('E_LIMIT_GIT_OUTPUT', 'git output exceeded limit') if $overflow;
    return {
        status => $status,
        stdout => $stdout,
        stderr => $stderr,
        argv   => \@command,
    };
}

sub collect_repository_state {
    my ($repo_root, $declared_paths) = @_;
    _fail('E_REPOSITORY_ROOT', 'repository root mismatch') if $repo_root ne REPOSITORY_ROOT;
    _fail('E_LIMIT_SOURCES', 'declared source count invalid')
        if ref($declared_paths) ne 'ARRAY' || !@{$declared_paths} || @{$declared_paths} > MAX_SOURCES;
    source_path_allowed($_) for @{$declared_paths};
    my $store_input = STORE_RELATIVE . "/\0";
    my $store_ignore = run_git_raw($repo_root, 'check-ignore', ['--no-index', '-z', '--stdin'], $store_input);
    _fail('E_REPOSITORY_GIT', 'packet-store ignore check failed')
        if $store_ignore->{status} != 0 || $store_ignore->{stderr} ne '' || $store_ignore->{stdout} ne $store_input;
    my $source_input = join('', map { $_ . "\0" } @{$declared_paths});
    my $source_ignore = run_git_raw($repo_root, 'check-ignore', ['--no-index', '-z', '--stdin'], $source_input);
    _fail('E_UNSAFE_SOURCE_IGNORED', 'declared source is ignored')
        if $source_ignore->{status} == 0 || $source_ignore->{stdout} ne '';
    _fail('E_REPOSITORY_GIT', 'source ignore check failed')
        if $source_ignore->{status} != 1 || $source_ignore->{stderr} ne '';
    my $top = run_git_raw($repo_root, 'rev-parse', ['--show-toplevel'], '');
    _fail('E_REPOSITORY_GIT', 'show-toplevel failed') if $top->{status} != 0 || $top->{stderr} ne '';
    (my $top_path = $top->{stdout}) =~ s/\n\z//;
    _fail('E_REPOSITORY_ROOT', 'git top-level mismatch') if $top_path ne $repo_root;

    my $git_dir = run_git_raw($repo_root, 'rev-parse', ['--absolute-git-dir'], '');
    _fail('E_REPOSITORY_GIT', 'git-dir failed') if $git_dir->{status} != 0 || $git_dir->{stderr} ne '';
    (my $git_dir_path = $git_dir->{stdout}) =~ s/\n\z//;

    my $head_result = run_git_raw($repo_root, 'rev-parse', ['--verify', 'HEAD^{commit}'], '');
    my $head = 'UNBORN';
    if ($head_result->{status} == 0) {
        _fail('E_REPOSITORY_GIT', 'head stderr') if $head_result->{stderr} ne '';
        ($head = $head_result->{stdout}) =~ s/\n\z//;
        _fail('E_REPOSITORY_HEAD', 'invalid head') if $head !~ /\A[0-9a-f]{40,64}\z/;
    }

    my $branch_result = run_git_raw($repo_root, 'symbolic-ref', ['--quiet', 'HEAD'], '');
    my $branch = 'DETACHED';
    if ($branch_result->{status} == 0) {
        _fail('E_REPOSITORY_GIT', 'branch stderr') if $branch_result->{stderr} ne '';
        ($branch = $branch_result->{stdout}) =~ s/\n\z//;
    }
    elsif ($branch_result->{status} != 1) {
        _fail('E_REPOSITORY_GIT', 'symbolic-ref failed');
    }

    my $status_result = run_git_raw($repo_root, 'status', ['--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=all'], '');
    _fail('E_REPOSITORY_GIT', 'git status failed') if $status_result->{status} != 0 || $status_result->{stderr} ne '';
    my @records = split("\0", $status_result->{stdout}, -1);
    pop @records if @records && $records[-1] eq '';
    _fail('E_LIMIT_STATUS', 'too many status entries') if @records > MAX_STATUS_ITEMS;
    my @changed_paths;
    while (@records) {
        my $record = shift @records;
        _fail('E_REPOSITORY_STATUS', 'malformed status record') if length($record) < 4;
        _fail('E_REPOSITORY_STATUS', 'malformed status separator') if substr($record, 2, 1) ne ' ';
        my $status = substr($record, 0, 2);
        my $path = substr($record, 3);
        source_path_allowed($path);
        push @changed_paths, $path;
        if ($status =~ /[RC]/) {
            _fail('E_REPOSITORY_STATUS', 'rename/copy source path absent') if !@records;
            my $origin = shift @records;
            source_path_allowed($origin);
            push @changed_paths, $origin;
        }
    }
    validate_dirty_paths(\@changed_paths, $declared_paths);

    my @index_args = ('--stage', '-z', '--', @{$declared_paths});
    my $index_result = run_git_raw($repo_root, 'ls-files', \@index_args, '');
    _fail('E_REPOSITORY_GIT', 'ls-files failed') if $index_result->{status} != 0 || $index_result->{stderr} ne '';

    my @worktree;
    for my $path (sort @{$declared_paths}) {
        source_path_allowed($path);
        my $absolute = assert_regular_contained($repo_root, $path, undef);
        my @st = lstat($absolute);
        push @worktree, {
            relative_path => $path,
            type          => 'regular',
            mode          => sprintf('0%03o', $st[2] & 0777),
            bytes         => 0 + $st[7],
            sha256        => sha256_file($absolute, MAX_SOURCE_BYTES),
        };
    }
    my $record = {
        schema_version => 1,
        repository_root => $repo_root,
        git_directory => $git_dir_path,
        head => $head,
        branch => $branch,
        status_sha256 => sha256_hex($status_result->{stdout}),
        index_sha256 => sha256_hex($index_result->{stdout}),
        worktree => \@worktree,
        packet_store_excluded => JSON::PP::true,
    };
    return ($record, sha256_hex(canonical_json($record)));
}

sub collect_repository_observation {
    my ($repo_root) = @_;
    _fail('E_REPOSITORY_ROOT', 'repository root mismatch') if $repo_root ne REPOSITORY_ROOT;
    my $top = run_git_raw($repo_root, 'rev-parse', ['--show-toplevel'], '');
    _fail('E_REPOSITORY_GIT', 'show-toplevel failed') if $top->{status} != 0 || $top->{stderr} ne '';
    (my $top_path = $top->{stdout}) =~ s/\n\z//;
    _fail('E_REPOSITORY_ROOT', 'git top-level mismatch') if $top_path ne $repo_root;

    my $head_result = run_git_raw($repo_root, 'rev-parse', ['--verify', 'HEAD^{commit}'], '');
    my $head = 'UNBORN';
    if ($head_result->{status} == 0) {
        _fail('E_REPOSITORY_GIT', 'head stderr') if $head_result->{stderr} ne '';
        ($head = $head_result->{stdout}) =~ s/\n\z//;
    }
    my $branch_result = run_git_raw($repo_root, 'symbolic-ref', ['--quiet', 'HEAD'], '');
    my $branch = 'DETACHED';
    if ($branch_result->{status} == 0) {
        _fail('E_REPOSITORY_GIT', 'branch stderr') if $branch_result->{stderr} ne '';
        ($branch = $branch_result->{stdout}) =~ s/\n\z//;
    }
    elsif ($branch_result->{status} != 1) {
        _fail('E_REPOSITORY_GIT', 'symbolic-ref failed');
    }
    my $status_result = run_git_raw($repo_root, 'status', ['--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=all'], '');
    _fail('E_REPOSITORY_GIT', 'git status failed') if $status_result->{status} != 0 || $status_result->{stderr} ne '';
    _fail('E_LIMIT_GIT_OUTPUT', 'status output exceeds limit') if length($status_result->{stdout}) > MAX_GIT_STREAM;
    my $observation = {
        schema_version => 1,
        repository_root => $repo_root,
        head => $head,
        branch => $branch,
        status_sha256 => sha256_hex($status_result->{stdout}),
    };
    return ($observation, sha256_hex(canonical_json($observation)));
}

sub _now_utc {
    return strftime('%Y-%m-%dT%H:%M:%SZ', gmtime(time));
}

sub _store_path {
    my ($repo_root) = @_;
    return File::Spec->catdir($repo_root, split('/', STORE_RELATIVE));
}

sub _validate_repo_literal {
    my ($repo_root) = @_;
    _fail('E_REPOSITORY_ROOT', 'repository root must be exact') if !defined($repo_root) || $repo_root ne REPOSITORY_ROOT;
    my $real = abs_path($repo_root);
    _fail('E_REPOSITORY_ROOT', 'repository root realpath mismatch') if !defined($real) || $real ne REPOSITORY_ROOT;
    my @st = lstat($repo_root);
    _fail('E_REPOSITORY_ROOT', 'repository root must be an owned physical directory')
        if !@st || !S_ISDIR($st[2]) || S_ISLNK($st[2]) || $st[4] != $<;
    return 1;
}

sub _parse_source_option {
    my ($value) = @_;
    _fail('E_USAGE_SOURCE', 'source option malformed') if !defined($value) || $value !~ /\A([^:]+):(.+)\z/;
    my ($role, $path) = ($1, $2);
    _fail('E_SOURCE_ROLE', 'source role invalid') if !_is_enum($role, \@SOURCE_ROLES);
    source_path_allowed($path);
    return ($role, $path);
}

sub _validate_option_tokens {
    my ($operation, $args) = @_;
    my %takes_value = map { $_ => 1 } qw(
        --repo-root --request-file --approval-gate --source --prior-packet-id
        --supersedes-packet-id --packet --review-root --verdict-file
        --approval-file --approved-verdict-sha256 --receipt-sha256
    );
    my %flag = map { $_ => 1 } qw(--initialize-store --verbose --rollback);
    my %seen;
    my @copy = @{$args};
    while (@copy) {
        my $token = shift @copy;
        _fail('E_USAGE_OPTIONS', 'unknown or nonliteral option')
            if !defined($token) || $token !~ /\A--[a-z][a-z0-9-]*\z/
            || (!$takes_value{$token} && !$flag{$token});
        _fail('E_USAGE_OPTIONS', 'option repetition is forbidden')
            if $seen{$token}++ && $token ne '--source';
        if ($takes_value{$token}) {
            _fail('E_USAGE_OPTIONS', 'option value absent') if !@copy || $copy[0] =~ /\A--/;
            shift @copy;
        }
    }
    return 1;
}

sub _assert_only_options {
    my ($options, $allowed) = @_;
    my %allowed = map { $_ => 1 } @{$allowed};
    for my $key (keys %{$options}) {
        next if $key eq 'sources' && !@{$options->{$key}};
        next if !defined($options->{$key});
        next if ($key eq 'initialize_store' || $key eq 'verbose' || $key eq 'rollback') && !$options->{$key};
        _fail('E_USAGE_OPTIONS', 'option is incompatible with operation') if !$allowed{$key};
    }
    return 1;
}

sub _validate_operation_options {
    my ($operation, $options) = @_;
    if ($operation eq 'create') {
        if ($options->{initialize_store}) {
            _assert_only_options($options, [qw(repo_root initialize_store sources)]);
        }
        else {
            _assert_only_options($options, [qw(repo_root request_file approval_gate sources prior_packet_id supersedes_packet_id)]);
            _fail('E_USAGE_CREATE', 'create fields missing')
                if !defined($options->{request_file}) || !defined($options->{approval_gate}) || !@{$options->{sources}};
        }
    }
    elsif ($operation eq 'validate') {
        _assert_only_options($options, [qw(repo_root packet review_root verdict_file approval_file sources)]);
        _fail('E_USAGE_VALIDATE', 'packet required') if !defined($options->{packet});
        my $review_count = scalar grep { defined($options->{$_}) } qw(review_root verdict_file approval_file);
        _fail('E_USAGE_REVIEW', 'review inputs must be complete') if $review_count != 0 && $review_count != 3;
    }
    elsif ($operation eq 'list') {
        _assert_only_options($options, [qw(repo_root verbose sources)]);
    }
    elsif ($operation eq 'consume') {
        if ($options->{rollback}) {
            _assert_only_options($options, [qw(repo_root rollback packet receipt_sha256 review_root approval_file sources)]);
            _fail('E_USAGE_ROLLBACK', 'rollback fields missing')
                if !defined($options->{packet}) || !defined($options->{receipt_sha256})
                || !defined($options->{review_root}) || !defined($options->{approval_file});
        }
        else {
            _assert_only_options($options, [qw(repo_root packet review_root verdict_file approval_file approved_verdict_sha256 sources)]);
            _fail('E_USAGE_CONSUME', 'consume fields missing')
                if !defined($options->{packet}) || !defined($options->{review_root})
                || !defined($options->{verdict_file}) || !defined($options->{approval_file})
                || !defined($options->{approved_verdict_sha256});
        }
    }
    return 1;
}

sub _parse_options {
    my ($operation, $args) = @_;
    _validate_option_tokens($operation, $args);
    my %options;
    my @sources;
    Getopt::Long::Configure(qw(no_auto_abbrev no_ignore_case no_getopt_compat require_order));
    my $ok = GetOptionsFromArray(
        $args,
        'repo-root=s' => \$options{repo_root},
        'initialize-store' => \$options{initialize_store},
        'request-file=s' => \$options{request_file},
        'approval-gate=s' => \$options{approval_gate},
        'source=s@' => \@sources,
        'prior-packet-id=s' => \$options{prior_packet_id},
        'supersedes-packet-id=s' => \$options{supersedes_packet_id},
        'packet=s' => \$options{packet},
        'review-root=s' => \$options{review_root},
        'verdict-file=s' => \$options{verdict_file},
        'approval-file=s' => \$options{approval_file},
        'approved-verdict-sha256=s' => \$options{approved_verdict_sha256},
        'verbose' => \$options{verbose},
        'rollback' => \$options{rollback},
        'receipt-sha256=s' => \$options{receipt_sha256},
    );
    _fail('E_USAGE_OPTIONS', 'invalid command option') if !$ok || @{$args};
    $options{sources} = \@sources;
    _fail('E_USAGE_ROOT', 'repo root required') if !defined $options{repo_root};
    _validate_repo_literal($options{repo_root});
    $options{repo_root} = REPOSITORY_ROOT;
    if (defined $options{packet}) {
        validate_packet_number($options{packet});
        ($options{packet}) = $options{packet} =~ /\A([0-9]{6})\z/;
    }
    for my $field (qw(prior_packet_id supersedes_packet_id approved_verdict_sha256 receipt_sha256)) {
        next if !defined $options{$field};
        validate_digest($options{$field});
        ($options{$field}) = $options{$field} =~ /\A([0-9a-f]{64})\z/;
    }
    if (defined $options{request_file}) {
        validate_relative_path($options{request_file});
        ($options{request_file}) = $options{request_file} =~ /\A(.+)\z/s;
    }
    for my $field (qw(review_root verdict_file approval_file)) {
        next if !defined $options{$field};
        _fail('E_USAGE_REVIEW', 'review path contains forbidden bytes') if $options{$field} =~ /[\r\n\0]/;
        ($options{$field}) = $options{$field} =~ /\A(.+)\z/s;
    }
    _validate_operation_options($operation, \%options);
    return \%options;
}

sub initialize_store {
    my ($repo_root) = @_;
    _validate_repo_literal($repo_root);
    my $local = File::Spec->catdir($repo_root, '.mneme-local');
    my $handoffs = File::Spec->catdir($local, 'handoffs');
    my $store = _store_path($repo_root);
    _fail('E_CONFLICT_STORE', 'packet store already exists') if lstat($store);

    my $ignore = run_git_raw($repo_root, 'check-ignore', ['--no-index', '-z', '--stdin'], ".mneme-local/handoffs/v1/\0");
    _fail('E_STORE_NOT_IGNORED', 'packet store is not ignored')
        if $ignore->{status} != 0 || $ignore->{stderr} ne ''
        || $ignore->{stdout} ne ".mneme-local/handoffs/v1/\0";
    my @repo_st = lstat($repo_root);
    for my $directory ($local, $handoffs) {
        if (!lstat($directory)) {
            mkdir($directory, 0700) or _fail('E_STORE_PARENT', 'cannot create protocol parent');
            chmod(0700, $directory) == 1 or _fail('E_STORE_MODE', 'cannot set protocol parent mode');
        }
        _assert_owned_directory($directory, 0700, $repo_st[0]);
    }
    my $staging = File::Spec->catdir($handoffs, '.v1.init.' . $$);
    mkdir($staging, 0700) or _fail('E_STORE_STAGE', 'cannot create initialization stage');
    for my $child (qw(packets staging locks)) {
        mkdir(File::Spec->catdir($staging, $child), 0700) or _fail('E_STORE_CHILD', 'cannot create store child');
    }
    my $sentinel = {
        schema_version => 1,
        record_type => 'mneme.handoff.store',
        repository_root => $repo_root,
        protocol_version => 1,
        owner_uid => 0 + $<,
        created_at => _now_utc(),
        implementation_sha256 => sha256_file(__FILE__, 200_000),
    };
    write_exclusive_synced(File::Spec->catfile($staging, 'MNEME_HANDOFF_STORE.json'), canonical_json($sentinel), 0600);
    _sync_directory($_) for map { File::Spec->catdir($staging, $_) } qw(packets staging locks);
    _sync_directory($staging);
    my @stage_entries;
    opendir(my $sdh, $staging) or _fail('E_STORE_STAGE', 'cannot inspect initialization stage');
    @stage_entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($sdh);
    closedir($sdh);
    validate_store_entries(\@stage_entries);
    _read_owned_file(File::Spec->catfile($staging, 'MNEME_HANDOFF_STORE.json'), MAX_JSON_BYTES, 0600, $repo_st[0]);
    rename($staging, $store) or _fail('E_STORE_RENAME', 'cannot publish packet store');
    my $synced = eval { _sync_directory($handoffs); 1 };
    _fail('E_WRITE_UNCERTAIN', 'store publication sync uncertain') if !$synced;
    return 1;
}

sub validate_store {
    my ($repo_root) = @_;
    _validate_repo_literal($repo_root);
    my $store = _store_path($repo_root);
    my @repo_st = lstat($repo_root);
    my $store_st = _assert_owned_directory($store, 0700, $repo_st[0]);
    opendir(my $dh, $store) or _fail('E_STORE_READ', 'cannot read packet store');
    my @entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($dh);
    closedir($dh);
    validate_store_entries(\@entries);
    for my $child (qw(packets staging locks)) {
        _assert_owned_directory(File::Spec->catdir($store, $child), 0700, $store_st->[0]);
    }
    my $staging_dir = File::Spec->catdir($store, 'staging');
    opendir(my $stdh, $staging_dir) or _fail('E_STORE_READ', 'cannot read staging directory');
    my @staging_entries = grep { $_ ne '.' && $_ ne '..' } readdir($stdh);
    closedir($stdh);
    _fail('E_CONFLICT_STAGE', 'orphan packet staging entry') if @staging_entries;
    my $locks_dir = File::Spec->catdir($store, 'locks');
    opendir(my $ldh, $locks_dir) or _fail('E_STORE_READ', 'cannot read locks directory');
    my @lock_entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($ldh);
    closedir($ldh);
    for my $lock_name (@lock_entries) {
        _fail('E_CONFLICT_LOCK', 'unexpected or stale lock present')
            if $ACTIVE_LOCK_NAME eq '' || $lock_name ne $ACTIVE_LOCK_NAME;
        my $lock_root = File::Spec->catdir($locks_dir, $lock_name);
        _assert_owned_directory($lock_root, 0700, $store_st->[0]);
        opendir(my $odh, $lock_root) or _fail('E_LOCK_READ', 'cannot read lock');
        my @owner_entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($odh);
        closedir($odh);
        _fail('E_CONFLICT_LOCK', 'lock entry mismatch')
            if join("\0", @owner_entries) ne 'owner.json';
        my $owner_bytes = _read_owned_file(
            File::Spec->catfile($lock_root, 'owner.json'), MAX_JSON_BYTES, 0600, $store_st->[0],
        );
        my $owner = decode_canonical_json($owner_bytes);
        my @owner_keys = qw(
            schema_version operation process_id packet_number start_time
            repository_root implementation_sha256
        );
        _closed_keys($owner, \@owner_keys, \@owner_keys);
        _fail('E_LOCK_RECORD', 'lock record schema mismatch')
            if !_json_integer($owner->{schema_version}) || $owner->{schema_version} != 1
            || !_is_enum($owner->{operation}, [qw(create consume rollback)])
            || !_json_integer($owner->{process_id}) || $owner->{process_id} < 1
            || !_utc_timestamp($owner->{start_time})
            || $owner->{repository_root} ne $repo_root;
        if ($owner->{operation} eq 'create') {
            _fail('E_LOCK_RECORD', 'create lock packet must be empty') if $owner->{packet_number} ne '';
        }
        else {
            validate_packet_number($owner->{packet_number});
        }
        validate_digest($owner->{implementation_sha256});
    }
    my $sentinel_bytes = _read_owned_file(
        File::Spec->catfile($store, 'MNEME_HANDOFF_STORE.json'),
        MAX_JSON_BYTES, 0600, $store_st->[0],
    );
    my $sentinel = decode_canonical_json($sentinel_bytes);
    my @sentinel_keys = qw(
        schema_version record_type repository_root protocol_version owner_uid
        created_at implementation_sha256
    );
    _closed_keys($sentinel, \@sentinel_keys, \@sentinel_keys);
    _fail('E_STORE_SENTINEL', 'sentinel schema mismatch')
        if !_json_integer($sentinel->{schema_version}) || $sentinel->{schema_version} != 1
        || !_json_string($sentinel->{record_type}) || $sentinel->{record_type} ne 'mneme.handoff.store';
    _fail('E_STORE_SENTINEL', 'sentinel repository mismatch') if $sentinel->{repository_root} ne $repo_root;
    _fail('E_STORE_SENTINEL', 'sentinel protocol mismatch')
        if !_json_integer($sentinel->{protocol_version}) || $sentinel->{protocol_version} != 1;
    _fail('E_STORE_SENTINEL', 'sentinel owner mismatch')
        if !_json_integer($sentinel->{owner_uid}) || $sentinel->{owner_uid} != $<;
    _fail('E_STORE_SENTINEL', 'sentinel date invalid') if !_utc_timestamp($sentinel->{created_at});
    validate_digest($sentinel->{implementation_sha256});
    my $ignore_input = STORE_RELATIVE . "/\0";
    my $ignore = run_git_raw($repo_root, 'check-ignore', ['--no-index', '-z', '--stdin'], $ignore_input);
    _fail('E_STORE_NOT_IGNORED', 'packet store ignore identity mismatch')
        if $ignore->{status} != 0 || $ignore->{stderr} ne '' || $ignore->{stdout} ne $ignore_input;
    return ($store, $sentinel);
}

sub create_packet {
    my ($options) = @_;
    my $catalog = validate_packet_catalog($options->{repo_root}, 0);
    my $store = $catalog->{store};
    _fail('E_USAGE_CREATE', 'request file required') if !defined $options->{request_file};
    _fail('E_USAGE_CREATE', 'approval gate invalid') if !_is_enum($options->{approval_gate}, \@APPROVAL_GATES);
    _fail('E_LIMIT_SOURCES', 'source count invalid') if !@{$options->{sources}} || @{$options->{sources}} > MAX_SOURCES;

    my @declared;
    my %roles;
    for my $source (@{$options->{sources}}) {
        my ($role, $path) = _parse_source_option($source);
        _fail('E_SOURCE_DUPLICATE', 'duplicate source') if exists $roles{$path};
        $roles{$path} = $role;
        push @declared, $path;
    }
    source_path_allowed($options->{request_file});
    _fail('E_REQUEST_SOURCE', 'request must be a proposal source')
        if !exists($roles{$options->{request_file}}) || $roles{$options->{request_file}} ne 'proposal';

    my $request_path = assert_regular_contained($options->{repo_root}, $options->{request_file}, undef);
    my $request_bytes = read_bounded_file($request_path, MAX_REQUEST_BYTES);
    my ($repo_record, $repo_sha) = collect_repository_state($options->{repo_root}, \@declared);

    my @source_rows;
    for my $path (@declared) {
        my $absolute = assert_regular_contained($options->{repo_root}, $path, undef);
        my @st = lstat($absolute);
        push @source_rows, {
            relative_path => $path,
            type => 'regular',
            mode => sprintf('0%03o', $st[2] & 0777),
            bytes => 0 + $st[7],
            sha256 => sha256_file($absolute, MAX_SOURCE_BYTES),
            role => $roles{$path},
        };
    }
    my $sources_tsv = canonical_sources_tsv(\@source_rows);
    my $sources_sha = sha256_hex($sources_tsv);
    my $request_sha = sha256_hex($request_bytes);

    my $lock_path = File::Spec->catdir($store, 'locks', 'create.lock');
    local $ACTIVE_LOCK_NAME = 'create.lock';
    acquire_lock($lock_path, {
        schema_version => 1,
        operation => 'create',
        process_id => 0 + $$,
        packet_number => '',
        start_time => _now_utc(),
        repository_root => $options->{repo_root},
        implementation_sha256 => sha256_file(__FILE__, 200_000),
    });

    my $packets_dir = File::Spec->catdir($store, 'packets');
    my $locked_catalog = validate_packet_catalog($options->{repo_root}, 0);
    my $next = $locked_catalog->{next_number};

    my $locked_request_bytes = read_bounded_file($request_path, MAX_REQUEST_BYTES);
    _fail('E_STALE_CREATE', 'request changed before lock') if sha256_hex($locked_request_bytes) ne $request_sha;
    my ($locked_repo_record, $locked_repo_sha) = collect_repository_state($options->{repo_root}, \@declared);
    _fail('E_STALE_CREATE', 'repository changed before lock') if $locked_repo_sha ne $repo_sha;
    for my $row (@source_rows) {
        my $absolute = assert_regular_contained($options->{repo_root}, $row->{relative_path}, undef);
        my @st = lstat($absolute);
        _fail('E_STALE_CREATE', 'source bytes changed before lock') if $st[7] != $row->{bytes};
        _fail('E_STALE_CREATE', 'source mode changed before lock') if sprintf('0%03o', $st[2] & 0777) ne $row->{mode};
        _fail('E_STALE_CREATE', 'source hash changed before lock') if sha256_file($absolute, MAX_SOURCE_BYTES) ne $row->{sha256};
    }
    $repo_record = $locked_repo_record;
    $repo_sha = $locked_repo_sha;

    my $packet = {
        schema_version => 1,
        protocol_version => 1,
        packet_number => $next,
        purpose => 'file-based review handoff',
        review_question => $options->{request_file},
        created_at => _now_utc(),
        repository_root => $options->{repo_root},
        head => $repo_record->{head},
        branch => $repo_record->{branch},
        repository_state_sha256 => $repo_sha,
        request_sha256 => $request_sha,
        sources_sha256 => $sources_sha,
        prior_packet_id => ($options->{prior_packet_id} // ''),
        superseded_packet_id => ($options->{supersedes_packet_id} // ''),
        approval_gate => $options->{approval_gate},
        non_authorization => 'packet consumption records a handoff and never authorizes project work',
        source_count => 0 + @source_rows,
        source_bytes => 0 + (do { my $sum = 0; $sum += $_->{bytes} for @source_rows; $sum }),
    };
    validate_digest($packet->{prior_packet_id}) if $packet->{prior_packet_id} ne '';
    validate_digest($packet->{superseded_packet_id}) if $packet->{superseded_packet_id} ne '';
    $packet->{packet_id} = compute_packet_id($packet, $request_sha, $sources_sha, $repo_sha);
    validate_packet_record($packet, $next, $options->{repo_root});
    validate_new_packet_lineage($locked_catalog, $packet);
    my $packet_json = canonical_json($packet);
    my $repository_json = canonical_json($repo_record);
    my @manifest_rows = (
        ['packet.json', length($packet_json), sha256_hex($packet_json)],
        ['request.md', length($request_bytes), $request_sha],
        ['sources.tsv', length($sources_tsv), $sources_sha],
        ['repository-state.json', length($repository_json), sha256_hex($repository_json)],
    );
    my $manifest = "path\tbytes\tsha256\n";
    $manifest .= join("\t", @{$_}) . "\n" for @manifest_rows;

    my $staging = File::Spec->catdir($store, 'staging', "create-$next.tmp");
    my $final = File::Spec->catdir($packets_dir, $next);
    mkdir($staging, 0700) or _fail('E_WRITE_STAGE', 'cannot create packet stage');
    mkdir(File::Spec->catdir($staging, 'transactions'), 0700) or _fail('E_WRITE_STAGE', 'cannot create transactions');
    mkdir(File::Spec->catdir($staging, 'rollbacks'), 0700) or _fail('E_WRITE_STAGE', 'cannot create rollbacks');
    my %files = (
        'packet.json' => $packet_json,
        'request.md' => $request_bytes,
        'sources.tsv' => $sources_tsv,
        'repository-state.json' => $repository_json,
        'packet-manifest.sha256' => $manifest,
    );
    for my $name (sort keys %files) {
        write_exclusive_synced(File::Spec->catfile($staging, $name), $files{$name}, 0600);
    }
    my @store_st = lstat($store);
    _assert_owned_directory($staging, 0700, $store_st[0]);
    _assert_owned_directory(File::Spec->catdir($staging, 'transactions'), 0700, $store_st[0]);
    _assert_owned_directory(File::Spec->catdir($staging, 'rollbacks'), 0700, $store_st[0]);
    opendir(my $sdh, $staging) or _fail('E_WRITE_STAGE', 'cannot inspect packet stage');
    my @stage_entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($sdh);
    closedir($sdh);
    my @expected_entries = sort (keys(%files), qw(transactions rollbacks));
    _fail('E_WRITE_STAGE', 'packet stage entry mismatch')
        if join("\0", @stage_entries) ne join("\0", @expected_entries);
    for my $name (sort keys %files) {
        my $verified = _read_owned_file(
            File::Spec->catfile($staging, $name),
            length($files{$name}), 0600, $store_st[0],
        );
        _fail('E_WRITE_STAGE', 'packet stage bytes mismatch') if $verified ne $files{$name};
    }
    _sync_directory(File::Spec->catdir($staging, 'transactions'));
    _sync_directory(File::Spec->catdir($staging, 'rollbacks'));
    _sync_directory($staging);
    _fail('E_CONFLICT_FINAL', 'packet path exists') if lstat($final);
    rename($staging, $final) or _fail('E_WRITE_RENAME', 'packet rename failed');
    my $synced = eval { _sync_directory($packets_dir); 1 };
    _fail('E_WRITE_UNCERTAIN', 'packet publication sync uncertain') if !$synced;
    release_lock_success($lock_path);
    return $packet;
}

sub _packet_paths {
    my ($store, $number) = @_;
    validate_packet_number($number);
    my $root = File::Spec->catdir($store, 'packets', $number);
    return ($root, map { File::Spec->catfile($root, $_) } qw(packet.json request.md sources.tsv repository-state.json packet-manifest.sha256));
}

sub validate_packet_directory {
    my ($repo_root, $number, $external) = @_;
    $external = {} if !defined $external;
    my ($store) = validate_store($repo_root);
    my @store_st = lstat($store);
    my ($root, $packet_path, $request_path, $sources_path, $repository_path, $manifest_path) = _packet_paths($store, $number);
    _assert_owned_directory($root, 0700, $store_st[0]);
    opendir(my $dh, $root) or _fail('E_PACKET_MISSING', 'packet directory absent');
    my @entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($dh);
    closedir($dh);
    validate_packet_entries(\@entries);
    my $packet_bytes = _read_owned_file($packet_path, MAX_JSON_BYTES, 0600, $store_st[0]);
    my $request_bytes = _read_owned_file($request_path, MAX_REQUEST_BYTES, 0600, $store_st[0]);
    my $sources_bytes = _read_owned_file($sources_path, MAX_TSV_BYTES, 0600, $store_st[0]);
    my $repository_bytes = _read_owned_file($repository_path, MAX_JSON_BYTES, 0600, $store_st[0]);
    my $manifest_bytes = _read_owned_file($manifest_path, MAX_TSV_BYTES, 0600, $store_st[0]);
    my $packet = decode_canonical_json($packet_bytes);
    my $repository = decode_canonical_json($repository_bytes);
    validate_packet_record($packet, $number, $repo_root);
    validate_repository_record($repository, $repo_root);

    my $request_sha = sha256_hex($request_bytes);
    my $sources_sha = sha256_hex($sources_bytes);
    my $repository_sha = sha256_hex(canonical_json($repository));
    _fail('E_STALE_REQUEST', 'request identity mismatch') if $request_sha ne $packet->{request_sha256};
    _fail('E_STALE_SOURCES', 'source manifest identity mismatch') if $sources_sha ne $packet->{sources_sha256};
    _fail('E_STALE_REPOSITORY', 'repository record identity mismatch') if $repository_sha ne $packet->{repository_state_sha256};
    my $source_rows = parse_sources_tsv($sources_bytes);
    _fail('E_PACKET_SOURCE_COUNT', 'packet source count mismatch') if $packet->{source_count} != @{$source_rows};
    my $source_total = 0;
    $source_total += $_->{bytes} for @{$source_rows};
    _fail('E_PACKET_SOURCE_BYTES', 'packet source bytes mismatch') if $packet->{source_bytes} != $source_total;
    _fail('E_PACKET_REQUEST_SOURCE', 'packet request is not declared proposal source')
        if !grep { $_->{relative_path} eq $packet->{review_question} && $_->{role} eq 'proposal' } @{$source_rows};
    _fail('E_REPOSITORY_WORKTREE', 'repository worktree count mismatch')
        if @{$repository->{worktree}} != @{$source_rows};
    for my $index (0 .. $#{$source_rows}) {
        my $source = $source_rows->[$index];
        my $worktree = $repository->{worktree}[$index];
        for my $field (qw(relative_path type mode bytes sha256)) {
            _fail('E_REPOSITORY_WORKTREE', 'repository/source identity mismatch')
                if "$source->{$field}" ne "$worktree->{$field}";
        }
    }
    _fail('E_REPOSITORY_HEAD', 'packet/repository head mismatch') if $packet->{head} ne $repository->{head};
    _fail('E_REPOSITORY_BRANCH', 'packet/repository branch mismatch') if $packet->{branch} ne $repository->{branch};

    my $computed = compute_packet_id($packet, $request_sha, $sources_sha, $repository_sha);
    _fail('E_PACKET_ID', 'packet id mismatch') if $computed ne $packet->{packet_id};

    my $expected_manifest = "path\tbytes\tsha256\n";
    for my $row (
        ['packet.json', length($packet_bytes), sha256_hex($packet_bytes)],
        ['request.md', length($request_bytes), sha256_hex($request_bytes)],
        ['sources.tsv', length($sources_bytes), sha256_hex($sources_bytes)],
        ['repository-state.json', length($repository_bytes), sha256_hex($repository_bytes)],
    ) {
        $expected_manifest .= join("\t", @{$row}) . "\n";
    }
    _fail('E_PACKET_MANIFEST', 'packet manifest mismatch') if $manifest_bytes ne $expected_manifest;

    my $transactions = File::Spec->catdir($root, 'transactions');
    my $rollbacks = File::Spec->catdir($root, 'rollbacks');
    _assert_owned_directory($transactions, 0700, $store_st[0]);
    _assert_owned_directory($rollbacks, 0700, $store_st[0]);
    opendir(my $tdh, $transactions) or _fail('E_TRANSACTION_DIR', 'transaction directory absent');
    my @transaction_entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($tdh);
    closedir($tdh);
    opendir(my $rdh, $rollbacks) or _fail('E_ROLLBACK_DIR', 'rollback directory absent');
    my @rollback_entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($rdh);
    closedir($rdh);
    _fail('E_TRANSACTION_ENTRY', 'transaction entry name invalid')
        if grep { $_ !~ /\A[0-9a-f]{64}\z/ } @transaction_entries;
    _fail('E_ROLLBACK_ENTRY', 'rollback entry name invalid')
        if grep { $_ !~ /\A[0-9a-f]{64}\.json\z/ } @rollback_entries;
    my $facts = {
        conflict => (@transaction_entries > 1 || @rollback_entries > 1) ? 1 : 0,
        stale => 0,
    };
    my ($verdict, $approval, $receipt, $receipt_sha);
    if (@transaction_entries == 1) {
        my $transaction_name = $transaction_entries[0];
        {
            my $transaction_root = File::Spec->catdir($transactions, $transaction_name);
            _assert_owned_directory($transaction_root, 0700, $store_st[0]);
            opendir(my $xdh, $transaction_root) or _fail('E_TRANSACTION_READ', 'cannot read transaction');
            my @tx_entries = sort grep { $_ ne '.' && $_ ne '..' } readdir($xdh);
            closedir($xdh);
            my @expected = qw(approval.json receipt.json verdict.json);
            $facts->{conflict} = 1 if join("\0", @tx_entries) ne join("\0", @expected);
            if (!$facts->{conflict}) {
                my $verdict_bytes = _read_owned_file(File::Spec->catfile($transaction_root, 'verdict.json'), MAX_VERDICT_BYTES, 0600, $store_st[0]);
                my $approval_bytes = _read_owned_file(File::Spec->catfile($transaction_root, 'approval.json'), MAX_APPROVAL_BYTES, 0600, $store_st[0]);
                my $receipt_bytes = _read_owned_file(File::Spec->catfile($transaction_root, 'receipt.json'), MAX_RECEIPT_BYTES, 0600, $store_st[0]);
                $verdict = decode_canonical_json($verdict_bytes, MAX_VERDICT_BYTES);
                $approval = decode_canonical_json($approval_bytes, MAX_APPROVAL_BYTES);
                $receipt = decode_canonical_json($receipt_bytes, MAX_RECEIPT_BYTES);
                my $verdict_sha = validate_verdict_approval($verdict, $approval, $verdict_bytes);
                validate_receipt($receipt);
                $receipt_sha = sha256_hex($receipt_bytes);
                _fail('E_TRANSACTION_RECEIPT', 'receipt directory identity mismatch') if $receipt_sha ne $transaction_name;
                _fail('E_TRANSACTION_PACKET', 'verdict packet mismatch')
                    if $verdict->{packet_number} ne $packet->{packet_number}
                    || $verdict->{packet_id} ne $packet->{packet_id};
                _fail('E_TRANSACTION_MANIFEST', 'verdict manifest mismatch')
                    if $verdict->{packet_manifest_sha256} ne sha256_hex($manifest_bytes);
                _fail('E_TRANSACTION_REPOSITORY', 'verdict repository mismatch')
                    if $verdict->{repository_state_sha256} ne $packet->{repository_state_sha256};
                _fail('E_TRANSACTION_SOURCES', 'verdict source mismatch')
                    if $verdict->{sources_sha256} ne $sources_sha;
                _fail('E_TRANSACTION_PACKET', 'transaction packet mismatch') if $receipt->{packet_id} ne $packet->{packet_id};
                _fail('E_TRANSACTION_VERDICT', 'transaction verdict mismatch') if $receipt->{verdict_sha256} ne $verdict_sha;
                _fail('E_TRANSACTION_APPROVAL', 'transaction approval mismatch') if $receipt->{approval_sha256} ne sha256_hex($approval_bytes);
                _fail('E_TRANSACTION_REPOSITORY', 'transaction repository mismatch') if $receipt->{repository_state_sha256} ne $packet->{repository_state_sha256};
                _fail('E_TRANSACTION_PACKET', 'transaction packet number mismatch') if $receipt->{packet_number} ne $packet->{packet_number};
                _fail('E_TRANSACTION_MANIFEST', 'transaction manifest mismatch') if $receipt->{packet_manifest_sha256} ne sha256_hex($manifest_bytes);
                _fail('E_TRANSACTION_SOURCES', 'transaction source mismatch') if $receipt->{sources_sha256} ne $sources_sha;
                _fail('E_TRANSACTION_VERDICT', 'transaction verdict value mismatch') if $receipt->{verdict} ne $verdict->{verdict};
                $facts->{verdict} = $verdict->{verdict};
                $facts->{receipt} = 1;
            }
        }
    }
    if (@rollback_entries == 1) {
        my $rollback_name = $rollback_entries[0];
        if (!defined($receipt_sha)) {
            $facts->{conflict} = 1;
        }
        else {
            my ($expected_sha) = $rollback_name =~ /\A([0-9a-f]{64})\.json\z/;
            my $rollback_bytes = _read_owned_file(File::Spec->catfile($rollbacks, $rollback_name), MAX_ROLLBACK_BYTES, 0600, $store_st[0]);
            _fail('E_ROLLBACK_ID', 'rollback filename identity mismatch') if sha256_hex($rollback_bytes) ne $expected_sha;
            my $rollback = decode_canonical_json($rollback_bytes, MAX_ROLLBACK_BYTES);
            validate_rollback($rollback, $receipt_sha, $rollback->{current_repository_state_sha256});
            _fail('E_ROLLBACK_PACKET', 'rollback packet mismatch') if $rollback->{packet_id} ne $packet->{packet_id};
            _fail('E_ROLLBACK_REPOSITORY', 'rollback original repository mismatch')
                if $rollback->{original_repository_state_sha256} ne $packet->{repository_state_sha256};
            $facts->{rolled_back} = 1;
        }
    }
    if ($external->{check_repository}) {
        my @declared = map { $_->{relative_path} } @{$source_rows};
        my ($current_record, $current_sha);
        my $ok = eval {
            ($current_record, $current_sha) = collect_repository_state($repo_root, \@declared);
            1;
        };
        if (!$ok) {
            my $code = failure_code($@);
            if ($code =~ /\AE_UNSAFE_(?:MISSING|OWNER|MODE|TYPE|LINK|SYMLINK|REALPATH|ESCAPE|SOURCE_ROOT|SOURCE_IGNORED)\z/
                || $code eq 'E_REPOSITORY_UNREPRESENTED') {
                $facts->{stale} = 1;
            }
            else {
                die $@;
            }
        }
        elsif ($current_sha ne $packet->{repository_state_sha256}) {
            $facts->{stale} = 1;
        }
    }
    if ($external && $external->{current_repository_sha256}) {
        $facts->{stale} = 1 if $external->{current_repository_sha256} ne $packet->{repository_state_sha256};
    }
    my $state = derive_state($facts);
    return {
        packet => $packet,
        repository => $repository,
        packet_root => $root,
        source_rows => $source_rows,
        transaction_entries => \@transaction_entries,
        rollback_entries => \@rollback_entries,
        verdict => $verdict,
        approval => $approval,
        receipt => $receipt,
        receipt_sha256 => $receipt_sha,
        state => $state,
        packet_manifest_sha256 => sha256_hex($manifest_bytes),
        sources_sha256 => sha256_hex($sources_bytes),
    };
}

sub validate_packet_catalog {
    my ($repo_root, $check_repository) = @_;
    my ($store) = validate_store($repo_root);
    my $packets = File::Spec->catdir($store, 'packets');
    opendir(my $dh, $packets) or _fail('E_PACKET_LIST', 'cannot list packets');
    my @numbers = sort grep { $_ ne '.' && $_ ne '..' } readdir($dh);
    closedir($dh);
    my $next = validate_number_sequence(\@numbers);
    my (%by_number, %by_id, %nodes, %superseded_by);
    for my $number (@numbers) {
        my $validated = validate_packet_directory(
            $repo_root,
            $number,
            { check_repository => ($check_repository ? 1 : 0) },
        );
        my $id = $validated->{packet}{packet_id};
        _fail('E_CONFLICT_PACKET_ID', 'duplicate packet identity') if exists $by_id{$id};
        $by_number{$number} = $validated;
        $by_id{$id} = $validated;
        $nodes{$id} = { prior => $validated->{packet}{prior_packet_id} };
    }
    validate_lineage(\%nodes);
    for my $number (@numbers) {
        my $validated = $by_number{$number};
        my $superseded = $validated->{packet}{superseded_packet_id};
        next if $superseded eq '';
        _fail('E_CONFLICT_SUPERSESSION', 'superseded packet does not exist') if !exists $by_id{$superseded};
        _fail('E_CONFLICT_SUPERSESSION', 'supersession must name the explicit predecessor')
            if $validated->{packet}{prior_packet_id} ne $superseded;
        _fail('E_CONFLICT_SUPERSESSION', 'packet superseded more than once') if $superseded_by{$superseded}++;
    }
    for my $id (keys %superseded_by) {
        my $validated = $by_id{$id};
        $validated->{state} = 'Stale' if $validated->{state} ne 'Conflict';
    }
    my %pending_by_gate;
    for my $number (@numbers) {
        my $validated = $by_number{$number};
        next if $validated->{state} ne 'Pending';
        my $gate = $validated->{packet}{approval_gate};
        if (defined $pending_by_gate{$gate}) {
            _fail('E_CONFLICT_GATE', 'overlapping live approval gate lacks predecessor relation')
                if $validated->{packet}{prior_packet_id} ne $pending_by_gate{$gate};
        }
        $pending_by_gate{$gate} = $validated->{packet}{packet_id};
    }
    return {
        store => $store,
        numbers => \@numbers,
        next_number => $next,
        by_number => \%by_number,
        by_id => \%by_id,
        pending_by_gate => \%pending_by_gate,
    };
}

sub validate_new_packet_lineage {
    my ($catalog, $packet) = @_;
    for my $field (qw(prior_packet_id superseded_packet_id)) {
        my $id = $packet->{$field};
        next if $id eq '';
        _fail('E_CONFLICT_LINEAGE_MISSING', 'new packet lineage target missing')
            if !exists $catalog->{by_id}{$id};
    }
    _fail('E_CONFLICT_SUPERSESSION', 'supersession must equal explicit predecessor')
        if $packet->{superseded_packet_id} ne ''
        && $packet->{prior_packet_id} ne $packet->{superseded_packet_id};
    my $live = $catalog->{pending_by_gate}{$packet->{approval_gate}};
    _fail('E_CONFLICT_GATE', 'new packet must name live predecessor for approval gate')
        if defined($live) && $packet->{prior_packet_id} ne $live;
    return 1;
}

sub _validate_review_file {
    my ($review_root, $path, $limit) = @_;
    _fail('E_REVIEW_ROOT', 'review root must be absolute') if !defined($review_root) || !File::Spec->file_name_is_absolute($review_root);
    _fail('E_REVIEW_PATH', 'review file must be absolute') if !defined($path) || !File::Spec->file_name_is_absolute($path);
    my @root_st = lstat($review_root);
    _fail('E_REVIEW_ROOT', 'review root absent') if !@root_st || !S_ISDIR($root_st[2]);
    _fail('E_REVIEW_MODE', 'review root mode must be 0700') if (($root_st[2] & 07777) != 0700);
    _fail('E_REVIEW_OWNER', 'review root owner mismatch') if $root_st[4] != $<;
    my $root_real = abs_path($review_root);
    my $path_real = abs_path($path);
    _fail('E_REVIEW_PATH', 'review file cannot resolve') if !defined($root_real) || !defined($path_real);
    _fail('E_REVIEW_ROOT', 'review root must be outside repository')
        if $root_real eq REPOSITORY_ROOT || index($root_real, REPOSITORY_ROOT . '/') == 0
        || index(REPOSITORY_ROOT, $root_real . '/') == 0;
    my $parent = dirname($root_real);
    my @parent_st = lstat($parent);
    _fail('E_REVIEW_MOUNT', 'review root mount point is forbidden')
        if !@parent_st || $parent_st[0] != $root_st[0];
    _fail('E_REVIEW_ESCAPE', 'review file outside root') if index($path_real, $root_real . '/') != 0;
    my @st = lstat($path);
    _fail('E_REVIEW_TYPE', 'review file must be regular') if !@st || !S_ISREG($st[2]) || S_ISLNK($st[2]);
    _fail('E_REVIEW_MODE', 'review file mode must be 0600') if (($st[2] & 07777) != 0600);
    _fail('E_REVIEW_OWNER', 'review file owner mismatch') if $st[4] != $<;
    return _read_owned_file($path_real, $limit, 0600, $root_st[0]);
}

sub consume_packet {
    my ($options) = @_;
    validate_packet_number($options->{packet});
    my $catalog = validate_packet_catalog($options->{repo_root}, $options->{rollback} ? 0 : 1);
    my $store = $catalog->{store};
    _fail('E_USAGE_REVIEW', 'review root required') if !defined $options->{review_root};
    my $lock_path = File::Spec->catdir($store, 'locks', "packet-$options->{packet}.lock");
    local $ACTIVE_LOCK_NAME = "packet-$options->{packet}.lock";
    if ($options->{rollback}) {
        validate_digest($options->{receipt_sha256});
        my $approval_bytes = _validate_review_file($options->{review_root}, $options->{approval_file}, MAX_APPROVAL_BYTES);
        my $approval = decode_canonical_json($approval_bytes, MAX_APPROVAL_BYTES);
        validate_rollback_approval($approval);
        my $validated = $catalog->{by_number}{$options->{packet}};
        _fail('E_PACKET_MISSING', 'packet directory absent') if !defined $validated;
        _fail('E_CONFLICT_ROLLBACK_STATE', 'packet has no active transaction')
            if !defined($validated->{receipt_sha256}) || $validated->{state} eq 'RolledBack';
        _fail('E_CONFLICT_ROLLBACK_RECEIPT', 'rollback approval targets another receipt')
            if $approval->{receipt_sha256} ne $options->{receipt_sha256}
            || $validated->{receipt_sha256} ne $options->{receipt_sha256};
        _fail('E_APPROVAL_MISMATCH', 'rollback approval packet mismatch')
            if $approval->{packet_id} ne $validated->{packet}{packet_id}
            || $approval->{packet_number} ne $options->{packet};
        my ($observation, $current_repository_sha) = collect_repository_observation($options->{repo_root});

        acquire_lock($lock_path, {
            schema_version => 1,
            operation => 'rollback',
            process_id => 0 + $$,
            packet_number => $options->{packet},
            start_time => _now_utc(),
            repository_root => $options->{repo_root},
            implementation_sha256 => sha256_file(__FILE__, 200_000),
        });
        my $approval_bytes_locked = _validate_review_file($options->{review_root}, $options->{approval_file}, MAX_APPROVAL_BYTES);
        _fail('E_APPROVAL_CHANGED', 'rollback approval changed under lock')
            if sha256_hex($approval_bytes_locked) ne sha256_hex($approval_bytes);
        $catalog = validate_packet_catalog($options->{repo_root}, 0);
        $validated = $catalog->{by_number}{$options->{packet}};
        _fail('E_PACKET_MISSING', 'packet disappeared under lock') if !defined $validated;
        _fail('E_CONFLICT_ROLLBACK_STATE', 'transaction changed under lock')
            if !defined($validated->{receipt_sha256})
            || $validated->{receipt_sha256} ne $options->{receipt_sha256}
            || $validated->{state} eq 'RolledBack';
        my ($locked_observation, $locked_repository_sha) = collect_repository_observation($options->{repo_root});
        _fail('E_STALE_ROLLBACK', 'repository observation changed under lock')
            if $locked_repository_sha ne $current_repository_sha;
        my $rollback = {
            schema_version => 1,
            record_type => 'mneme.handoff.rollback',
            packet_id => $validated->{packet}{packet_id},
            receipt_sha256 => $options->{receipt_sha256},
            approval_sha256 => sha256_hex($approval_bytes),
            original_repository_state_sha256 => $validated->{packet}{repository_state_sha256},
            current_repository_state_sha256 => $current_repository_sha,
            reason => 'user-approved protocol rollback',
            rollback_date => _now_utc(),
        };
        my $bytes_value = canonical_json($rollback);
        my $sha = sha256_hex($bytes_value);
        my $rollback_dir = File::Spec->catdir($validated->{packet_root}, 'rollbacks');
        my $stage = File::Spec->catfile($rollback_dir, ".staging-$sha");
        my $final = File::Spec->catfile($rollback_dir, "$sha.json");
        atomic_publish_file($stage, $final, $bytes_value, undef);
        release_lock_success($lock_path);
        return { state => 'RolledBack', rollback_sha256 => $sha };
    }

    validate_digest($options->{approved_verdict_sha256});
    my $verdict_bytes = _validate_review_file($options->{review_root}, $options->{verdict_file}, MAX_VERDICT_BYTES);
    my $approval_bytes = _validate_review_file($options->{review_root}, $options->{approval_file}, MAX_APPROVAL_BYTES);
    my $verdict = decode_canonical_json($verdict_bytes, MAX_VERDICT_BYTES);
    my $approval = decode_canonical_json($approval_bytes, MAX_APPROVAL_BYTES);
    my $verdict_sha = validate_verdict_approval($verdict, $approval, $verdict_bytes);
    _fail('E_APPROVAL_VERDICT_HASH', 'approved verdict argument mismatch') if $verdict_sha ne $options->{approved_verdict_sha256};
    my $validated = $catalog->{by_number}{$options->{packet}};
    _fail('E_PACKET_MISSING', 'packet directory absent') if !defined $validated;
    _fail('E_PACKET_NOT_PENDING', 'packet is not pending') if $validated->{state} ne 'Pending';
    for my $field (qw(packet_id repository_state_sha256)) {
        _fail('E_APPROVAL_MISMATCH', 'verdict packet mismatch') if $verdict->{$field} ne $validated->{packet}{$field};
    }
    _fail('E_APPROVAL_MISMATCH', 'verdict source mismatch') if $verdict->{sources_sha256} ne $validated->{sources_sha256};
    _fail('E_APPROVAL_MISMATCH', 'verdict manifest mismatch') if $verdict->{packet_manifest_sha256} ne $validated->{packet_manifest_sha256};

    acquire_lock($lock_path, {
        schema_version => 1,
        operation => 'consume',
        process_id => 0 + $$,
        packet_number => $options->{packet},
        start_time => _now_utc(),
        repository_root => $options->{repo_root},
        implementation_sha256 => sha256_file(__FILE__, 200_000),
    });
    my $verdict_bytes_locked = _validate_review_file($options->{review_root}, $options->{verdict_file}, MAX_VERDICT_BYTES);
    my $approval_bytes_locked = _validate_review_file($options->{review_root}, $options->{approval_file}, MAX_APPROVAL_BYTES);
    _fail('E_VERDICT_CHANGED', 'verdict changed under lock') if sha256_hex($verdict_bytes_locked) ne sha256_hex($verdict_bytes);
    _fail('E_APPROVAL_CHANGED', 'approval changed under lock') if sha256_hex($approval_bytes_locked) ne sha256_hex($approval_bytes);
    $catalog = validate_packet_catalog($options->{repo_root}, 1);
    $validated = $catalog->{by_number}{$options->{packet}};
    _fail('E_PACKET_MISSING', 'packet disappeared under lock') if !defined $validated;
    _fail('E_PACKET_NOT_PENDING', 'packet changed under lock') if $validated->{state} ne 'Pending';

    my $receipt = {
        schema_version => 1,
        record_type => 'mneme.handoff.receipt',
        packet_number => $options->{packet},
        packet_id => $validated->{packet}{packet_id},
        packet_manifest_sha256 => $validated->{packet_manifest_sha256},
        repository_state_sha256 => $validated->{packet}{repository_state_sha256},
        sources_sha256 => $validated->{sources_sha256},
        verdict => $verdict->{verdict},
        verdict_sha256 => $verdict_sha,
        approval_sha256 => sha256_hex($approval_bytes),
        implementation_sha256 => sha256_file(__FILE__, 200_000),
        runtime_sha256 => $BINARY_IDENTITIES{perl}{sha256},
        git_sha256 => $BINARY_IDENTITIES{git}{sha256},
        consumed_at => _now_utc(),
        project_work_authorized => JSON::PP::false,
        project_work_executed => JSON::PP::false,
    };
    validate_receipt($receipt);
    my $receipt_bytes = canonical_json($receipt);
    my $receipt_sha = sha256_hex($receipt_bytes);
    my $transactions = File::Spec->catdir($validated->{packet_root}, 'transactions');
    my $stage = File::Spec->catdir($transactions, ".staging-$receipt_sha");
    my $final = File::Spec->catdir($transactions, $receipt_sha);
    atomic_publish_directory($stage, $final, {
        'verdict.json' => $verdict_bytes,
        'approval.json' => $approval_bytes,
        'receipt.json' => $receipt_bytes,
    }, undef);
    release_lock_success($lock_path);
    return { state => derive_state({ verdict => $verdict->{verdict}, receipt => 1 }), receipt_sha256 => $receipt_sha };
}

sub list_packets {
    my ($options) = @_;
    my $catalog = validate_packet_catalog($options->{repo_root}, 1);
    my $output = '';
    for my $number (@{$catalog->{numbers}}) {
        my $validated = $catalog->{by_number}{$number};
        my $packet = $validated->{packet};
        $output .= render_list_line({
            packet_number => $number,
            packet_id => $packet->{packet_id},
            state => $validated->{state},
            verdict => (defined($validated->{verdict}) ? $validated->{verdict}{verdict} : undef),
            created_at => $packet->{created_at},
            head => $packet->{head},
            reason => 'OK',
            repository_state_sha256 => $packet->{repository_state_sha256},
            paths => [],
        }, $options->{verbose});
    }
    return $output;
}

sub dispatch {
    my ($argv) = @_;
    _fail('E_USAGE_OPERATION', 'operation required') if !@{$argv};
    my $operation = shift @{$argv};
    _fail('E_USAGE_OPERATION', 'unknown operation') if !_is_enum($operation, [qw(create validate list consume)]);
    my $options = _parse_options($operation, $argv);
    if ($operation eq 'create') {
        if ($options->{initialize_store}) {
            _fail('E_USAGE_CREATE', 'initialize-store cannot take packet fields')
                if defined($options->{request_file}) || @{$options->{sources}};
            initialize_store($options->{repo_root});
            return "initialized\n";
        }
        my $packet = create_packet($options);
        return join("\t", $packet->{packet_number}, $packet->{packet_id}, 'Pending') . "\n";
    }
    if ($operation eq 'validate') {
        validate_packet_number($options->{packet});
        my $catalog = validate_packet_catalog($options->{repo_root}, 1);
        my $validated = $catalog->{by_number}{$options->{packet}};
        _fail('E_PACKET_MISSING', 'packet directory absent') if !defined $validated;
        if (defined($options->{verdict_file}) || defined($options->{approval_file})) {
            _fail('E_USAGE_REVIEW', 'complete review inputs required')
                if !defined($options->{review_root}) || !defined($options->{verdict_file}) || !defined($options->{approval_file});
            my $vb = _validate_review_file($options->{review_root}, $options->{verdict_file}, MAX_VERDICT_BYTES);
            my $ab = _validate_review_file($options->{review_root}, $options->{approval_file}, MAX_APPROVAL_BYTES);
            my $verdict = decode_canonical_json($vb);
            my $approval = decode_canonical_json($ab);
            validate_verdict_approval($verdict, $approval, $vb);
            _fail('E_PACKET_NOT_PENDING', 'packet is not pending') if $validated->{state} ne 'Pending';
            _fail('E_APPROVAL_MISMATCH', 'verdict packet mismatch')
                if $verdict->{packet_id} ne $validated->{packet}{packet_id}
                || $verdict->{packet_number} ne $options->{packet}
                || $verdict->{repository_state_sha256} ne $validated->{packet}{repository_state_sha256}
                || $verdict->{sources_sha256} ne $validated->{sources_sha256}
                || $verdict->{packet_manifest_sha256} ne $validated->{packet_manifest_sha256};
            return join("\t", $options->{packet}, $validated->{packet}{packet_id}, 'Ready') . "\n";
        }
        return join("\t", $options->{packet}, $validated->{packet}{packet_id}, $validated->{state}) . "\n";
    }
    if ($operation eq 'list') {
        return list_packets($options);
    }
    my $result = consume_packet($options);
    return join("\t", $options->{packet}, $result->{state}, ($result->{receipt_sha256} // $result->{rollback_sha256})) . "\n";
}

sub exit_for_failure_code {
    my ($code) = @_;
    return $EXIT_CODE{usage} if $code =~ /\AE_USAGE/;
    return $EXIT_CODE{stale} if $code =~ /\AE_STALE/;
    return $EXIT_CODE{conflict} if $code =~ /\AE_CONFLICT/;
    return $EXIT_CODE{approval} if $code =~ /\AE_APPROVAL/;
    return $EXIT_CODE{repository} if $code =~ /\AE_(?:REPOSITORY|GIT)/;
    return $EXIT_CODE{unsafe} if $code =~ /\AE_(?:UNSAFE|REVIEW_(?:ROOT|PATH|ESCAPE|TYPE|MODE|OWNER|MOUNT))/;
    return $EXIT_CODE{lock} if $code =~ /\AE_LOCK/;
    return $EXIT_CODE{limit} if $code =~ /\AE_LIMIT/;
    return $EXIT_CODE{runtime} if $code =~ /\AE_RUNTIME/;
    return $EXIT_CODE{uncertain} if $code eq 'E_WRITE_UNCERTAIN';
    return $EXIT_CODE{invalid} if $code =~ /\AE_(?:JSON|SCHEMA|DIGEST|PACKET|STORE|TSV|SOURCE|REQUEST|VERDICT|RECEIPT|ROLLBACK|TRANSACTION|LIST|FILE|REVIEW|SYNC)/;
    return $EXIT_CODE{internal};
}

sub main {
    my @arguments = @_;
    umask(0077);
    my $output;
    my $ok = eval {
        verify_runtime_identity();
        $output = dispatch(\@arguments);
        1;
    };
    if (!$ok) {
        my $error = $@;
        my $code = failure_code($error);
        my $exit = exit_for_failure_code($code);
        print STDERR "$code\n";
        return $exit;
    }
    print STDOUT $output;
    return 0;
}

unless (caller) {
    exit main(@ARGV);
}

1;

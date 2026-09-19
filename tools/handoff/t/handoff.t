use strict;
use warnings;
use bytes;
use utf8;
use JSON::PP ();
use Digest::SHA qw(sha256_hex);
use Fcntl qw(:DEFAULT);
use File::Spec ();
use File::Temp ();
use Test::More tests => 38;

my $source_path = '/Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl';
my $fixture_path = '/Users/bogac/dev/forgejo/mneme/tools/handoff/t/fixture-cases.json';

my $loaded = do $source_path;
die "cannot load production source: $@ $!" if !$loaded;

my $fixture_bytes = Mneme::Handoff::read_bounded_file($fixture_path, 262_144);
my $fixtures = Mneme::Handoff::decode_canonical_json($fixture_bytes, 262_144);
die 'fixture case count is not 38' if ref($fixtures) ne 'ARRAY' || @{$fixtures} != 38;

my @implementation_paths = (
    '/Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl',
    '/Users/bogac/dev/forgejo/mneme/tools/handoff/README.md',
    '/Users/bogac/dev/forgejo/mneme/tools/handoff/t/handoff.t',
    '/Users/bogac/dev/forgejo/mneme/tools/handoff/t/fixture-cases.json',
);
my %implementation_before = map {
    $_ => Mneme::Handoff::sha256_file($_, 262_144)
} @implementation_paths;

my %fixture_by_id;
for my $index (0 .. 37) {
    my $expected_id = sprintf('HT-%03d', $index + 1);
    my $row = $fixtures->[$index];
    die "fixture id mismatch $expected_id" if ref($row) ne 'HASH' || $row->{id} ne $expected_id;
    die "duplicate fixture id $expected_id" if $fixture_by_id{$expected_id};
    $fixture_by_id{$expected_id} = $row;
}

my $temporary = File::Temp->newdir(
    'mneme-handoff-test-XXXXXXXX',
    DIR => '/private/tmp',
    CLEANUP => 1,
);
my $test_root = "$temporary";
chmod(0700, $test_root) == 1 or die 'cannot set test-root mode';

sub caught_code {
    my ($callback) = @_;
    my $ok = eval {
        $callback->();
        1;
    };
    return '' if $ok;
    return Mneme::Handoff::failure_code($@);
}

sub valid_packet_metadata {
    return {
        schema_version => 1,
        protocol_version => 1,
        packet_number => '000001',
        purpose => 'synthetic review',
        review_question => 'docs/SYNTHETIC.md',
        created_at => '2026-09-19T00:00:00Z',
        repository_root => '/Users/bogac/dev/forgejo/mneme',
        head => ('1' x 40),
        branch => 'refs/heads/synthetic',
        repository_state_sha256 => ('a' x 64),
        request_sha256 => ('b' x 64),
        sources_sha256 => ('c' x 64),
        prior_packet_id => '',
        superseded_packet_id => '',
        approval_gate => 'implementation-review',
        non_authorization => 'packet consumption records a handoff and never authorizes project work',
        source_count => 1,
        source_bytes => 12,
    };
}

sub valid_verdict_and_approval {
    my $verdict = {
        schema_version => 1,
        record_type => 'mneme.handoff.verdict',
        status => 'Proposed',
        packet_number => '000001',
        packet_id => ('d' x 64),
        packet_manifest_sha256 => ('e' x 64),
        repository_state_sha256 => ('a' x 64),
        sources_sha256 => ('c' x 64),
        verdict => 'Approve',
        rationale => 'Synthetic rationale.',
        unresolved_concerns => [],
        reviewer_role => 'synthetic-reviewer',
        proposal_date => '2026-09-19',
    };
    my $verdict_bytes = Mneme::Handoff::canonical_json($verdict);
    my $approval = {
        schema_version => 1,
        record_type => 'mneme.handoff.user-approval',
        status => 'Accepted',
        authority => 'user',
        packet_number => '000001',
        packet_id => ('d' x 64),
        verdict_sha256 => sha256_hex($verdict_bytes),
        repository_state_sha256 => ('a' x 64),
        approval_date => '2026-09-19',
        decision_reference => 'synthetic://approval/000001',
        approval_statement_sha256 => ('f' x 64),
    };
    return ($verdict, $verdict_bytes, $approval);
}

sub valid_receipt {
    return {
        schema_version => 1,
        record_type => 'mneme.handoff.receipt',
        packet_number => '000001',
        packet_id => ('1' x 64),
        packet_manifest_sha256 => ('2' x 64),
        repository_state_sha256 => ('3' x 64),
        sources_sha256 => ('4' x 64),
        verdict => 'Approve',
        verdict_sha256 => ('5' x 64),
        approval_sha256 => ('6' x 64),
        implementation_sha256 => ('7' x 64),
        runtime_sha256 => ('8' x 64),
        git_sha256 => ('9' x 64),
        consumed_at => '2026-09-19T00:00:00Z',
        project_work_authorized => JSON::PP::false,
        project_work_executed => JSON::PP::false,
    };
}

sub valid_rollback {
    my ($receipt_sha, $current_sha) = @_;
    return {
        schema_version => 1,
        record_type => 'mneme.handoff.rollback',
        packet_id => ('1' x 64),
        receipt_sha256 => $receipt_sha,
        approval_sha256 => ('2' x 64),
        original_repository_state_sha256 => ('3' x 64),
        current_repository_state_sha256 => $current_sha,
        reason => 'synthetic user-approved protocol rollback',
        rollback_date => '2026-09-19T00:00:00Z',
    };
}

sub fixture_expected {
    my ($id) = @_;
    return $fixture_by_id{$id}{expected};
}

sub synthetic_inventory {
    my ($root, $relative) = @_;
    my $path = $relative eq '' ? $root : File::Spec->catfile($root, split('/', $relative));
    opendir(my $dh, $path) or die "cannot inventory synthetic directory $relative";
    my @names = sort grep { $_ ne '.' && $_ ne '..' } readdir($dh);
    closedir($dh);
    my @rows;
    for my $name (@names) {
        my $child_relative = $relative eq '' ? $name : "$relative/$name";
        my $child = File::Spec->catfile($path, $name);
        my @st = lstat($child);
        die "cannot lstat synthetic path $child_relative" if !@st;
        if (-l _) {
            push @rows, join("\t", $child_relative, 'symlink', sprintf('0%03o', $st[2] & 0777), readlink($child));
        }
        elsif (-d _) {
            push @rows, join("\t", $child_relative, 'directory', sprintf('0%03o', $st[2] & 0777), 0);
            push @rows, synthetic_inventory($root, $child_relative);
        }
        elsif (-f _) {
            push @rows, join(
                "\t", $child_relative, 'regular', sprintf('0%03o', $st[2] & 0777),
                $st[7], Mneme::Handoff::sha256_file($child, 262_144),
            );
        }
        else {
            die "unexpected synthetic path type $child_relative";
        }
    }
    return @rows;
}

my %case;

$case{'HT-001'} = sub {
    my $packet = valid_packet_metadata();
    $packet->{packet_id} = Mneme::Handoff::compute_packet_id(
        $packet,
        $packet->{request_sha256},
        $packet->{sources_sha256},
        $packet->{repository_state_sha256},
    );
    ok($packet->{packet_id} =~ /\A[0-9a-f]{64}\z/, 'packet identity is exact sha256');
    is(Mneme::Handoff::derive_state({}), fixture_expected('HT-001'), 'valid packet is pending');
};

$case{'HT-002'} = sub {
    my $value = { z => [3, 2, 1], a => 'synthetic' };
    my $first = Mneme::Handoff::canonical_json($value);
    my $second = Mneme::Handoff::canonical_json(Mneme::Handoff::decode_canonical_json($first));
    is($second, $first, fixture_expected('HT-002'));
};

$case{'HT-003'} = sub {
    my $code = caught_code(sub {
        Mneme::Handoff::decode_canonical_json("{\"a\":1,\"a\":1}\n");
    });
    is($code, 'E_JSON_NONCANONICAL', fixture_expected('HT-003'));
};

$case{'HT-004'} = sub {
    my $code = caught_code(sub {
        Mneme::Handoff::decode_canonical_json("{ \"a\" : 1 }\n");
    });
    is($code, 'E_JSON_NONCANONICAL', fixture_expected('HT-004'));
};

$case{'HT-005'} = sub {
    my $cr = caught_code(sub { Mneme::Handoff::decode_canonical_json("{\"a\":1}\r\n"); });
    my $trailing = caught_code(sub { Mneme::Handoff::decode_canonical_json("{\"a\":1}\n\n"); });
    is($cr, 'E_JSON_CR', 'CRLF rejected');
    ok($trailing eq 'E_JSON_LF' || $trailing eq 'E_JSON_PARSE', fixture_expected('HT-005'));
};

$case{'HT-006'} = sub {
    is(caught_code(sub { Mneme::Handoff::validate_packet_number('12'); }), 'E_PACKET_NUMBER', fixture_expected('HT-006'));
};

$case{'HT-007'} = sub {
    is(caught_code(sub { Mneme::Handoff::validate_number_sequence(['000001', '000001']); }), 'E_CONFLICT_NUMBER', fixture_expected('HT-007'));
};

$case{'HT-008'} = sub {
    is(caught_code(sub { Mneme::Handoff::validate_number_sequence(['000001', '000003']); }), 'E_CONFLICT_GAP', fixture_expected('HT-008'));
};

$case{'HT-009'} = sub {
    my $root = File::Spec->catdir($test_root, 'ht009');
    mkdir($root, 0700) or die 'ht009 mkdir';
    my $target = File::Spec->catfile($root, 'target');
    Mneme::Handoff::write_exclusive_synced($target, "synthetic\n", 0600);
    my $link = File::Spec->catfile($root, 'link');
    symlink($target, $link) or die 'ht009 symlink';
    is(caught_code(sub { Mneme::Handoff::assert_regular_contained($root, 'link', 0600); }), 'E_UNSAFE_SYMLINK', fixture_expected('HT-009'));
};

$case{'HT-010'} = sub {
    is(caught_code(sub { Mneme::Handoff::source_path_allowed('.mneme-data/mail.eml'); }), 'E_UNSAFE_SOURCE_ROOT', fixture_expected('HT-010'));
};

$case{'HT-011'} = sub {
    my @entries = qw(packet.json request.md sources.tsv repository-state.json packet-manifest.sha256 transactions rollbacks project.bin);
    is(caught_code(sub { Mneme::Handoff::validate_packet_entries(\@entries); }), 'E_PACKET_EXTRA', fixture_expected('HT-011'));
};

$case{'HT-012'} = sub {
    is(Mneme::Handoff::derive_state({ stale => 1, source_mismatch => 1 }), fixture_expected('HT-012'), 'source drift is stale');
};

$case{'HT-013'} = sub {
    is(Mneme::Handoff::derive_state({ stale => 1, head_mismatch => 1 }), fixture_expected('HT-013'), 'repository drift is stale');
};

$case{'HT-014'} = sub {
    is(caught_code(sub { Mneme::Handoff::validate_dirty_paths(['docs/unrepresented.md'], ['docs/declared.md']); }), 'E_REPOSITORY_UNREPRESENTED', fixture_expected('HT-014'));
};

$case{'HT-015'} = sub {
    is(Mneme::Handoff::derive_state({ stale => 1, superseded => 1 }), fixture_expected('HT-015'), 'superseded packet is stale');
};

$case{'HT-016'} = sub {
    my $one = '1' x 64;
    my $two = '2' x 64;
    my $nodes = { $one => { prior => $two }, $two => { prior => $one } };
    is(caught_code(sub { Mneme::Handoff::validate_lineage($nodes); }), 'E_CONFLICT_LINEAGE_CYCLE', fixture_expected('HT-016'));
};

$case{'HT-017'} = sub {
    is(Mneme::Handoff::derive_state({ proposed_verdict => 'Approve' }), fixture_expected('HT-017'), 'verdict alone remains pending');
};

$case{'HT-018'} = sub {
    my (undef, undef, $approval) = valid_verdict_and_approval();
    $approval->{authority} = 'agent';
    is(caught_code(sub { Mneme::Handoff::validate_approval($approval); }), 'E_APPROVAL_AUTHORITY', fixture_expected('HT-018'));
};

$case{'HT-019'} = sub {
    my ($verdict, $verdict_bytes, $approval) = valid_verdict_and_approval();
    $approval->{verdict_sha256} = '0' x 64;
    is(caught_code(sub { Mneme::Handoff::validate_verdict_approval($verdict, $approval, $verdict_bytes); }), 'E_APPROVAL_VERDICT_HASH', fixture_expected('HT-019'));
};

$case{'HT-020'} = sub {
    my ($verdict, $verdict_bytes, $approval) = valid_verdict_and_approval();
    my $sha = Mneme::Handoff::validate_verdict_approval($verdict, $approval, $verdict_bytes);
    is($sha, sha256_hex($verdict_bytes), fixture_expected('HT-020'));
};

$case{'HT-021'} = sub {
    is(Mneme::Handoff::derive_state({ verdict => 'Approve', receipt => 1 }), fixture_expected('HT-021'), 'approved receipt is consumed');
};

$case{'HT-022'} = sub {
    is(Mneme::Handoff::derive_state({ verdict => 'Reject', receipt => 1 }), fixture_expected('HT-022'), 'reject transaction closes packet');
};

$case{'HT-023'} = sub {
    is(Mneme::Handoff::derive_state({ verdict => 'ChangesRequested', receipt => 1 }), fixture_expected('HT-023'), 'changes requested closes packet');
};

$case{'HT-024'} = sub {
    is(Mneme::Handoff::derive_state({ conflict => 1, verdict => 'Approve', receipt => 1 }), fixture_expected('HT-024'), 'conflict wins over receipt');
};

$case{'HT-025'} = sub {
    my $receipt = valid_receipt();
    $receipt->{project_work_authorized} = JSON::PP::true;
    is(caught_code(sub { Mneme::Handoff::validate_receipt($receipt); }), 'E_RECEIPT_AUTHORITY', fixture_expected('HT-025'));
};

$case{'HT-026'} = sub {
    my $receipt_sha = '5' x 64;
    my $current_sha = '6' x 64;
    my $transaction = "immutable transaction\n";
    my $before = sha256_hex($transaction);
    my $rollback = valid_rollback($receipt_sha, $current_sha);
    ok(Mneme::Handoff::validate_rollback($rollback, $receipt_sha, $current_sha), 'rollback validates');
    is(sha256_hex($transaction), $before, 'transaction remains immutable');
    is(Mneme::Handoff::derive_state({ rolled_back => 1 }), fixture_expected('HT-026'), 'state is rolled back');
};

$case{'HT-027'} = sub {
    my $rollback = valid_rollback('7' x 64, '6' x 64);
    is(caught_code(sub { Mneme::Handoff::validate_rollback($rollback, '5' x 64, '6' x 64); }), 'E_CONFLICT_ROLLBACK_RECEIPT', fixture_expected('HT-027'));
};

$case{'HT-028'} = sub {
    my $stage = File::Spec->catdir($test_root, 'ht028.stage');
    my $final = File::Spec->catdir($test_root, 'ht028.final');
    my $code = caught_code(sub {
        Mneme::Handoff::atomic_publish_directory($stage, $final, { 'packet.json' => "{}\n" }, sub {
            my ($point) = @_;
            die "synthetic pre-rename fault\n" if $point eq 'before_rename';
        });
    });
    ok($code eq 'E_INTERNAL' && -d $stage && !-e $final, fixture_expected('HT-028'));
};

$case{'HT-029'} = sub {
    my $stage = File::Spec->catdir($test_root, 'ht029.stage');
    my $final = File::Spec->catdir($test_root, 'ht029.final');
    my $code = caught_code(sub {
        Mneme::Handoff::atomic_publish_directory($stage, $final, { 'packet.json' => "{}\n" }, sub {
            my ($point) = @_;
            die "synthetic post-rename fault\n" if $point eq 'after_rename';
        });
    });
    ok($code eq 'E_INTERNAL' && !-e $stage && -d $final, fixture_expected('HT-029'));
};

$case{'HT-030'} = sub {
    my $stage = File::Spec->catdir($test_root, 'ht030.stage');
    my $final = File::Spec->catdir($test_root, 'ht030.final');
    my $code = caught_code(sub {
        Mneme::Handoff::atomic_publish_directory($stage, $final, {
            'approval.json' => "{}\n",
            'receipt.json' => "{}\n",
            'verdict.json' => "{}\n",
        }, sub {
            my ($point) = @_;
            die "synthetic transaction fault\n" if $point eq 'after_files';
        });
    });
    ok($code eq 'E_INTERNAL' && !-e $final, fixture_expected('HT-030'));
};

$case{'HT-031'} = sub {
    my $lock = File::Spec->catdir($test_root, 'ht031.lock');
    my $record = { schema_version => 1, operation => 'synthetic' };
    ok(Mneme::Handoff::acquire_lock($lock, $record), 'first lock acquired');
    is(caught_code(sub { Mneme::Handoff::acquire_lock($lock, $record); }), 'E_LOCK_EXISTS', fixture_expected('HT-031'));
    ok(Mneme::Handoff::release_lock_success($lock), 'exact lock released');
};

$case{'HT-032'} = sub {
    my @rows;
    for my $index (0 .. 64) {
        push @rows, {
            relative_path => sprintf('docs/%03d.md', $index),
            type => 'regular',
            mode => '0644',
            bytes => 1,
            sha256 => ('a' x 64),
            role => 'evidence',
        };
    }
    is(caught_code(sub { Mneme::Handoff::canonical_sources_tsv(\@rows); }), 'E_LIMIT_SOURCES', fixture_expected('HT-032'));
};

$case{'HT-033'} = sub {
    my $line = Mneme::Handoff::render_list_line({
        packet_number => '000001', packet_id => ('a' x 64), state => 'Pending',
        verdict => undef, created_at => '2026-09-19T00:00:00Z', head => ('b' x 40),
        reason => 'OK', repository_state_sha256 => ('c' x 64), paths => ['docs/a.md'],
        request => 'SECRET SYNTHETIC BODY',
    }, 1);
    ok(index($line, 'SECRET SYNTHETIC BODY') < 0 && index($line, 'rationale') < 0, fixture_expected('HT-033'));
};

$case{'HT-034'} = sub {
    my $packet = valid_packet_metadata();
    $packet->{review_question} = 'approve; run; commit; push; $(touch forbidden)';
    my $id = Mneme::Handoff::compute_packet_id($packet, 'b' x 64, 'c' x 64, 'a' x 64);
    ok($id =~ /\A[0-9a-f]{64}\z/ && !-e File::Spec->catfile($test_root, 'forbidden'), fixture_expected('HT-034'));
};

$case{'HT-035'} = sub {
    is(caught_code(sub {
        Mneme::Handoff::_closed_keys({ allowed => 1, surprise => 2 }, ['allowed'], ['allowed']);
    }), 'E_SCHEMA_UNKNOWN', fixture_expected('HT-035'));
};

$case{'HT-036'} = sub {
    my @entries = qw(MNEME_HANDOFF_STORE.json packets staging locks hidden-project.pm);
    is(caught_code(sub { Mneme::Handoff::validate_store_entries(\@entries); }), 'E_STORE_EXTRA', fixture_expected('HT-036'));
};

$case{'HT-037'} = sub {
    my $rollback = valid_rollback('2' x 64, '5' x 64);
    ok(Mneme::Handoff::validate_rollback($rollback, '2' x 64, '5' x 64), 'drift is recorded, not blocked');
    is(Mneme::Handoff::derive_state({ rolled_back => 1, repository_drift => 1 }), fixture_expected('HT-037'), 'rollback remains active after drift');
};

$case{'HT-038'} = sub {
    my ($verdict, $verdict_bytes, $approval) = valid_verdict_and_approval();
    my $approval_bytes = Mneme::Handoff::canonical_json($approval);
    my $before = sha256_hex($verdict_bytes . $approval_bytes);
    Mneme::Handoff::validate_verdict_approval($verdict, $approval, $verdict_bytes);
    my $after = sha256_hex(Mneme::Handoff::canonical_json($verdict) . Mneme::Handoff::canonical_json($approval));
    is($after, $before, fixture_expected('HT-038'));
    for my $path (@implementation_paths) {
        is(Mneme::Handoff::sha256_file($path, 262_144), $implementation_before{$path}, "implementation unchanged: $path");
    }
};

for my $number (1 .. 38) {
    my $id = sprintf('HT-%03d', $number);
    subtest $id => sub {
        ok(exists($case{$id}), 'case implementation exists');
        $case{$id}->();
        done_testing();
    };
}

diag("synthetic temporary root: $test_root");
diag("synthetic temporary inventory:\n" . join("\n", synthetic_inventory($test_root, '')));
undef $temporary;
die 'temporary test root was not rolled back' if -e $test_root;
diag("synthetic temporary rollback verified: $test_root absent");

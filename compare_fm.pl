#!/usr/bin/env perl

use strict;
use warnings;
use v5.028;

use Digest::xxHash qw[xxhash32 xxhash32_hex xxhash64 xxhash64_hex];
use File::Map qw(map_file);
use Parallel::ForkManager;
use Forks::Queue;

sub compare {
    map_file my $map, ($_[0]);
    $_[1] = xxhash64_hex( $map, 0 );
}

my $pm = Parallel::ForkManager->new(scalar @ARGV);
my $q = Forks::Queue->new();

DATA_LOOP:
for my $file (@ARGV) {
    $pm->start and next DATA_LOOP;

    compare($file, my $fh);
    $q->put($fh);

    $pm->finish;
}
$pm->wait_all_children;
$q->end;

my @fh = $q->get(scalar @ARGV);

if (keys %{{ map {$_,1} @fh }} ne 1){
    exit(1)
}

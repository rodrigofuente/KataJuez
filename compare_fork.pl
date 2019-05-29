#!/usr/bin/env perl

use strict;
use warnings;
use v5.028;

use Digest::xxHash qw[xxhash32 xxhash32_hex xxhash64 xxhash64_hex];
use File::Map qw(map_file);
use Forks::Super;
use Forks::Queue;

my $q = Forks::Queue->new();

sub compare {
    map_file my $map, ($_[0]);
    $q->put(xxhash64_hex( $map, 0 ))
}

for my $file (@ARGV) {
    my $proc = fork { sub => \&compare, args => [$file] };
    $proc->wait
}

my @fh = $q->get(scalar @ARGV);
if (keys %{{ map {$_,1} @fh }} ne 1){
    exit(1)
}

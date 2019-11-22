#!/usr/bin/perl
use strict;
use warnings;

if ($#ARGV < 0 ) {
    print("translates lingpipe pos output into stan ready output");
    print("usage: perl trainPOS.pl pos_data.txt > pos.rdata");
    exit;
}


my %word_to_int;
my %int_to_word;
my %pos_to_int;
my %int_to_pos;
my @word_order;
my @pos_order;
my @transit_prior;
my @emit_prior;
my $word_counter = 0;
my $pos_counter = 0;

while(<>) {
    if (/token pos="([^"]*)">([^<]*)<\/token>/) {
	my $pos = $1;
	my $word = $2;
#	print "$_\n";
	if (!defined($word_to_int{$word})) {
	    $word_to_int{$word} = ++$word_counter;
	    $int_to_word{$word_counter} = $word;
	}
	if (!defined($pos_to_int{$pos})) {
	    $pos_to_int{$pos} = ++$pos_counter;
	    $int_to_pos{$pos_counter} = $pos;
	}
	push(@word_order,$word_to_int{$word});
	push(@pos_order,$pos_to_int{$pos});
    }
}

print("K <- " . (scalar (keys %pos_to_int)) . "\n");
print("V <- " . (scalar (keys %word_to_int)) . "\n");
print("T <- " . (scalar @word_order) . "\n");
print("w <- c(". join(",",@word_order). ")\n");
print("z <- c(". join(",",@pos_order). ")\n");

for (my $i=0; $i < scalar (keys %pos_to_int); $i++) {
    $transit_prior[$i] = .5;
}

for (my $i=0; $i < scalar (keys %word_to_int); $i++) {
    $emit_prior[$i] = .5;
}
print("alpha <- c(". join(",",@transit_prior) . ")\n");
print("beta <- c(". join(",",@emit_prior) . ")\n");


__END__;

my $filePath = $ARGV[0];
if ($filePath =~ s/.stan//) { #remove #1 annoying error
    print("removing trailing .stan from file name passed to complier\n");
}

if (-e "$filePath.o") {
    print "removing $filePath.o\n";
    system("rm $filePath.o");
}

if (-e "$filePath.hpp") {
    print "removing $filePath.hpp\n";
    system("rm $filePath.hpp");
}

if (-e "$filePath") {
    print "removing $filePath\n";
    system("rm $filePath");
}

print("Compiling $filePath\n");
system("make $filePath");

$ARGV[0] = $filePath;
    
system(@ARGV);





#!/bin/bash

perfMemPlus="perfMemPlus/perfMemPlus"
numa="numactl --cpunodebind=0 --interleave=0,1"
outputDir="data"
cmd="pmbw/pmbw -M 3000000000 -s 300000000 -S 3000000000 -p 1 -P 1 -f PermRead64UnrollLoop"
numRep=10
numRepStart=1

if [ -d "$outputDir" ]; then
	rm -r $outputDir
fi
mkdir $outputDir
for (( i=$numRepStart; i <= $numRep; i++ )); do
	$numa $perfMemPlus -c 4000 -a 1024 -o "$outputDir/pmbw-orig-4000-1-$i.db" $cmd
done

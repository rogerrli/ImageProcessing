#!/usr/bin/env bash
read -p 'Which folder to update or ALL?' varFolder

if [ $varFolder == 'ALL' ]
then
    for i in */;
    do
        cp -r ./BASE/src/ ./$i/src/
        cp ./BASE/run.sh ./$i/run.sh
    done
else
    cp -r ./BASE/src/ ./$varFolder/src/
    cp ./BASE/run.sh ./$varFolder/run.sh
fi

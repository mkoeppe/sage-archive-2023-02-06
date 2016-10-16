#! /bin/bash
set -e # exit on errors

function finish {
    for a in `find logs -name "*.log"`; do
        echo "###### $a ######"
        cat $a
    done
}

trap finish EXIT

export MAKE="make -j4"

make V=0 SAGE_SPKG="travis_wait 120 sage-spkg"

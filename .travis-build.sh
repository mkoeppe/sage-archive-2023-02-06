#! /bin/bash
set -e # exit on errors

function finish {
    for a in `find logs -name "*.log"`; do
        echo "###### $a ######"
        cat $a
    done
}

#trap finish EXIT

export MAKE="make -j4"

export SAGE_INSTALL_CCACHE=yes

make V=0 SAGE_PV="PYTHONUNBUFFERED=1 sage-progress-meter" $TARGET


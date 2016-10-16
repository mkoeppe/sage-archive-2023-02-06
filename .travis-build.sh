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

function hungry_spinner {
    function kill_spinner {
	kill $SPINNER_PID
    }
    trap kill_spinner EXIT 
    trap kill_spinner SIGPIPE 
    trap kill_spinner SIGINT 
    ( sleep 6; while true; do echo -n . >/dev/tty ; sleep 6; done ) &
    SPINNER_PID=$!
    cat
};
export -f hungry_spinner

make V=0 SAGE_PV="hungry_spinner"

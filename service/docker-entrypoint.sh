#!/bin/sh

if [ ! $DASFLAG ]; then
    if [ ! $FLAG ]; then
        if [ ! $GZCTF_FLAG ]; then
            echo flag{TEST_DASFLAG} > /flag
        else
            echo $GZCTF_FLAG > /flag
            export GZCTF_FLAG=no_FLAG
            GZCTF_FLAG=no_FLAG
        fi
    else
        echo $FLAG > /flag
        export FLAG=no_FLAG
        FLAG=no_FLAG
    fi
else
    echo $DASFLAG > /flag
    export DASFLAG=no_FLAG
    DASFLAG=no_FLAG
fi

python3 /app/main.py &

socat TCP4-LISTEN:12345,reuseaddr,fork EXEC:"python3 -i",stderr
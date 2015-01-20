#!/bin/bash
VENV=$WORKSPACE/venv
source $VENV/bin/activate
export PYTHONPATH="$WORKSPACE/..:$WORKSPACE/lib"
pylint --rcfile scripts/pylintrc $WORKSPACE > pylint.txt
echo "pylint complete"

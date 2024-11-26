#!/bin/bash

echo "Pushing Problem Set" $1 "to Canvas..."

python3 $TOMATO_PATH/submit.py $1 $CANVAS_BASE $CANVAS_TOKEN
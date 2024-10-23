#!/bin/bash

echo "Pushing Problem Set" $1 "to Canvas..."

# run the python program /Users/isaaczhu/MIT/tomato/pull.py

python3 /Users/isaaczhu/MIT/tomato/submit.py $1 $CANVAS_BASE $CANVAS_TOKEN
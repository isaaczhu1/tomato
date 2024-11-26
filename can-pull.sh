#!/bin/bash

echo "Pulling from Canvas..."

# run the python program $TOMATO_PATH/pull.py
python3 $TOMATO_PATH/pull.py $TOMATO_PATH $CANVAS_BASE $CANVAS_TOKEN
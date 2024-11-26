# tomato
submit Canvas assignments through terminal via API

to use, set environment variables:

export CANVAS_TOKEN=... # (see e.g. https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312)

export CANVAS_BASE="https://canvas.mit.edu/api/v1" # set appropriately

export TOMATO_PATH="/Users/isaaczhu/MIT/tomato" # path to tomato, set appropriately

and also

export PATH="$PATH:$TOMATO_PATH"
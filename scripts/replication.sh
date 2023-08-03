#!/bin/bash

arg1="$1"

# Display the arguments
echo "Argument 1: $arg1"

rsync -av /root/storage/$arg1 <user>@<ip>:/path/to/dir/

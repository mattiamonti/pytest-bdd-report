#!/bin/bash

# Define the target directory
directory="."

# Check if the target is not a directory
if [ ! -d "$directory" ]; then
  exit 1
fi

file_names=""
# Loop through files in the target directory
for file in "$directory"/*; do
  if [ -f "$file" ]; then
    if [[ $file == *.robot ]]; then
        file_names+=" $file"
        #python3 -m robot "$file"
        #echo "$file"
    fi
  fi
done

#echo $file_names
python3 -m robot $file_names

#!/bin/bash

# Variables
folder="$1"
code_folder="$folder/src/"
docs_folder="$folder/docs/"

echo "--- Testing Code ---"

if [ -d "$folder/tests" ]
then
     rm -rf "$folder"/tests/*
else
     mkdir "$folder"/tests
fi

echo "----- Running PyLint tests -----"
if [ -f .pylintrc ]
then
     pylint --rcfile=.pylintrc "$code_folder"*.py > "$folder"tests/linter_tests.txt
else
     echo "No .pylintrc file found: Running normal pylint."
     echo "Careful, this project uses google style python. Retrieve the .proper pylintrc file and run the tests again."
     echo "Google's pylintrc can be found here: https://google.github.io/styleguide/pyguide.html"
     pylint "$code_folder"*.py > "$folder"tests/linter_tests.txt
fi

echo "----- Running Type checks -----"
pytype "$code_folder"*.py > "$folder"tests/type_checks.txt

echo "All tests ran successfully"

echo "Building documentation"
export SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -f -o "$docs_folder"/source "$code_folder"
cd "$docs_folder"
make clean
make html
firefox ./build/html/index.html
echo "Exiting"

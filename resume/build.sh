#!/bin/bash
set -e

# Build the resume with Tectonic. A single call runs every pass it needs
# (references, layout), so there is no second xelatex run.
echo "Compiling resume with tectonic..."
cd "$(dirname "$0")"
tectonic main.tex
mv -f main.pdf Resume.pdf
echo "PDF compilation successful!"
echo "Generated: Resume.pdf"

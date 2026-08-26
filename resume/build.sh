#!/bin/bash
set -e

# Build the resume using the same latexmk/XeLaTeX command as CI. Latexmk runs
# every pass needed for references and layout in one invocation.
echo "Compiling resume with latexmk and XeLaTeX..."
cd "$(dirname "$0")"
latexmk -xelatex -interaction=nonstopmode -halt-on-error -jobname=Resume main.tex
echo "PDF compilation successful!"
echo "Generated: Resume.pdf"

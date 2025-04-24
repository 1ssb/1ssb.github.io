#!/bin/bash
set -e

echo "Compiling Resume locally..."
cd "$(dirname "$0")"
xelatex -interaction=nonstopmode -jobname=Resume main.tex
xelatex -interaction=nonstopmode -jobname=Resume main.tex
echo "PDF compilation successful!"
echo "Generated: Resume.pdf"
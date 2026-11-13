#!/bin/bash
# print header (authors/affiliations/abstract start) of arXiv html
python3 /workspace/physio-fm-history/research/pg.py "https://arxiv.org/html/$1" | grep -v "^ *$" | awk '/^arXiv:/{f=1} f' | head -${2:-40} | cut -c1-400

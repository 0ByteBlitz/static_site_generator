#!/bin/bash

# Run the Python script to generate the site
python3 src/main.py

# Serve the site on port 8888
cd docs && python3 -m http.server 8888

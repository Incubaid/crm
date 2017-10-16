#!/bin/bash
set -e

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
pip install -r requirements-testing.pip
pip install -e .
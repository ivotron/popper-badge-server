#!/usr/bin/env bash
# [wf] execute install-server stage

cd ../..
mkdir venv
python -m virtualenv venv/
source venv/bin/activate
pip install -r requirements.txt

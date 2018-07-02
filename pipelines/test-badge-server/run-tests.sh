#!/usr/bin/env bash
# [wf] execute run-tests stage


cd ../..
source venv/bin/activate
pytest tests.py

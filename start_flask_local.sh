#!/bin/bash
export FLASK_APP=annotate_elan.py
export FLASK_DEBUG=1
python3 -m flask run

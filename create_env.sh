#!/bin/bash


## Requirements
## gcc, make, Python 2.5+, python-pip, virtualenv

## Instalation
## Create a virtualenv, and activate this: 

virtualenv env 
source env/bin/activate
pip install -r requirnments.txt
python test.py
python run.py

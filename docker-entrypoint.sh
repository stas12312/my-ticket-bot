#!/bin/sh

python migrations/run_migrations.py
python src/main.py

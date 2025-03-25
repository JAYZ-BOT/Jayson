#!/bin/bash
gunicorn app:app --bind 0.0.0.0:10000 --log-level debug --log-file gunicorn_error.log

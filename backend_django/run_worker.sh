#!/bin/bash

export PYTHONPATH=/
cd backend
celery -A backend worker --loglevel=info
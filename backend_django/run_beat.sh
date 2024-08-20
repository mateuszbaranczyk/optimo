#!/bin/bash

export PYTHONPATH=/
cd backend/
celery -A backend beat --loglevel=info
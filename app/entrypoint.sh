#!/bin/bash
cd /app/database
orator migrate -f

exec "$@"

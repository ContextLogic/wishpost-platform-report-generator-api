#!/bin/sh

# Entrypoint for worker
exec /production/report_generator_service/persistent/virtualenv/bin/python /production/report_generator_service/current/report_generator_service/report_generator_service/worker.py
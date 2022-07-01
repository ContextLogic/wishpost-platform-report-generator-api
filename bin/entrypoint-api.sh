#!/bin/sh

# Entrypoint for api server
exec /production/report_generator_service/persistent/virtualenv/bin/gevent-wsgi report_generator_service.server:app

#!/bin/sh
./manage.py runserver --settings=settings_server 8001&
./manage.py runserver --settings=settings_client 8000&


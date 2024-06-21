#!/bin/bash
pip install requests flask datetime requests-cache gunicorn
# Script pour démarrer Gunicorn avec Flask
exec gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app 
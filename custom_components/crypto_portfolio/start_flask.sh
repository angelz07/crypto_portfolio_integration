#!/bin/bash

# Log de debug
echo "Starting Flask app setup" >> /config/start_flask.log

# Installer les dépendances nécessaires
pip install requests flask datetime requests-cache gunicorn >> /config/start_flask.log 2>&1

# Log de debug
echo "Dependencies installed" >> /config/start_flask.log

# Démarrer Gunicorn avec Flask
exec gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app >> /config/start_flask.log 2>&1

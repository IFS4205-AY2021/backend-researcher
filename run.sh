#! bin/bash

# ls /home
# ls /home/researcher
echo "Starting Django Server..."
python3 app/manage.py runserver 0.0.0.0:8000

# For container debug
sleep 600

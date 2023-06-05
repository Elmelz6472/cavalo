#!/bin/bash

# Change directory to the project folder
cd ~/Desktop/cavalo/App/CardinalSite/

# Activate the virtual environment
source ./virtual_env/bin/activate

# Grant executable permissions to the virtual_env/bin/python file
chmod +x virtual_env/bin/python

# Update the project folder using git pull
pull_output=$(git pull)

# Echo the git pull output
echo "$pull_output"


# Run the python manage.py command using the Python interpreter from the virtual environment
virtual_env/bin/python manage.py runserver &

# Store the process ID of the Django server
server_pid=$!

# Open the Django server URL in the default browser
open "http://127.0.0.1:8000/"

# Pause to keep the Terminal window open until the user presses a key
read -n 1 -s -r -p "Press any key to stop the server..."

# Terminate the Django server process
kill $server_pid

# Deactivate the virtual environment
deactivate

#!/bin/bash
echo "Bem vindo pai, rodarei seus comandos:"

gnome-terminal --tab --title "BROKER" -- bash -c "cd bin; ./activemq stop; ./activemq start; exec bash -i"

gnome-terminal --tab --title "PUBLISH" -- bash -c "python3 publisher.py; exec bash -i"

gnome-terminal --tab --title "LISTENER" -- bash -c "python3 listener.py; exec bash -i"


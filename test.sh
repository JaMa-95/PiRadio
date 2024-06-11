#/bin/sh 
while true; do
    read -p "Do you want to install web frontend?" yn
    case $yn in
        [Yy]* ) echo "HELLO" ; break;;
        [Nn]* ) echo "BYE"; break;;
        * ) echo "Please answer yes or no.";;
    esac
done
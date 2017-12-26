#!/bin/bash

usage(){
    echo "Usage:"
    echo -e "\t./prepare --prod (Install Production dependencies)"
    echo -e "\t./prepare --dev (Install Development dependencies)"
    echo ""
    exit 1
}

environment=""


if [ "$1" != "" ]; then
    if [ "$1" == "--prod" ];then
        environment="prod"
    elif [ "$1" == "--dev" ];then
        environment="dev"
    else
        usage
    fi

else
    usage
fi



echo '************************************'
echo 'Installing System-Level Dependencies'
echo '************************************'
echo ''

if [ $(uname) == 'Linux' ];then
    cat requirements.apt | xargs sudo apt-get install -y
    sudo curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
else
    xargs brew install < requirements.brew
fi

clear

echo '************************************'
echo 'Installing Python-Level Dependencies'
echo '************************************'
echo ''

if [ "$environment" == "prod" ]; then
    pip3 install -r requirements.pip
else
    pip3 install -r requirements-testing.pip
fi

clear

echo '************************************'
echo 'Installing Nodejs-Level Dependencies'
echo '************************************'
echo ''

if [ "$environment" == "prod" ]; then
    echo -e 'No production level npm packages required\n'
else
    cat requirements.npm | sudo xargs npm install -g
fi

echo 'DONE!'

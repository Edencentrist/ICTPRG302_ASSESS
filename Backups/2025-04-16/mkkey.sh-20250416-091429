#!/bin/sh

if [ ! -f ~/.ssh/id_rsa.pub ]; then

  ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ''
  echo 'eval $(ssh-agent -s)' >> ~/.bash_profile
  echo 'ssh-add ~/.ssh/id_rsa' >> ~/.bash_profile
  source ~/.bash_profile
  echo 
  echo "Copy the public key below:"
  echo
  cat ~/.ssh/id_rsa.pub

else

  echo 
  echo "An id_rsa key already exists. Copy the public key below:"
  echo
  cat ~/.ssh/id_rsa.pub

fi

#!/bin/bash

# TODO This script needs to run on an EC2 instance as the PIP library dependencies can be OS specific and Lambda runs on Amazon Linux
# To complete this task we need to automate launching an EC2 instance, deploying the shell script, running the script, and pushing the output folder somewhere that
# terraform can find it

# PREPARE WORKING DIRECTORY
WORKDIR="function"
if [ -d $WORKDIR ]; then
  rm -Rf $WORKDIR
fi

mkdir $WORKDIR

# DOWNLOAD THE LATEST LAMBDA CODE FROM THE ds-pdf-gen-lambda repo
curl https://raw.githubusercontent.com/nationalarchives/ds-disco-pdf-gen-lambda/master/PrepareFiles.py >$WORKDIR/PrepareFiles.py
curl https://raw.githubusercontent.com/nationalarchives/ds-disco-pdf-gen-lambda/master/handler.py >$WORKDIR/handler.py
mkdir $WORKDIR/font
curl https://github.com/nationalarchives/ds-disco-pdf-gen-lambda/blob/master/font/Arial.ttf >$WORKDIR/font/Arial.ttf

# USE PIP TO DOWNLOAD PYTHON DEPENDENCIES TO A VENV AND MOVE THEM TO THE WORKING DIR FOR PACKAGING, THEN DELETE THE VENV
cd $WORKDIR
python3 -m venv venv
. venv/bin/activate

# TODO I did create a requirements.txt file but suspect it is only applicable for a Mac. We need to get a requirements.txt file
# for an Amazon Linux EC2 instance so that we can bake the necessary version numbers in the deployment.
pip install -r ../requirements.txt
deactivate
mv -v venv/lib/python3.7/site-packages/PIL venv/lib/python3.7/site-packages/Pillow-6.2.2.dist-info .
rm -Rf venv

# AT THIS POINT $WORKDIR IS READY FOR ZIPPING BY TERRAFORM

#!/bin/bash

wget https://pfda-production-static-files.s3.amazonaws.com/cli/pfda-linux-2.7.1.tar.gz

tar -xvzf ./pfda-linux-2.7.1.tar.gz

mv pfda /usr/bin/

if [ -e /usr/bin/pfda ]
then
    echo "pfda cli installed successfully!"
else
    echo "ERROR: pdfa cli did not installed!"
fi
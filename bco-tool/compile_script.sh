#!/bin/sh

dx login --token $1 --noprojects
java -jar $4 compile $2 -project $3 > dx_compiler.log
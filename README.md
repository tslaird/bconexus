# BCOnexus

### Information

This is a fork of the dnanexus bconexus interface for creating/editing bco objects.
The original docker image is hosted at (https://hub.docker.com/r/dnanexus/bconexus/tags).
However, that image is only built for linux/arm64/v8 architecture. So I forked the github repository (https://github.com/biocompute-objects/dnanexus.git) in order to build an image with linux/amd64.

**Note: there were minor edits made to certain files in order to get the docker image up and running.** You can see those in teh file diffs for the Dockerfile, settings.py, and urls.py


### To build the docker container after cloning this repo you can run:
```
docker build --platform linux/amd64 -t bconexus .
```

### To run the application:
```
docker run -p 8000:8000 bconexus
```
Then navigate to http://localhost/8000

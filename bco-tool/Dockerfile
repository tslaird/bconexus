FROM ubuntu:20.04
# ARG VERSION

# Install java-8
RUN apt-get update && \
    apt-get install -y wget openjdk-8-jdk-headless git

# dxCompiler
COPY dxCompiler-2.10.3.jar /dxCompiler-2.10.3.jar

# install pfda cli
COPY install_pfda.sh /install_pfda.sh

ENV PYTHONUNBUFFERED 1

RUN mkdir /bconexus

WORKDIR /bconexus

ADD . /bconexus/

RUN apt-get update && \
    apt-get install -y python3-pip

RUN pip3 install -r requirements_latest.txt

RUN ./install_pfda.sh

EXPOSE 8000

CMD ["gunicorn","bconexus.wsgi","--bind","0.0.0.0:8000"]
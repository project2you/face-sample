FROM python:3.6-slim-stretch
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    nano \
    htop \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN pip3 install pillow
RUN pip3 install flask
RUN pip3 install face-recognition
RUN pip3 install uwsgi

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS
COPY app.py /home
COPY test1.jpg /home
COPY test2.jpg /home

COPY requirements.txt /home

RUN cd /home && \
    pip3 install -r requirements.txt

WORKDIR /home
CMD [ "python3", "-u", "./app.py" ]

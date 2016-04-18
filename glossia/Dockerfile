FROM ubuntu:15.10

RUN adduser --system --quiet --home /var/lib/glossia --no-create-home --shell /bin/false --group --gecos "Go-Smart Simulation Server" glossia

RUN apt-get update

RUN apt-get install -y python python-pip python3 python3-pip libjsoncpp-dev cmake python3-yaml git python3-lxml \
                       python3-zope.interface python3-paramiko

RUN pip3 install munkres 'autobahn<=0.12.1' hachiko pyroute2

ENV GLOSSIA_COMMIT 587e5dd
RUN cd /usr/src && git clone https://github.com/go-smart/glossia.git glossia && cd glossia && git checkout ${GLOSSIA_COMMIT}

RUN mkdir -p /opt/glossia

WORKDIR /opt/glossia

ENV GLOSSIA_PREFIX=/usr/local
RUN cmake /usr/src/glossia -DCMAKE_INSTALL_PREFIX=${GLOSSIA_PREFIX}

RUN make

RUN make install

RUN mkdir -p /var/run/glossia /var/lib/glossia

RUN chown -R glossia:glossia /var/run/glossia

VOLUME /var/run/glossia

WORKDIR /var/run/glossia

COPY env.sh configure.py /

ENV GLOSSIA_SIMULATION_DIRECTORY /simdata
ENTRYPOINT ["/env.sh"]

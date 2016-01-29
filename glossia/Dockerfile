FROM ubuntu:15.10

RUN adduser --system --quiet --home /var/lib/gssa --no-create-home --shell /bin/false --group --gecos "Go-Smart Simulation Server" gssa

RUN apt-get update

RUN apt-get install -y python python-pip python3 python3-pip libjsoncpp-dev cmake python3-yaml git python3-lxml \
                       python3-zope.interface python3-paramiko

RUN pip3 install munkres autobahn hachiko

ENV GSSA_COMMIT f408fbb
RUN cd /usr/src && git clone https://github.com/numa-engineering/gosmart-gssa.git gssa && cd gssa && git checkout ${GSSA_COMMIT}

RUN mkdir -p /opt/gssa

WORKDIR /opt/gssa

ENV GSSA_PREFIX=/usr/local
RUN cmake /usr/src/gssa -DCMAKE_INSTALL_PREFIX=${GSSA_PREFIX}

RUN make

RUN make install

RUN mkdir -p /var/run/gssa /var/lib/gssa

RUN chown -R gssa:gssa /var/run/gssa

VOLUME /var/run/gssa

WORKDIR /var/run/gssa

COPY env.sh configure.py /

ENTRYPOINT ["/env.sh"]

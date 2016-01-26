FROM ubuntu:15.10

RUN adduser --system --quiet --home /var/run/gssa --no-create-home --shell /bin/false --group --gecos "Go-Smart Simulation Architecture" gssa

RUN apt-get  update

RUN apt-get install -y python3-pip

RUN pip3 install hachiko

RUN mkdir -p /shared && chown -R gssa:gssa /shared

ENTRYPOINT ["/usr/bin/python3", "/bridge.py"]

VOLUME /shared

COPY bridge.py /bridge.py

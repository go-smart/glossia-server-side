#!/bin/sh

export HOST="${CROSSBAR_HOST}"
export PORT="${CROSSBAR_PORT}"

mkdir -p /var/run/gssa
cd /var/run/gssa

python3 /configure.py ${GSSA_PREFIX}/etc/gosmart/gssa.yml

groupadd -g `stat -c "%g" "${DOCKERLAUNCH_SOCKET}"` dockerlaunch

# We put gssa in the dockerlaunch group - this is the only
# real reason we have to have root running this script
# There's no way to interact with Docker without punching
# a security hole (thankfully), so dockerlaunch exists to
# minimize it, by making this socket the known puncture
# with a predefined set of interactions. This is /all/
# that the dockerlaunch groups should ever have access to.
usermod -aG dockerlaunch gssa

chown -R gssa:gssa /simdata

su gssa -s /bin/sh -c "go-smart-simulation-server --host $HOST --websocket-port $PORT $@"

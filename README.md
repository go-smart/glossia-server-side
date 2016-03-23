Glossia (aka. GSSA)
===================

The Go-Smart Simulation Architecture
------------------------------------

**Primary authors** : [NUMA Engineering Services Ltd](http://www.numa.ie) (NUMA), Dundalk, Ireland

**Project website** : http://www.gosmart-project.eu/

This project is co-funded by: European Commission under grant agreement no. 600641.

This set of containers and scripts provides a means for setting up a Glossia server using docker-compose.
Please note that the provided docker-compose.yml will start a Crossbar instance also - if you wish to
connect to an existing Crossbar instance, use `docker run` with arguments based on those in the
docker-compose.yml file.

Usage
-----

The simulation server (Glossia) may be launched by the command

```sh
    cd compose
    sudo docker-compose up -d
```

Note that the host must have a running `dockerlaunchd` instance, with a socket in
`/var/run/docker-launch/docker-launch.sock` accessible to the `dockerlaunch`
user group.

If Crossbar is interrupted unexpectedly, you may need to manually remove the `node.pid` file from
the `web` subdirectory.

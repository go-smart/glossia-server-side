#!/usr/bin/env python3

import argparse
import logging
import pwd
import grp
import asyncio
import os
import shutil
import functools
from functools import partial
from hachiko.hachiko import AIOEventHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

gssa_prefix = '/simdata'
container_prefix = '/shared'
gssa_socket_name = 'update.sock'


@asyncio.coroutine
def handle_relay(writer, reader, _):
    while True:
        data = yield from reader.read(1024)
        if not data:
            break
        writer.write(data)
        yield from writer.drain()


def exit(loop, observer):
    observer.stop()

    if loop:
        loop.stop()
        logging.info("Stopped event loop")

    observer.join()
    logging.info("Observer exited")


class DockerBridgeHandler(AIOEventHandler, FileSystemEventHandler):
    active = False

    def __init__(self, exit, input_directory, output_directory, output_directory_tmp, loop=None, **kwargs):
        self._exit = exit
        self._loop = loop
        self._input_directory = input_directory
        self._output_directory = (output_directory_tmp, output_directory)

        logging.info('From directory is ' + input_directory)
        logging.info('To directory is ' + output_directory)

        AIOEventHandler.__init__(self, loop)
        FileSystemEventHandler.__init__(self, **kwargs)

    @asyncio.coroutine
    def update_socket_relay(self, update_socket):
        logging.info("Starting bridge socket")
        gssa_socket = update_socket
        _, writer = yield from asyncio.open_unix_connection(gssa_socket, loop=self._loop)
        logging.info("Connected")
        socket_location = os.path.join('/shared', 'update.sock')
        yield from asyncio.start_unix_server(
            functools.partial(handle_relay, writer),
            socket_location,
            loop=self._loop
        )
        uid = pwd.getpwnam('gssa').pw_uid
        gid = grp.getgrnam('gssa').gr_gid
        os.chown(socket_location, uid, gid)
        logging.info("Server started")

    def copy(self):
        shutil.copytree(self._input_directory, self._output_directory[0])
        # Ensures everything is in place on the FS when the modified event fires
        os.rename(*self._output_directory)

    @asyncio.coroutine
    def on_moved(self, event):
        logging.info("[MVD] %s" % event.src_path)
        if event.dest_path == self._input_directory:
            self.copy()
            self._exit()


@asyncio.coroutine
def run(loop, gssa_id):
    input_observer = Observer()
    output_observer = Observer()

    input_prefix = os.path.join(gssa_prefix, gssa_id)

    input_event_handler = DockerBridgeHandler(
        partial(exit, None, input_observer),
        os.path.join(input_prefix, 'input.final'),
        os.path.join(container_prefix, 'input'),
        os.path.join(container_prefix, '.input.tmp'),
        loop=loop
    )

    output_event_handler = DockerBridgeHandler(
        partial(exit, loop, output_observer),
        os.path.join(container_prefix, 'output.final'),
        os.path.join(input_prefix, 'output'),
        os.path.join(input_prefix, '.output.tmp'),
        loop=loop
    )

    update_socket = os.path.join(input_prefix, gssa_socket_name)
    yield from input_event_handler.update_socket_relay(update_socket)

    input_observer.schedule(input_event_handler, input_prefix)

    try:
        input_event_handler.copy()
    except OSError:
        input_observer.start()
        logging.info('Input observation thread started')
    else:
        logging.info('Input available before observer ready')

    output_observer.schedule(output_event_handler, container_prefix)

    # Make sure the output isn't already there
    try:
        output_event_handler.copy()
    except OSError:
        output_observer.start()
        logging.info('Output observation thread started')
    else:
        logging.info('Output available before observer ready')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy input directory to simulation container')
    parser.add_argument("prefix", help="Prefix for the /simdata/[prefix]/input path on GSSA")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logging.info('Starting up...')

    loop = asyncio.get_event_loop()

    asyncio.async(run(loop, args.prefix))

    try:
        loop.run_forever()
    finally:
        loop.close()

    logging.info('Loop closed and exiting...')

import yaml
from os import environ
import sys
import logging


def insert_setting(ymlkey, envkey, cast=str):
    keys = ymlkey.split('.')
    level = config
    for k in keys[:-1]:
        if k not in level:
            level[k] = {}
        level = level[k]
    level[keys[-1]] = cast(environ[envkey])

try:
    config_file = sys.argv[1]
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
except (OSError, KeyError) as e:
    logging.error(
        "You must provide one arg: the gssa.yml file to configure"
    )
    raise

insert_setting('dockerlaunch.socket_location', 'DOCKERLAUNCH_SOCKET')

with open(config_file, 'w') as f:
    yaml.safe_dump(config, f, default_flow_style=False)

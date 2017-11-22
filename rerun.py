#!/usr/bin/env python
#
# https://github.com/dbrandt/rerun
#
# A simple script that tries to recreate an approximate docker run
# command from the metadata of a running container. It's not complete
# and it's not tested in very many situations. If you want to extend it,
# please do. I'll accept any pull request within the scope.
#
# Daniel Brandt <me@dbrandt.se>
#

import sys
import shlex

import docker


usage = """Recreate an approximate docker run-command from a running container.

  %s <container_id>""" % (sys.argv[0],)


def get_container_config(api_client, container_id):
    c = api_client.containers(filters={"id": container_id})
    config = api_client.inspect_container(c[0].get("Id")).get("Config")

    return config

def construct_command(config):
    cmd = "docker run --rm -it \\\n"
    if config.get("Entrypoint"):
        cmd += "    --entrypoint %(Entrypoint)s \\\n" % config
    for env in config.get("Env", []):
        key, val = env.split("=")
        cmd += "    -e %s=%s \\\n" % (key, shlex.quote(val))
    for port, _ in config.get("ExposedPorts").items():
        port, proto = port.split("/")
        if proto == "tcp":
            cmd += "    -p %s:%s \\\n" % (port, port)
    cmd += "    %(Image)s \\\n" % config
    cmd += "    %s\n" % (" ".join(config.get("Cmd")),)

    return cmd


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)
    cid = sys.argv[1]

    api_client = docker.APIClient()

    config = get_container_config(api_client, cid)
    cmd = construct_command(config)

    print(cmd)

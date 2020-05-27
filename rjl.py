#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2019  Hauke Petersen <dev@haukepetersen.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import yaml
import argparse
import subprocess

STATUSFILE = "/tmp/rjl-target-config.yml"


def get_env(target):
    env = ["BOARD={}".format(target['board'])]
    if 'node' in target:
        env.append("IOTLAB_NODE={}".format(target['node']))
    if 'exp_id' in target:
        env.append("IOTLAB_EXP_ID={}".format(target['exp_id']))
    if 'port' in target:
        env.append("PORT={}".format(target['port']))
    if 'programmer' in target:
        env.append("PROGRAMMER={}".format(target['programmer']))
    if 'serial' in target:
        if target['programmer'] == 'jlink':
            env.append("JLINK_SERIAL={}".format(target['serial']))
        else:
            env.append("DEBUG_ADAPTER_ID={}".format(target['serial']))
    return env

def main(args):
    nodes = {}

    # read session configuration
    with open(STATUSFILE, 'r', encoding='utf-8') as f:
        nodes = yaml.load(f, Loader=yaml.FullLoader)


    # find entry for given target
    if args.target not in nodes:
        sys.exit("Error: given target is not connected")

    env = get_env(nodes[args.target])
    print(env)

    print(args.cmd)

    # special case: open terminal if 'term' is the command
    if 'term' in args.cmd:
        print("foo", nodes[args.target]['port'])
        subprocess.call('pyterm -p {}'.format(nodes[args.target]['port']), shell=True)
        return

    cmd = ' '.join(env + args.cmd)
    print(cmd)
    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("target", help="Name of the target node")
    p.add_argument("cmd", nargs="+", help="command to execute")
    args = p.parse_args()

    main(args)

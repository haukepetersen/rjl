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

import os
import re
import sys
import yaml
import argparse
import subprocess as proc

STATUSFILE = "/tmp/rjl-target-config.yml"
DEFAULTCFG = "{}/.rjl.yml".format(os.path.expanduser('~'))


def read_devs():
    serials = {}
    acmdev = proc.check_output(['ls /dev/ttyACM*'],
                               shell=True).decode('utf-8').splitlines()
    for tty in acmdev:
        info = proc.check_output(['udevadm', 'info',
                                  '--name={}'.format(tty)]).decode('utf-8')
        m = re.search("SEGGER_J-Link_(\d+)", info)
        if m:
            serials[m.group(1)] = {'port': tty}
    return serials


def main(args):
    config_file = args.config_file
    env = {}
    cfg = None

    if not config_file:
        config_file = DEFAULTCFG

    with open(config_file, 'r', encoding='utf-8') as f:
        cfg = yaml.load(f)

    if not cfg:
        sys.exit("Error: unable to read configuration file")

    # read all ttyACM* devices and their serial numbers
    devs = read_devs()

    # map devices to configuration entires
    for target in cfg['targets']:
        serial = target['serial']
        if serial in devs:
            target.update(devs[serial])
            env[target['name']] = target

    # write session configuration
    with open(STATUSFILE, 'w', encoding='utf-8') as f:
        yaml.dump(env, f, default_flow_style=False)

    # output list of active devices
    for k in sorted(list(env)):
        serial = env[k]['serial']
        port = env[k]['port']
        board = env[k]['board']

        print("{:>4}:  SERIAL={}  PORT={}  BOARD={}".format(k, serial,
                                                            port, board))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("config_file", nargs="?", help="target configuration file")
    args = p.parse_args()
    main(args)

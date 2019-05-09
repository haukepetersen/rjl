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
import json
import yaml
import argparse
import subprocess as proc

STATUSFILE = "/tmp/rjl-target-config.yml"
DEFAULTCFG = "{}/.rjl.yml".format(os.path.expanduser('~'))

def find_cfg(cfg, node):
    for target in cfg['targets-iotlab']:
        if target['node'] == node:
            return target


def main(args):
    cfg = {}
    nodes = {}
    config_file = args.config_file


    # load config file
    if not config_file:
        config_file = DEFAULTCFG
    with open(config_file, 'r', encoding='utf-8') as f:
        cfg = yaml.load(f)

    # read active experiments
    res = proc.check_output(['iotlab-experiment get -l --state Running'],
                            shell=True)
    dat = json.loads(res)

    for exp in dat['items']:
        for node in exp['resources']:
            t = find_cfg(cfg, node)
            # print(t, exp['id'])
            nodes[t['name']] = {
                'node': node,
                'exp_id': exp['id'],
                'board': t['board'] }

    with open(STATUSFILE, 'w', encoding='utf-8') as f:
        yaml.dump(nodes, f, default_flow_style=False)

    for k in sorted(list(nodes)):
        node =  nodes[k]['node']
        exp_id = nodes[k]['exp_id']
        board = nodes[k]['board']

        print("{:>4}:  BOARD={} IOTLAB_NODE={} IOTLAB_EXP_ID={}".format(k, board,
                                                                        node, exp_id))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("config_file", nargs="?", help="target configuration file")
    args = p.parse_args()
    main(args)

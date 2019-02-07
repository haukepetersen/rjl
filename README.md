# RIOT JLink helper

This tool was designed to simplify the handling of multiple, jlink-based
development boards connected to your host machine when working with RIOT.

It simply maintains a mapping from user defined names to the tuple of
`(JLINK_SERIAL, BOARD, PORT)` environment variables.

## Usage
Short:
1. run `rjl-config.py [CONFIG_FILE]`
2. in your RIOT application, run e.g. `rjl MY_TARGET_NAME make flash term`

Long:
1. Create a configuration file with all your nodes, their jlink serial numbers,
   and custom names. The default location for this file is `~/.rjl.yml`. See
   also the `config_example.yml` file in this repository.

2. Run `jrl-config.py` from anywhere on your system. This will iterate through
   all `/dev/ttyACM*` devices currently connected to the host system. All
   devices that have an entry in the selected configuration file will be put
   into a temporary mapping file.

3. Go into any RIOT application folder and simply call `rjl.py NAME make term`
   or whatever RIOT make command you need. The `NAME` parameter will take care
   of automatically setting the the `BOARD`, `JLINK_SERIAL`, and `PORT`
   environment variables to the configuration tied to that target name.

#!/usr/bin/env python3
# ^^ Shebang for running on nix systems without calling python



# ---------------------------------------------------------------------------- #
#                            Non-lib package imports                           #
# ---------------------------------------------------------------------------- #
import sys

# ------------------------- Check if verbose flag set ------------------------ #
if '-v' in sys.argv: verbose = True
else: verbose = False



# ---------------------------------------------------------------------------- #
#                              Lib package imports                             #
# ---------------------------------------------------------------------------- #

# ------------------- Load configuration and cli libraries ------------------- #
#
# Load config and cli libraries so we can prepare the configuration
# files and cli library (so we can access verbose) prior to loading
# other libraries and the program
#
from lib.config     import config
from lib.cli        import cli
config = config(verbose); cli = cli(verbose)# Initialise config and cli libs

# -------------------------- Generate configuration -------------------------- #
if config.getConfig() == {}:
    cli.verbose("Building config")
    config.buildConfig('default')
    config = config(verbose)#Reload config lib
    cli = cli(verbose)#Reload cli lib
else:
    cli.verbose("Config found")
    cli.verbose(f"Configuration: {config.getConfig()}")

# -------------------------------- Import libs ------------------------------- #
#
# With all dependencies loaded we can now go ahead and load the rest
# of the libraries
#
from lib.api        import api
from lib.package    import package
from lib.detection  import detection
from lib.data       import data
detection = detection(verbose); data = data(verbose); api = api(verbose); package = package(verbose);# Initialise all other libs

# Log out config location
cli.verbose(f"Configuration location: {config.configLocation}")



# ---------------------------------------------------------------------------- #
#                                  Check flags                                 #
# ---------------------------------------------------------------------------- #

# ------------------- Check if any static flags were called ------------------ #
if cli.checkStaticFlag(sys.argv): #Check with cli module if any static flags were passed (version, help etc, anything that isn't an operation) 
    cli.verbose('Static flag passed, exiting')
    exit(0)#Static flag passed, exit

# ------------------------------- Command flags ------------------------------ #
"""try:#Please note the below is a placeholder
    if sys.argv[1] == 'install':
        api.getPackage('something')

    elif sys.argv[1] == 'remove':
        api.getPackage('something')

    elif sys.argv[1] == 'config':
        api.getPackage('something')

    elif sys.argv[1] == 'update':
        api.getPackage('something')
except: cli.verbose('No flags passed'); pass"""

print(package.getRemoteIndex())
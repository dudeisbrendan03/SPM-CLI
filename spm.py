#!/usr/bin/env python3
# ^^ Shebang for running on nix systems without calling python

# Package imports
import sys

# Check if verbose flag
if '-v' in sys.argv: verbose = True
else: verbose = False

# Load configuration and cli libraries
from lib.config     import config
from lib.cli        import cli
cli = cli(verbose); config = config(verbose)

# Generate configuration
if config.getConfig() == {}:
    cli.verbose("Building config")
    config.buildConfig('default')
else:
    cli.verbose("Config found")
    cli.verbose(f"Configuration: {config.getConfig()}")

# Import other libraries
from lib.api        import api
from lib.package    import package
from lib.detection  import detection
from lib.data       import data
detection = detection(verbose); data = data(verbose); api = api(verbose); package = package(verbose);# Initialise everything

# Log out config location
cli.verbose(f"Configuration location: {config.configLocation}")

# Check if any static flags were called
if cli.checkStaticFlag(sys.argv): #Check with cli module if any static flags were passed (version, help etc, anything that isn't an operation) 
    cli.verbose('Static flag passed, exiting')
    exit(0)#Static flag passed, exit

# Main program
try:
    if sys.argv[1] == 'install':
        api.getPackage('something')

    elif sys.argv[1] == 'remove':
        api.getPackage('something')

    elif sys.argv[1] == 'config':
        api.getPackage('something')

    elif sys.argv[1] == 'update':
        api.getPackage('something')
except: cli.verbose('No flags passed'); pass

print(package.getRemoteIndex())
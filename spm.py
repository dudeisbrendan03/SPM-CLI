#!/usr/bin/env python
# ^^ Shebang for running on nix systems without calling python

# Package imports
import sys

# Import lib
from lib.cli        import cli
from lib.api        import api
from lib.package    import package
from lib.detection  import detection
from lib.data       import data
from lib.config     import config
cli = cli(); detection = detection(); data = data(); config = config(); api = api(); package = package();# Initialise everything

# Check if verbose flag
if '-v' in sys.argv: verbose = True
else: verbose = False

# Generate configuration
if config.getConfig() == False:
    cli.verbose("Building config",verbose)
    config.buildConfig('default')
else:
    cli.verbose("Config found",verbose)
    cli.verbose(f"Configuration: {config.getConfig()}",verbose)

# Log out config location
cli.verbose(f"Configuration location: {config.configLocation}",verbose)

# Check if any static flags were called
if cli.checkStaticFlag(sys.argv): #Check with cli module if any static flags were passed (version, help etc, anything that isn't an operation) 
    cli.verbose('Static flag passed, exiting',verbose)
    exit(0)#Static flag passed, exit

# Main program
if sys.argv[1] == 'install':
    api.getPackage('something')

elif sys.argv[1] == 'remove':
    api.getPackage('something')

elif sys.argv[1] == 'config':
    api.getPackage('something')

elif sys.argv[1] == 'update':
    api.getPackage('something')

#!/usr/bin/env python3
# ^^ Shebang for running on nix systems without calling python



# ---------------------------------------------------------------------------- #
#                            Non-lib package imports                           #
# ---------------------------------------------------------------------------- #
import sys
import os

# ------------------------------ import json lib ----------------------------- #
from lib.etc import getJson as json; json=json()

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

# ------------------------ Import custom exception lib ----------------------- #
import lib.issue as SPMCLIExceptions

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
try:
    if sys.argv[1] == 'install':
        try: package.downloadPackage(sys.argv[2])
        except SPMCLIExceptions.BadPackageName as e: print("You specified an invalid package or something went wrong"); cli.verbose('Uncaught exception occured in runtime '+str(e))

    elif sys.argv[1] == 'remove':
        api.getPackage('something')

    elif sys.argv[1] == 'config':
        api.getPackage('something')

    elif sys.argv[1] == 'update':
        api.getPackage('something')

    elif sys.argv[1] == 'fetch':
    # ------------ download all the remote package information to disk ----------- #
        if '--save' in sys.argv:
            if '--delete' in sys.argv:#let us delete the cache
                print("WARNING: Deleting all cached packages")
                try: data.deleteConfigDirectory('packages/')
                except FileNotFoundError: print("There are no packages cached on the system")
            else:
                print("Download all remote package information to the disk, this may take a while...")
                package.getAllRemotePackages()
    # ----------- delete the local package index if --delete is passed ----------- #
        elif '--delete' in sys.argv:
            print("Deleting the remote index stored on disk...")
            cli.verbose("Calling data.deleteFile to wipe index from disk")
            data.deleteConfigFile('remote.index')
            cli.verbose("The remote index was destroyed")


    # --------------- debug option - print out the index to stdout --------------- #
        elif '-v' in sys.argv and '--get' in sys.argv:
            cli.verbose("Fetching and printing the package index on disk...")
            try:
                print(json.dumps(package.getDiskIndex(),indent=4))
            except json.decoder.JSONDecodeError:
                print("Couldn't decode the JSON passed:\n"+str(package.getDiskIndex()))

    # ----------------------- normal package index download ---------------------- #
        else:
            print("Updating the remote package index...")
            if os.path.exists(detection.getPath('$HOME')+'remote.index') == True: print("Overwriting remote package index on disk...")
            cli.verbose('Calling getRemoteIndex to write to disk')
            try: package.getRemoteIndex()
            except: print("Failed to write to the remote index store on disk")

    else: cli.verbose('No flags passed'); pass
except IndexError: print('No flags passed, assuming help'); cli.checkStaticFlag(['--help']) 
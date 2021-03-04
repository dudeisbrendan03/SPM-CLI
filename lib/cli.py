"""
SPM-CLI

cli tools library


"""





class cli(object):
    def __init__(self,verbose) -> None:
        super().__init__()
        
        #Set verbose flag
        self.verbosef = verbose

        #Import config lib
        from lib.config import config
        from lib.detection import detection
        self.detection = detection(verbose)
        self.config = config(verbose)
        self.shipping = self.config.shipping()

    def checkStaticFlag(self,args):
        if '--version' in args:
            print(self.shipping)
            print(f"""SPM-CLI
  ____________   _____  
 /  ___/\\____ \ /     \\ 
 \\___ \\ |  |_> >  Y Y  \\
/____  >|   __/|__|_|  /
     \\/ |__|         \\/ 
_________________________

   Version: {self.shipping['version']}
    Author: {self.shipping['author']}
Repository: {self.shipping['repository']}
       Tag: {self.shipping['release']}
""")
            return True
        elif '--help' in args or '-h' in args:
            print(f"""spm-api
Release {self.shipping['version']}

Usage:
    ./spm.py [OPTIONS] COMMAND <COMMAND FLAGS> <VERBOSE>

    Options:
        --help | -h
            Displays this help message
        
        --version
            Displays the version and shipping information for this release

    Commands:
        install
            Installs package to your system
            
            Flags:
                something

        remove
            Removes a package from your system
            
            Flags:
                something
        
        update
            Updates a package on your system

            Flags:
                something

        fetch
            Downloads the remote package index to your disk

            Flags:
                --delete
                    Deletes the remote index on your disk

                --save
                    Download every remote package and store to disk

                --get (requires verbose)
                    Logs out into verbose the contents of remote.index
    
    Verbose:
        -v
            Verbose stdout output for debugging purposes

""")
            return True
        return False

    def verbose(self,message):
        if self.verbosef: print(f"[VERBOSE] {message}")

    def clear(self):
        from os import system as s
        if self.detection.platformname() == 'Windows': s('cls')
        else: s('clear')
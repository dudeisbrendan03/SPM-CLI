"""
SPM-CLI

cli tools library


"""





class cli(object):
    def __init__(self) -> None:
        super().__init__()
        
        #Import config lib
        from lib.config import config
        self.config = config()
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
    ./spm.py [OPTIONS] COMMAND <COMMAND FLAGS>

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
""")
            return True
        return False

    @staticmethod
    def verbose(message,flag=False):
            if flag: print(f"[VERBOSE] {message}")
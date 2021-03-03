"""
SPM-API

package tools library


"""





class package(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        
        import lib.etc as etc
        from lib.api import api
        from lib.detection import detection
        from lib.cli import cli;cli=cli(verbose)
        self.json = etc.getJson()
        self.api = api(verbose)
        self.detection = detection(verbose)
        self.log = cli.verbose

    def buildIndex(self):
        print("WARNING\nRebuilding the package index will allow the installation of packages if it doesn't exist, but overwriting an existing package index will remove your ability to manage and uninstall packages installed and controller by spm")
        input("Press ENTER to continue, destroying the current index and building a new one, or Ctrl+C to abort, leaving files untouched.")
    
    def getRemoteIndex(self):
        print("Trying to download remote index...")
        self.log('Writing .spm/remote.index')
        with open(self.detection.getpath('$HOME')+'.spm/remote.index','w') as f:
            self.log('Fetching remote index and writing to disk')
            f.write(self.json.dumps(self.api.getIndex()))
        print("Written remote index to disk")
        
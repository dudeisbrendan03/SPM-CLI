"""
SPM-API

package tools library


"""





class package(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        
        import lib.etc as etc
        from lib.api import api
        self.json = etc.getJson()
        self.api = api(verbose)

    def buildIndex(self):
        print("WARNING\nRebuilding the package index will allow the installation of packages if it doesn't exist, but overwriting an existing package index will remove your ability to manage and uninstall packages installed and controller by spm")
        input("Press ENTER to continue, destroying the current index and building a new one, or Ctrl+C to abort, leaving files untouched.")
    
    def getRemoteIndex(self):
        print("Trying to download remote index...")
        return self.api.getIndex()
"""
SPM-CLI

data tools library


"""

from json.decoder import JSONDecodeError


class data(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        import lib.etc as etc
        from lib.detection import detection
        from lib.cli import cli;
        self.cli=cli(verbose)
        self.detection = detection(verbose)
        self.log = self.cli.verbose
        self.json = etc.getJson()

    def updateFile(self,filepath,data):
        try:
            with open(filepath,'r') as f:
                try: originalData= self.json.load(f)# Read the data with json.load
                except: raise JSONDecodeError
        except: raise FileNotFoundError

        try:
            with open(filepath,'w') as f:# Open the file in write
                newData = {**data, **originalData}# Combine our arrays
                f.write(self.json.dumps(newData))# Write the data
        except: raise IOError

# ------------------------- config directory options ------------------------- #
    def createConfigDirectory(self,filepath):
        self.log('Data called to create dir')
        try:
            import os
            target = self.detection.getPath('$CONFIG')+filepath
            self.log('Created target path to created')
            if not os.path.exists(target):
                self.log("Target directory doesn't exist... creating")
                os.mkdir(target)
            self.log('Created a directory')
        except: pass

# ---------------------------- config file options --------------------------- #
    def createConfigFile(self,filepath,data):
        self.log('Data called to create file')
        try:
            import os
            target = self.detection.getPath('$CONFIG')+filepath
            self.log('Created target path to create')
            self.log('Writing')
            with open(target,'w') as f:
                f.write(data)
        except: pass

    def deleteConfigFile(self,filepath):
        self.log('Data called to remove file')
        try:
            import os
            target = self.detection.getPath('$CONFIG')+filepath
            self.log('Created target path to delete')
            if os.path.exists(target):
                self.log('Target file exists... removing')
                os.remove(target)
                self.log('Deleted a file')
        except: pass

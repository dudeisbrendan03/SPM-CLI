"""
SPM-CLI

data tools library


"""

from json.decoder import JSONDecodeError


class data(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        import os

        import lib.etc as etc
        from lib.detection import detection
        from lib.cli import cli;
        self.os = os
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
        target = self.detection.getPath('$CONFIG')+filepath
        self.log('Created target path to created')
        if not self.os.path.exists(target):
            self.log("Target directory doesn't exist... creating")
            self.os.mkdir(target)
        self.log('Created a directory')

# ---------------------------- config file options --------------------------- #
    def createConfigFile(self,filepath,data):
        self.log('Data called to create file')
        try:
            target = self.detection.getPath('$CONFIG')+filepath
            self.log('Created target path to create')
            self.log('Writing')
            with open(target,'w') as f:
                f.write(data)
        except: pass

    def deleteConfigFile(self,filepath):
        self.log('Data called to remove file')
        try:
            target = self.detection.getPath('$CONFIG')+filepath
            self.log('Created target path to delete')
            if self.os.opath.exists(target):
                self.log('Target file exists... removing')
                self.os.oremove(target)
                self.log('Deleted a file')
        except: pass

    def readConfigFile(self,filepath):
        self.log('Data called to read file')
        try:
            target = self.detection.getPath('$CONFIG')+filepath
            self.log('Created target path to read')
            if self.os.path.exists(target):
                self.log('File exists... reading')
                with open(target,'r') as f:
                    return self.json.load(f)
            self.log(f"Failed to see if {self.detection.getPath('$CONFIG')+filepath} exists")
            pass
        except: pass
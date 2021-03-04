"""
SPM-CLI

data tools library


"""

from json.decoder import JSONDecodeError
from re import I


class data(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        import os
        import requests
        import lib.issue as SPMCLIExceptions
        import lib.etc as etc
        
        from lib.detection import detection
        from lib.cli import cli;
        
        self.SPMCLIExceptions = SPMCLIExceptions
        self.requests = requests
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

    def deleteConfigDirectory(self,filepath):
        self.log('Data called to destroy dir')
        from shutil import rmtree
        try: rmtree(self.detection.getPath('$CONFIG')+filepath); self.log('Deleted directory')
        except FileNotFoundError: self.log('Directory specified does not exist'); raise FileNotFoundError("Directory specified does not exist")

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

# ---------------------------------------------------------------------------- #
#                          network based file options                          #
# ---------------------------------------------------------------------------- #

# ------------------------------ download a file ----------------------------- #

    def getFilename_fromCd(cd):#https://www.tutorialspoint.com/answers/arjun-thakur
        from re import findall
        if not cd:
            return None
        fname = findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def downloadFile(self,uri,writeLocation):
        self.log('Trying to download: '+str(uri))
        try:
            r = self.requests.get(uri, allow_redirects=True)
            try: filename = self.getFilename_fromCd(r.headers.get('content-disposition'))
            except:
                from re import compile
                self.log("Couldn't determine filename, attempting alternative method")
                plainuri = compile(r"https?://(www\.)?").sub('',uri).strip().strip('/')
                try: filename = plainuri.split('/')[-1]
                except IndexError: filename = plainuri
                self.log("Output using regex: "+str(filename))
                
            self.log(f"Writing to {writeLocation+'/'+filename}")
            open(writeLocation+'/'+filename, 'wb').write(r.content)
            return (True, str(filename))
        except:
            self.log('Failed to download the content requested!')
            return (False, '')
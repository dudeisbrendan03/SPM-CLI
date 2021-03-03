"""
SPM-CLI

data tools library


"""

from json.decoder import JSONDecodeError


class data(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        import lib.etc as etc
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

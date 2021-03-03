"""
SPM-CLI

config tools library


"""

class config(object):
    def __init__(self) -> None:
        super().__init__()
        #Detection
        from lib.detection import detection

        self.detection = detection()

        self.configLocation = self.detection.getpath('$CONFIG')+'config'# Config location

        #Import json using simplejson, and if that fails change to (native) json
        import lib.etc as etc
        self.json = etc.getJson()
        
        

    def shipping(self):
        try:
            with open(self.detection.getpath('$CONFIG')+'defaults/shipping.json') as f:
                shippingData = self.json.load(f)
        except:
            shippingData = {}

        return shippingData

    def getConfig(self):
        try:
            with open(self.configLocation,'r') as f:
                return self.json.load(f)
        except:
            return False


    def buildConfig(self,configType=''):
        from os import mkdir
        if configType == 'default':
            #Make directory if it doesn't exist
            try: mkdir(self.detection.getpath('$HOME')+'.spm')
            except: pass

            with open(self.configLocation,'w') as f:
                f.write(self.json.dumps(self.buildDefaults('default')))

    def buildDefaults(self,configType=''):
        if configType == 'default':
            with open(self.detection.getpath('$CONFIG')+'defaults/config.json') as f:
                return self.json.load(f)
        
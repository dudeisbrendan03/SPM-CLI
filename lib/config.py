"""
SPM-CLI

config tools library


"""

class config(object):
    def __init__(self,verbose) -> None:
        super().__init__()
        #Detection
        from lib.detection import detection

        self.detection = detection(verbose)
        self.verbosef = verbose
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
                configObj = self.json.load(f)
                if configObj['ssl']: configObj['baseurl'] = f"https://{configObj['endpoint']}"
                else: configObj['baseurl'] = f"http://{configObj['endpoint']}"
                return configObj
        except:
            return {}


    def buildConfig(self,configType=''):
        from os import mkdir
        from lib.cli import cli # importing here to prevent circular import
        cli = cli(self.verbosef)
        if configType == 'default':
            #Make directory if it doesn't exist
            try: mkdir(self.detection.getpath('$HOME')+'.spm');self.cli.verbose('Created .spm directory')
            except: cli.verbose(f"Failed to create .spm directory, it is likely to already exist. Failed to make {self.detection.getpath('$HOME')+'.spm'}");pass

            with open(self.configLocation,'w') as f:
                try:
                    f.write(self.json.dumps(self.buildDefaults('default')))
                    cli.verbose('Written default config to disk')
                except:
                    cli.verbose('Failed to write default config to disk')

    def buildDefaults(self,configType=''):
        from lib.cli import cli # importing here to prevent circular import
        cli = cli(self.verbosef)
        if configType == 'default':
            with open(self.detection.getpath('$CONFIG')+'defaults/config.json') as f:
                cli.verbose('Read default config')
                return self.json.load(f)
        
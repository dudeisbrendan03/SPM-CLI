"""
SPM-CLI

data tools library


"""

class config(object):
    def __init__(self,config={}) -> None:
        super().__init__()
        #Detection
        import lib.detection

        self.systemDir = lib.detection.systempath

        self.debug = {}
        if not "shipping" in config:
            config['shipping'] = ''

        #Import json
        try:
            from simplejson import json
            self.debug['jsonModule'] = 'simplejson'
            self.json = json
        except:
            import json
            self.debug['jsonModule'] = 'nativejson'
            self.json = json
        

    def shipping(self):
        

        return shippingData
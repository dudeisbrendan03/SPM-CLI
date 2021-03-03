"""
SPM-CLI

cli tools library


"""





class cli(object):
    def __init__(self) -> None:
        super().__init__()
        
        #Import config lib
        import lib.config
        configTools = new lib.config()
        version = configTools.shipping.version
        

    def about(self):


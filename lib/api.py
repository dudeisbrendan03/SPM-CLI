"""
SPM-API

api tools library


"""





class api(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        import requests
        self.requests = requests

        #from lib.etc import getJson
        from lib.cli import cli;cli=cli(verbose)
        from lib.config import config
        #self.json = getJson() - can just use requests.json
        self.configlib = config(verbose)
        self.config = self.configlib.getConfig()
        print("conf "+str(self.config))
        #if self.config == False: raise FileNotFoundError("Missing configuration")

        self.log = cli.verbose

    def getPackage(self, package, username=None,password=None):
        self.log('Getting package information')
        self.log(f'Opening request to {self.config['baseurl']}/{package}')
        r = self.requests.get(f'{self.config['baseurl']}/{package}')
        if not r.status_code == 200: self.log('Server did not respond with OK (200)'); return False
        
        self.log('Reading response body as JSON')
        #body = self.json.loads(r.)
        return r.json()

    def getIndex(self):
        self.log('Fetching remote index')
        self.log(f'Opening request to {self.config['baseurl']}/index')
        r = self.requests.get(f'{self.config['baseurl']}/index')
        if not r.status_code == 200: self.log('Server did not respond with OK (200)'); return False
        
        self.log('Reading response body as JSON')
        return r.json()
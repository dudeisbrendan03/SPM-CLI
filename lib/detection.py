"""
SPM-CLI

detection tools library


"""

class detection(object):
    def __init__(self,verbose) -> None:
        super().__init__()

        #Get users paltform
        from platform import system
        self.sysplatform = system()
        from os import name as genericplatform
        self.genericplatform = genericplatform

    def platform(self):
        return self.genericplatform
        
    def platformname(self):
        return self.sysplatform
        
    def getPath(self,path):
        if path ==      '$HOME':
            from os import path
            return path.expanduser('~/')
        elif path ==    '$DISK':
            if self.platformname() == 'Linux' or self.platformname() == 'Darwin': return '/'
            elif self.platformname() == 'Windows': return 'C:\\'
        elif path ==    '$CONFIG':
            if self.platformname() == 'Linux' or self.platformname() == 'Darwin': return self.getPath('$HOME')+'.spm/'
            elif self.platformname() == 'Windows': return self.getPath('$HOME')+'.spm\\'

        return False #not implemented
                
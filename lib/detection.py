"""
SPM-CLI

detection tools library


"""

class detection(object):
    def __init__(self) -> None:
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
        
    def getpath(self,path):
        if path ==      '$HOME':
            if self.platformname() == 'Linux' or self.platformname() == 'Darwin': return '~/'
            elif self.platformname() == 'Windows':
                from os import environ
                return f"{environ['USERPROFILE']}\\"
        elif path ==    '$DISK':
            if self.platformname() == 'Linux' or self.platformname() == 'Darwin': return '/'
            elif self.platformname() == 'Windows': return 'C:\\'
        elif path ==    '$CONFIG':
            if self.platformname() == 'Linux' or self.platformname() == 'Darwin': return self.getpath('$HOME')+'/.spm/'
            elif self.platformname() == 'Windows': return self.getpath('$HOME')+'.spm\\'

        return False #not implemented
                
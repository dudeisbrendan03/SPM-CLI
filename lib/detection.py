"""
SPM-CLI

detection tools library


"""

class detection(object):
    def __init__(self,config={}) -> None:
        super().__init__()

        #Get users paltform
        from platform import system
        self.sysplatform = system()
        from os import name as genericplatform
        self.genericplatform = genericplatform

    def platform(self):
        return self.sysplatform
        
    def platformname(self):
        return self.genericplatform
        
    def getpath(self,path):
        if path ==      '$HOME':
            if self.platform() == 'Linux' or self.platform() == 'Darwin': return '~'
            elif self.platform() == 'Windows': return '%userprofile%'
        elif path ==    '$DISK':
            if self.platform() == 'Linux' or self.platform() == 'Darwin': return '/'
            elif self.platform() == 'Windows': return 'C:\\'
        elif path ==    '$CONFIG':
            if self.platform() == 'Linux' or self.platform() == 'Darwin': return self.getpath('$HOME')+'/.spm/'
            elif self.platform() == 'Windows': return self.getpath('$HOME')+'\\.spm\\'

        return False #not implemented
                
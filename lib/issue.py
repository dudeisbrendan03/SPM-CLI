class Issues(Exception):
    """Base class for custom all issues raised by the cli"""
    pass

class BadPackageName(Issues):
    """The package name submitted does not meet the expected format, therefore it couldn't be processed accordingly"""
    pass

class FailedContentDownload(Issues):
    """Failed to download required content for a requested package, therefore the installation will not be able to continue"""
    pass

class FailedInstallation(Issues):
    """The installation failed for an unknown reason"""
    def __init__(self, msg='Installation failed for an unknown reason', error='', *args, **kwargs):
        if error != '': super().__init__(msg+"\nPython returned the error:\n"+str(error), *args, **kwargs) 
        else: super().__init__(msg, *args, **kwargs)
    pass

class UnsupportedOperatingSystem(FailedInstallation):
    """The operating system you're using is not supported by this package"""
    def __init__(self, msg="The operating system you're using is not supported by this package", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
    pass

class FailedScriptExecution(FailedInstallation):
    def __init__(self, msg="The installation failed while attempting to execute a script", filename='',*args, **kwargs):
        super().__init__(msg+'The reported file was: '+filename, *args, **kwargs)
    pass

class FailedCommandExecution(FailedInstallation):
    def __init__(self, msg="The installation failed while attempting to execute a script", command='',*args, **kwargs):
        super().__init__(msg+'The reported command was: '+command, *args, **kwargs)
    pass


class IntegrityError(Issues):
    """A file specified to be required for the installation, removal or modification of this software failed a checksum comparison"""
    pass

class UnsupportedVersion(Issues):
    pass

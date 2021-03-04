class Issues(Exception):
    """Base class for custom all issues raised by the cli"""
    pass

class BadPackageName(Issues):
    """The package name submitted does not meet the expected format, therefore it couldn't be processed accordingly"""
    pass

class FailedContentDownload(Issues):
    """Failed to download required content for a requested package, therefore the installation will not be able to continue"""
    pass
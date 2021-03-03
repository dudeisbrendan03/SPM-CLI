import sys
def logToConsole(prefix,state,message): print(f"[{state}] {prefix}: {message}")

if 'm.data' in sys.argv:
    from lib.data import data

if 'm.detection' in sys.argv:
    logToConsole('m.detection','I','Importing library')
    from ..lib.detection import detection

    logToConsole('m.detection','I','Initialising library')
    detectionTest=  detection()

    logToConsole('m.detection','I','Getting the platform')
    try:
        logToConsole('m.detection','N',detection.platform)
    except:
        logToConsole('m.detection','E','Failed to get the platform')

    logToConsole('m.detection','I','Getting the platform name')
    try:
        logToConsole('m.detection','N',detection.platformname)
    except:
        logToConsole('m.detection','E','Failed to get the platform')


if 'm.cli' in sys.argv:
    pass

if 'm.config' in sys.argv:
    pass
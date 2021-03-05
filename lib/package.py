"""
SPM-API

package tools library


package(object)
    init(verbose) -->
        args:
            verbose <-> Will log debug information to console if set to true, this flag is used to pass into cli
        
        steps:
            1. Import into self scope
                1. Import libs from outside the project
                2. Import libs from inside the project
                3. Import custom exceptions
                4. Get the configuration
                5. Initialise any classes which have yet to be initialized
    
    downloadPackage(package) -->
        args:
            package -> The uri format package you want to download
        
        steps:
            1. Parse package information
                1. Check if we already have the information cached locally
                    1. pass
                    2. Connect to API and download the package information, then cache it
                3. Load the information cached
                4. Ensure it is dict, not str
            2. Check if the system may install this package
                1. Get the support system
                2. Get the current system
                3. Check not Darwin package
                4. Check if systems match or if both darwin
            3. Download all content/assets
                1. Create temporary directories
                2. Download all data present in content


                tbc


"""





class package(object):
    def __init__(self,verbose) -> None:
        super().__init__()

# --------------------------- import 3rd/non-class --------------------------- #
        import lib.etc as etc
        import os

# ----------------------------- import libraries ----------------------------- #
        from lib.api import api
        from lib.detection import detection
        from lib.data import data
        from lib.config import config
        from lib.cli import cli;cli=cli(verbose)

# ----------------------------- Custom exceptions ---------------------------- #
        import lib.issue as SPMCLIExceptions
        self.SPMCLIExceptions = SPMCLIExceptions

# -------------------------------- get config -------------------------------- #
        self.config = config(verbose)

# ----------------------- initialise all other classes ----------------------- #
        self.data = data(verbose)
        self.os = os
        self.cli = cli
        self.etc = etc
        self.json = etc.getJson()
        self.api = api(verbose)
        self.detection = detection(verbose)
        self.log = cli.verbose
        self.verbose = verbose

    def buildIndex(self):
        print("WARNING\nRebuilding the package index will allow the installation of packages if it doesn't exist, but overwriting an existing package index will remove your ability to manage and uninstall packages installed and controller by spm")
        input("Press ENTER to continue, destroying the current index and building a new one, or Ctrl+C to abort, leaving files untouched.")
    
    def getRemoteIndex(self):
        print("Trying to download remote index...")
        self.log('Writing .spm/remote.index')
        with open(self.detection.getPath('$CONFIG')+'remote.index','w') as f:
            self.log('Fetching remote index and writing to disk')
            f.write(self.json.dumps(self.api.getIndex()))
        print("Written remote index to disk")
    
    def getDiskIndex(self):
        print("Retrieving disk index...")
        self.log('Opening and writing the file to stdout')
        with open(self.detection.getPath('$CONFIG')+'remote.index','r') as f:
            return self.json.load(f)

    def getAllRemotePackages(self):
        print("Retrieving all remote packages, this may take a while...")
        localPackageIndex = self.getDiskIndex()
        try:
            self.log('Importing progressbar')
            from progressbar import progressbar
            self.log('Create package asset directory')
            self.data.createConfigDirectory('packages')
            self.cli.clear()
            #print("Fetching packages...")
            for package in progressbar(localPackageIndex):
                print(f"\nFetching {package} ({ localPackageIndex[package]['uri'] })")
                self.getPackageLoopCall(localPackageIndex, package)
                self.cli.clear()
            print("Finished fetching packages from remote")

        except (ModuleNotFoundError,ImportError):
            self.log("Missing progressbar library")
            self.log('Create package asset directory')
            self.data.createConfigDirectory('packages')
            self.cli.clear()
            x=0
            for package in localPackageIndex:
                print(f'Downloading package data\n {x}/{len(localPackageIndex)} - {str(round((x/len(localPackageIndex))*100,1))+"%"} ')
                print(f"\nFetching {package} ({ localPackageIndex[package]['uri'] })")
                self.getPackageLoopCall(localPackageIndex, package)
                self.cli.clear()
                x+=1
            print("Finished fetching packages from remote")

        except Exception as e:
            self.log(f"Something went wrong, the error returned was: {e}")
            print("Something went wrong, try clearing the package cache first then trying again with 'spm fetch --delete' and 'spm fetch --save --delete'")

    def getPackageLoopCall(self, localPackageIndex, package):#Extracted this- less duplicate code
        self.log('Asking API for package data...')
        packageData, apiResponse = self.api.getPackage(localPackageIndex[package]["uuid"])
        if apiResponse == 200:
            self.log('Got the following to write to the disk '+str(packageData))
            self.log(f'Writing package to disk in ~/.spm/packages/{package}')
            self.data.createConfigFile(f'packages/{package}',self.json.dumps(str(packageData)))
        elif apiResponse == 403: self.log('The package is private')
        else: self.log('Server did not reply with ok')
        #input("Press ENTER to iterrate")

    def fetchPackageData(self, package,appendBaseUri=True):
        self.log('Asking API for package data...')
        if appendBaseUri: packageData, apiResponse = self.api.getPackage(self.config.getConfig()['baseurl']+'/'+package) #e.g. "spm install breisbrenny/SomePackage"
        else: packageData, apiResponse = self.api.getPackage('/'+package) #e.g. "spm install breisbrenny/SomePackage"
        if apiResponse == 200:
            self.log('Got the following to write to the disk '+str(packageData))
            
            self.log('Writing package to disk')
            self.data.createConfigFile(f'packages/{package}',self.json.dumps(str(packageData)))#Important we turn the content from dict into json or we wont be able to decode in the future
            return (True,packageData)
        elif apiResponse == 403: self.log('The package is private'); return (False, {})
        else: self.log('Server did not reply with ok'); return (False, {})
        #input("Press ENTER to iterrate")self.cli.clear()

# ---------------------------------------------------------------------------- #
#                               package management                             #
# ---------------------------------------------------------------------------- #

# --------------- action routine for install, remove and update -------------- #
    def actionRoutine(self,packageData,where,thisSystem,action=['Installing','Installed']):
        step = 1; steps = len(packageData[where][thisSystem])
        for i in packageData[where][thisSystem]:
            #info for end-user
            self.cli.clear()
            print(f"{action[0]} {packageData['name']} v{packageData['version']}...")
            print(f"--------------------------------\nOn step {str(step)} of {str(steps)}  -  {int(round((step-1/steps)*100,1))}% complete\n--------------------------------\nStep: {i['name']}\n--------------------------------")
            self.log('Current step: '+str(i))
            #time.sleep(1)

            #Is step a command
            if i['method'] == 'command':
                commandToRun = i['command']
                print("Executing: "+str(commandToRun))
                self.os.system(commandToRun)
                if exitCode != 0: 
                    raise self.SPMCLIExceptions.FailedCommandExecution(command=commandToRun)

            #Is step a script
            if i['method'] == 'script':
                # Script filename is at packageData[ content[ scripts[script] ][1] ]

                #Get the filename of the script we want
                scriptToRun=packageData["content"][int(packageData["scripts"][i["script"]])]["filename"]
                self.log('Attempting to identify the script to execute ' + str(scriptToRun))

                #Get the temporary path to the script
                temporaryPath = self.detection.getPath('$CONFIG')+'temporary/content/'

                #Determine how we should execute the script
                if self.detection.platformname() == 'Darwin': 'sh ' + temporaryPath + scriptToRun
                elif 'lin' in thisSystem: scriptToRun = 'bash ' + temporaryPath + scriptToRun
                elif 'win' in thisSystem: scriptToRun = './' +  temporaryPath + scriptToRun

                print("Executing "+str(scriptToRun))
                exitCode = self.os.system(scriptToRun)
                if exitCode != 0:
                    raise self.SPMCLIExceptions.FailedScriptExecution(filename=temporaryPath)


        self.cli.clear()
        print(f"{action[1]} {packageData['name']} v{packageData['version']}...")
        print(f"--------------------------------\nCompleted !    -  100% complete\n--------------------------------")


# -------------------------- package integrity check ------------------------- #
    def checkPackageContentIntegrity(self,packageData):
        step = 1; steps = len(packageData["content"])
        for i in packageData["content"]:
            self.cli.clear()
            print(f"Checking integrity of {packageData['name']} v{packageData['version']}...")
            print(f"--------------------------------\nOn step {str(step)} of {str(steps)}  -  {int(round((step-1/steps)*100,1))}% complete\n--------------------------------\nFile: {i['filename']}\n--------------------------------")
            self.log('Current step: '+str(i))
            print(f"The asset {i['filename']} was downloaded from {i['address']} and is expected to have a sha256 hash of {packageData['checksum'][i['address']]}")
            print("\nGenerating the sha256sum...")
            checksum=self.etc.sha256sum(packageData['checksum'][i['address']],self.detection.getPath('$CONFIG')+'temporary/content/'+i['filename'])
            if checksum == True: print(f"The downloaded file ({i['filename']}) has a valid checksum")
            else: raise self.SPMCLIExceptions.IntegrityError(i['filename'])

# ------------------------------ get system data ----------------------------- #
    def canInstall(self,packageData):
            #Operating system flag
            thisSystem = ''
            if self.detection.platform() == 'nt': thisSystem+='win'
            elif self.detection.platform() == 'posix': thisSystem+='lin'

            #Check CPU architecture
            import struct
            thisSystem+=str(struct.calcsize("P") * 8)

            if packageData['platform'] != 'Darwin':
                if thisSystem != 'any':
                    if thisSystem != packageData['platform']:
                        if struct.calcsize("P") * 8 == 32:
                            print("WARN: Check you don't have 32-bit python installed on a 64-bit operating system!")
                        print(f"ERROR: This package needs {packageData['platform']}, your system is {thisSystem}\n")
                        raise self.SPMCLIExceptions.UnsupportedOperatingSystem
            else:
                print("This package is for MacOS, checking it's compatible")
                if self.detection.platformname() != 'Darwin':
                    print(f"ERROR: This package needs {packageData['platform']}, your system is {thisSystem}\n")
                    raise self.SPMCLIExceptions.UnsupportedOperatingSystem
            
            return thisSystem

# -------------------- download content from package data -------------------- #
    def downloadedContent(self,packageData):
            #Create all required directories to store data during installation
            self.log("Creating temporary dirs in config dir")
            try: self.data.deleteConfigDirectory('temporary'); self.log('Temporary directory exists, deleted it')#make sure temporary directory doesnt exist
            except: self.log("Temporary directory doesn't exist, good to go")
            self.data.createConfigDirectory('temporary')
            self.data.createConfigDirectory('temporary/content')
            #self.data.createConfigDirectory('temporary/other')
            downloadedContent = []
            try:
                from progressbar import progressbar
                for i in progressbar(packageData['content']):
                    print(f"\nDownloading: {i}")#loop through content and download each one
                    downloadResult = self.data.downloadFile(i['address'],self.detection.getPath('$CONFIG')+'temporary/content',i['filename'])
                    if downloadResult[0] == False:
                        print("Failed to download "+str(i))
                        raise self.SPMCLIExceptions.FailedContentDownload
                    downloadedContent.append(str(downloadResult[1]))
                    self.cli.clear()

            except (ModuleNotFoundError, ImportError):
                self.log('progressbar2 not installed')
                for i in range(len(packageData['content'])):#same as above with custom progress info since we cant use progressbar2
                    print(f'Downloading package data\n {i}/{packageData["content"]} - {str(round((i/len(packageData["content"]))*100,1))+"%"} ')
                    print(F"Downloading: {packageData['content'][i]['address']}")
                    downloadResult = self.data.downloadFile(packageData['content'][i]['address'],self.detection.getPath('$CONFIG')+'temporary/content',packageData['content'][i]['filename'])
                    if downloadResult[0] == False:
                        print("Failed to download "+str(packageData['content'][i]))
                        raise self.SPMCLIExceptions.FailedContentDownload
                    downloadedContent.append(str(downloadResult[1]))
                    self.cli.clear()

            print("Finished downloading assets")#we've passed, all gucci time to continue

    def downloadPackage(self, package):
        try:

# ------------------------- parse package information ------------------------ #
            packageuuid = f"{package.split('/')[1]}.{package.split('/')[0]}"#Make the package uuid
            
            print("Checking package status...")
            self.log('Checking if package is already downloaded')
            self.log(f"Searching for: {self.detection.getPath('$CONFIG')+'packages/'+packageuuid}")

            if self.os.path.exists(self.detection.getPath('$CONFIG')+'packages/'+packageuuid):#Check if the package data is already downloaded
                print("Found package in cache!")
                packageData = self.data.readConfigFile('packages/'+packageuuid)
            else:#call the function inside this module to download the package data
                print("Pacakge doesn't exist locally, going to fetch it")
                passed, packageData = self.fetchPackageData(package,False)
                if passed:
                    self.data.readConfigFile(f"packages/{packageData['uuid']}")
                else:
                    print("The package you requested doesn't exist or isn't publicly available")
                    return

# ------------------------- got data, load and verify ------------------------ #
            self.log("Managed to retrieve required data, going to go ahead and attempt to install it")
            self.log(f"Package contents: {str(packageData)}")
            self.log("Ensure that data is dict- Converting package data from str to dict")
            #inform the user that we have the data, check the data is a dict and not a str because i think i have some inconsistent use of json.*, i'll sort it later
            try: packageData=self.json.loads(packageData.replace("'",'"'))
            except AttributeError: self.log("Data is already dict!")
            print(f"Getting ready to install {packageData['name']} version {packageData['version']} by {packageData['author']}...")

            # Time to install!! :)

            print("Downloading files and archives for package...")

# ------------------------- download package content ------------------------- #
            self.downloadedContent(packageData)

# ----------------- check if system may install this package ----------------- #
            thisSystem = self.canInstall(packageData)

            self.log("Determined user is running "+thisSystem)


# --------------------------- check asset integrity -------------------------- #
            self.checkPackageContentIntegrity(packageData)
# -------------------------------- change cwd -------------------------------- #
            #Ensure we wont accidentally write into the cwd by changing it
            #we'll move to the temp dir
            self.os.chdir(self.detection.getPath('$CONFIG')+'temporary/')

# ---------------------------- begin installation ---------------------------- #
            self.log(f'Steps:\n{self.json.dumps(packageData["install"],indent=4)}')
            if self.verbose == True: self.log(f"Package data: {self.json.dumps(packageData,indent=4)}");self.log(f'Steps for your system (there are {len(packageData["install"][thisSystem])}):\n{self.json.dumps(packageData["install"][thisSystem],indent=4)}')#; input("[VERBOSE] Press ENTER to continue")
            # Install step loop
            print("Installing...")
            #import time
            self.actionRoutine(packageData,'install',thisSystem)
            print("Cleaning")


# ---------------------------- all done, clean up ---------------------------- #
            self.data.deleteConfigDirectory('temporary')#finished the installation, delete the temporary directory


        except IndexError: raise self.SPMCLIExceptions.BadPackageName
        except Exception as e: raise self.SPMCLIExceptions.FailedInstallation(e)
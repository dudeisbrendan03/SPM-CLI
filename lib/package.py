"""
SPM-API

package tools library


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
        self.json = etc.getJson()
        self.api = api(verbose)
        self.detection = detection(verbose)
        self.log = cli.verbose

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
        packageData, apiResponse = self.api.getPackage(localPackageIndex[package]["apiIdentifier"])
        if apiResponse == 200:
            self.log('Got the following to write to the disk '+str(packageData))
            self.log('Writing package to disk')
            self.data.createConfigFile(f'packages/{package}',self.json.dumps(str(packageData)))
        elif apiResponse == 403: self.log('The package is private')
        else: self.log('Server did not reply with ok')
        #input("Press ENTER to iterrate")

    def fetchPackageData(self, package):
        self.log('Asking API for package data...')
        packageData, apiResponse = self.api.getPackage(self.config.getConfig()['baseurl']+'/'+package) #e.g. "spm install breisbrenny/SomePackage"
        if apiResponse == 200:
            self.log('Got the following to write to the disk '+str(packageData))
            
            self.log('Writing package to disk')
            self.data.createConfigFile(f'packages/{package}',self.json.dumps(str(packageData)))#Important we turn the content from dict into json or we wont be able to decode in the future
            return (True,packageData)
        elif apiResponse == 403: self.log('The package is private'); return (False, {})
        else: self.log('Server did not reply with ok'); return (False, {})
        #input("Press ENTER to iterrate")self.cli.clear()

    def downloadPackage(self, package):
        try:
            packageuuid = f"{package.split('/')[1]}.{package.split('/')[0]}"#Make the package uuid
            
            print("Checking package status...")
            self.log('Checking if package is already downloaded')
            self.log(f"Searching for: {self.detection.getPath('$CONFIG')+'packages/'+packageuuid}")

            if self.os.path.exists(self.detection.getPath('$CONFIG')+'packages/'+packageuuid):#Check if the package data is already downloaded
                print("Found package in cache!")
                packageData = self.data.readConfigFile('packages/'+packageuuid)
            else:#call the function inside this module to download the package data
                print("Pacakge doesn't exist locally, going to fetch it")
                passed, packageData = self.fetchPackageData(package)
                if passed:
                    self.data.readConfigFile(f"packages/{packageData['uuid']}")
                else:
                    print("The package you requested doesn't exist or isn't publicly available")
                    return

            self.log("Managed to retrieve required data, going to go ahead and attempt to install it")
            self.log(f"Package contents: {str(packageData)}")
            self.log("Ensure that data is dict- Converting package data from str to dict")
            #inform the user that we have the data, check the data is a dict and not a str because i think i have some inconsistent use of json.*, i'll sort it later
            packageData=self.json.loads(packageData.replace("'",'"'))
            print(f"Getting ready to install {packageData['name']} version {packageData['version']} by {packageData['author']}...")

            # Time to install!! :)

            print("Downloading files and archives for package...")

            #Create all required directories to store data during installation
            self.log("Creating temporary dirs in config dir")
            try: self.data.deleteConfigDirectory('temporary'); self.log('Temporary directory exists, deleted it')#make sure temporary directory doesnt exist
            except: self.log("Temporary directory doesn't exist, good to go")
            self.data.createConfigDirectory('temporary')
            self.data.createConfigDirectory('temporary/content')
            self.data.createConfigDirectory('temporary/scripts')
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
                for i in len(packageData['content']):#same as above with custom progress info since we cant use progressbar2
                    print(f'Downloading package data\n {i}/{packageData["content"]} - {str(round((i/len(packageData["content"]))*100,1))+"%"} ')
                    print(F"Downloading: {packageData['content'][i]['address']}")
                    downloadResult = self.data.downloadFile(packageData['content'][i]['address'],self.detection.getPath('$CONFIG')+'temporary/content',packageData['content'][i]['filename'])
                    if downloadResult[0] == False:
                        print("Failed to download "+str(packageData['content'][i]))
                        raise self.SPMCLIExceptions.FailedContentDownload
                    downloadedContent.append(str(downloadResult[1]))
                    self.cli.clear()

            print("Finished downloading assets")#we've passed, all gucci time to continue

            self.log(f'Steps: {self.json.stringify(packageData["install"])}')
            
            #self.data.deleteConfigDirectory('temporary')#finished the installation, delete the temporary directory


        except IndexError: raise self.SPMCLIExceptions.BadPackageName
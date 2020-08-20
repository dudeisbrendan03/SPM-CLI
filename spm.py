#/usr/bin/python3
import json
import sys
import time

with open('shipping.json') as f:
  shippingData = json.load(f)


if '-v' in sys.argv: #Version info
    print(f"""S* Package Manager
    Version:    {shippingData['version']}
    Author:     {shippingData['release']}
    Repository: {shippingData['repository']}
    """)

if '-b' in sys.argv: #Build local package index
    print("""WARNING!
    Rebuilding the package index will allow the installation of packages if it doesn't exist, but overwriting an existing package index will remove your ability to manage and uninstall packages installed and controller by spm""")
    if input("Continue (y/n): ") == 'y':
        print("Rebuilding the index.")
        exampleIndex = {"indexDate": time.time(),"indexGenerationVersion": shippingData['release'],"packages": []}
        with open('primary.index', 'w') as f:
            json.dump(exampleIndex, f)


if '-u' in sys.argv: #Download entire remote index
    print()
# repo.py #
import json
import os

MANIFESTFILE = os.path.join(os.path.dirname(__file__),"manifest.json")

class Repo:
    def __init__(self):
        self.packages = {}
        self.loadManifest()

    def loadManifest(self):
        if os.path.exists(MANIFESTFILE):
            with open(MANIFESTFILE,"r") as f:
                self.packages = json.load(f)
        else:
            self.packages = {}

    def saveManifest(self):
        with open(MANIFESTFILE,"w") as f:
            json.dump(self.packages,f,indent=4)

    def addPackages(self,name,ver,desc=""):
        self.packages[name]={
            "version": ver,
            "description": desc
        }
        self.saveManifest()
        print(f"[Repo:repo.py] package: '{name}' version: '{ver}' added to repo.")

    def updatePackage(self,name,ver):
        if name in self.packages:
            self.packages[name]["version"] = ver
            self.saveManifest()
            print(f"[Repo:repo.py] package '{name}' updated to version: '{ver}'.")
        else:
            print(f"[Repo:repo.py] package '{name}' not found. error: {hex(len('Repo_pkg_not_found_err'))}")

    def listPackages(self):
        print("[Repo:repo.py] available packages:")
        for name,data in self.packages.items():
            print(f" - {name} version: {data['version']}: {data['description']}")

    def getVer(self,name):
        return self.packages.get(name,{}).get("version")

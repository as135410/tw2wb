import config
import json
import os
class Data:
    def __init__(self):
        self.dbfile = config.getConfig("other", "dbfile")
        self.db = {}
        self._loadDb()

    def _loadDb(self):
        if not os.path.exists(self.dbfile):
            return

        with open(self.dbfile, "r") as f:
            j = f.read()
            f.close()

        if len(j) == 0:
            return

        self.db = json.loads(j)
            
    def _write2local(self):
        if len(self.db) == 0:
            return

        with open(self.dbfile, "w") as f:
            j = json.dumps(self.db)
            f.write(j)
            f.close()

    def downloadPictur(self, pic):
        return

    def exist(self, key):
        return key in self.db.keys()

    def insert(self, key):
        self.db[key] = True
        


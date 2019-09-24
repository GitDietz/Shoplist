import datetime as d
import csv,os

class logger:
    def __init__(self,fname):
        self.filename = fname
        if not os.path.exists(self.filename):
            with open(self.filename,'w'):pass
        self.add_log('Logger initialised')

    def add_log(self,log_item):
        with open(self.filename,'a') as f:
            f.write(str(d.datetime.now()) + ', ' + log_item + '\n')

#newlog = logger('myLog.txt')

#newlog.add_log('Some new stuff')

    @classmethod
    def new_log(cls,fname):
        return cls(fname)

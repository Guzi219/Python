# -*- coding:utf-8 -*_
import ConfigParser
import os


class INIFILE:
    """
    a class which can process *.ini file
    with read and write function.
    """

    def __init__(self, fileName):
        self.fileName = fileName
        self.initflag = False
        self.cfg = None
        self.readhandle = None
        self.writehandle = None
        self.Init()

    # must write something if you set is_write to true. otherwise your file become empty.
    def Init(self):
        self.cfg = ConfigParser.ConfigParser()
        try:
            self.readhandle = open(self.fileName, 'r')
            self.cfg.readfp(self.readhandle)
            self.writehandle = open(self.fileName, 'r+')
            self.initflag = True
        except Exception, e:
            self.initflag = False
            print e
            os._exit(0)
        return self.initflag

    # close the file
    def UnInit(self):
        if self.initflag:
            self.readhandle.close()
            self.writehandle.close()

    def GetValue(self, Section, Key, Default='0'):
        try:
            value = self.cfg.get(Section, Key)
        except Exception, e:
            # print e
            value = Default
        return value

    def SetValue(self, Section, Key, Value):
        if not self.cfg.has_section(Section):
            print 'Section [%s] does not exists. add it first' % (Section)
            self.cfg.add_section(Section)
        self.cfg.set(Section, Key, Value)
        return self

    def EndWrite(self):
        self.cfg.write(self.writehandle)
        return self


# file = INIFILE('demo.ini')
# num = file.GetValue('Main', 'totalpage', '000')
# print num
# if file.initflag:
#     file.SetValue('Main', 'totalpage', '805').SetValue('Sum', 'loadpage', '855').EndWrite().UnInit()
#     print file.GetValue('Main', 'TotalPage', '000')

# -*- coding:utf-8 -*_
import ConfigParser, sys
class INIFILE:
    """
    a class which can process *.ini file
    with read and write function.
    """
    def __init__(self, fileName):
        self.fileName = fileName
        # print self.fileName
        self.initflag = False
        self.cfg = None
        self.readhandle = None
        self.writehandle = None
        self.is_read = False
        self.is_write = False

    #is_read :is read enable? is_write: is write enable?
    #must write something if you set is_write to true. otherwise your file become empty.
    def Init(self, is_read, is_write):
        self.cfg = ConfigParser.ConfigParser()
        try:
            if is_read:
                self.is_read = True
                self.readhandle = open(self.fileName, 'r')
                self.cfg.readfp(self.readhandle)

            if  is_write:
                self.is_write = True
                self.writehandle =  open(self.fileName, 'w')

            self.initflag = True
        except Exception, e:
            self.initflag = False
            print e
        return self.initflag

    #close the file
    def UnInit(self):
        if self.initflag:
            if self.is_read:
                self.readhandle.close()
                #print '================close the read handle================'
            if self.is_write:
                self.writehandle.close()
                #print '================close the write handle================'

    def GetValue(self, Section, Key, Default = '0'):
        try:
            value = self.cfg.get(Section, Key)
        except Exception, e:
            #print e
            value = Default
        return value

    def SetValue(self, Section, Key, Value):
        if not self.is_write:
            print 'can not SetValue, switch the write function to true first.'
            return
        if not self.cfg.has_section(Section):
            print 'Section [%s] does not exists. Going to add it first' %(Section)
            self.cfg.add_section(Section)
        self.cfg.set(Section, Key, Value)
        self.cfg.write(self.writehandle)


# file = INIFILE('totalpage.ini')
# file.Init()
# num = file.GetValue('Main', 'totalpage', '')
# print num
#
# file.SetValue('Main', 'totalpage', '805')
# print file.GetValue('Main', 'TotalPage', '0')
#
# file.SetValue('DEMO', 'whoami', 'Admin')
# print file.GetValue('DEMO', 'whoami', 'Admin')
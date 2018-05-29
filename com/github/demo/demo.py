# -*- coding: utf-8 -*-

"""
替换掉语料中的xml标签
"""
# 输入文件
filePath = ur'F:\浪潮\上海检察机关文书智能检索系统\语义分析课题\news_tensite_xml.smarty\news_tensite_xml.smarty.dat'
# 输出文件
outFilePath = ur'F:\浪潮\上海检察机关文书智能检索系统\语义分析课题\news_tensite_xml.smarty\news_tensite_xml.smarty.txt'
with open(outFilePath, 'w') as out:
    with open(filePath, 'r') as infile:
        index = 1;
        for line in infile:
            if (line.__contains__('<contenttitle>')):
                line = line.decode('gbk', errors='ignore')
                line = line.replace('<contenttitle>', '').replace('</contenttitle>', '')
                print line
                out.write(line.encode('utf-8', errors='ignore'))
            if (line.__contains__('<content>')):
                line = line.decode('gbk', errors='ignore')
                line = line.replace('<content>', '').replace('</content>', '')
                print line
                out.write(line.encode('utf-8', errors='ignore'))

            index = index + 1
        print 'process %s line' % (index)

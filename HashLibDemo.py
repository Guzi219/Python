# -*- coding: utf8 -*-
import hashlib
import os
import sys
import shutil

# print (hashlib.md5('123').hexdigest())
# print (hashlib.md5('123.').hexdigest())
#
# img_file1 = open('tmp/20170108_p_1_01_.jpg').read()
# img_file2 = open('tmp/20170109_p_1_09_.jpg').read()
#
# hash_img1 = hashlib.md5(img_file1).hexdigest()
# hash_img2 = hashlib.md5(img_file2).hexdigest()
#
# print hash_img1
# print hash_img2

# print os.getcwd()
# print os.listdir(os.getcwd())

#list all file in dir
if os.path.exists('tmp'):
    listfile = os.listdir('tmp')
#store the img_hash as key, the filepath as value..
hash_imgs = {}

if 'listfile' in locals().keys():
    for file in listfile:
        #print type(file) the type of 'file' is str.
        # print 'now is file : %s' %(file)
        f = open('tmp/'+file,'rb')
        hash_img = hashlib.md5(f.read()).hexdigest() #md5 this file.
        f.close()
        # print type(hash_img)
        # print hash_img
        if not hash_imgs.has_key(hash_img):
            hash_imgs[hash_img] = file
        else:
            print '--------------'
            print '%s already exsits.' %(file) #the current file to be record.
            print hash_imgs.get(hash_img) #the file already record.
            print '--------------'
            #copy the repeating file to 'repeat'
            shutil.copyfile('tmp/'+file,'repeat/'+file)
            shutil.copyfile('tmp/'+hash_imgs.get(hash_img),'repeat/'+hash_imgs.get(hash_img))
    # print str(hash_imgs)

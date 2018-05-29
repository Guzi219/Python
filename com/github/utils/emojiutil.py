# -*- coding: utf-8 -*-
#remove emoji charset
import re
emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)
#something wrong
def remove_emoji(text):
    return emoji_pattern.sub(r'', text)

def filter_emoji_nouse(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
        print 'filter_emoji now'
    except Exception, e:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        print e
    return co.sub(restr, desstr)

def remove_emoji(desstr,restr=''):
    try:
        highpoints = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        print 'remove emoji now.'
    except re.error:
        print 'failed to remove emoji.'
        highpoints = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        # mytext = u'<some string containing 4-byte chars>'
        desstr = highpoints.sub(u'\u25FD', desstr)
    return desstr

def remove_define_emoji(desstr,restr=''):
    try:
         co = re.compile(u'&#x1f60c;')
         print 'remove define emoji only.'
    except Exception, e:
        print 'error ===='
        print e
    return co.sub(restr,desstr)
#!/usr/bin/env python
#
# Copyright (C) 2015, Red Hat Inc.
#
# Search a mailman archive argv[1] and extract all emails which match regex
# specified by argv[2], storing the results in the file specified by argv[3]
# (if one exists)

import gzip
import StringIO
import urllib2
import re
import sys
import mailbox
import os
import datetime

class streammedMbox(mailbox.mbox):
    def __init__(self, stringOfBytes):
        self._file = StringIO.StringIO(stringOfBytes)
        self._toc = None
        self._next_key = 0
        self._pending = False
        self._locked = False
        self._file_length = None
        self._factory = None
        self._path='/dev/null'
        self._message_factory = mailbox.mboxMessage

def webdatetime(txt):
    if txt is None or txt == '':
        return datetime.now()
    
    try:
        txt_split = txt.split(" ")
        txt_split = txt_split[:-1]
        checktxt = ' '.join(txt_split)
        return datetime.datetime.strptime(checktxt, '%a, %d %b %Y %H:%M:%S')
    except ValueError, v:
        print "Error converting %s" % txt
        raise v
        
def cached_url_open(url):
    HOMEDIR=os.path.expanduser('~')
    fs_converted_url = re.sub('[/:@]*', '_', url)
    if not os.path.exists(HOMEDIR + '/.sma_cache'):
        os.makedirs(HOMEDIR + '/.sma_cache')
    if os.path.exists(HOMEDIR + '/.sma_cache/' + fs_converted_url):
        request = urllib2.Request(url)
        request.get_method = lambda : 'HEAD'
        response = urllib2.urlopen(request)
        headers = response.info()
        webdate = webdatetime(headers['last-modified'])
        filedate = datetime.datetime.fromtimestamp(os.path.getmtime(HOMEDIR + '/.sma_cache/' + fs_converted_url))
        if filedate >= webdate:
            fileop = open(HOMEDIR + '/.sma_cache/' + fs_converted_url, 'r')
            return fileop.read()
        print "%s: webdate: %s vs filedate: %s" % (url, str(webdate), str(filedate))
        
    response = urllib2.urlopen(url)
    result = response.read()

    fileop = open(HOMEDIR + '/.sma_cache/' + fs_converted_url, 'w')
    fileop.write(result)
    
    return result

def mailman_archives(MailmanUrl):
    html = cached_url_open(MailmanUrl)
    grp = re.findall('href="[^"]+.txt.gz"', html)

    archives = []
    
    for archive in grp:
        archive1 = re.sub(r'href=', '', archive)
        app = re.sub(r'"', '', archive1)
        archives.append(app)

    return archives

def get_mailman_mailbox_from_archive(ArchiveUrl):
    print "Scanning %s" % ArchiveUrl
    zipped = cached_url_open(ArchiveUrl)
    unzipped = gzip.GzipFile(fileobj=StringIO.StringIO(zipped))

    return streammedMbox(unzipped.read())

def part_regex_body(msg, regexForBody):
    if msg.is_multipart():
        for part in msg.get_payload():
            if part_regex_body(part, regexForBody):
                return True
        return False
    else:
        result = re.findall(regexForBody, msg.get_payload())
        if result is not None and len(result) > 0:
            return True
    return False

def mbox_messages_matching_or(ArchiveUrl, regexForBody=None, From=None, To=None, Date=None):
    mbx = get_mailman_mailbox_from_archive(ArchiveUrl)
    matchingMsgs = []
    for msgkey in mbx.iterkeys():
        matched = False
        msg = mbx[msgkey]
        if From is not None and From == msg['from']:
            matched = True
        if To is not None and To == msg['to']:
            matched = True
        if regexForBody is not None:
            if part_regex_body(msg, regexForBody) is True:
                matched = True

        if matched:
            matchingMsgs.append(msg)

    return matchingMsgs

if __name__ == "__main__":

    mbx = None
    
    if len(sys.argv) > 3:
        mbox_file = sys.argv[3]
        mbx = mailbox.mbox(mbox_file)

    for arch in mailman_archives(sys.argv[1]):
        newmsgs = mbox_messages_matching_or(sys.argv[1] + arch, sys.argv[2])
        for message in newmsgs:
            if mbx is not None: mbx.add(message)
            print "%s (%s) %s" % (message['from'], message['subject'], message['date'])

    print "results written to %s" % (mbox_file)

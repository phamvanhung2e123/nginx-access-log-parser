__author__ = "Richard O'Dwyer"
__email__ = "richard@richard.do"
__license__ = "None"

import re

def process_log(log):
    requests = get_requests(log)
    files = get_files(requests)
    totals = file_occur(files)
    return totals

def get_requests(f):
    log_line = f.read()
    pat = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s' #IP address
           '\[(.+)\]\s' #datetime
           '"GET\s(.+)\s\w+/.+"\s' #requested file
           '(\d+)\s' #status
           '(\d+)' #time response
           '\s"(.+)"\s' #referrer
           '"(.+)"' #user agent
        )
    requests = find(pat, log_line, None)
    return requests

def find(pat, text, match_item):
    match = re.findall(pat, text)
    if match:
        return match
    else:
        return False

def get_files(requests):
    #get requested files with req
    requested_files = []
    count=0
    count1000=0
    count2000=0
    count3000=0
    count5000=0
    for req in requests:
        #req[2] for req file match, change to
        #data you want to count totals
        requested_files.append(req[2])
        count +=1
        if(int(req[4])>1000):
            count1000 +=1
        if(int(req[4])>2000):
            count2000 +=1
        if(int(req[4])>3000):
            count3000 +=1
        if(int(req[4])>5000):
            print req
            count5000 +=1
    print "Count " + str(count) + "\n"
    print "Count 1000 " + str(count1000) + "\n"
    print "Count 2000  " + str(count2000) + "\n"
    print "Count 3000 " + str(count3000) + "\n"
    print "Count 5000 " + str(count5000) + "\n"

    return requested_files

def file_occur(files):
    #file occurrences in requested files
    d = {}
    for file in files:
        d[file] = d.get(file,0)+1
    return d

if __name__ == '__main__':

    #nginx access log, standard format
    log_file = open('../nginx/access.log', 'r')


    #return dict of files and total requests
    process_log(log_file)
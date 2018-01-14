#!/usr/bin/python

import re
import sys

# Mapper.py output
# date<TAB>sender<TAB>receivers<TAB>body<TAB>message_id<TAB>message_uri<TAB>count

regex1 = r'(\b(?=\w*[@\.])[\w\-\.@]+\b)'  # get email adressess (contain one @ and one .)
regex2 = r'(<.*>)'  # get everything between the brackets
regex3 = r'\"(.*)\"'


def get_first_match(pattern, x):
    match = re.search(pattern, x)
    if match:
        return match.group(0)
    else:
        return re.sub(r'\"', '', x)


def func(x):
    # ["allen, phillip"] -> ["phillip allen"]
    g = lambda x: x.split(',')
    namelastname = g(x)[1].strip() + " " + g(x)[0].strip() if ',' in x and '""' in x else x
    return re.sub(r"\"|\'", '', namelastname)


id_count = 1
key = None
sender1 = None
sender2 = None
recievers = []
date = None
subject = None
body = ''
newkey = None
message_id = None
message_uri = None
in_body = False
previous_line = 0

# file = open("data/emails.txt", 'r')
# for line in file:

for line in sys.stdin:
    line = line.strip()

    if line.startswith("Message-URI:"):
        previous_line = 1
        newkey = line.strip("Message-URI:").strip()

    elif line.startswith("Message-ID: "):
        message_id = line.strip("Message-ID:").strip()
        message_id = re.sub(r'<|>', "", message_id)

    elif line.startswith("Date: ") and previous_line > 0:
        date = re.sub(r"Date: ", "", line).strip()

    elif line.startswith("From:") and not in_body:
        sender = re.split(r'From:', line)[1].strip()
        sender2 = get_first_match(regex1, sender)
        sender2 = re.sub(regex2, '', sender2)
        if len(sender2) == 1: sender2 = None
        # sender = re.sub(regex1 + '|' + regex2, '', sender)
        sender1 = get_first_match(regex3, sender)
        if '@' not in sender1: sender1 = re.sub(r'\.|\"', '', sender1)

    elif sender1 is None and line.startswith("X-From:") and not in_body:
        sender = re.split(r'X-From:', line)[1].strip()
        sender2 = get_first_match(regex1, sender)
        sender2 = re.sub(regex2, '', sender2)
        if len(sender2) == 1: sender2 = None
        sender = re.sub(regex1 + '|' + regex2, '', sender)
        sender1 = get_first_match(regex3, sender)
        if '@' not in sender1: sender1 = re.sub(r'\.|\"', '', sender1)

    elif line.startswith("To:") and not in_body:
        recievers = re.sub("To:", "", line).strip()
        recievers = [x.strip().split('<')[0] for x in re.split(r'>,', recievers)]
        if len(recievers) > 15:
            continue
        else:
            recievers = list(map(func, recievers))

    elif len(recievers) == 0 and line.startswith("X-To:") and not in_body:
        recievers = re.sub("X-To:", "", line).strip()
        recievers = [x.strip().split('<')[0] for x in re.split(r'>,', recievers)]
        if len(recievers) > 15:
            continue
        else:
            recievers = list(map(func, recievers))

    elif line.startswith('X-FileName: '):
        in_body = True
        message_uri = newkey

    elif in_body and 'Message-URI:' not in line and 'X-FileName:' not in line and 'Message-ID:' not in line:
        body += " " + re.sub(" ", " ", line).strip()

    if not key:
        key = newkey

    if key != newkey and date is not None and sender1 is not None and len(
            recievers) > 0 and message_uri is not None and body != '':
        print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (str(date), sender1, ",".join(recievers), body, message_id, message_uri, id_count)

        id_count += 1
        key = newkey
        sender = None
        recievers = []
        date = None
        subject = None
        body = ''
        in_body = False
        message_uri = None

if key != None and date is not None and sender1 is not None and len(
        recievers) > 0 and message_uri is not None and body != '':
    print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (str(date), sender1, ",".join(recievers), body, message_id, message_uri, id_count)
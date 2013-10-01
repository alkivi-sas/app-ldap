#!/usr/bin/python
import sys
import json
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append('/')

import cgi
import cgitb
cgitb.enable()

from alkivi.common import logger

# Define the global logger
logger.Logger.instance(
        min_log_level_to_mail  = logger.WARNING,
        min_log_level_to_save  = logger.DEBUG_DEBUG,
        min_log_level_to_print = logger.LOG,
        filename='/var/log/alkivi/ldap.log',
        emails=['root@localhost'])

from alkivi.common.helpers import LdapClient
from alkivi.exceptions import *

# Get base from /etc/ldap/ldap.conf
#cat /etc/ldap/ldap.conf | grep BASE | sed 's/BASE //'
file = '/etc/ldap/ldap.conf'
import re
rx = re.compile('^BASE (.*?)$')
for line in open(file).readlines():
    m = rx.search(line)
    if(m):
        basedn, = m.groups()
        break

if(not(basedn)):
    logger.warn('Unable to find basedn in /etc/ldap/ldap.conf')
    raise
else:
    basedn='ou=people,'+basedn


def main():

    #
    # Params
    #
    arguments = cgi.FieldStorage()
    action    = arguments['action'].value

    #
    # Get Local PCA data
    #
    logger.debug('action to do: %s' % (action))

    if(action=='updatePassword'):
        response = updatePassword(arguments)
    else:
        raise InvalidParameter('Action %s is not correct' % action)


    print "Content-type: application/json"
    print
    print json.JSONEncoder().encode(response)

def updatePassword(arg):

    for key in ['user', 'oldPassword', 'newPassword']:
        if(not(arg[key].value)):
            raise MissingParameter('Parameter %s is missing' % key)

    user        = arg['user'].value
    oldPassword = arg['oldPassword'].value
    newPassword = arg['newPassword'].value

    Client = LdapClient(server='ldaps://localhost', basedn=basedn)
    Client.updatePassword(user, oldPassword, newPassword)

    response = { 'status': 100 }

    return response

def returnError(message):
    response = { 'status': 200, 'msg': message }
    print "Content-type: application/json"
    print
    print json.JSONEncoder().encode(response)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
        returnError(str(e))

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Moodle Webservice
#    Copyright (c) 2011 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Raimon Esteve <resteve@zikzakmedia.com>
#                       Jesus Martín <jmartin@zikzakmedia.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from config import *
from moodle import MDL

mdl = MDL()
# xmlrpc Connection
print mdl.conn_xmlrpc(server)

"""
Create new courses
"""
courses = [{
    'shortname': 'test6', # shortname must be unique
    'fullname': 'Test 6',
    'categoryid': 1,
    #'visible': 1,
    'id': 2,
    #'maxbytes': 2097152,
    #'showreports': 0,
    #'startdate': 1314396000,
    #'defaultgroupingid': 0,
    #'summaryformat': 1,
    #'completionstartonenrol': 0,
    #'groupmode': 0,
    #'numsections': 10,
    #'showgrades': 1,
    #'enablecompletion': 0,
    #'hiddensections': 0,
    #'format': 'topics',
    #'completionnotify': 0,
    #'lang': '',
    #'categorysortorder': 10001,
    #'timecreated': 1314367091,
    #'groupmodeforce': 0,
    #'forcetheme': '',
    #'summary': u'<p>\ufeff</p>',
    #'idnumber': '',
    #'newsitems': 5,
    #'timemodified': 1314367091
}]

print mdl.create_courses(server, courses)

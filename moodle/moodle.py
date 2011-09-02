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

class MDL:
    """ 
    Main class to connect Moodle webservice
    More information about Webservice:
        http://docs.moodle.org/20/en/Web_Services_API
        http://docs.moodle.org/dev/Web_services
        http://docs.moodle.org/dev/Creating_a_web_service_client
        http://docs.moodle.org/dev/Web_services_Roadmap#Web_service_functions
    """

    """
    Moodle Connection Methods available: XML-RPC, REST
    TODO: SOAP, AMF Protocols
    """

    def conn_rest(self, server, function):
        """
        Connection to Moodle with REST Webservice
        server = {
            'protocol': 'rest',
            'uri': 'http://www.mymoodle.org',
            'token': 'mytokenkey',
        }
        """
        if 'uri' not in server or 'token' not in server:
            return False

        if server['uri'][-1] == '/':
            server['uri'] = server['uri'][:-1]

        url = '%s/webservice/%s/server.php' % (server['uri'], server['protocol'])
        data = 'wstoken=%s&wsfunction=%s' % (server['token'], function)

        import urllib2
        from xml.dom.minidom import parse, parseString
        request = urllib2.Request(url, data)
        f = urllib2.urlopen(request)
        result = f.read()
        f.close()
        return result


    def rest_protocol(self, server, params, function=None, key_word=None):
        """
        Construct the correct function to call
        """
        if function is None:
            function = ""
        if key_word is None:
            key_word = ""
        count = 0
        for param in params:
            if type(param) is dict:
                for item in iter(param):
                    function += '&%s[%s][%s]=' % (key_word, str(count), item)
                    function += '%s' % param[item]
            else:
                function += '&%s[%s]=' % (key_word, str(count))
                function += '%s' % param
            count += 1

        return self.conn_rest(server, function)


    def conn_xmlrpc(self, server, service=None, params=None):
        """
        Connection to Moodle with XML-RPC Webservice
        server = {
            'protocol': 'xmlrpc',
            'uri': 'http://www.mymoodle.org',
            'token': 'mytokenkey',
        }
        """
        if 'uri' not in server or 'token' not in server:
            return False

        import xmlrpclib

        if server['uri'][-1] == '/':
            server['uri'] = server['uri'][:-1]

        url = '%s/webservice/%s/server.php?wstoken=%s' % (server['uri'], server['protocol'], server['token'])
        return xmlrpclib.ServerProxy(url)


    def xmlrpc_protocol(self, server, params, function=None, key_word=None):
        """
        Select the correct function to call
        """

        def moodle_course_get_courses(params):
            return proxy.moodle_course_get_courses()
        
        def moodle_course_create_courses(params):
            return proxy.moodle_course_create_courses(params)
            
        def moodle_user_get_users_by_id(params):
            return proxy.moodle_user_get_users_by_id(params)

        def moodle_user_create_users(params):
            return proxy.moodle_user_create_users(params)
            
        def moodle_user_update_users(params):
            return proxy.moodle_user_update_users(params)
            
        def moodle_enrol_manual_enrol_users(params):
            return proxy.moodle_enrol_manual_enrol_users(params)
            
        def not_implemented_yet(params):
            return False

        proxy = self.conn_xmlrpc(server)
        select_method = {
            "moodle_course_get_courses": moodle_course_get_courses,
            "moodle_course_create_courses": moodle_course_create_courses,
            "moodle_user_get_users_by_id": moodle_user_get_users_by_id,
            "moodle_user_create_users": moodle_user_create_users,
            "moodle_user_update_users": moodle_user_update_users,
            "moodle_enrol_manual_enrol_users": moodle_enrol_manual_enrol_users,
            "not_implemented_yet": not_implemented_yet,
        }

        if function is None or function not in select_method:
            function = "not_implemented_yet"
        return select_method[function](params)


    def get_courses(self, server):
        """
        Get all courses
        Input:
            server = {
                'protocol': 'xmlrpc|rest',
                'uri': 'http://www.mymoodle.org',
                'token': 'mytokenkey',
            }
        Output:
            xmlrpc protocol:    list of dictionaries
            rest protocol:      xml file format
        """
        if 'protocol' not in server:
            return False
        params=''
        function = 'moodle_course_get_courses'
        key_word = ''
        protocol = {
            "xmlrpc": self.xmlrpc_protocol,
            "rest": self.rest_protocol,
        }
        return protocol[server['protocol']](server, params, function)


    def create_courses(self, server, params):
        """
        Create new course
        Input:
            server = {
                'protocol': 'xmlrpc|rest',
                'uri': 'http://www.mymoodle.org',
                'token': 'mytokenkey',
            }
            params = [{                    # Input a list of dictionaries
                'shortname': 'test4',      # Required & unique
                'fullname': 'test4',       # Required
                'categoryid': 1,           # Required
            }]
        Output:
            xmlrpc protocol:    list of dictionaries
            rest protocol:      xml file format
        """
        if 'protocol' not in server:
            return False
        function = 'moodle_course_create_courses'
        key_word = 'courses'
        protocol = {
            "xmlrpc": self.xmlrpc_protocol,
            "rest": self.rest_protocol,
        }
        return protocol[server['protocol']](server, params, function, key_word)


    def get_users(self, server, params):
        """
        Get users by id
        Input:
            server = {
                'protocol': 'xmlrpc|rest',
                'uri': 'http://www.mymoodle.org',
                'token': 'mytokenkey',
            }
            params = [{                    # Input a list of dictionaries
                'shortname': 'test4',      # Required & unique
                'fullname': 'test4',       # Required
                'categoryid': 1,           # Required
            }]
        Output:
            xmlrpc protocol:    list of dictionaries
            rest protocol:      xml file format
        params = ((1,2,3,4,5,...))     # Input a tuple of tuple
        """
        if 'protocol' not in server:
            return False
        function = 'moodle_user_get_users_by_id'
        key_word = 'userids'
        protocol = {
            "xmlrpc": self.xmlrpc_protocol,
            "rest": self.rest_protocol,
        }
        return protocol[server['protocol']](server, params, function, key_word)


    def create_users(self, server, params):
        """
        Create new user
        Input:
            server = {
                'protocol': 'xmlrpc|rest',
                'uri': 'http://www.mymoodle.org',
                'token': 'mytokenkey',
            }
            params = [{                      # Input a list of dictionaries
                'username': username,        # Required & unique
                'password': password,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
            }]
        Output:
            xmlrpc protocol:    list of dictionaries
            rest protocol:      xml file format
        """
        if 'protocol' not in server:
            return False
        function = 'moodle_user_create_users'
        key_word = 'users'
        protocol = {
            "xmlrpc": self.xmlrpc_protocol,
            "rest": self.rest_protocol,
        }
        return protocol[server['protocol']](server, params, function, key_word)


    def update_users(self, server, params):
        """
        Create new user
        Input:
            server = {
                'protocol': 'xmlrpc|rest',
                'uri': 'http://www.mymoodle.org',
                'token': 'mytokenkey',
            }
            params = [{                     # Input a list of dictionaries
                'id': 2,                    # Required & unique
                'firstname': firstname,     # Value to modify
            }]
        Output:
            xmlrpc protocol:    None
            rest protocol:      None
        """
        if 'protocol' not in server:
            return False
        function = 'moodle_user_update_users'
        key_word = 'users'
        protocol = {
            "xmlrpc": self.xmlrpc_protocol,
            "rest": self.rest_protocol,
        }
        return protocol[server['protocol']](server, params, function, key_word)


    def enrol_users(self, server, params):
        """
        Create new user
        Input:
            server = {
                'protocol': 'xmlrpc|rest',
                'uri': 'http://www.mymoodle.org',
                'token': 'mytokenkey',
            }
        enrol =[{                        # Input a list of dictionaries
            'roleid': 1,
            'userid': 5,
            'courseid': 3,
        }]
        Output:
            xmlrpc protocol:    None
            rest protocol:      None
        """
        if 'protocol' not in server:
            return False
        function = 'moodle_enrol_manual_enrol_users'
        key_word = 'enrolments'
        protocol = {
            "xmlrpc": self.xmlrpc_protocol,
            "rest": self.rest_protocol,
        }
        return protocol[server['protocol']](server, params, function, key_word)

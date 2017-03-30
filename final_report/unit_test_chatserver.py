import unittest
import mock
from mock import patch
import chatserver_functions
from chatserver_functions import *
import chatserver
from chatserver import *
import socket
import threading
import thread
import json
import sqlite3
import datetime

class MyTest(unittest.TestCase):


	def test_check_options (self):
		self.assertEqual(check_options("", ""), 'INVALID COMMAND')
		self.assertEqual(check_options('SEARCH_USER', )

	def test_login(self):    
		self.assertEqual(login({'USER':"marc", "PASSWORD":"pass"}), False)
		self.assertEqual(login({'USER':"marc", "PASSWORD":""}), False)

	def test_search_user(self):
		self.assertEqual(search_user({'USER':"mary"}),False)

	def test_add_user(self):
		self.assertEqual(add_user({'USER':'marc', 'CONTACT':'shweta'}), True)

	def test_get_contacts(self):
		self.assertEqual(get_contacts({'USER':'checca'}), ['marc', 'sagar', 'test'])

	def test_query_user(self):
		self.assertEqual(query_user({'USER': 'checca'}), {'USER': u'checca', 'PASSWORD': u"'\\xd0\\xafLY\\xd6\\xb7\\xcd\\x8e\\x15zp\\xc9\\x83N \\xaco\\x19I8\\xecj\\xdaK\\xd0\\xafLY\\xd6\\xb7\\xcd\\x8e\\x15zp\\xc9\\x83N \\xaco\\x19I8\\xecj\\xdaK'", 'CONNECTION': u'127.0.0.1:53151', 'DATE' : u'2017-03-26 21:17:53.057000'})

	def test_new_user(self):
		self.assertEqual(new_user({'USER': 'emma', 'PASSWORD':'emma', 'CONNECTION': '123'}, True))

	


suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)


'''if __name__ == '__main__':
    unittest.main()'''
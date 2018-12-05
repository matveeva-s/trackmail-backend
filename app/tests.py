import unittest
from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'Hello, world!', rv.data)
        self.assertEqual("text/html", rv.mimetype)

    def test_login(self):
        rv = self.app.post('/login/', data={"full_name": "Sveta", "password": "qwerty"})
        self.assertEqual(b'{"full_name":"Sveta","password":"qwerty"}\n', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_form(self):
        rv = self.app.post('/form/', data={"first_name": "Jack", "last_name": "Daniels"})
        self.assertEqual(b'{"first_name":"Jack","last_name":"Daniels"}\n', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_search_user(self):
        rv = self.app.post('/search_user/', data={"query": "Jack", "limit": "5"})
        self.assertEqual(b'{"limit":"5","query":"Jack"}\n', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_search_chats(self):
        rv = self.app.post('/search_chats/', data={"query": "homechat", "limit": "3"})
        self.assertEqual(b'{"limit":"3","query":"homechat"}\n', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_list_chats(self):
        rv = self.app.get('/list_chats/')
        self.assertEqual(b'{"chats": "[Chat1, Chat2]"}', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_create_pers_chat(self):
        rv = self.app.post('/create_pers_chat/')
        self.assertEqual(b'{"chat": "Chat"}', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_create_group_chat(self):
        rv = self.app.post('/create_group_chat/')
        self.assertEqual(b'{"chat": "Chat"}', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_add_members_to_group_chat(self):
        rv = self.app.post('/add_members_to_group_chat/')
        self.assertEqual(b'{}', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_leave_group_chat(self):
        rv = self.app.post('/leave_group_chat/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{}', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_send_message(self):
        rv = self.app.post('/send_message/')
        self.assertEqual(b'{"message": "Message"}', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_read_message(self):
        rv = self.app.get('/read_message/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"chat": "Chat"}', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_upload_file(self):
        rv = self.app.post('/upload_file/')
        self.assertEqual(b'{"attach": "Attachment"}', rv.data)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)

    def test_list_chats_POST(self):
        rv = self.app.post('/list_chats/')
        self.assertEqual(405, rv.status_code)

    def test_create_pers_chat_GET(self):
        rv = self.app.get('/create_pers_chat/')
        self.assertEqual(405, rv.status_code)

    def test_create_group_chat_GET(self):
        rv = self.app.get('/create_group_chat/')
        self.assertEqual(405, rv.status_code)

    def test_add_members_to_group_chat_GET(self):
        rv = self.app.get('/add_members_to_group_chat/')
        self.assertEqual(405, rv.status_code)

    def test_leave_group_chat_GET(self):
        rv = self.app.get('/leave_group_chat/')
        self.assertEqual(405, rv.status_code)

    def test_send_message_GET(self):
        rv = self.app.get('/send_message/')
        self.assertEqual(405, rv.status_code)

    def test_read_message_POST(self):
        rv = self.app.post('/read_message/')
        self.assertEqual(405, rv.status_code)

    def ltest_load_file_GET(self):
        rv = self.app.get('/load_file/')
        self.assertEqual(405, rv.status_code)

class JSONRPCTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def send_message_test(self):
        rv = self.app.post('/api/', data={"jsonrpc":"2.0","method":"send_message","params":[1,1,"try_to_send_message"],"id":"1"	})
        self.assertEqual(b'{"id": "1","jsonrpc": "2.0","result": null}', rv.data)

    def read_message_test(self):
        rv = self.app.post('/api/', data={"jsonrpc":"2.0","method":"read_message","params":[1,1,11],"id":"1"})
        self.assertEqual(b'{"id": "1","jsonrpc": "2.0","result": null}', rv.data)

    def get_chat_messages_test(self):
        rv = self.app.post('/api/', data={"jsonrpc":"2.0","method":"get_chat_messages","params":[1,1],"id":"1"})
        self.assertEqual(b'{"id": "1","jsonrpc": "2.0", "result": {"0": [8, 1, 1, "try1", "Wed, 05 Dec 2018 01:27:26 GMT"]}}', rv.data)

if __name__ == "__main__":
    unittest.main()

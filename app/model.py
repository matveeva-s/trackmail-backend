from . import db

def chat_list():
    return db.query_all("""SELECT * FROM chat""")

def create_pers_chat(name):
    topic = "chat with " + name
    return db.update_base("""
        INSERT INTO chat (is_group_chat, topic, last_message)
        VALUES ('false', %(topic)s, NULL);
        """, topic = topic)

def search_user(name):
    return db.query_one("""
        SELECT * FROM users 
        WHERE nick = %(nick)s;
        """, nick = name)

def search_chat(name):
    return db.query_one("""
        SELECT * FROM chat 
        WHERE topic = %(topic)s;
        """, topic = 'chat with ' + name)

def send_message(chat_id, user_id, content):
    db.update_base("""
        INSERT INTO message (chat_id, user_id, content)
        VALUES (%(chat_id)s, %(user_id)s, %(content)s);
        """, chat_id = chat_id, user_id = user_id, content = content)
    return db._commit_db(0)

def get_chat_messages(chat_id, limit):
    return db.query_all("""
        SELECT * FROM message
        WHERE chat_id = %(chat_id)s
        LIMIT %(limit)s""", chat_id = chat_id, limit = limit)

def read_message(user_id, chat_id, message_id):
    db.update_base("""
        UPDATE member
	    SET last_read_message_id = %(message_id)s
	    WHERE chat_id = %(chat_id)s
	    AND user_id = %(user_id)s
        """, user_id=user_id, chat_id=chat_id, message_id=message_id)
    return db._commit_db(0)

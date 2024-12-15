
import sqlite3


def _connect():
    return sqlite3.connect("telegram_career.db")


def _create_new_chat(chat_type: str)->int:
    conn = _connect()
    cur = conn.cursor()
    
    get_chat_type = f"SELECT id FROM chat_type WHERE type = \"{chat_type}\""
    cur.execute(get_chat_type)
    chat_type_id = cur.fetchone()
    query = "INSERT INTO chat (chat_type) VALUES (?)"
    cur.execute(query,chat_type_id)
    conn.commit()
    new_chat_id = cur.lastrowid
    print(new_chat_id)
    cur.close()
    conn.close()
    
    return new_chat_id


def _add_message(chat_id: int, message: str,system_message: int):
    conn = _connect()
    cur = conn.cursor()
    query = "INSERT INTO message (chat_id, message,system) VALUES (?, ?,?)"
    cur.execute(query,(chat_id,message,system_message))
    conn.commit()
    cur.close()
    conn.close()


def _get_messages(chat_id: int):
    conn = _connect()
    cur = conn.cursor()
    query = "SELECT message ,system FROM message WHERE chat_id = ?"
    cur.execute(query,(chat_id,))
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return messages




if __name__ == "__main__":
    _add_message(2,"Hello",1)
    _add_message(2,"Hi",0)
    print(_get_messages(1))

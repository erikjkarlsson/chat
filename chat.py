# Name:    chat.py
# License: GPLv2 or later
# Author:  blu3
# Version: 1.0
# Date:    09150307
#
#  Description
#  ¨¨¨¨¨¨¨¨¨¨¨
#  A tiny sqlite3 based chat, with possibilities to post,
#  edit and read messages.
#
#  Defines
#  ¨¨¨¨¨¨¨
#  timestring(  )                                                        
#  create_database( path )                                               
#  clear_database( path  str )                                          
#  send_message( path, message, author=..., time=...)  
#  recive_messages( path )
#  lookup_message(path, message_id)
#  message_count(path)
#  previous_message_id( path )
#  refresh_database( path )                                              
#  remove_message( path, message_id=..., author = ... )
#  prettify( messages )
#  edit_message( path, message_id, message=..., author=..., time=... )
#
#  How To Use
#  ¨¨¨¨¨¨¨¨¨¨
#  (1) Create a database with sqlite3 and store the name in DB_PATH
#  (2) Run create_database(DB_PATH) to create all the tables etc.
#  (3) ???
#  (4) profit!!!
#
# Post a message:   send_message()
# Edit a message:   edit_message()
# Remove a message: remove_message()
# Read the chat:    recive_messages(), lookup_message()
#
# refresh_database() will reorganize the database 
# which takes some time, but will make it faster
# to use if large.
#
# clear_database() will remove all tables created 
# for the chat, leaving a blank database.
#

#import hashlib
import sqlite3
from time    import localtime
from os.path import isfile


DB_PATH = "./data/chat.db"

class Message:
    def __init__(self, id, author, message, time):
        self.id = id
        self.author = author
        self.message = message
        self.time = time

    def str(self):
        s_id = f'Id.{self.id}'
        return f'{s_id} `{self.author}` at {self.time}\n>{self.message}'

    
    def sync(self):
        "Sync with database as the message may have been edited"
        
        m = lookup_message(DB_PATH, self.id)
        self.author  = m.author
        self.time    = m.time
        self.message = m.message
        
    def send(self):
        "Create a new message in the database"

        # NOTE  
        # This will create a new message with all of
        # the same variable values and update the
        # id to match the message. In turn this 
        # updates what the message is representing,
        # now being a new message. Usage of this
        # should be CAREFULLY performed.
        
        self.id = send_message(DB_PATH, self.message,
                               self.author, self.time)
        
#    def __del__(self):
#        "Delete the object and representing message in database"
#        
#        remove_message(DB_PATH, self.id)
        

def prettify(messages):
    """Prettify the output recived with recive_messages()

    messages: A list of Messages
    """

    for m in messages:
        print(m.str(), end='\n\n')
        

def timestring():
    """Get the current time as a string"""
    
    t = time.localtime()
    return f'{t.tm_year}/{t.tm_mon}/{t.tm_mday} {t.tm_hour}:{t.tm_min}:{t.tm_sec}'


def create_database(path):
    """Create all tables for the chat database"""
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor()
    
        cur.execute("BEGIN")        

        cur.execute("""
CREATE TABLE IF NOT EXISTS chat (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       author  TEXT,
       message TEXT,
       time    TEXT
);
        """)
        
        con.commit()
    
        cur.execute("BEGIN")
        
        cur.execute("""
CREATE INDEX IF NOT EXISTS chat_index ON chat(id);
    """)        
        con.commit()

        con.close()        
    except:
        BaseException("Unable to create database")

        
def clear_database(path : str):
    """Remove all tables related to the chat.
    
    path: the path to a sqlite3 database
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor()

        cur.execute("BEGIN")        
        cur.execute("DROP TABLE IF EXISTS chat")
        cur.execute("DROP INDEX IF EXISTS chat_index")
        con.commit()

        con.close()
    except:
        
        BaseException("Unable to clear database")
        
        
def send_message(path, message, author="Anonymous", mtime=timestring()):
    """ Send a message in the chat and return the message id

    path: path to the chat database
    message: the text in the message
    author: the author of the message
    time: the time the message was posted (preferably)
    """
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 

        cur.execute("BEGIN")

        cur.execute(f'INSERT INTO chat (author, message, time) VALUES (?, ?, ?)',
                    (author, message, mtime,))

        cur.execute(f'SELECT MAX(chat.id) FROM chat')

        # This does NOT cause any race conditions since
        # it is in one transaction, hence concurrent

        con.commit()

        last_id = cur.fetchall()[0][0]

        con.close()
        return last_id

    except:        
        BaseException("problem sending message")

def message_count(path):
    """ Return the amount of messages

    path: the path to the chat database
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 
        res = cur.execute(f'SELECT COUNT(*) FROM chat')

        # id is defined as unique, hence only one message
        # i use this to bind result into m quick
        cnt = res.fetchall()[0][0]
        con.close()

        return cnt
    except:
        BaseException("problem fetching messages")
    
    
def lookup_message(path, message_id):
    """ Return a structure containing all messages in the chat.

    path: the path to the chat database
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 
        res = cur.execute(f'SELECT * FROM chat WHERE id = ?', (message_id,))
    
        msg = None

        # id is defined as unique, hence only one message
        # i use this to bind result into m quick
        for m in res.fetchall():
            msg = Message(m[0], m[1], m[2], m[3])
            
        con.close()

        return msg
    except:
        BaseException("problem fetching messages")

def lookup_message(path, message_id):
    """ Return a structure containing all messages in the chat.

    path: the path to the chat database
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 
        res = cur.execute(f'SELECT * FROM chat WHERE id = ?', (message_id,))
    
        msg = None

        # id is defined as unique, hence only one message
        # i use this to bind result into m quick
        for m in res.fetchall():
            msg = Message(m[0], m[1], m[2], m[3])
            
        con.close()

        return msg
    except:
        BaseException("problem fetching messages")
        
def previous_message_id(path):
    """ Return the previous message

    path: the path to the chat database
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 
        res = cur.execute(f'SELECT MAX(chat.id) FROM chat')
    
        previous_id = res.fetchall()[0][0]

        con.close()

        return previous_id
    except:
        BaseException("problem fetching messages")

        
def refresh_database(path):
    """ Free up pages and align table data to be contiguous

    path: the path to the chat database
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 

        cur.execute("BEGIN")
        cur.execute("VACUUM chat")
        con.commit()
        
    finally:
        con.close()
    
    
def remove_message(path, message_id = 0, author = None):
    """ Remove a message from the chat by id or author

    path: the path to the chat database
    message_id: the id of the target message to be removed
    author: the author of the message[s] to be removed
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 

        if not ( author == None ):
            # Delete by author name
            cur.execute("BEGIN")
            cur.execute(f'DELETE FROM chat WHERE author = ?', (author,))
            con.commit()
        else:
            # Delete by Id
            cur.execute("BEGIN")
            cur.execute(f'DELETE FROM chat WHERE id = ?', (message_id,))
            con.commit()            
    
        con.close()

    except:
        BaseException("problem removing message")

def edit_message(path, message_id, message=None, author=None, mtime=None):
    """ edit a message from the chat by id

    path: the path to the chat database
    message_id: the id of the target message
    message: new message of the edited message
    author: new author of the edited message
    mtime: new time of the edited message
    """
    
    try:
        con = sqlite3.connect(path)
        cur = con.cursor() 

        if not ( message == None ):
            cur.execute("BEGIN")
            cur.execute("UPDATE chat set message = ? WHERE id = ?",
                        (message, message_id,))
            con.commit()

        elif not ( author == None ):
            cur.execute("BEGIN")
            cur.execute("UPDATE chat set author = ? WHERE id = ?",
                        (message, author,))
            con.commit()            

        elif not ( mtime == None ):
            cur.execute("BEGIN")
            cur.execute("UPDATE chat set time = ? WHERE id = ?",
                        (message, mtime,))
            con.commit()            

            
        con.close()

    except:
        BaseException("problem removing message")











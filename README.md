# chat
  A tiny sqlite3 based chat, with possibilities to post,
  edit and read messages.

## Defines
 - `prettify( messages )`
 - `timestring(  )`                                                        
 - `create_database( path )`                                               
 - `clear_database( path  str )`                                          
 - `send_message( path, message, author=..., time=...)`  
 - `recive_messages( path )`
 - `recive_message(path, message_id)`
 - `refresh_database( path )`                                             
 - `remove_message( path, message_id=..., author = ... )`                 
 - `edit_message( path, message_id, message=..., author=..., time=... )`
 - `Message( id, author, message, time )`
 
## How To Use
 
  1. Create a database with sqlite3 and store the name in DB_PATH
  ```sh
  mkdir data
  echo .save ./data/chat.db | sqlite3
  ```
  2. Run create_database(DB_PATH) to create all the tables etc.
  3. ???
  ```
>>> send_message(DB_PATH, "Hello world")

>>> send_message(DB_PATH, "Foo")

>>> send_message(DB_PATH, "Bar")

>>> prettify(recive_messages(DB_PATH))

Id.1 `Anonymous` at 2022/9/15 6:34:41
>Hello world

Id.2 `Anonymous` at 2022/9/15 6:34:41
>Foo

Id.3 `Anonymous` at 2022/9/15 6:34:41
>Bar
  ```
  4. profit!!!
  
## Functionalities  
 - Post a message:   `send_message()`
 - Edit a message:   `edit_message()`
 - Remove a message: `remove_message()`
 - Read the chat:    `recive_messages()`, `lookup_message()`

- `refresh_database()` will reorganize the database 
which takes some time, but will make it faster
 to use if large.

- `clear_database()` will remove all tables created 
 for the chat, leaving a blank database.


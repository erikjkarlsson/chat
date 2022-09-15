from chat import *
from flask import Flask
from flask import make_response
from flask import render_template
from flask import url_for
from flask import request

DB_PATH = "./data/chat.db"

app = Flask(__name__)

def escape(s):
    return s

@app.get("/chat")
def chat():

    msgs = recive_messages(DB_PATH)    
    return render_template("chat.html", messages = msgs,
                           notice = "Welcome")

@app.post("/del/<int:msg_id>")
def dele(msg_id):
    try:
        remove_message(DB_PATH, msg_id)
        msgs = recive_messages(DB_PATH)
        return render_template("chat.html", messages = msgs,
                               notice = "Post removed!")
    except:
        msgs = recive_messages(DB_PATH)
        return render_template("chat.html", messages = msgs,
                               notice = "Cannot remove")


@app.post("/chat")
def post():
    
    user = escape(str(request.form['username']))
    msg  = escape(str(request.form['message']))

    if (user == "") or (msg == ""):
        return render_template("chat.html", messages = msgs,
                               notice = "Invalid Message")

    # Detect spam, if there are 4 equal messages in the
    # 7 previous messages => spam
    elif message_occurences(DB_PATH, msg,
                            previous_message_id(DB_PATH) - 7) > 4:

        return render_template("chat.html", messages = msg,
                               notice = "Spam Detected")

    else:
        try:
            send_message(DB_PATH, msg, user)

        finally:
            msgs = recive_messages(DB_PATH)

            return render_template("chat.html", messages = msgs,
                                   notice = "Message posted")
    
    
#url_for("static", filename="./css/style.css")

if __name__ == '__main__':
    app.run()

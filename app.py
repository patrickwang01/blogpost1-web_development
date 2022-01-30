from flask import Flask, g, render_template, request
app = Flask(__name__)

# set FLASK_ENV=development
# flask run

import sqlite3

def get_message_db():
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()
    
    # create messages table
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER, handle TEXT, message TEXT)")

    return g.message_db


def insert_message(request):
    message = request.form["message"]
    handle = request.form["handle"]

    g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()

    # count number of rows in table
    rows = len(cursor.fetchall())

    # set parameters for insertion
    params = (1 + rows, message, handle)

    # insert message into table 
    cursor.execute("INSERT INTO messages(id, handle, message) VALUES (?, ?, ?)", params)
    
    g.message_db.commit()
    g.message_db.close()

    return message, handle

@app.route('/', methods = ['POST', 'GET'])
def submit():
    if request.method == "GET":
        return render_template('submit.html')

    else:
        insert_message(request)
        return render_template('submit.html', thanks = True)


def random_messages(n):

    g.message_db = sqlite3.connect("messages_db.sqlite")
    cursor = g.message_db.cursor()

    params = str(n)

    cursor.execute("SELECT * FROM messages ORDER BY RANDOM() LIMIT (?)", params)
    results = cursor.fetchall()

    g.message_db.close()

    return results

@app.route('/view')
def view():
    results = random_messages(5)
    return render_template('view.html', entries = results)



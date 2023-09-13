from flask import Flask, g, Blueprint
import sqlite3
from views import appointment


app = Flask(__name__)
app.register_blueprint(appointment)

@app.route("/")
def index():
    print("Index running!")

@app.before_request
def before_request_func():
    print("before_request executing!")

@app.after_request
def after_request_func(response):
    print("after_request executing!")
    if g.db  is not None:
        print('Closing connection')
        g.db.close()
    return response

if __name__ == "__main__":
    app.run()
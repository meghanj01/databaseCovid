from flask import Flask, g
import sqlite3
from views import appointment

# create flask application
app = Flask(__name__)

# register the apps
app.register_blueprint(appointment)


@app.route("/")
def index():
    print("Index running!")


# before request and after request can be used to create db connection and close db connection future scope
# @app.before_request
# def before_request_func():
#     print("before_request executing!")

# @app.after_request
# def after_request_func(response):
#     print("after_request executing!")
#     if g.db  is not None:
#         print('Closing connection')
#         g.db.close()
#     return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")

from flask import Flask, request
from routes import bp as routes_blueprint

app = Flask(__name__)
app.static_folder = 'static'

app.register_blueprint(routes_blueprint)
app.secret_key="secret key"

if __name__ == '__main__':
    app.run(debug=True)
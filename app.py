from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIG/START DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

# DATABASE MODELING
# rows - register | columns - infos
# Product (rows) | id, name, price, description (colums)
class Product (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String(120), nullable = False)
    price = db.Column (db.Float, nullable = False)
    # "Text" does not have character limitation, like the string
    description = db.column (db.Text, nullable = True)

# ROOT - ROUTE - FUNCTION
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug = True)
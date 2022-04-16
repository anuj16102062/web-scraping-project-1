from flask import Flask
app = Flask(__name__)


class Drink(db.Model):
    id = db.Column(db.integer,primary_key = True)
    name = db.Column(db.String(80),nullable=False,unique=True)
    description = db.Column(db.String(120))


    def __repr__(self):
        return f"{self.name}  -- {self.description}"

@app.route('/')
def hello():
    return "WELCOME ANUJ KUMAR PANDEY"

@app.route('/drinks')
def get_drinks():
    return {'drinks':'cocacola'}
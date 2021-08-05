import psycopg2
from flask import Flask

app= Flask(__name__)
app.secret_key='ifpb2021'
db= psycopg2.connect('dbname=bd_carros user=postgres password=12345 host=127.0.0.1')
from views import *


if __name__ == '__main__':
    app.run(debug=True )








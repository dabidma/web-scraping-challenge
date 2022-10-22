from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

#connect to mongo
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

#initialize flask
app = Flask(__name__)

#create root route
@app.route('/')
def echo():
    mars = collection.find_one()
    return render_template('index.html',mars=mars)

@app.route('/scrape')
def scrape():
    scrape_mars.scrape()
    return redirect('/', code = 302)

#debugger to edit while running
if __name__ == "__main__":
    app.run(debug=True)
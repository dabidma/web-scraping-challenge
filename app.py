from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#initialize flask
app = Flask(__name__)

#setup mongo db
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#create root route
@app.route('/')
def echo():
    mars_info = mongo.db.mars.find_one()
    return render_template('index.html',mars=mars_info)

@app.route('/scrape')
def scrape():
    mars_info = scrape_mars.scrape()
    mongo.db.mars.update_one({}, {'$set': mars_info})
    return redirect('/', code = 302)

#debugger to edit while running
if __name__ == "__main__":
    app.run(debug=True)
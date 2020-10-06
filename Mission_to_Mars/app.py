from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

# Set up mongo connection with PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017"

mongo = PyMongo(app)


@app.route("/")

def index():
    mars = mongo.db.mars.find_one()
    
    return render_template("index.html", mars=mars)
    
### Scrape route for mars_scrape()
@app.route("/scrape")

def scrape():

    print("Scraping...")
    
    mars_data = mars_scrape.scrape()
    mongo.db.mars.update({}, mars_data, upsert=True)
    
    # Redirect back to Landing Page
    return redirect("/")
  


if __name__ == "__main__":
    ##print (mars_scrape.scrape())
    app.run(debug=True)
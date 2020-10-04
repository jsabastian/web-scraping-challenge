from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

# Set up mongo connection with PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"

mongo = PyMongo(app)

### Scrape route for mars_scrape()
@app.route("/scrape")
def scrape_urls():

    print("Scraping...")

    mars_scraping = mars_scrape.scrape_urls()
    mongo.db.mars.update({}, mars_scraping, upsert=True)
    
    # Redirect back to Landing Page
    return redirect("/", code=302)
  
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    
    return render_template("index.html", mars=mars)

if __name__ == "__main__":
    ##print (mars_scrape.scrape_urls())
    app.run(debug=True)
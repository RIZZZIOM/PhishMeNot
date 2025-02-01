from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route('/')
def homePage():
    print("\nAccessed homepage\n")
    return render_template("index.html")

@app.route('/templates')
def tempPage():
    print("\nAccessed templates page\n")
    return render_template("templates.html")

@app.route('/settings')
def settingsPage():
    print("\nAccessed settings page\n")
    return render_template("settings.html")

@app.route('/campaigns')
def campPage():
    print("\nAccessed campaigns page")
    return render_template("campaigns.html")

@app.route('/documentation')
def docPage():
    print("\nAccessed documentation page\n")
    return render_template("documentation.html")

@app.route('/results')
def resPage():
    print("\nAccessed results page\n")
    return render_template("results.html")

app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)


# app code


# pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/your_character")
def your_character():
    return render_template("your_character.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

@app.route("/advice")
def advice():
    return render_template("advice.html")

if __name__ == "__main__":
    app.run()
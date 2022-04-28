from flask import Flask, render_template, request
from controller import reader_controller as rc

app = Flask(__name__, template_folder="views")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", context=rc.dataHome())

@app.route("/detail/file/<filename>", methods=['GET'])
def detail(filename):
    path = request.args.get("path")
    return render_template("index.html", context=rc.readSingleFile(path))

@app.route("/detail/<folder>/<file>", methods=["GET"])
def get_by_folder(folder, file):
    path = request.args.get("path")
    return render_template("index.html", context=rc.readFileInFolder(path))

@app.route("/search", methods=["GET"])
def search():
    return render_template("index.html", context=rc.search(request.args.get("query")))


app.run(debug=False, port=4000)
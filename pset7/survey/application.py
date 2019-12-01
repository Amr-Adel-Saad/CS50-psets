import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form.get("gender")
    hobby = request.form["hobby"]

    # Check for user inputs
    if not name or not age or not gender or not hobby:
        return render_template("error.html", message="Please complete required fields.")
    # Check if file is empty and write header and then CSV
    else:
        with open("survey.csv", "r", newline="") as survey:
            if not survey.read(1):
                with open("survey.csv", "a", newline="") as survey:
                    datawriter = csv.writer(survey)
                    datawriter.writerow(["Name", "Age", "Gender", "Hobby"])
        with open("survey.csv", "a", newline="") as survey:
            datawriter = csv.writer(survey)
            datawriter.writerow([name, age, gender, hobby])
            return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # Read CSV file and render its contents into html file
    with open("survey.csv", "r", newline="") as survey:
        survey_reader = csv.reader(survey)
        for row in survey_reader:
            return render_template("sheet.html", survey=survey_reader)

    return render_template("error.html", message="No submissions yet.")

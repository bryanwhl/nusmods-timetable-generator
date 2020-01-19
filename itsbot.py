from flask import Flask, request, render_template
import Scrapper
import json

'''
Flask setup
'''

app = Flask(__name__)
app.config["DEBUG"] = True
appName = "NUSTimeTable"

@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")

@app.route("/generate", methods=["POST"])
def Generated():
    semester = int(request.form["semNumber"])

    moduleInput = request.form["modules"]
    moduleArray = moduleInput.split(" ")

    startTime = int(request.form["startTime"])
    endTime = int(request.form["endTime"])

    blockSize = int(request.form["blockSize"])

    prioritizeFreeTime = True if request.form["freeDaySetting"] == "Yes" else False
    prioritizeDistance = True if request.form["locationSetting"] == "Yes" else False

    parameters = {"moduleArray" : moduleArray,
                  "semester" : semester,
                  "startTime" : startTime,
                  "endTime" : endTime,
                  "blockSize" : blockSize,
                  "prioritizeFreeTime" : prioritizeFreeTime,
                  "prioritizeDistance" : prioritizeDistance}
    urls = Scrapper.generate(parameters)

    return render_template("result.html", url1=urls[0], url2=urls[1], url3=urls[2], url4=urls[3], url5=urls[4])

if __name__ == '__main__':
    app.run()

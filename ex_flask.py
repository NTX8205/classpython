from flask import Flask, render_template, request
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/current")
def current():
    now = datetime.now()
    return render_template("current.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/hi")
def hi():# 載入原始檔案
    f = open("count.txt", "r")
    count = int(f.read())
    f.close()
    count += 1# 計數加1
    f = open("count.txt", "w")# 覆寫檔案
    f.write(str(count))
    f.close()
    return "本網站總拜訪人次：" + str(count)


if __name__ == "__main__":
    app.run()
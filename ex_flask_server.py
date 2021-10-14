from flask import Flask, render_template, request
from datetime import datetime
from waitress import serve
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>許哲睿Python測試網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/current>開啟網頁及顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=0011>開啟網頁及傳送使用者暱稱</a><br>"
    homepage += "<a href=/hi>計算總拜訪次數</a><br>"
    homepage += "<a href=https://www1.pu.edu.tw/~s1092805/index.html>我的個人頁面</a><br>"
    return homepage

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
    f = open('classpython\count.txt', "r")
    count = int(f.read())
    f.close()
    count += 1# 計數加1
    f = open('classpython\count.txt', "w")# 覆寫檔案
    f.write(str(count))
    f.close()
    return "本網站總拜訪人次：" + str(count)


if __name__ == "__main__":
    app.run()
    #serve(app, host='0.0.0.0', port=8080)
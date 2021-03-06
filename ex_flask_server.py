import subprocess
from flask import Flask, render_template, request
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("project-analytics-8acd9-firebase-adminsdk-6usuy-2415c74209.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def index():
    homepage = "<h1>許哲睿Python測試網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/current>開啟網頁及顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=許哲睿>開啟網頁及傳送使用者暱稱</a><br>"
    homepage += "<a href=/login>透過表單輸入名字傳值</a><br>"
    homepage += "<a href=/hi>計算總拜訪次數</a><br>"
    homepage += "<a href=/aboutme>關於子青老師 (響應式網頁實例)</a><br>"
    homepage += "<br><a href=/read>讀取Firestore資料</a><br>"
    homepage += "<a href=/resource>MIS resource</a><br>"
    homepage += "<br><a href=/spider>讀取開眼電影即將上映影片，寫入Firestore</a><br>"
    homepage += "<br><a href=/search>輸入關鍵字進行資料查詢</a><br>"
    return homepage

@app.route('/mis')
def course():
    return "<h1>資訊管理導論</h1>"

@app.route('/current')
def current():
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("current.html", datetime = str(now))

@app.route('/welcome', methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route('/hi')
def hi():# 載入原始檔案
    f = open('count.txt', "r")
    count = int(f.read())
    f.close()
    count += 1# 計數加1
    f = open('count.txt', "w")# 覆寫檔案
    f.write(str(count))
    f.close()
    return "本網站總拜訪人次：" + str(count)

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return "您輸入的名字為：" + user 
    else:
        return render_template("login.html")

@app.route("/resource")
def classweb():
    return render_template("links.html")

@app.route("/aboutme")
def about():
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("aboutme.html",datetime = str(now))

@app.route("/read")
def read():
    Result = ""
    collection_ref = db.collection("靜宜資管")
    docs = collection_ref.order_by(
        "mail", direction=firestore.Query.DESCENDING).get()
    for doc in docs:
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"
    return Result

@app.route('/spider')
def spider():
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result = sp.select(".filmListAllX li")
    lastUpdate = sp.find("div", class_="smaller09").text[5:]

    for item in result:
        picture = item.find("img").get("src").replace(" ", "")
        title = item.find("div", class_="filmtitle").text
        movie_id = item.find("div", class_="filmtitle").find(
            "a").get("href").replace("/", "").replace("movie", "")
        hyperlink = "http://www.atmovies.com.tw" + \
            item.find("div", class_="filmtitle").find("a").get("href")
        show = item.find("div", class_="runtime").text.replace("上映日期：", "")
        show = show.replace("片長：", "")
        show = show.replace("分", "")
        showDate = show[0:10]
        showLength = show[13:]

        doc = {
            "title": title,
            "picture": picture,
            "hyperlink": hyperlink,
            "showDate": showDate,
            "showLength": showLength,
            "lastUpdate": lastUpdate
        }

        doc_ref = db.collection("電影").document(movie_id)
        doc_ref.set(doc)
    return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        collection_ref = db.collection("電影")
        docs = collection_ref.order_by("showDate").get()
        info = ""
        for doc in docs:
            if MovieTitle in doc.to_dict()["title"]:
                info += "片名：" + doc.to_dict()["title"] + "<br>"
                info += "海報：" + doc.to_dict()["picture"] + "<br>"
                info += "影片介紹：" + doc.to_dict()["hyperlink"] + "<br>"
                info += "片長：" + doc.to_dict()["showLength"] + " 分鐘<br>"
                info += "上映日期：" + doc.to_dict()["showDate"] + "<br><br>"
        return info
    else:
        return render_template("input.html")


if __name__ == "__main__":
    app.run()
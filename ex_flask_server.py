import subprocess
from flask import Flask, render_template, request
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate(
    "project-analytics-8acd9-firebase-adminsdk-6usuy-2415c74209.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    homepage += "<br><a href=/create>新增Firestore資料</a><br>"
    homepage += "<br><a href=/delete>刪除Firestore資料</a><br>"
    homepage += "<br><a href=/update>上傳Firestore資料</a><br>"
    homepage += "<a href=/resource>MIS resource</a><br>"
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

@app.route("/create")
def create():
    docs = [

        {

            "name": "陳武林",

            "mail": "wlchen@pu.edu.tw",

            "lab": 665

        },

        {

            "name": "莊育維",

            "mail": "ywchuang@pu.edu.tw",

            "lab": 566

        },

        {

            "name": "汪于茵",

            "mail": "yywang13@pu.edu.tw",

            "lab": 674

        },

        {

            "name": "許哲睿",

            "mail": "s1092805@pu.edu.tw",

            "lab": 659

        }

    ]


    collection_ref = db.collection("靜宜資管")

    for doc in docs:

        collection_ref.add(doc)

@app.route("/delete")
def delete():
    collection_ref = db.collection("靜宜資管")


    docs = collection_ref.where("lab", "==", 579).get()

    NewData = {"name": "子青老師"}

    for doc in docs:

        doc_ref = db.collection("靜宜資管").document(doc.id)

        doc_ref.delete()

@app.route("/update")
def update():
    Rcollection_ref = db.collection("靜宜資管")

    docs = collection_ref.where("lab","==", 579).get()

    NewData = {"name": "子青老師"}

    for doc in docs:

        doc_ref = db.collection("靜宜資管").document(doc.id)

        doc_ref.update(NewData)
if __name__ == "__main__":
    app.run()
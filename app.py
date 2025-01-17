from flask import Flask,render_template
from flask.templating import render_template, render_template_string
from werkzeug.datastructures import RequestCacheControl
from flask import request
from config import S3_KEY, S3_SECRET, S3_BUCKET
import boto3
import sqlite3 as sql
app=Flask("sagar")

@app.route("/")
def home():
     return render_template("index.html")

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET

)

@app.route("/videos",methods=["GET","POST"])
def videos():
     try:
          title=request.form.get("title")
          dis=request.form.get("dis")
          video=request.files["video"]
          file_name=video.filename
          video.save(file_name)
          s3.upload_fileobj(
                video,
                S3_BUCKET,
                video.filename,
                ExtraArgs={
                  "ACL": "public-read",
                  "ContentType": video.content_type
             },
              key=file_name
              )
          aws_region= boto3.client('s3').get_bucket_location(Bucket=S3_BUCKET)['LocationConstraint']
          url=f"https://{S3_BUCKET}.s3.{aws_region}.amazonaws.com/{file_name}"

          print(url)

          with sql.connect("playback.db") as con:
              cur = con.cursor()
              print("here 1")
              cur.execute("INSERT INTO Play (Ti,Des,Li) VALUES (?,?,?)",(title,dis,url))
              print("here 2")
              con.commit()
              print("here 3")
         
          print("here")
     except:
          # con.rollback()
          return render_template("index.html")

     return render_template("videos.html",url=url)


@app.route('/list')
def list():
    con = sql.connect("playback.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from play")

    rows = cur.fetchall()
    return render_template("list.html", rows = rows)
     
    
if __name__ == "__main__":
    app.run(debug=True)
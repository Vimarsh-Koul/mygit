from flask import Flask,render_template
from flask.templating import render_template, render_template_string
from werkzeug.datastructures import RequestCacheControl
from flask import request
import os
import subprocess
import boto3
app=Flask("sagar")

@app.route("/")
def home():
     return render_template("home.html")

s3 = boto3.client(
   "s3",
   aws_access_key_id="AKIA6HUK4R44SOQFHAWY",
   aws_secret_access_key=S3_SECRET
)
@app.route("/videos",methods=["GET","POST"])
def videos():
     try:
          title=request.form.get("title")
          video=request.files["video"]
          print(video)
          print(video.content_type)
          file_name=video.filename
          video.save(file_name)
          


     except:
          return render_template("home.html")

     return render_template("videos.html",url = f'https://mynkt30.s3.amazonaws.com/{key}')
    
#     return render_template("videos.html",title=title,video=file_n)
if __name__ == "__main__":
    app.run(debug=True)
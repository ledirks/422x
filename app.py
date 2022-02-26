from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from flask_bootstrap import Bootstrap
import boto3
import pymysql
from config import S3_BUCKET,S3_KEY,S3_SECRET,APPLICATION_PASS

s3 = boto3.client('s3',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET)

app = Flask(__name__)
Bootstrap(app)

conn = pymysql.connect(
        host= 'database-1.czglra39ojmn.us-east-1.rds.amazonaws.com', 
        port = '3306',
        user = 'admin', 
        password = 'password',
        db = 'db',
        )

@app.route('/')
def index():
    username = request.args.get("username")
    password = request.args.get("password") 
    cur=conn.cursor()
    cur.execute("SELECT password FROM users where username = 'username'")
    details = cur.fetchone()
    if password == details[0] 
        return redirect(url_for('images'))

    return render_template('index.html')

@app.route('/images')
def images():
    resource = boto3.resource('s3')
    bucket = resource.Bucket('se422project')
    object_list = bucket.objects.all()

    return render_template('dashboard.html',files=object_list)

@app.route('/search', methods=['GET'])
def search():
    file_name = request.args.get("search")
    resource = boto3.resource('s3')
    bucket = resource.Bucket('se422project')
    object_list = bucket.objects.filter(Prefix=file_name)

    return render_template('dashboard.html',files=object_list)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    resource = boto3.resource('s3')
    bucket = resource.Bucket('se422project')
    bucket.Object(file.filename).put(Body=file)

    return redirect(url_for('images'))

@app.route('/download', methods=['POST'])
def download():
    obj_key = request.form['key']
    resource = boto3.resource('s3')
    bucket = resource.Bucket('se422project')
    file_obj = bucket.Object(obj_key).get()

    resp = Response(file_obj['Body'].read())
    resp.headers['Content-Disposition'] = 'attachment;filename=' + format(obj_key)
    resp.mimetype = 'text/plain'

    return resp

if __name__ == '__main__':
    app.run()


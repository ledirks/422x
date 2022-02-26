from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET,S3_KEY,S3_SECRET,APPLICATION_PASS

s3 = boto3.client('s3',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET)

app = Flask(name)
Bootstrap(app)

@app.route('/')
def index():
    password = request.args.get("login")
    if password == 'helloworld':
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
@app.route('/search', methods=['GET'])
def search():
    file_name = request.args.get("search")
    resource = boto3.resource('s3')
    bucket = resource.Bucket('se422project')
    object_list = bucket.objects.filter(Prefix=file_name)

    return render_template('dashboard.html',files=object_list)
import pymysql

conn = pymysql.connect(
        host= 'database-1.czglra39ojmn.us-east-1.rds.amazonaws.com', 
        port = '3306',
        user = 'admin', 
        password = 'password',
        db = 'db',

        )

@app.route('/images')
def images(): 
    username = request.args.get("?")
    password = request.args.get("login") 
    cur=conn.cursor()
    cur.execute("SELECT password FROM users where username = 'username'")
    details = cur.fetchone()
    if password == details.password:
        return redirect(url_for('images'))
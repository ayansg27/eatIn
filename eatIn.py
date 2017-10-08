from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'abcd1234'
app.config['MYSQL_DATABASE_DB'] = 'eatIn'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
#database connect
conn = mysql.connect()
cur =conn.cursor()


@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT emailid FROM user WHERE emailid = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE emailid = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                password = password_form.encode('utf-8')
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
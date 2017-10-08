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
    error=None
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        signuptype_cust = request.form['radioCustomer']
        signuptype_chef = request.form['radioChef']
        if signuptype_cust:
            cust_fname = request.form['fname']
            cust_lname = request.form['lname']
            cust_email = request.form['email']
            cust_phone = request.form['phone']
            cust_password = request.form['password']
            cust_cpassword = request.form['cpassword']
            cust_address = request.form['address']
            cust_street = request.form['street']
            cust_city = request.form['city']
            cust_state = request.form['state']
            cust_zipcode = request.form['zipcode']
            cust_country = request.form['country']
            cust_preference = request.form['preference']
            sql_user="insert into user (emailid,password,fname,lname,user_type) values(%s,%s,%s,%s,%s)"
            sql_customer="insert into customer (address,street,city,state,zipcode,country,phone_number,preference) values(%s,%s,%s,%s,%d,%s,%s,%s)"
            if cust_password==cust_cpassword:
                cur.execute(sql_user, (cust_email, cust_cpassword, cust_fname, cust_lname, "customer"))
                cur.execute(sql_customer, (cust_address, cust_street, cust_city, cust_state, cust_zipcode, cust_country, cust_phone,cust_preference))
                return redirect(url_for('login', created=true))
            else:
                error="Passwords don't match"
                return render_template('signup.html', custerror=error)

        if signuptype_chef:
            chef_cfname = request.form['cfname']
            chef_clname = request.form['clname']
            chef_cemail = request.form['cemail']
            chef_cphone = request.form['cphone']
            chef_cpassword = request.form['cpassword']
            chef_ccpassword = request.form['ccpassword']
            chef_caddress = request.form['caddress']
            chef_cstreet = request.form['cstreet']
            chef_ccity = request.form['ccity']
            chef_cstate = request.form['cstate']
            chef_czipcode = request.form['czipcode']
            chef_ccountry = request.form['ccountry']
            chef_cuisine = request.form['cuisine']
            sql_user = "insert into user (emailid,password,fname,lname,user_type) values(%s,%s,%s,%s,%s)"
            sql_chef = "insert into chef (address,street,city,state,zipcode,country,phone_number) values(%s,%s,%s,%s,%s,%s,%s)"
            if chef_cpassword == chef_ccpassword:
                cur.execute(sql_user, (chef_cemail, chef_cpassword, chef_cfname, chef_clname, "chef"))
                cur.execute(sql_chef,(chef_caddress, chef_cstreet, chef_ccity, chef_cstate, chef_czipcode, chef_ccountry, chef_cphone))
                return redirect(url_for('login', created=true))
            else:
                error = "Passwords don't match"
                return render_template('signup.html', cheferror=error)


if __name__ == '__main__':
    app.run(debug=True)
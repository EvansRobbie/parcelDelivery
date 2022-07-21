from flask import *
import pyrebase
app = Flask(__name__)
#This secret key encripts your user session for security reasons
app.secret_key = 'A1_445T_@!jhf5gH' #16,32,64
import pymysql

connection = pymysql.connect(host='localhost', user='root', password='', database='parcel_db')

@app.route('/')
def index():
    #create query
    sql= 'SELECT * FROM benefits_tbl'
    sql2 = 'SELECT * FROM news_tbl'

    cursor = connection.cursor()
    cursor.execute(sql)

    cursor2 = connection.cursor()
    cursor2.execute(sql2)
#check how many rows were counted
    if cursor.rowcount == 0:
        #nothing on the benefits_tbl
        return render_template('index.html', msg = 'Nothing on the benefits')
    else:
        #get all rows
        rows = cursor.fetchall()
        news = cursor2.fetchall()
        return render_template('index.html', rows = rows, news = news)





@app.route('/action', methods = ['POST','GET'])
def action():
    if request.method == 'POST':
        # receive the posted username and password variables
        customer_username = request.form['customer_username']
        password = request.form['password']

        # We now move to the db and confirm if above details exists
        sql = "SELECT * FROM customers where customer_username = %s and customer_password = %s"
        # create a cursor an d execute above sql
        cursor = connection.cursor()
        # execute the sql,provide email and password to fit %s placeholders
        cursor.execute(sql, (customer_username, password))

    # Check if match was found
        if cursor.rowcount == 0:
            flash("Wrong credentials")
            return render_template('index.html', error='Wrong credentials')
        elif cursor.rowcount == 1:
            # create a user to track who is logged in
            # Attach user email to the session
            session['user'] = customer_username
            flash("Login Successfull")
            return redirect('/')
        else:
            flash("Error Occured,Try later")
            return render_template('index.html', error='Error Occured,Try later')

    else:
        return render_template('index.html')

@app.route('/action1', methods = ['POST', 'GET'])
def action1():
    if request.method == 'POST':
        customer_fname = request.form['customer_fname']
        customer_lname = request.form['customer_lname']
        customer_username = request.form['customer_username']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_password = request.form['customer_password']
        customer_password2 = request.form['customer_password2']
        customer_gender = request.form['customer_gender']
        customer_address = request.form['customer_address']


        # validations
        import re
        if customer_password != customer_password2:
            flash("password do not match")
            return render_template('index.html',password= 'password do not match')

        elif len(customer_password)< 8:
            flash("password must have 8 characters")
            return render_template('index.html',password= 'password must have 8 characters')

        elif not re.search("[a-z]", customer_password):
            flash("must have a small letter")
            return render_template('index.html',password='must have a small letter')

        elif not re.search("[A-Z]", customer_password):
            flash("must have a capital letter")
            return render_template('index.html',password='must have a capital letter')

        elif not re.search("[0-9]", customer_password):
            flash("must have a number")
            return render_template('index.html',password='must have a number')

        elif not re.search("[_@$]", customer_password):
            flash("must have a symbol")
            return render_template('index.html',password='must have a symbol')
        else:
            sql = "INSERT INTO customers_tbl(customer_fname,customer_lname,customer_username,customer_email,customer_phone,customer_password,customer_gender,customer_address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor= connection.cursor()
            try:
                cursor.execute(sql, (customer_fname, customer_lname, customer_username, customer_email, customer_phone, customer_password,
                customer_gender, customer_address))
                connection.commit()
                flash("saved successfully")
                return render_template('index.html', success='saved successfully')

            except:
                flash("failed")
                return render_template('index.html', error='failed')

    else:
        flash("Request Failed")
        return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user')
    flash("Your session has ended.See you later")
    return redirect('/') #clear session

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    return render_template('contact.html')

@app.route('/courier', methods = ['POST', 'GET'])
def courier():
    if request.method == 'POST':
        collection_address = request.form['collection_address']
        sender_phone = request.form['sender_phone']
        delivery_address = request.form['delivery_address']
        reciever_phone = request.form['reciever_phone']
        weight = request.form['weight']
        length = request.form['length']
        width = request.form['width']
        height= request.form['height']
        order_status = request.form['order_status']
        #capture the user session
        email = session['user']

        #validations
        import re
        if len(sender_phone) < 13:
            return render_template('courier.html', sender_phone='must have 13 numbers')
        elif len(reciever_phone) < 13:
            return render_template('courier.html', reciever_phone='must have 13 numbers')
        else:
            sql = "insert into courier_tbl(collection_address,sender_phone,delivery_address,reciever_phone,weight,length,width,height,order_status,email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            try:
                cursor.execute(sql,(collection_address,sender_phone,delivery_address,reciever_phone,weight,length,width,height,order_status,email))
                connection.commit()
                return render_template('courier.html', success= 'saved successfully')
            except:
                return render_template('courier.html', error='failed')
    else:
        return render_template('courier.html')

@app.route('/parcel', methods = ['POST', 'GET'])
def parcel():
    if request.method == 'POST':
        collection_address = request.form ['collection_address']
        delivery_address  = request.form ['delivery_address']
        order_status = request.form['order_status']
        #capture session of the user
        customer_username = session['user']
        customer_phone = session['user']
        sql = "insert into sameday_tbl (collection_address,delivery_address,customer_username,customer_phone,order_status) VALUES(%s,%s,%s,%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql,(collection_address,delivery_address,customer_username,customer_phone,order_status))
        connection.commit()
        flash("parcel details recieved")
        return render_template('parcel.html', success = 'parcel details recieved')
    else:
        flash("failed to load details")
        return render_template('parcel.html', error = 'failed to load details')
@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/track', methods= ['POST', 'GET'])
def track():
    if request.method == 'POST':
        parceltrack_id = request.form['parceltrack_id']
        sql = "select * from courier_tbl where parceltrack_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql,(parceltrack_id))

        if cursor.rowcount == 0:
           return render_template('track.html', error='No parcel with that ID')
        else:
           # get all rows
           rows = cursor.fetchall()
           # print(rows)
           return render_template('track.html', rows = rows)
    else:
        return render_template('track.html')

@app.route('/admin', methods = ['POST','GET'])
def admin():
    if request.method == 'POST':
        # receive the posted username and password variables
        admin_email = request.form['admin_email']
        admin_password = request.form['admin_password']

        # We now move to the db and confirm if above details exists
        sql = "SELECT * FROM admin_tbl where admin_email = %s and admin_password = %s"
        # create a cursor an d execute above sql
        cursor = connection.cursor()
        # execute the sql,provide email and password to fit %s placeholders
        cursor.execute(sql, (admin_email, admin_password))

    # Check if match was found
        if cursor.rowcount == 0:
            flash("Wrong credentials")
            return render_template('dashboard.html', error='Wrong credentials')
        elif cursor.rowcount == 1:
            # create a user to track who is logged in
            # Attach user email to the session
            session['admin'] = admin_email
            flash("Admin logged in successfuly")
            return redirect('/dashboard')
        else:
            flash("Error Occured,Try later")
            return render_template('dashboard.html', error='Error Occured,Try later')

    else:
        flash("Please Login")
        return render_template('dashboard.html')

@app.route('/customer')
def customer():
    if 'admin' in session:
        sql = "SELECT * FROM customers_tbl ORDER BY reg_date DESC"
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return render_template('customer.html', msg = 'No Customers')
        else:
            rows = cursor.fetchall()
            return render_template('customer.html', rows = rows)
    else:
        return redirect('/admin')

@app.route('/adminlogout')
def adminlogout():
    session.pop('admin')
    flash("Admin session ended")
    return redirect('/admin') #clear session
@app.route('/dashboard')
def dashboard():
        sql = "select * from dashboard_tbl"
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return render_template('dashboard.html', msg='No parcels')
        else:
            rows = cursor.fetchall()
            return render_template('dashboard.html', rows = rows)

@app.route('/order')
def order():
    if 'admin' in session:
        sql = "SELECT * FROM courier_tbl"
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return render_template('order.html', msg = 'No Customers')
        else:
            rows = cursor.fetchall()
            return render_template('order.html', rows = rows)
    else:
        return redirect('/admin')

@app.route('/same')
def same():
    if 'admin' in session:
        sql = "SELECT * FROM sameday_tbl"
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return render_template('same.html', msg = 'No Customers')
        else:
            rows = cursor.fetchall()
            return render_template('same.html', rows = rows)
    else:
        return redirect('/admin')

@app.route('/customer_del/<customer_id>')
def customer_del(customer_id):
    if 'admin' in session:
        sql = "delete from customers_tbl where customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (customer_id))
        flash("Deleted successfully")
        return redirect('/customer')
    else:
        return redirect('/admin')

@app.route('/customer_update/<customer_id>',methods = ['POST','GET'])
def customer_update(customer_id):
    if request.method == 'POST':
        customer_fname = request.form['customer_fname']
        customer_lname = request.form['customer_lname']
        customer_username = request.form['customer_username']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_password = request.form['customer_password']
        customer_gender = request.form['customer_gender']
        customer_address = request.form['customer_address']
        sql = "UPDATE customers_tbl SET customer_fname = %s ,customer_lname = %s,customer_username = %s,customer_email= %s,customer_phone = %s,customer_password = %s,customer_gender = %s,customer_address = %s WHERE customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (customer_fname, customer_lname, customer_username, customer_email, customer_phone, customer_password,
        customer_gender, customer_address,customer_id))
        connection.commit()
        flash("Customer Updated Successfully")
        return redirect('/customer')

    else:

        sql = "SELECT * FROM customers_tbl where customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (customer_id))
        row = cursor.fetchone()
        return render_template('customer.html', row=row)
        #return redirect('/admin')


@app.route('/insert', methods = ['POST', 'GET'])
def insert():
    if request.method == 'POST':
        customer_fname = request.form['customer_fname']
        customer_lname = request.form['customer_lname']
        customer_username = request.form['customer_username']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_password = request.form['customer_password']
        customer_gender = request.form['customer_gender']
        customer_address = request.form['customer_address']
        sql = "INSERT INTO customers_tbl(customer_fname,customer_lname,customer_username,customer_email,customer_phone,customer_password,customer_gender,customer_address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor= connection.cursor()
        cursor.execute(sql, (customer_fname, customer_lname, customer_username, customer_email, customer_phone, customer_password,
        customer_gender, customer_address))
        connection.commit()
        flash("Customer added Successfully")
        return redirect('/customer')

    else:
         return redirect('/admin')

if(__name__ == '__main__'):
    app.run(debug=True)

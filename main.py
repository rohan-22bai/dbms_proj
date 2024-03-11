from flask import Flask, render_template, request, redirect, session
import mysql.connector as ms

conn = ms.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="rohan",
    database="dbms_proj"
)

if conn.is_connected():
    print("Hi")

mc = conn.cursor()

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template("home.html")

@app.route('/signup')
def signup_page():
    return render_template("signup.html")

@app.route('/login')
def success_page():
    return render_template("login.html")

@app.route('/dashboard', methods=['POST'])
def dashboard_page():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        # Replace 'your_table_name' with the actual name of your table
        mc.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, passwd))
        result = mc.fetchall()
        conn.commit()  # Call the function to commit the transaction
        if result:
            print(result)
            return render_template("dashboard.html", result=result)
        else:
            err = "Invalid username or password!"
            return render_template("login.html", err=err)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

import psycopg2
from flask import Flask, request, jsonify, render_template, session
#from werkzeug.security import generate_password_hash, check_password_hash
from Adapter import Adapter

db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")


app = Flask(__name__)
app.secret_key = 'dasoida327163821'

@app.route('/registration',methods=['POST','GET'])
def registration_page():
    return render_template('registration.html')

@app.route('/deleting_user')
def delete_page():
    return render_template('deleting_user.html')

@app.route('/loggingin')
def login_page():
    return render_template('login.html')



@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    user = db.select_sth_by_condition(sth="*",table="users",condition=f"username = '{username}'")
    if not(user):
        db.insert("users","username, password",f"'{username}', '{password}'")
        return jsonify({'message': 'User registered successfully'})
    else:
        return jsonify({'message': 'Username is taken'})

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    user = db.select_sth_by_condition(sth="*",table="users",condition=f"username = '{username}' AND password = '{password}'")
    
    if user:
        session['id'] = str(db.select_sth_by_condition(sth="id",table="users",condition=f"username = '{username}' AND password = '{password}'"))[2:-3]
        print(session.get('id'))
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'})

@app.route('/account')
def account_info():
    id = session.get('id')
    if id:
        return render_template('account.html',data_list=db.select_sth_by_condition(sth="*",table="users",condition=f"id = {id}"))
    else:
        return render_template('login.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    id = session.get('id')
    if id:
        db.delete_by_id(table="users",id=id)
        session.pop('id',None)
        return jsonify({'message': "user deleted sucessfuly"})
    else:
        return render_template('/login')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
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
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    username = request.form['username']
    password = request.form['password']
    user = db.select_sth_by_condition(sth="*",table="users",condition=f"username = '{username}'")
    if not(user):
        db.hash_insert(username=username,password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
        del db
        return render_template('login.html')
    else:
        return render_template('registration.html',data="Имя пользователя занято!")

@app.route('/login', methods=['POST'])
def login_user():
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    username = request.form['username']
    password = request.form['password']
    user = db.select_sth_by_condition(sth="*",table="users",condition=f"username = '{username}' ")
    user = list(str(user).split(", "))
    check = check_password_hash(user[2][1:-3],password)
    if user and check:
        session.pop('id',None)
        session['id'] = user[0][2:]
        data_list=db.select_sth_by_condition(sth="username",table="users",condition=f"id = {session.get('id')}")
        del db
        return render_template('account.html',data_list=data_list)
    else:
        return render_template('login.html',data="Неверное имя пользователя или пароль")

@app.route('/account')
def account_info():
    id = session.get('id')
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    if id:
        data_list=db.select_sth_by_condition(sth="username",table="users",condition=f"id = {id}")
        return render_template('account.html',data_list=data_list)
    else:
        return render_template('login.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    id = session.get('id')
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    if id:
        db.delete_by_id(table="users",id=id)
        session.pop('id',None)
        del db
        return jsonify({'message': "user deleted sucessfuly"})
    else:
        return render_template('login.html')

@app.route('/change_username',methods=['POST','GET'])
def usrchng_loadpage():
    return render_template('usernamechange.html')

@app.route('/usrchng', methods=['POST'])
def username_change():
    db = Adapter(schema="Blue_project",host="rc1d-9cjee2y71olglqhg.mdb.yandexcloud.net",port="6432",dbname="sch58_db",sslmode="verify-full",user="Admin",password="atdhfkm2024",target_session_attrs="read-write")
    username = request.form['username']
    id = session.get('id')
    db.update(table="users",request=f"username = '{username}'",id=id)
    data_list=db.select_sth_by_condition(sth="*",table="users",condition=f"id = {id}")
    del db
    return render_template('account.html',data_list=data_list)

if __name__ == '__main__':
    app.run(debug=True)
from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="toko_boneka",
    password="")

userAdmin = {
    "username" : "admin",
    "password" : "1234"
}

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from user where username = %s and password = md5(%s) ")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    password = request.form['password']
    if username == userAdmin["username"]and password == userAdmin["password"]:
        session["user"] = username
        return redirect(url_for("home"))
    else:
        return f"Username atau Password salah...!"
    
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

    
@app.route('/home')
def home():
        return render_template("home.html")

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    cursor = mydb.cursor()
    pembeli = request.form["pembeli"]
    boneka = request.form["boneka"]
    jumlah = request.form["jumlah"]

    query = ("insert into toko values( %s, %s, %s, %s, %s)")
    data = ( "", pembeli, boneka, jumlah )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect("/tampil")

@app.route('/tampil')
def tampil():
    cursor = mydb.cursor()
    cursor.execute("select * from toko")
    data = cursor.fetchall()
    return render_template('tampil.html',data=data) 

@app.route('/hapus/<id>')
def hapus(id):
    cursor = mydb.cursor()
    query = ("delete from toko where id = %s")
    data = (id,)
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect('/tampil')

    

@app.route('/update/<id>')
def update(id):
    cursor = mydb.cursor()
    query = ("select * from toko where id = %s")
    data = (id,)
    cursor.execute( query, data )
    value = cursor.fetchone()
    return render_template('update.html',value=value) 

@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    cursor = mydb.cursor()
    id = request.form["id"]
    pembeli = request.form["pembeli"]
    boneka = request.form["boneka"]
    jumlah = request.form["jumlah"]

    query = ("update toko set pembeli = %s, boneka = %s, jumlah = %s where id = %s")
    data = ( pembeli, boneka, jumlah, id, )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect('/tampil')
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'appLogin'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'dbvertex'

mysql = MySQL(app)

@app.route('/ingresar', methods=["GET", "POST"])
def ingresar():
    if request.method=="GET":
        if 'username' in session:
            print("Entraste")
            return render_template('home.html')
        else:
            print("No entraste")
            return render_template('login.html')
    else:
        nombre = request.form['username']
        contra = request.form['password']
        contra_encode = contra.encode("utf-8")
        print(contra_encode)

        cur = mysql.connection.cursor()

        cur.callproc('autenticar', [nombre])

        usuario = cur.fetchone()

        cur.close()

        if(usuario != None):
            contra_encriptado_encode = usuario[1].encode()
            print(contra_encriptado_encode)
            if(contra_encode == contra_encriptado_encode):
                session['username'] = usuario[0]
                return render_template('home.html')
            else:
                flash("Ha ingresado mal sus datos, ingrese de nuevo")
                return render_template('login.html')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('login.html')

@app.route('/juegos')
def juegos():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('verJuegos')
        data = cur.fetchall()
        cur.close()

        return render_template('juegos.html', juegos = data)
    else:
        return render_template('login.html')

@app.route('/crearjuego', methods = ['GET','POST'])
def crearjuego():
    if 'username' in session:
        if request.method == "POST":
            try:
                fabricante = request.form['fabricante']
                duracion = request.form['duracion']
                version = request.form['version']
                idioma = request.form['idioma']
                nombre = request.form['nombre']
                internet = request.form['internet']
                descripcion = request.form['descripcion']
                jugadores = request.form['jugadores']
                inicio = request.form['inicio']
                final = request.form['final']

                args = (fabricante,duracion,version,idioma,nombre,internet,descripcion,jugadores,inicio,final)
                cursor = mysql.connection.cursor()
                cursor.callproc('crearJuego', args)
                mysql.connection.commit()

                flash("Ha creado el juego correctamente!!!", "success")
                return redirect(url_for('juegos'))
            except:
                flash("No se ha creado el juego correctamente!!!", "danger")
                return redirect('juegos')
        else:
            return render_template('crearjuego.html')
    else:
        return render_template('login.html')

@app.route('/buscarjuego', methods = ['GET', 'POST'])
def buscarjuego():
    if 'username' in session:
        if request.method == "GET":
            cur = mysql.connection.cursor()
            cur.callproc('verJuegos')
            data = cur.fetchall()
            cur.close()
            return render_template('buscarjuego.html', nombres = data)
        else:
            return render_template('juegos.html')
    else:
        return render_template('login.html')

@app.route('/modificarjuego', methods = ['GET', 'POST'])
def modificarjuego():
    if 'username' in session:
        name = request.form.get('nombres')
        if request.method == "GET":
            return redirect(url_for('juegos'))
        else:
            cur = mysql.connection.cursor()
            cur.callproc('verjuego', [name])
            data = cur.fetchall()
            cur.close()
            return render_template('modificarjuego.html', juegos = data)
    else:
        return render_template('login.html')

@app.route('/updatejuego', methods = ['GET','POST'])
def updatejuego():
    if 'username' in session:
        if request.method == "POST":
            try:
                ident = request.form['id']
                fabricante = request.form['fabricante']
                duracion = request.form['duracion']
                version = request.form['version']
                idioma = request.form['idioma']
                nombre = request.form['nombre']
                internet = request.form['internet']
                descripcion = request.form['descripcion']
                jugadores = request.form['jugadores']
                inicio = request.form['inicio']
                final = request.form['final']

                args = (ident, fabricante, duracion, version, idioma, nombre, internet, descripcion, jugadores, inicio, final)
                cursor = mysql.connection.cursor()
                cursor.callproc('modificarjuego', args)

                mysql.connection.commit()

                flash("Ha modificado el juego correctamente!!!", "success")
                return redirect(url_for('juegos'))
            except:
                flash("No se ha modificado el juego correctamente", "danger")
                return redirect('juegos')
        else:
            flash("No se ha modificado el juego correctamente", "danger")
            return redirect('juegos')
    else:
        return render_template('login.html')

@app.route('/clientes', methods = ['GET','POST'])
def clientes():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('verclientes')
        data = cur.fetchall()
        cur.close()

        return render_template('clientes.html', juegos = data)
    else:
        return render_template('login.html')

@app.route('/crearcliente', methods = ['GET', 'POST'])
def crearcliente():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('vertiposcliente')
        data = cur.fetchall()
        cur.close()
        if request.method == "POST":
            try:
                nombres = request.form['nombres']
                apellidos = request.form['apellidos']
                fecha = request.form['cumple']
                correo = request.form['correo']
                celular = request.form['celular']
                rango = request.form['rango']
                tipo = request.form['tipocliente']

                args = (nombres, apellidos, fecha, correo, celular, rango, tipo)
                cursor = mysql.connection.cursor()
                cursor.callproc('crearcliente', args)
                mysql.connection.commit()

                flash("Ha creado el cliente correctamente!!!", "success")
                return redirect(url_for('clientes'))
            except:
                flash("No se ha creado el cliente correctamente", "danger")
                return redirect('clientes')
        return render_template('crearcliente.html', tipos = data)
    else:
        return render_template('login.html')

@app.route('/gafas')
def gafas():
    if 'username' in session:
        return render_template('gafas.html')
    else:
        return render_template('login.html')

@app.route('/eventos')
def eventos():
    if 'username' in session:
        return render_template('eventos.html')
    else:
        return render_template('login.html')

@app.route('/salir')
def salir():
    session.clear()

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
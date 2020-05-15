from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'appLogin'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 1433
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'dbvertex'

mysql = MySQL(app)

@app.route('/ingresar', methods=["GET", "POST"])
def ingresar():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usuario WHERE Nombre = %s AND Pass = %s', (username, password,))
        usuario= cur.fetchone()
        if usuario:
            session['loggedin'] = True
            session['username'] = usuario['Nombre']
            return render_template('home.html')
        else:

            flash("Ha ingresado mal sus datos, ingrese de nuevo")
            return render_template('login.html')

    return render_template('login.html')


@app.route('/')
def index():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('verproxeventos')
        data = cur.fetchall()
        cur.close()

        cursor = mysql.connection.cursor()
        cursor.callproc('vereventospasados')
        datos = cursor.fetchall()
        cursor.close()
        return render_template('home.html', proximos = data, pasados = datos)
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

        cursor = mysql.connection.cursor()
        cursor.callproc('vertiposcliente')
        datos = cursor.fetchall()
        cursor.close()

        return render_template('clientes.html', clientes = data, tipos = datos)
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

@app.route('/buscarcliente', methods=['GET','POST'])
def buscarcliente():
    if 'username' in session:
        if request.method == "GET":
            cur = mysql.connection.cursor()
            cur.callproc('verclientes')
            data = cur.fetchall()
            cur.close()
            return render_template('buscarcliente.html', clientes = data)
        else:
            return render_template('clientes.html')
    else:
        return render_template('login.html')

@app.route('/modificarcliente', methods=['GET','POST'])
def modificarcliente():
    if 'username' in session:
        if request.method == "POST":
            name = request.form['id']
            cur = mysql.connection.cursor()
            cur.callproc('vercliente', [name])
            data = cur.fetchall()
            cur.close()

            cursor = mysql.connection.cursor()
            cursor.callproc('vertiposcliente')
            tipo = cursor.fetchall()
            cursor.close()
            return render_template('modificarcliente.html', clientes = data, tipos = tipo)
        else:
            return redirect(url_for('clientes'))
    else:
        return render_template('login.html')

@app.route('/updatecliente', methods=['GET','POST'])
def updatecliente():
    if 'username' in session:
        if request.method == "POST":
            try:
                ident = request.form['id']
                nombres = request.form['nombres']
                apellidos = request.form['apellidos']
                fecha = request.form['cumple']
                correo = request.form['correo']
                celular = request.form['celular']
                rango = request.form['rango']
                tipo = request.form['tipocliente']

                args = (ident, nombres, apellidos, fecha, correo, celular, rango, tipo)

                cursor = mysql.connection.cursor()
                cursor.callproc('modificarCliente', args)

                mysql.connection.commit()

                flash("Ha modificado el cliente correctamente!!!", "success")
                return redirect(url_for('clientes'))
            except:
                flash("No se ha modificado el cliente correctamente", "danger")
                return redirect(url_for('clientes'))
        else:
            flash("No se ha modificado el cliente correctamente", "danger")
            return redirect(url_for('clientes'))
    else:
        return render_template('login.html')

@app.route('/gafas')
def gafas():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('verGafas')
        data = cur.fetchall()
        cur.close()

        cursor = mysql.connection.cursor()
        cursor.callproc('vertipogafas')
        datos = cursor.fetchall()
        cursor.close()
        return render_template('gafas.html', gafas=data, tipos=datos)
    else:
         return render_template('login.html')

@app.route('/creargafas', methods = ['GET','POST'])
def creargafas():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('vertipogafas')
        data = cur.fetchall()
        cur.close()
        if request.method == "POST":
            try:
                fechaCompra = request.form['fechaCompra']
                versionS = request.form['versionS']
                vidaUtil = request.form['vidaUtil']
                Horas = request.form['Horas']
                SerialF = request.form['SerialF']
                SerialI = request.form['SerialI']
                SerialO = request.form['SerialO']
                Modelo = request.form['Modelo']

                if versionS == "" or vidaUtil == "" or SerialF == "" or SerialI == "" or SerialO == "":
                    flash("No ha llenado los campos completamente!!!", "danger")
                    return redirect('gafas')
                else:
                    args = (fechaCompra, versionS, vidaUtil, Horas, SerialF, SerialI, SerialO, Modelo)
                    cursor = mysql.connection.cursor()
                    cursor.callproc('crearGafas', args)
                    mysql.connection.commit()

                    flash("Ha adicionado las gafas correctamente!!!", "success")
                    return redirect(url_for('gafas'))
            except:
                flash("No se han adicionado las gafas correctamente!!!", "danger")
                return redirect('gafas')
        return render_template('creargafas.html', gafas=data)
    else:
        return render_template('login.html')

@app.route('/buscargafas', methods = ['GET', 'POST'])
def buscargafas():
    if 'username' in session:
        if request.method == "GET":
            cur = mysql.connection.cursor()
            cur.callproc('verGafas')
            data = cur.fetchall()
            cur.close()
            return render_template('buscargafas.html', gafas = data)
        else:
            return render_template('gafas.html')
    else:
        return render_template('login.html')

@app.route('/creartipogafa', methods=['GET', 'POST'])
def creartipogafa():
    if 'username' in session:
        if request.method == "POST":
            modelo = request.form['Modelo']
            almacenamiento = request.form['Almacenamiento']
            try:
                args = (modelo, almacenamiento)
                cur = mysql.connection.cursor()
                cur.callproc('creartipogafa', args)
                mysql.connection.commit()

                flash("Ha adicionado el modelo de gafas correctamente!!!", "success")
                return redirect(url_for('gafas'))

            except:
                flash("No ha adicionado el modelo de gafas correctamente!!!", "danger")
                return redirect(url_for('gafas'))
        return render_template('crearmodelogafas.html')
    else:
        return render_template('login.html')

@app.route('/modificargafas', methods = ['GET', 'POST'])
def modificargafas():
    if 'username' in session:
        name = request.form.get('gafas')
        if request.method == "GET":
            return redirect(url_for('gafas'))
        else:
            cur = mysql.connection.cursor()
            cur.callproc('vergafa', [name])
            data = cur.fetchall()
            cur.close()
            return render_template('modificargafas.html', gafas = data)
    else:
        return render_template('login.html')

@app.route('/updateGafas', methods = ['GET','POST'])
def updategafas():
    if 'username' in session:
        if request.method == "POST":
            try:
                ident = request.form['id']
                fechaCompra = request.form['fechaCompra']
                versionS = request.form['versionS']
                vidaUtil = request.form['vidaUtil']
                Horas = request.form['Horas']
                SerialF = request.form['SerialF']
                SerialI = request.form['SerialI']
                SerialO = request.form['SerialO']
                Modelo = request.form['modelo']

                args = (ident, fechaCompra, versionS, vidaUtil, Horas, SerialF, SerialI, SerialO, Modelo)
                cursor = mysql.connection.cursor()
                cursor.callproc('modificargafas', args)
                mysql.connection.commit()

                flash("Ha Modificado las gafas correctamente!!!", "success")
                return redirect(url_for('gafas'))
            except:
                flash("No se han Modificado las gafas correctamente!!!", "danger")
                return redirect('gafas')
        else:
            return render_template('creargafas.html')
    else:
        return render_template('login.html')

@app.route('/eventos')
def eventos():
  if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('vereventos')
        data = cur.fetchall()
        cur.close()
        return render_template('eventos.html', eventos = data)
  else:
         return render_template('login.html')

@app.route('/crearevento', methods = ['GET','POST'])
def crearevento():
    if 'username' in session:
        if request.method == "POST":
            try:
                fecha= request.form['fecha']
                Hora = request.form['Hora']
                Duracion = request.form['Duracion']
                Npersonas= request.form['Npersonas']
                Eventocor= request.form['Eventocor']
                Lugar= request.form['Lugar']
                Opinion=request.form['Opinion']
                args = (fecha, Hora, Duracion, Npersonas, Eventocor, Lugar, Opinion )
                cursor = mysql.connection.cursor()
                cursor.callproc('crearEvento', args)
                mysql.connection.commit()

                flash("Ha adicionado el evento correctamente!!!", "success")
                return redirect(url_for('eventos'))
            except:
                flash("No se han adicionado las gafas correctamente!!!", "danger")
                return redirect('eventos')
        else:
            return render_template('crearevento.html')
    else:
        return render_template('login.html')


@app.route('/buscarevento', methods = ['GET', 'POST'])
def buscarevento():
    if 'username' in session:
        if request.method == "GET":
            cur = mysql.connection.cursor()
            cur.callproc('vereventos')
            data = cur.fetchall()
            cur.close()
            return render_template('buscarevento.html', eventos = data)
        else:
            return render_template('eventos.html')
    else:
        return render_template('login.html')


@app.route('/modificarevento', methods = ['GET', 'POST'])
def modificarevento():
    if 'username' in session:
        ident = request.form.get('nombres')
        if request.method == "GET":
            return redirect(url_for('eventos'))
        else:
            cur = mysql.connection.cursor()
            cur.callproc('verEvento', [ident])
            data = cur.fetchall()
            cur.close()
            return render_template('modificarevento.html', eventos = data)
    else:
        return render_template('login.html')


@app.route('/updateeventos', methods = ['GET','POST'])
def updateeventos():
    if 'username' in session:
        if request.method == "POST":
            try:
                ident = request.form['id']
                Fecha = request.form['fecha']
                Hora = request.form['Hora']
                Duracion = request.form['Duracion']
                Npersonas = request.form['Npersonas']
                Eventocor = request.form['Eventocor']
                Lugar = request.form['Lugar']
                Opinion = request.form['Opinion']

                args = (ident, Fecha, Hora, Duracion, Npersonas, Eventocor, Lugar, Opinion )
                cursor = mysql.connection.cursor()
                cursor.callproc('modificarEvento', args)
                mysql.connection.commit()

                flash("Ha Modificado el evento correctamente!!!", "success")
                return redirect(url_for('eventos'))
            except:
                flash("No se han Modificado el evento correctamente!!!", "danger")
                return redirect('eventos')
        else:
            return render_template('crearevento.html')
    else:
        return render_template('login.html')        

@app.route('/juegosgafas')
def juegosgafas():
  if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('vereventos')
        data = cur.fetchall()
        cur.close()
        return render_template('juegosgafas.html', eventos = data)
  else:
         return render_template('login.html')

@app.route('/juegosclientes')
def juegosclientes():
  if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('vereventos')
        data = cur.fetchall()
        cur.close()
        return render_template('juegosclientes.html', eventos = data)
  else:
         return render_template('login.html')

@app.route('/juegoseventos')
def juegoseventos():
  if 'username' in session:
        cur = mysql.connection.cursor()
        cur.callproc('vereventos')
        data = cur.fetchall()
        cur.close()
        return render_template('juegoseventos.html', eventos = data)
  else:
         return render_template('login.html')

@app.route('/salir')
def salir():
    session.clear()

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort, Response
import psycopg2
from calculo_precios import calculotunning, calculocompramos, calculopintura, calculovendemos, calculoestetica, calculomotor, calculocontrato
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from functools import wraps



app = Flask(__name__)
app.config.update(DEBUG = True, SECRET_KEY = b'\xf0!\x06\xce\xdd\xf5r\x82\xc9.!\n\x1e\xed\xdb.')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



# SQL CONNECTION
dbname = 'concetaller'
host = 'localhost'
port = '3306'
user = 'root'
pwd = ''

#connection = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=pwd)

try:
    connection = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=pwd)
    cur2 = connection.cursor()
    cur2.execute("SELECT * FROM stock_coches JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE en_venta = TRUE ORDER by nombre ASC")
except psycopg2.InterfaceError as err:
    connection = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=pwd)
    cur = connection.cursor()
    cur.execute("SELECT * FROM stock_coches JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE en_venta = TRUE ORDER by nombre ASC")

#SETTINGS
app.secret_key = b'\xf0!\x06\xce\xdd\xf5r\x82\xc9.!\n\x1e\xed\xdb.'

################################################################################################################################


class User(UserMixin):
	def __init__(self, id):
		self.id = id

	def get_id(self):         
		return str(self.id)

#Mock user database
users = {'admin': {'admin': 'somoslosjefes', 'role': 'Admin'},
		    'Mecanico': {'Mecanico': '1234', 'role': 'Mecanico'}}


def admin_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		user = current_user.get_id()
		if users[user]['role'] == "Admin":
			return f(*args, **kwargs)
		else:
			flash("Necesitas ser administrador para acceder a esta pagina.")
			return redirect(url_for('login'))

	return wrap
	


 
#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		
		username = request.form['Correo Electronico']
		password = request.form['Contraseña']
		#CHECK
		if username in users and password == users[username][username]:
			user = User(id=username)
			login_user(user)
			return redirect(url_for('Inicio'))
		return redirect(url_for('login'))
		
	return render_template("login.html")


#LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    flash("Has finalizado la sesión con éxito.")
    return redirect(url_for('login'))
#---------------------------------------------------------------


#CALLBACK TO RELOAD     
@login_manager.user_loader
def load_user(userid):
    return User(userid)




################################################################################################################################

#Inicio1
@app.route('/')
def Inicio():
    return render_template("inicio.html")

#Inicio 2   
@app.route('/inicio')
def Inicio2():
    return render_template("inicio.html")








#Register
@app.route('/registro')
def registro():
    return render_template("registro.html")

#Añadir usuarios base de datos
@app.route('/add_register', methods=["POST", "GET"])
def add_register():
    if request.method == "POST":
        nombre = request.form["Usuario"]
        email = request.form["Correo Electronico"]
        password = request.form["Password"]
        cur = connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email, pass) VALUES (%s, %s, %s)",(nombre, email, password))
        connection.commit()
        
        flash("Usuario registrado con éxito.", category='success')
        return redirect(url_for('registro'))







#Visual servicios mecanicos
@app.route('/serviciosmec')
@login_required
def serviciosmec():
    cur = connection.cursor()
    cur.execute("SELECT * FROM empleados ORDER by nombre_ic ASC")
    data = cur.fetchall()
    cur2 = connection.cursor()
    cur2.execute("SELECT * FROM servicios ORDER by tipo_servicio ASC")
    data2 = cur2.fetchall()
    cur3 = connection.cursor()
    cur3.execute("SELECT * FROM clientes ORDER by nombre ASC")
    data3 = cur3.fetchall()
    return render_template("serviciosmec.html", mecanicos = data, servicios = data2, clientes = data3)

#Añadir servicios mecanicos
@app.route('/add_serviciosmec/', methods=["POST", "GET"])
@login_required
def add_serviciosmec():
    if request.method == "POST":
        
        empleado = request.form["Nombre Mecanico"] #DOY NOMBRE PERO NECESITO ID_EMPLEADO
        cur = connection.cursor()
        cur.execute("SELECT id_empleado FROM empleados WHERE lower(nombre_ic) = lower('" + empleado + "')")
        id_mecanico = cur.fetchall()[0]
        print(cur.fetchall)

        cliente  = request.form["Nombre Cliente"] #DOY NOMBRE PERO NECESITO ID_CLIENTE
        cur2 = connection.cursor()
        cur2.execute("SELECT id_cliente FROM clientes WHERE lower(nombre) = lower('" + cliente + "')")
        id_cliente = cur2.fetchall()[0]
        print(cur.fetchall)

        servicio = request.form["Tipo de Servicio"] #DOY servicio PERO NECESITO LA id_servicko
        cur3 = connection.cursor()
        cur3.execute("SELECT id_servicio FROM servicios WHERE lower(tipo_servicio) = lower('" + servicio + "')")
        id_servicio = cur3.fetchall()[0]
        print(cur3.fetchall)

        cantidad = request.form["Cantidad"]

        precioserviciocobrado = request.form["Precio a cobrar"]


        cur4 = connection.cursor()
        cur4.execute("INSERT INTO servicios_mec (id_mecanico, id_cliente, id_servicio, cantidad, precio_servicio_cobrado) VALUES (%s, %s, %s, %s, %s)",(id_mecanico, id_cliente, id_servicio, cantidad, precioserviciocobrado))
        connection.commit()
       
     
        flash("Servicio facturado con éxito.", category='success')
        return redirect(url_for('serviciosmec'))

#Editar servicio mecanico
@app.route('/serviciosmec/<id>')
@login_required
def get_serviciosmec(id):
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur5 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE id_stock = {0}".format(id))
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo")
    cur5.execute("SELECT * FROM clientes ORDER by nombre")
    data5 = cur.fetchall()
    data6 = cur2.fetchall()

    data9 = cur5.fetchall()
    print(data5[0])
    print(data6)
    return render_template("serviciosmec.html",  stock = data5[0], vehiculos = data6, clientes = data9)


#Visual gestoria   
@app.route('/gestoria')
@login_required
@admin_required
def transferencias():
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM modelo_coches ORDER by nombre ASC")
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo ORDER by nombre ASC")
    datatres = cur.fetchall()
    datacuatro = cur2.fetchall()
    print(datatres)
    print(datacuatro)
    return render_template("gestoria.html", vehiculos = datatres, stocks = datacuatro)

#añadir trasnferencia
@app.route('/add_transferencia/<id>', methods=["POST", "GET"])
@login_required
@admin_required
def add_transferencia(id):
    if request.method == "POST":
        
        antiguopropietario = request.form["Antiguo Propietario"] #DOY NOMBRE PERO NECESITO ID_CLIENTE
        cur = connection.cursor()
        cur.execute("SELECT id_cliente FROM clientes WHERE lower(nombre) = lower('" + antiguopropietario + "')")
        id_cliente1 = cur.fetchall()[0]
        print(cur.fetchall)

        nuevopropietario  = request.form["Nuevo Propietario"] #DOY NOMBRE PERO NECESITO ID_CLIENTE
        cur2 = connection.cursor()
        cur2.execute("SELECT id_cliente FROM clientes WHERE lower(nombre) = lower('" + nuevopropietario + "')")
        id_cliente2 = cur2.fetchall()[0]
        print(cur.fetchall)

        matricula = request.form["Matricula"] #DOY MATRICULA PERO NECESITO LA ID_STOCK
        cur3 = connection.cursor()
        cur3.execute("SELECT id_stock FROM stock_coches WHERE lower(matricula) = lower('" + matricula + "')")
        id_stock = cur3.fetchall()[0]
        print(cur3.fetchall)

        preciotransferencia = request.form["Precio de transferencia final"]

        cur4 = connection.cursor()
        cur4.execute("INSERT INTO gestoria (id_cliente_vendedor, id_cliente_comprador, id_stock, precio_transferencia) VALUES (%s, %s, %s, %s)",(id_cliente1, id_cliente2, id_stock, preciotransferencia))
        connection.commit()
       
        flash("Vehiculo transferido con éxito.", category='success')
        return redirect(url_for('taller'))

# editar transferencia
@app.route('/transferencia/<id>')
@login_required
@admin_required
def get_transferencia(id):
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur5 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE id_stock = {0}".format(id))
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo")
    cur5.execute("SELECT * FROM clientes ORDER by nombre")
    data5 = cur.fetchall()
    data6 = cur2.fetchall()

    data9 = cur5.fetchall()
    print(data5[0])
    print(data6)
    return render_template("transferencia.html",  stock = data5[0], vehiculos = data6, clientes = data9)



#Visual coches comprados
@app.route('/coches_comprados')
@login_required
@admin_required
def coches_comprados():
    cur = connection.cursor()
    cur.execute("SELECT * FROM compras INNER JOIN empleados ON compras.id_empleado = empleados.id_empleado INNER JOIN stock_coches ON compras.id_stock = stock_coches.id_stock INNER JOIN modelo_coches ON modelo_coches.id_modelo = stock_coches.id_modelo ORDER by id_compra DESC")
    data = cur.fetchall()
    return render_template("coches_comprados.html", compras = data)


#Visual coches vendidos
@app.route('/coches_vendidos')
@login_required
@admin_required
def coches_vendidos():
    cur = connection.cursor()
    cur.execute("SELECT * FROM ventas INNER JOIN empleados ON ventas.id_empleado = empleados.id_empleado INNER JOIN stock_coches ON ventas.id_stock = stock_coches.id_stock INNER JOIN modelo_coches ON modelo_coches.id_modelo = stock_coches.id_modelo ORDER by id_venta DESC")
    data = cur.fetchall()
    return render_template("coches_vendidos.html", ventas = data)


#Visual coches transferidos
@app.route('/coches_transferidos')
@login_required
@admin_required
def coches_transferidos():
    cur = connection.cursor()
    cur.execute("SELECT * FROM gestoria ORDER by id_transferencia ASC")
    data = cur.fetchall()
    return render_template("coches_transferidos.html", transferencias = data)



# Visual movimientos compraventa
@app.route('/mov_compraventa')
@login_required
@admin_required
def mov_compraventa():
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM mov_compraventa ORDER by id_movcomp ASC")
    cur2.execute("SELECT SUM(movcomp) FROM mov_compraventa")
    data = cur.fetchall()
    data2 = cur2.fetchall()
    return render_template("mov_compraventa.html", movimientos = data, totales = data2)

# Añadir movimiento compraventa
@app.route('/add_movcompra', methods=["POST"])
@login_required
@admin_required
def add_movcompra():
    if request.method == "POST":
        cantidad = int(request.form["Ingresar Importe"])
        concepto = request.form["Concepto"]
        cur = connection.cursor()
        cur.execute('INSERT INTO mov_compraventa (movcomp, concepto) VALUES (%s, %s)',(cantidad, concepto ))
        connection.commit()
        flash("Movimiento agregado con exito.", category='success')
        return redirect(url_for('mov_compraventa'))

# Visual movimientos taller mecanico
@app.route('/mov_tallermecanico')
@login_required
@admin_required
def mov_tallermecanico():
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM mov_mecanicos ORDER by id_movtaller ASC")
    cur2.execute("SELECT SUM(movtaller) FROM mov_mecanicos")
    data = cur.fetchall()
    data2 = cur2.fetchall()
    return render_template("mov_tallermecanico.html", movimientos = data, totales = data2)


# Añadir movimiento taller
@app.route('/add_movtaller', methods=["POST"])
@login_required
@admin_required
def add_movtaller():
    if request.method == "POST":
        cantidad = int(request.form["Ingresar Importe"])
        concepto = request.form["Concepto"]
        cur = connection.cursor()
        cur.execute('INSERT INTO mov_mecanicos (movtaller, concepto) VALUES (%s, %s)',(cantidad, concepto))
        connection.commit()
        flash("Movimiento agregado con exito.", category='success')
        return redirect(url_for('mov_tallermecanico'))

@app.route('/estadisticas')
@login_required
@admin_required
def estadisticas():
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur3 = connection.cursor()
    cur4 = connection.cursor()
    cur5 = connection.cursor()
    cur6 = connection.cursor()
    cur7 = connection.cursor()
    cur.execute("SELECT SUM(movcomp) FROM mov_compraventa")
    cur2.execute("SELECT SUM(precio_venta) FROM ventas")
    cur3.execute("SELECT SUM(precio_compra) FROM compras")
    cur4.execute("SELECT SUM(movtaller) FROM mov_mecanicos")
    cur5.execute("SELECT SUM(precio_cobrado) FROM reparaciones")
    cur6.execute("SELECT SUM(precio_transferencia) FROM gestoria")
    cur7.execute("SELECT SUM(precio_servicio_cobrado) FROM servicios_mec")
    data = cur.fetchall()
    data2 = cur2.fetchall()
    data3 = cur3.fetchall()
    data4 = cur4.fetchall()
    data5 = cur5.fetchall()
    data6 = cur6.fetchall()
    data7 = cur7.fetchall()
    
    return render_template("estadisticas.html", movimientos = data, ventas = data2, compras = data3, movimientosdos = data4, tuneos = data5, transferencias = data6, servicios = data7)

#Visual taller
@app.route('/taller')
@login_required
def taller():
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM modelo_coches ORDER by nombre ASC")
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo ORDER by nombre ASC")
    datatres = cur.fetchall()
    datacuatro = cur2.fetchall()
    print(datatres)
    print(datacuatro)
    return render_template("taller.html", vehiculos = datatres, stocks = datacuatro)

#Añadir tunear coche
@app.route('/add_tunning/<id>', methods=["POST", "GET"])
@login_required
def add_tunning(id):
    if request.method == "POST":
        
        id_servicio = 3

        empleado = request.form["Nombre Mecanico"] #DOY NOMBRE PERO NECESITO ID_EMPLEADO
        cur = connection.cursor()
        cur.execute("SELECT id_empleado FROM empleados WHERE lower(nombre_ic) = lower('" + empleado + "')")
        id_empleado = cur.fetchall()[0]
        print(cur.fetchall)

        cliente = request.form["Nombre Cliente"] #DOY NOMBRE PERO NECESITO ID_CLIENTE
        cur2 = connection.cursor()
        cur2.execute("SELECT id_cliente FROM clientes WHERE lower(nombre) = lower('" + cliente + "')")
        id_cliente = cur2.fetchall()[0]
        print(cur.fetchall)

        matricula =  request.form["Matricula"] #DOY MATRICULA PERO NECESITO LA ID_STOCK
        cur3 = connection.cursor()
        cur3.execute("SELECT id_stock FROM stock_coches WHERE lower(matricula) = lower('" + matricula + "')")
        id_stock = cur3.fetchall()[0]
        print(cur3.fetchall)


        precio_cobrado = request.form["total"]

        cur4 = connection.cursor()
        cur4.execute("INSERT INTO reparaciones (id_servicio, id_empleado, id_cliente, id_stock, precio_cobrado) VALUES (%s, %s, %s, %s, %s)",(id_servicio, id_empleado, id_cliente, id_stock, precio_cobrado))
        connection.commit()
       

     
        flash("Vehiculo tuneado con éxito.", category='success')
        return redirect(url_for('taller'))

#Editar tunear coche
@app.route('/tunning/<id>')
@login_required
def get_tunning(id):
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur4 = connection.cursor()
    cur5 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE id_stock = {0}".format(id))
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo")
    cur4.execute("SELECT * FROM empleados ORDER by nombre_ic ASC")
    cur5.execute("SELECT * FROM clientes ORDER by nombre")
    data5 = cur.fetchall()
    data6 = cur2.fetchall()
    data8 = cur4.fetchall()
    data9 = cur5.fetchall()
    print(data5[0])
    print(data6)
    return render_template("tunning.html",  stock = data5[0], vehiculos = data6, empleados = data8, clientes = data9)






# Visual comprar coche
@app.route('/concesionario')
@login_required
@admin_required
def concesionario():
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE en_venta = FALSE ORDER BY nombre")
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE en_venta = TRUE ORDER BY nombre")
    data = cur.fetchall()
    data2 = cur2.fetchall()
    print(data)
    print(data2)
    return render_template("concesionario.html", coches = data, cars = data2)


# Añadir comprar coche
@app.route('/add_compra/<id>', methods=["POST", "GET"])
@login_required
@admin_required
def add_compra(id):
    if request.method == "POST":

        empleado = request.form["Nombre Comprador"] #DOY NOMBRE PERO NECESITO ID_EMPLEADO
        cur = connection.cursor()
        cur.execute("SELECT id_empleado FROM empleados WHERE lower(nombre_ic) = lower('" + empleado + "')")
        id_empleado = cur.fetchall()[0]
        print(cur.fetchall)

        matricula =  request.form["Matricula"] #DOY MATRICULA PERO NECESITO LA ID_STOCK
        cur2 = connection.cursor()
        cur2.execute("SELECT id_stock FROM stock_coches WHERE lower(matricula) = lower('" + matricula + "')")
        id_stock = cur2.fetchall()[0]
        print(cur2.fetchall)

        precio_compra = int(request.form["Precio de compra final"])
        disponibleventa = request.form.get("Disponible para venta", True)
        imagencoche = request.form["Insertar foto"]

        cur3 = connection.cursor()
        cur3.execute("INSERT INTO compras (id_empleado, precio_compra, id_stock) VALUES (%s, %s, %s)",(id_empleado, precio_compra, id_stock))
        connection.commit()
       
        cur4 = connection.cursor()
        cur4.execute("UPDATE stock_coches SET en_venta=%s, foto_stock=%s WHERE id_stock=%s", (disponibleventa, imagencoche, id))
        connection.commit()
     
        flash("Vehiculo comprado con éxito.", category='success')
        return redirect(url_for('concesionario'))


# Editar comprar coche
@app.route('/comprar/<id>')
@login_required
@admin_required
def get_compra(id):
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur3 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE id_stock = {0}".format(id))
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo")
    cur3.execute("SELECT * FROM empleados ORDER by nombre_ic DESC")
    datacinco = cur.fetchall()
    dataseis = cur2.fetchall()
    datasiete = cur3.fetchall()
    print(datacinco[0])
    print(dataseis)
    return render_template("comprar.html",  stock = datacinco[0], vehiculos = dataseis, empleados = datasiete)





# Añadir vender coche
@app.route('/add_venta/<id>', methods=["POST", "GET"])
@login_required
@admin_required
def add_venta(id):
    if request.method == "POST":

        empleado = request.form["Nombre Vendedor"] #DOY NOMBRE PERO NECESITO ID_EMPLEADO
        cur = connection.cursor()
        cur.execute("SELECT id_empleado FROM empleados WHERE lower(nombre_ic) = lower('" + empleado + "')")
        id_empleado = cur.fetchall()[0]
        print(cur.fetchall)

        cliente = request.form["Nombre Cliente"] #DOY NOMBRE PERO NECESITO ID_cliente
        cur = connection.cursor()
        cur.execute("SELECT id_cliente FROM clientes WHERE lower(nombre) = lower('" + cliente + "')")
        id_cliente = cur.fetchall()[0]
        print(cur.fetchall)

        matricula =  request.form["Matricula"] #DOY MATRICULA PERO NECESITO LA ID_STOCK
        cur2 = connection.cursor()
        cur2.execute("SELECT id_stock FROM stock_coches WHERE lower(matricula) = lower('" + matricula + "')")
        id_stock = cur2.fetchall()[0]
        print(cur2.fetchall)

        precio_venta = int(request.form["Precio de venta final"])
        disponibleventa = request.form.get("Disponible para venta", False)

        cur3 = connection.cursor()
        cur3.execute("INSERT INTO ventas (id_cliente, id_empleado, precio_venta, id_stock) VALUES (%s, %s, %s, %s)",(id_cliente, id_empleado, precio_venta, id_stock))
        connection.commit()
       
        cur4 = connection.cursor()
        cur4.execute("UPDATE stock_coches SET en_venta=%s WHERE id_stock=%s", (disponibleventa, id))
        connection.commit()
     
        flash("Vehiculo vendido con éxito.", category='success')
        return redirect(url_for('concesionario'))


# Editar vender coche
@app.route('/vender/<id>')
@login_required
@admin_required
def get_venta(id):
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur3 = connection.cursor()
    cur4 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE id_stock = {0}".format(id))
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo")
    cur3.execute("SELECT * FROM empleados ORDER by nombre_ic DESC")
    cur4.execute("SELECT * FROM clientes ORDER by nombre DESC")
    datacinco = cur.fetchall()
    dataseis = cur2.fetchall()
    datasiete = cur3.fetchall()
    dataocho = cur4.fetchall()
    print(datacinco[0])
    print(dataseis)
    print(datasiete)
    print(dataocho)
    return render_template("vender.html",  stock = datacinco[0], vehiculos = dataseis, trabajadores = datasiete, clientes = dataocho)





#CATALOGO LISTO
@app.route('/catalogo')
def catalogo():
    cur = connection.cursor()
    cur.execute("SELECT * FROM stock_coches JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo WHERE en_venta = TRUE ORDER by nombre ASC")
    data = cur.fetchall()
    print(data)
    return render_template("catalogo.html", stocks = data)



# Editar foto coches stock
@app.route("/foto/<id>")
@login_required
@admin_required
def get_foto(id):
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches WHERE id_stock = {0}".format(id))
    cur2.execute("SELECT * FROM modelo_coches ORDER by nombre ASC")
    datacinco = cur.fetchall()
    dataseis = cur2.fetchall()
    print(datacinco[0])
    print(dataseis)
    return render_template("foto.html",  stock = datacinco[0], vehiculos = dataseis)

#Actualizar foto stock coches
@app.route("/update_foto/<id>", methods = ["POST"])
@login_required
@admin_required
def update_foto(id):
    if request.method == "POST":
        foto = request.form["Foto del vehiculo"]
        cur = connection.cursor()
        cur.execute('UPDATE stock_coches SET foto_stock=%s WHERE id_stock=%s',(foto, id))
        connection.commit()
        flash("Foto modificada con éxito.", category='success')
        return redirect(url_for('concesionario'))



# Visual stock base de datos
@app.route('/alta_vehiculo')
@login_required
def stock():
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM modelo_coches ORDER by nombre ASC")
    cur2.execute("SELECT * FROM stock_coches INNER JOIN modelo_coches ON stock_coches.id_modelo = modelo_coches.id_modelo ORDER by nombre ASC")
    datatres = cur.fetchall()
    datacuatro = cur2.fetchall()
    print(datatres)
    print(datacuatro)
    return render_template("alta_vehiculo.html", vehiculos = datatres, stocks = datacuatro)

# Añadir stock base de datos
@app.route('/add_stock', methods=["POST", "GET"])
@login_required
def add_stock():
    if request.method == "POST":
        modelo = str(request.form.get("Modelo vehículo"))
        cur = connection.cursor()
        cur.execute("Select id_modelo FROM modelo_coches WHERE lower(nombre) = lower('" + modelo + "')")
        id_coche = cur.fetchall()[0]
        print(cur.fetchall)
        matricula = request.form["Matricula"]
        cur = connection.cursor()
        cur.execute("SELECT * FROM stock_coches WHERE lower(matricula) = lower('" + matricula + "')")
        datatres = cur.fetchall()
        disponibleventa = False
    if len(datatres) >0:
        flash("Esta matrícula ya existe en la base de datos.", category='danger')
        return redirect(url_for('stock'))
    else:
        cur.execute('INSERT INTO stock_coches (id_modelo, matricula, en_venta) VALUES (%s, %s, %s)',(id_coche, matricula, disponibleventa))
        connection.commit()
        flash("Matrícula añadida correctamente a la base de datos.", category='success')
        return redirect(url_for('stock'))

# Editar stock base de datos
@app.route('/edittres/<id>')
@login_required
@admin_required
def get_stock(id):
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute("SELECT * FROM stock_coches WHERE id_stock = {0}".format(id))
    cur2.execute("SELECT * FROM modelo_coches ORDER by nombre ASC")
    datacinco = cur.fetchall()
    dataseis = cur2.fetchall()
    print(datacinco[0])
    print(dataseis)
    return render_template("edit_stock.html",  stock = datacinco[0], vehiculos = dataseis)

# Actualizar stock base de datos
@app.route("/updatetres/<id>", methods = ["POST", "GET"])
@login_required
@admin_required
def update_stock(id):
    if request.method == "POST":
        modelo = str(request.form.get("Modelo vehículo"))
        cur = connection.cursor()
        cur.execute("Select id_modelo FROM modelo_coches WHERE lower(nombre) = lower('" + modelo + "')")
        id_coche = cur.fetchall()[0]
        print(cur.fetchall)
        matricula = request.form["Matricula"]
        cur = connection.cursor()
        cur.execute("SELECT * FROM stock_coches WHERE lower(matricula) = lower('" + matricula + "')")
        datatres = cur.fetchall()
    if len(datatres) >0:
        flash("Esta matrícula ya existe en la base de datos.", category='danger')
        return redirect(url_for('stock'))
    else:
        cur.execute('UPDATE stock_coches SET id_modelo=%s, matricula=%s WHERE id_stock=%s',(id_coche, matricula, id))
        connection.commit()
        flash("Matrícula añadida correctamente a la base de datos.", category='success')
        return redirect(url_for('stock'))

# Eliminar stock base de datos
@app.route('/deletetres/<string:id>')
@login_required
@admin_required
def delete_stock(id):
    cur = connection.cursor()
    cur.execute("DELETE FROM stock_coches WHERE id_stock = {0}".format(id))
    connection.commit()
    flash("Stock eliminado con éxito.", category='success')
    return redirect(url_for("stock"))





# Visual clientes base de datos
@app.route('/alta_clientes')
@login_required
def clientes():
    cur = connection.cursor()
    cur.execute("SELECT * FROM clientes ORDER by nombre ASC")
    datados = cur.fetchall()
    print(datados)
    return render_template("alta_clientes.html", clientes = datados)

# Añadir clientes base de datos
@app.route('/add_cliente', methods=["POST", "GET"])
@login_required
def add_cliente():
    if request.method == "POST":
        nombre = request.form["Nombre cliente"]
        telefono = request.form["Teléfono"]
        descuento_empleado = request.form.get("Descuento Empleado", False)
        descuento_vip = request.form.get("Descuento Vip", False)
        imagen = request.form["DNI del Cliente"]
        mas_info = request.form["Más Info"]
    cur = connection.cursor()
    cur.execute("SELECT * FROM clientes WHERE lower(nombre) = lower('" + nombre + "')")
    datados = cur.fetchall()
    if len(datados) >0:
        flash("Este cliente ya existe en la base de datos.", category='danger')
        return redirect(url_for('clientes'))
    else:
        cur.execute('INSERT INTO clientes (nombre, telefono, descuento_empleado, descuento_vip, imagen, mas_info) VALUES (%s, %s, %s, %s, %s, %s)',(nombre, telefono, descuento_empleado, descuento_vip, imagen, mas_info))
        connection.commit()
        flash("Cliente añadido correctamente a la base de datos.", category='success')
        return redirect(url_for('clientes'))

# Editar clientes base de datos
@app.route('/editdos/<id>')
@login_required
@admin_required
def get_cliente(id):
    cur = connection.cursor()
    cur.execute("SELECT * FROM clientes WHERE id_cliente = {0}".format(id))
    datados = cur.fetchall()
    print(datados[0])
    return render_template("edit_clientes.html", cliente = datados[0])

# Actualizar clientes base de datos
@app.route("/updatedos/<id>", methods = ["POST", "GET"])
@login_required
@admin_required
def update_cliente(id):
    if request.method == "POST":
        nombre = request.form["Nombre cliente"]
        telefono = request.form["Teléfono"]
        descuento_empleado = request.form.get("Descuento Empleado", False)
        descuento_vip = request.form.get("Descuento Vip", False)
        imagen = request.form["DNI del Cliente"]
        mas_info = request.form["Más Info"]
        cur = connection.cursor()
        cur.execute('UPDATE clientes SET nombre=%s, telefono=%s, descuento_empleado=%s, descuento_vip=%s, imagen=%s, mas_info=%s WHERE id_cliente=%s',(nombre, telefono, descuento_empleado, descuento_vip, imagen, mas_info, id))
        connection.commit()
        flash("Cliente actualizado con éxito.", category='success')
        return redirect(url_for("clientes"))    

# Eliminar clientes base de datos
@app.route('/deletedos/<string:id>')
@login_required
@admin_required
def delete_cliente(id):
    cur = connection.cursor()
    cur.execute("DELETE FROM clientes WHERE id_cliente = {0}".format(id))
    connection.commit()
    flash("Cliente eliminado con éxito.", category='success')
    return redirect(url_for("clientes"))


# Visual coche base de datos
@app.route('/precios')
@login_required
@admin_required
def precios():
    cur = connection.cursor()
    cur.execute("SELECT * FROM modelo_coches ORDER by nombre ASC")
    data = cur.fetchall()
    print(data)
    return render_template("precios.html", vehiculos = data)

# Añadir coche base de datos
@app.route('/add_car', methods=["POST"])
@login_required
@admin_required
def add_car():
    if request.method == "POST":
        nombrecoche = request.form["Nombre vehículo"]
        precio_nuevo = int(request.form["Precio de concesionario"])
        cur = connection.cursor()
        precio_fulltunning = int(calculotunning(precio_nuevo))
        precio_compramos = int(calculocompramos(precio_fulltunning, precio_nuevo))
        precio_vendemos = int(calculovendemos(precio_nuevo, precio_fulltunning))
        precio_pintura = int(calculopintura(precio_nuevo))
        precio_estetica = int(calculoestetica (precio_nuevo))
        precio_motor = int(calculomotor(precio_nuevo))
        precio_contratos = int(calculocontrato (precio_nuevo))
        cur.execute("SELECT * FROM modelo_coches WHERE lower(nombre) = lower('"+ nombrecoche + "')")
        data = cur.fetchall()
        if len(data) >0:
            flash("Este vehículo ya existe en la base de datos.",category='danger')
            return redirect(url_for('precios'))
        else:
            cur.execute('INSERT INTO modelo_coches (nombre, precio_nuevo, precio_compramos, precio_vendemos, precio_pintura, precio_estetica, precio_motor, precio_fulltunning, precio_contratos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(nombrecoche, precio_nuevo, precio_compramos, precio_vendemos, precio_pintura, precio_estetica, precio_motor, precio_fulltunning, precio_contratos))
            connection.commit()
            flash("Vehículo añadido correctamente a la base de datos.", category='success')
            return redirect(url_for('precios'))

# Editar coche base de datos
@app.route('/edit/<id>')
@login_required
@admin_required
def get_car(id):
    cur = connection.cursor()
    cur.execute("SELECT * FROM modelo_coches WHERE id_modelo = {0}".format(id))
    data = cur.fetchall()
    print(data[0])
    return render_template("edit_vehicle.html", vehicle = data[0])

# Actualizar coche base de datos
@app.route("/update/<id>", methods = ["POST"])
@login_required
@admin_required
def update_vehicle(id):
    if request.method == "POST":
        nombrecoche = request.form["Nombre vehículo"]
        precio_nuevo = int(request.form["Precio de concesionario"])
        cur = connection.cursor()
        precio_fulltunning = int(calculotunning(precio_nuevo))
        precio_compramos = int(calculocompramos(precio_fulltunning, precio_nuevo))
        precio_vendemos = int(calculovendemos(precio_nuevo, precio_fulltunning))
        precio_pintura = int(calculopintura(precio_nuevo))
        precio_estetica = int(calculoestetica (precio_nuevo))
        precio_motor = int(calculomotor(precio_nuevo))
        precio_contratos = int(calculocontrato (precio_nuevo))
        cur.execute('UPDATE modelo_coches SET nombre=%s, precio_nuevo=%s, precio_fulltunning=%s, precio_compramos=%s, precio_vendemos=%s, precio_pintura=%s, precio_estetica=%s, precio_motor=%s, precio_contratos=%s WHERE id_modelo=%s',(nombrecoche, precio_nuevo, precio_fulltunning, precio_compramos, precio_vendemos,precio_pintura,precio_estetica, precio_motor, precio_contratos, id))
        connection.commit()
        flash("Vehículo actualizado con éxito.", category='success')
        return redirect(url_for("precios"))    

# Eliminar coche base de datos
@app.route('/delete/<string:id>')
@login_required
@admin_required
def delete_car(id):
    cur = connection.cursor()
    cur.execute("DELETE FROM modelo_coches WHERE id_modelo = {0}".format(id))
    connection.commit()
    flash("Vehiculo eliminado con éxito.", category='success')
    return redirect(url_for("precios"))




# Estilizador para numeros con .€
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.0f} €".format(value).replace(',','.')



if __name__ == "__main__":
    app.run(port = 3000, debug = True, host='0.0.0.0') 
from flask import flask, request


pintura = request.form.get("Descuento Empleado", False)
tunning = request.form.get("Descuento Empleado", False)
motor = request.form.get("Descuento Empleado", False)
full = request.form.get("Descuento Empleado", False)

def calculo_tunning():
    descuento_empleado = request.form.get("Descuento Empleado", False)

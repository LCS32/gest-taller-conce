CREATE TABLE servicios_mec(
id_servicio_mec SERIAL NOT NULL PRIMARY KEY,
id_mecanico INT NOT NULL,
id_cliente INT NOT NULL,
id_servicio INT NOT NULL,
cantidad INT NOT NULL,
precio_servicio_cobrado INT NOT NULL,
FOREIGN KEY (id_mecanico) REFERENCES empleados (id_empleado),
FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
FOREIGN KEY (id_servicio) REFERENCES servicios (id_servicio)
);


-- public.modelo_coches definition

-- Drop table

-- DROP TABLE modelo_coches;

CREATE TABLE modelo_coches (
	id_modelo serial NOT NULL,
	nombre varchar(50) NOT NULL,
	precio_nuevo int4 NOT NULL,
	precio_compramos int4 NULL,
	precio_vendemos int4 NULL,
	precio_pintura int4 NULL,
	precio_estetica int4 NULL,
	precio_motor int4 NULL,
	precio_fulltunning int4 NULL,
	precio_contratos int4 NULL,
	CONSTRAINT modelo_coches_nombre_key UNIQUE (nombre),
	CONSTRAINT modelo_coches_pkey PRIMARY KEY (id_modelo)
);


-- public.servicios definition

-- Drop table

-- DROP TABLE servicios;

CREATE TABLE servicios (
	id_servicio serial NOT NULL,
	tipo_servicio varchar(50) NULL,
	precio_servicio int4 NOT NULL,
	CONSTRAINT servicios_pkey PRIMARY KEY (id_servicio)
);


-- public.usuarios definition

-- Drop table

-- DROP TABLE usuarios;

CREATE TABLE usuarios (
	id_user serial NOT NULL,
	nombre varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	pass varchar(50) NOT NULL,
	CONSTRAINT usuarios_email_key UNIQUE (email),
	CONSTRAINT usuarios_nombre_key UNIQUE (nombre),
	CONSTRAINT usuarios_pkey PRIMARY KEY (id_user)
);


-- public.clientes definition

-- Drop table

-- DROP TABLE clientes;

CREATE TABLE clientes (
	id_cliente serial NOT NULL,
	id_user int4 NULL,
	nombre varchar(50) NOT NULL,
	telefono varchar(9) NULL,
	descuento_empleado bool NULL DEFAULT false,
	descuento_vip bool NULL DEFAULT false,
	imagen bytea NULL,
	mas_info varchar(5000) NULL,
	CONSTRAINT clientes_nombre_key UNIQUE (nombre),
	CONSTRAINT clientes_pkey PRIMARY KEY (id_cliente),
	CONSTRAINT clientes_telefono_key UNIQUE (telefono),
	CONSTRAINT clientes_id_user_fkey FOREIGN KEY (id_user) REFERENCES usuarios(id_user)
);


-- public.empleados definition

-- Drop table

-- DROP TABLE empleados;

CREATE TABLE empleados (
	id_empleado serial NOT NULL,
	id_user int4 NULL,
	tipo_empleado varchar(50) NULL,
	CONSTRAINT empleados_pkey PRIMARY KEY (id_empleado),
	CONSTRAINT empleados_id_user_fkey FOREIGN KEY (id_user) REFERENCES usuarios(id_user)
);


-- public.stock_coches definition

-- Drop table

-- DROP TABLE stock_coches;

CREATE TABLE stock_coches (
	id_stock serial NOT NULL,
	id_modelo int4 NULL,
	matricula varchar(8) NOT NULL,
	en_venta bool NULL DEFAULT false,
	CONSTRAINT stock_coches_pkey PRIMARY KEY (id_stock),
	CONSTRAINT stock_coches_id_modelo_fkey FOREIGN KEY (id_modelo) REFERENCES modelo_coches(id_modelo)
);


-- public.ventas definition

-- Drop table

-- DROP TABLE ventas;

CREATE TABLE ventas (
	id_venta serial NOT NULL,
	id_cliente int4 NULL,
	id_empleado int4 NULL,
	precio_venta int4 NOT NULL,
	id_stock int4 NULL,
	hora time NULL,
	fecha date NULL,
	CONSTRAINT ventas_pkey PRIMARY KEY (id_venta),
	CONSTRAINT ventas_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
	CONSTRAINT ventas_id_empleado_fkey FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
	CONSTRAINT ventas_id_stock_fkey FOREIGN KEY (id_stock) REFERENCES stock_coches(id_stock)
);


-- public.compras definition

-- Drop table

-- DROP TABLE compras;

CREATE TABLE compras (
	id_compra serial NOT NULL,
	id_empleado int4 NULL,
	precio_compra int4 NOT NULL,
	id_stock int4 NULL,
	hora time NULL,
	fecha date NULL,
	CONSTRAINT compras_pkey PRIMARY KEY (id_compra),
	CONSTRAINT compras_id_empleado_fkey FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
	CONSTRAINT compras_id_stock_fkey FOREIGN KEY (id_stock) REFERENCES stock_coches(id_stock)
);


-- public.reparaciones definition

-- Drop table

-- DROP TABLE reparaciones;

CREATE TABLE reparaciones (
	id_reparacion serial NOT NULL,
	id_servicio int4 NULL,
	id_empleado int4 NULL,
	id_cliente int4 NULL,
	id_stock int4 NULL,
	precio_cobrado int4 NOT NULL,
	hora time NULL,
	fecha date NULL,
	CONSTRAINT reparaciones_pkey PRIMARY KEY (id_reparacion),
	CONSTRAINT reparaciones_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
	CONSTRAINT reparaciones_id_empleado_fkey FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
	CONSTRAINT reparaciones_id_servicio_fkey FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio),
	CONSTRAINT reparaciones_id_stock_fkey FOREIGN KEY (id_stock) REFERENCES stock_coches(id_stock)
);
-- Precio full tunning
UPDATE modelo_coches SET precio_fulltunning =
CASE 
	WHEN precio_nuevo >= 200000 THEN int '136000'
	WHEN precio_nuevo > 50000 THEN int '30000'
	WHEN precio_nuevo > 20000 THEN int '12400'
	WHEN precio_nuevo > 9000 THEN int '9400'
	WHEN precio_nuevo > 0 THEN int '1100'
END


-- Precio compramos
UPDATE modelo_coches SET precio_compramos = 
ROUND ((precio_nuevo + precio_fulltunning)/2,-1)


-- Precio vendemos
UPDATE modelo_coches SET precio_vendemos = 
ROUND ((precio_nuevo + precio_fulltunning)-(precio_nuevo+precio_fulltunning)*0.2,-1)


--Precio pintura
UPDATE modelo_coches SET precio_pintura =
CASE 
	WHEN precio_nuevo >= 200000 THEN int '16000'
	WHEN precio_nuevo > 50000 THEN int '5000'
	WHEN precio_nuevo > 20000 THEN int '3000'
	WHEN precio_nuevo > 9000 THEN int '2000'
	WHEN precio_nuevo > 0 THEN int '300'
END


--Precio estetica
UPDATE modelo_coches SET precio_estetica =
CASE 
	WHEN precio_nuevo >= 200000 THEN int '20000'
	WHEN precio_nuevo > 50000 THEN int '5000'
	WHEN precio_nuevo > 20000 THEN int '3400'
	WHEN precio_nuevo > 9000 THEN int '2400'
	WHEN precio_nuevo > 0 THEN int '300'
END

--Precio motor
UPDATE modelo_coches SET precio_motor =
CASE 
	WHEN precio_nuevo >= 200000 THEN int '100000'
	WHEN precio_nuevo > 50000 THEN int '20000'
	WHEN precio_nuevo > 20000 THEN int '6000'
	WHEN precio_nuevo > 9000 THEN int '5000'
	WHEN precio_nuevo > 0 THEN int '500'
END

--Precio contratos
UPDATE modelo_coches SET precio_contratos =
round (precio_nuevo *1/100+1000,-1)


-- DROP DATABASE restaurante5_db;

-- CREATE DATABASE restaurante5_db;
USE restaurante5_db;


CREATE TABLE categoria_tb ( -- creating categories table ( menu plates categories)
	cat_id INT AUTO_INCREMENT,
    cat_nombre VARCHAR(20),
    
    PRIMARY KEY (cat_id)
);

CREATE TABLE menu_tb ( -- creating menu table, menu plates
	men_id INT AUTO_INCREMENT,
    cat_id INT,
    men_nombre VARCHAR(20),
    men_desc VArCHAR(50),
    men_precio 	DECIMAL(10,2),
    
    PRIMARY KEY (men_id),
    FOREIGN KEY (cat_id) REFERENCES categoria_tb(cat_id)
);

CREATE TABLE nit_tb ( -- registered nits table
	nit_id INT AUTO_INCREMENT,
    nit_numero INT,
    nit_dueno VARCHAR(30),
    
    PRIMARY KEY (nit_id)
);

CREATE TABLE empleado_tb (
	emp_id INT AUTO_INCREMENT,
    emp_nombre VARCHAR(30),
    emp_apellidoP VARCHAR(20),
    emp_apellidoM VARCHAR(20),
    emp_ci INT,
    emp_direccion VARCHAR(30),
    emp_celular VARCHAR(10),
    emp_estado BOOLEAN,
    emp_sueldo DECIMAL(10,2),
	
    PRIMARY KEY (emp_id)
);


CREATE TABLE usuario_tb (
	usu_id INT AUTO_INCREMENT,
    usu_nombre VARCHAR(20),
    usu_contra VARCHAR(30),
    emp_id INT,
    
    FOREIGN KEY (emp_id) REFERENCES empleado_tb (emp_id),
    PRIMARY KEY (usu_id)
);

CREATE TABLE cargo_tb (
	car_id INT AUTO_INCREMENT,
    car_nombre VARCHAR(50),
    car_desc VARCHAR(70),
    
    PRIMARY KEY (car_id)
);


CREATE TABLE empleadoXCargo_tb (
	car_id INT,
    emp_id INT,
    
    FOREIGN KEY (car_id) REFERENCES cargo_tb (car_id),
    FOREIGN KEY (emp_id) REFERENCES empleado_tb (emp_id),
    PRIMARY KEY (car_id, emp_id)
);

CREATE TABLE proveedor_tb (
	pro_id INT AUTO_INCREMENT,
    pro_nombre VARCHAR(20),
    pro_direccion VARCHAR(70),
    pro_celular VARCHAR(10),
    
    PRIMARY KEY (pro_id)
);

CREATE TABLE notaCompra_tb (
	notC_id INT AUTO_INCREMENT,
    notC_fecha DATE,
    notC_total DECIMAL(10,2),
	usu_id INT,
    pro_id INT,

    PRIMARY KEY (notC_id),
    FOREIGN KEY (usu_id) REFERENCES usuario_tb (usu_id),
    FOREIGN KEY (pro_id) REFERENCES proveedor_tb (pro_id)
);



CREATE TABLE producto_tb (
	prod_id INT AUTO_INCREMENT,
    prod_nombre VARCHAR(20),
    prod_duracion INT,

	PRIMARY KEY (prod_id)
);

	CREATE TABLE nCompraXProducto_tb(
        ncp_cantidad INT,
        ncp_precio DECIMAL(10,2),
        ncp_subt DECIMAL(10,2),
		nc_id INT,
        prod_id INT,
        FOREIGN KEY (nc_id) REFERENCES notaCompra_tb (notC_id),
        FOREIGN KEY (prod_id) REFERENCES producto_tb (prod_id),
		primary key(nc_id, prod_id)
    );
    
    
    CREATE TABLE notaEntrada_tb (
	notE_id INT AUTO_INCREMENT,
    notE_fecha DATE,
    usu_id INT,
    
    PRIMARY KEY(notE_id),
    FOREIGN KEY (usu_id) REFERENCES usuario_tb (usu_id)
);

CREATE TABLE nEntradaXProducto_tb (
    nep_cantidad INT,
    prod_id INT,
    ne_id INT,
    FOREIGN KEY (prod_id) REFERENCES producto_tb (prod_id),
    FOREIGN KEY (ne_id) REFERENCES notaEntrada_tb (notE_id),
    PRIMARY KEY (ne_id, prod_id)
);

CREATE TABLE almacen_tb (
	alm_id INT AUTO_INCREMENT,
    alm_nombre VARCHAR(20),
    alm_ubicacion VARCHAR(50),
    
    PRIMARY KEY (alm_id) 
);

CREATE TABLE lote_tb (
	lot_id  INT AUTO_INCREMENT,
    lot_cantI INT,
    lot_fecha DATE,
    prod_id INT,	
    alm_id INT,
	nep_id INT,
    
    PRIMARY KEY (lot_id),
    FOREIGN KEY (alm_id) REFERENCES almacen_tb (alm_id),
    FOREIGN KEY (nep_id, prod_id) REFERENCES nEntradaXProducto_tb (ne_id, prod_id)
);

CREATE TABLE movimientoLote_tb (
	lot_id INT,
    cant INT,
    
    FOREIGN KEY (lot_id) REFERENCES lote_tb (lot_id)
);

CREATE TABLE accion_tb (
	acc_id INT AUTO_INCREMENT,
    acc_nombre VARCHAR(20),
    
    PRIMARY KEY (acc_id)
);

CREATE TABLE bitacora_tb (
	bit_id INT AUTO_INCREMENT,
    bit_fecha DATE,
    bit_hora TIME,
    usu_id INT,
    acc_id INT,
    
    PRIMARY KEY (bit_id),
    FOREIGN KEY (usu_id) REFERENCES usuario_tb (usu_id),
    FOREIGN KEY (acc_id) REFERENCES accion_tb (acc_id)
);


CREATE TABLE notaSalida_tb (
	notS_id INT AUTO_INCREMENT,
    notS_fecha DATE,
    usu_id INT,
    alm_id INT,
    
    PRIMARY KEY (notS_id),
    FOREIGN KEY (usu_id) REFERENCES usuario_tb (usu_id),
    FOREIGN KEY (alm_id) REFERENCES almacen_tb (alm_id)
);


CREATE TABLE nSalidaXProducto_tb (
    nsp_cantidad INT,
    prod_id INT,
    notS_id INT,
    
    FOREIGN KEY (prod_id) REFERENCES producto_tb (prod_id),
    FOREIGN KEY (notS_id) REFERENCES notaSalida_tb (notS_id),
    PRIMARY KEY (notS_id, prod_id) 
);


CREATE TABLE pedido_tb (
	ped_id INT AUTO_INCREMENT,
    ped_fecha DATE,
    ped_hora TIME,
    ped_tipo VARCHAR(10),
    ped_total DECIMAL(10,2),
    notS_id INT,
    
    PRIMARY KEY (ped_id),
    FOREIGN KEY (notS_id) REFERENCES notaSalida_tb (notS_id)
);

CREATE TABLE Recibo(
    rec_id INT,
    rec_fecha DATE,
    rec_hora TIME,
    rec_total DECIMAL(12,2),
    nit_id INT,

    PRIMARY KEY (rec_id),
    FOREIGN KEY (nit_id) REFERENCES nit_tb(nit_id)
);

CREATE TABLE pedidoXMenu (
    pm_cantidad INT,
    pm_subtotal DECIMAL(10,2),
    men_id INT,
    ped_id INT,
    
    FOREIGN KEY (men_id) REFERENCES menu_tb (men_id),
    FOREIGN KEY (ped_id) REFERENCES pedido_tb (ped_id),
    PRIMARY KEY (ped_id, men_id)
);

-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

CREATE TABLE conversionVenta(
	cv_id INT AUTO_INCREMENT,
    cv_cantidad INT,
    prod_id INT,
    
    PRIMARY KEY (cv_id),
    FOREIGN KEY (prod_id) REFERENCES producto_tb (prod_id)
);

CREATE TABLE stockVenta(
	sv_cantidad INT,
    cv_id INT,
    ns_id INT,
    
    FOREIGN KEY (cv_id) REFERENCES conversionventa (cv_id),
    FOREIGN KEY (ns_id) REFERENCES notaSalida_tb (notS_id),
    PRIMARY KEY (ns_id, cv_id)
);


-- drop database restaurante5_db;


select * from empleado_tb;




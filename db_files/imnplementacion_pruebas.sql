use restaurante5_db;
select * from proveedor_tb;


insert into accion_tb (acc_nombre) values 
('iniciar sesion'),
('cerrar sesion');

insert into accion_tb (acc_nombre) values 
('registrar empleado'),
('registrar cargo'),
('registrar proveedor'),
('registrar usuario');

insert into accion_tb (acc_nombre) values 
('registrar nit');


insert into accion_tb (acc_nombre) values 
('registrar producto');

insert into accion_tb (acc_nombre) values 
('registrar notaCompra');

insert into accion_tb (acc_nombre) values 
('eliminar notaCompra');

select * from accion_tb;

select * from bitacora_tb;
select * from cargo_tb;

select * from producto_tb where prod_id = 5;
select * from ncompraxproducto_tb;


alter table ncompraxproducto_tb add ncp_id int not null auto_increment primary key first;

-- ==============================
-- MODIFYING COMPRAXPRODUCTOS TABLE
-- ==============================
show create table ncompraxproducto_tb;
select * from ncompraxproducto_tb;

alter table ncompraxproducto_tb drop foreign key ncompraxproducto_tb_ibfk_1;
alter table ncompraxproducto_tb drop foreign key ncompraxproducto_tb_ibfk_2;

alter table ncompraxproducto_tb drop primary key;
alter table ncompraxproducto_tb add ncp_id int not null auto_increment primary key first;

ALTER TABLE ncompraxproducto_tb ADD CONSTRAINT fk_nc_id FOREIGN KEY (nc_id) REFERENCES notaCompra_tb(notC_id);
ALTER TABLE ncompraxproducto_tb ADD CONSTRAINT fk_prd_id FOREIGN KEY (prod_id) REFERENCES producto_tb(prod_id);

show columns from ncompraxproducto_tb;


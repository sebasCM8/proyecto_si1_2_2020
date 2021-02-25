# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CategoriaTb(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_nombre = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria_tb'

class MenuTb(models.Model):
    men_id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(CategoriaTb, on_delete=models.CASCADE, blank=True, null=True)
    men_nombre = models.CharField(max_length=20, blank=True, null=True)
    men_desc = models.CharField(max_length=50, blank=True, null=True)
    men_precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_tb'

class NitTb(models.Model):
    nit_id = models.AutoField(primary_key=True)
    nit_numero = models.IntegerField(blank=True, null=True)
    nit_dueno = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nit_tb'

class EmpleadoTb(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_nombre = models.CharField(max_length=30, blank=True, null=True)
    emp_apellidop = models.CharField(db_column='emp_apellidoP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    emp_apellidom = models.CharField(db_column='emp_apellidoM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    emp_ci = models.IntegerField()
    emp_direccion = models.CharField(max_length=30, blank=True, null=True)
    emp_celular = models.CharField(max_length=10, blank=True, null=True)
    emp_estado = models.IntegerField(blank=True, null=True)
    emp_sueldo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleado_tb'

    def __str__(self):
        return("{} {}".format(self.emp_nombre, self.emp_apellidop))

    def es_admin(self):
        cargos = self.cargotb_set.all()
        cadmin = CargoTb.objects.filter(car_id=1)[0]
        if cadmin in cargos: 
            return True 
        else:
            return False

class UsuarioTb(models.Model):
    usu_id = models.AutoField(primary_key=True)
    usu_nombre = models.CharField(max_length=20, blank=True, null=True)
    usu_contra = models.CharField(max_length=30, blank=True, null=True)
    emp = models.ForeignKey(EmpleadoTb, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_tb'

class CargoTb(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_nombre = models.CharField(max_length=50, blank=True, null=True)
    car_desc = models.CharField(max_length=70, blank=True, null=True)

    puestos = models.ManyToManyField(EmpleadoTb, through='EmpleadoxcargoTb')

    def __str__(self):
        return "{}".format(self.car_nombre)

    class Meta:
        managed = False
        db_table = 'cargo_tb'


class EmpleadoxcargoTb(models.Model):
    car = models.ForeignKey(CargoTb, on_delete=models.CASCADE)
    emp = models.ForeignKey(EmpleadoTb, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'empleadoxcargo_tb'
        unique_together = (('car', 'emp'),)

class ProveedorTb(models.Model):
    pro_id = models.AutoField(primary_key=True)
    pro_nombre = models.CharField(max_length=20, blank=True, null=True)
    pro_direccion = models.CharField(max_length=70, blank=True, null=True)
    pro_celular = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor_tb'


class ProductoTb(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_nombre = models.CharField(max_length=20, blank=True, null=True)
    prod_duracion = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto_tb'

class NotacompraTb(models.Model):
    notc_id = models.AutoField(db_column='notC_id', primary_key=True)  # Field name made lowercase.
    notc_fecha = models.DateField(db_column='notC_fecha', blank=True, null=True)  # Field name made lowercase.
    notc_total = models.DecimalField(db_column='notC_total', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    usu = models.ForeignKey(UsuarioTb, on_delete=models.CASCADE)
    pro = models.ForeignKey(ProveedorTb, on_delete=models.CASCADE)

    detalle = models.ManyToManyField(ProductoTb, through='NcompraxproductoTb')

    class Meta:
        managed = False
        db_table = 'notacompra_tb'



class NcompraxproductoTb(models.Model):
    ncp_cantidad = models.IntegerField(blank=True, null=True)
    ncp_precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ncp_subt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nc = models.ForeignKey(NotacompraTb, on_delete=models.CASCADE)
    prod = models.ForeignKey(ProductoTb, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ncompraxproducto_tb'
        unique_together = (('nc', 'prod'),)

class NotaentradaTb(models.Model):
    note_id = models.AutoField(db_column='notE_id', primary_key=True)  # Field name made lowercase.
    note_fecha = models.DateField(db_column='notE_fecha', blank=True, null=True)  # Field name made lowercase.
    usu = models.ForeignKey(UsuarioTb, on_delete= models.CASCADE)

    detalle = models.ManyToManyField(ProductoTb, through='NentradaxproductoTb')

    class Meta:
        managed = False
        db_table = 'notaentrada_tb'

class NentradaxproductoTb(models.Model):
    nep_cantidad = models.IntegerField(blank=True, null=True)
    prod = models.ForeignKey(ProductoTb, on_delete= models.CASCADE)
    ne = models.ForeignKey(NotaentradaTb, on_delete= models.CASCADE)

    class Meta:
        managed = False
        db_table = 'nentradaxproducto_tb'
        unique_together = (('ne', 'prod'),)

class AlmacenTb(models.Model):
    alm_id = models.AutoField(primary_key=True)
    alm_nombre = models.CharField(max_length=20, blank=True, null=True)
    alm_ubicacion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'almacen_tb'

class LoteTb(models.Model):
    lot_id = models.AutoField(primary_key=True)
    lot_canti = models.IntegerField(db_column='lot_cantI', blank=True, null=True)  # Field name made lowercase.
    lot_fecha = models.DateField(blank=True, null=True)
    prod = models.ForeignKey(ProductoTb, on_delete= models.CASCADE)
    alm = models.ForeignKey(AlmacenTb, on_delete= models.CASCADE)
    nep = models.ForeignKey(NotaentradaTb, on_delete= models.CASCADE)

    class Meta:
        managed = False
        db_table = 'lote_tb'

class MovimientoloteTb(models.Model):
    lot = models.ForeignKey(LoteTb, on_delete= models.CASCADE)
    cant = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimientolote_tb'

class AccionTb(models.Model):
    acc_id = models.AutoField(primary_key=True)
    acc_nombre = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accion_tb'

class BitacoraTb(models.Model):
    bit_id = models.AutoField(primary_key=True)
    bit_fecha = models.DateField(blank=True, null=True)
    bit_hora = models.TimeField(blank=True, null=True)
    usu = models.ForeignKey(UsuarioTb, on_delete= models.CASCADE)
    acc = models.ForeignKey(AccionTb, on_delete= models.CASCADE)

    class Meta:
        managed = False
        db_table = 'bitacora_tb'

class NotasalidaTb(models.Model):
    nots_id = models.AutoField(db_column='notS_id', primary_key=True)  # Field name made lowercase.
    nots_fecha = models.DateField(db_column='notS_fecha', blank=True, null=True)  # Field name made lowercase.
    usu = models.ForeignKey(UsuarioTb, on_delete= models.CASCADE)
    alm = models.ForeignKey(AlmacenTb, on_delete= models.CASCADE)

    detalle = models.ManyToManyField(ProductoTb, through='NsalidaxproductoTb')

    class Meta:
        managed = False
        db_table = 'notasalida_tb'


class NsalidaxproductoTb(models.Model):
    nsp_cantidad = models.IntegerField(blank=True, null=True)
    prod = models.ForeignKey(ProductoTb, on_delete= models.CASCADE)
    nots = models.ForeignKey(NotasalidaTb, on_delete= models.CASCADE)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nsalidaxproducto_tb'
        unique_together = (('nots', 'prod'),)

class PedidoTb(models.Model):
    ped_id = models.AutoField(primary_key=True)
    ped_fecha = models.DateField(blank=True, null=True)
    ped_hora = models.TimeField(blank=True, null=True)
    ped_tipo = models.CharField(max_length=10, blank=True, null=True)
    ped_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nots = models.ForeignKey(NotasalidaTb, on_delete= models.CASCADE, db_column='notS_id')  # Field name made lowercase.

    detalle = models.ManyToManyField(MenuTb, through='Pedidoxmenu')

    class Meta:
        managed = False
        db_table = 'pedido_tb'

class Recibo(models.Model):
    rec_id = models.IntegerField(primary_key=True)
    rec_fecha = models.DateField(blank=True, null=True)
    rec_hora = models.TimeField(blank=True, null=True)
    rec_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    nit = models.ForeignKey(NitTb, on_delete= models.CASCADE)

    class Meta:
        managed = False
        db_table = 'recibo'

class Pedidoxmenu(models.Model):
    pm_cantidad = models.IntegerField(blank=True, null=True)
    pm_subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    men = models.ForeignKey(MenuTb, on_delete= models.CASCADE)
    ped = models.ForeignKey(PedidoTb, on_delete= models.CASCADE)

    class Meta:
        managed = False
        db_table = 'pedidoxmenu'
        unique_together = (('ped', 'men'),)        
# fin












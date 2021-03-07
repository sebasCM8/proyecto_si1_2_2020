# Generated by Django 3.1.6 on 2021-03-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccionTb',
            fields=[
                ('acc_id', models.AutoField(primary_key=True, serialize=False)),
                ('acc_nombre', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'accion_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AlmacenTb',
            fields=[
                ('alm_id', models.AutoField(primary_key=True, serialize=False)),
                ('alm_nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('alm_ubicacion', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'almacen_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BitacoraTb',
            fields=[
                ('bit_id', models.AutoField(primary_key=True, serialize=False)),
                ('bit_fecha', models.DateField(blank=True, null=True)),
                ('bit_hora', models.TimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bitacora_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CargoTb',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('car_nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('car_desc', models.CharField(blank=True, max_length=70, null=True)),
            ],
            options={
                'db_table': 'cargo_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CategoriaTb',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('cat_nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('cat_estado', models.IntegerField(db_column='cat_estado')),
            ],
            options={
                'db_table': 'categoria_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmpleadoTb',
            fields=[
                ('emp_id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('emp_apellidop', models.CharField(blank=True, db_column='emp_apellidoP', max_length=20, null=True)),
                ('emp_apellidom', models.CharField(blank=True, db_column='emp_apellidoM', max_length=20, null=True)),
                ('emp_ci', models.IntegerField()),
                ('emp_direccion', models.CharField(blank=True, max_length=30, null=True)),
                ('emp_celular', models.CharField(blank=True, max_length=10, null=True)),
                ('emp_estado', models.IntegerField(blank=True, null=True)),
                ('emp_sueldo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'empleado_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmpleadoxcargoTb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'empleadoxcargo_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LoteTb',
            fields=[
                ('lot_id', models.AutoField(primary_key=True, serialize=False)),
                ('lot_canti', models.IntegerField(blank=True, db_column='lot_cantI', null=True)),
                ('lot_fecha', models.DateField(blank=True, null=True)),
                ('lot_estado', models.IntegerField(blank=True, db_column='lot_estado', null=True)),
            ],
            options={
                'db_table': 'lote_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MenuTb',
            fields=[
                ('men_id', models.AutoField(primary_key=True, serialize=False)),
                ('men_nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('men_desc', models.CharField(blank=True, max_length=50, null=True)),
                ('men_precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('men_estado', models.IntegerField(db_column='men_estado')),
            ],
            options={
                'db_table': 'menu_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovimientoloteTb',
            fields=[
                ('movl_id', models.AutoField(primary_key=True, serialize=False)),
                ('cant', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'movimientolote_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NcompraxproductoTb',
            fields=[
                ('ncp_id', models.AutoField(db_column='ncp_id', primary_key=True, serialize=False)),
                ('ncp_cantidad', models.IntegerField(blank=True, null=True)),
                ('ncp_precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ncp_subt', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'ncompraxproducto_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NentradaxproductoTb',
            fields=[
                ('nep_id', models.AutoField(db_column='nep_id', primary_key=True, serialize=False)),
                ('nep_cantidad', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'nentradaxproducto_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NitTb',
            fields=[
                ('nit_id', models.AutoField(primary_key=True, serialize=False)),
                ('nit_numero', models.IntegerField(blank=True, null=True)),
                ('nit_dueno', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'nit_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotacompraTb',
            fields=[
                ('notc_id', models.AutoField(db_column='notC_id', primary_key=True, serialize=False)),
                ('notc_fecha', models.DateField(blank=True, db_column='notC_fecha', null=True)),
                ('notc_total', models.DecimalField(blank=True, db_column='notC_total', decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'notacompra_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotaentradaTb',
            fields=[
                ('note_id', models.AutoField(db_column='notE_id', primary_key=True, serialize=False)),
                ('note_fecha', models.DateField(blank=True, db_column='notE_fecha', null=True)),
            ],
            options={
                'db_table': 'notaentrada_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotasalidaTb',
            fields=[
                ('nots_id', models.AutoField(db_column='notS_id', primary_key=True, serialize=False)),
                ('nots_fecha', models.DateField(blank=True, db_column='notS_fecha', null=True)),
                ('nots_estado', models.IntegerField(blank=True, db_column='nots_estado', null=True)),
            ],
            options={
                'db_table': 'notasalida_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NsalidaxproductoTb',
            fields=[
                ('nsp_id', models.AutoField(db_column='nsp_id', primary_key=True, serialize=False)),
                ('nsp_cantidad', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'nsalidaxproducto_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PedidoTb',
            fields=[
                ('ped_id', models.AutoField(primary_key=True, serialize=False)),
                ('ped_fecha', models.DateField(blank=True, null=True)),
                ('ped_hora', models.TimeField(blank=True, null=True)),
                ('ped_tipo', models.CharField(blank=True, max_length=10, null=True)),
                ('ped_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'pedido_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pedidoxmenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pm_cantidad', models.IntegerField(blank=True, null=True)),
                ('pm_subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'pedidoxmenu',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductoTb',
            fields=[
                ('prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('prod_nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('prod_duracion', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'producto_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProveedorTb',
            fields=[
                ('pro_id', models.AutoField(primary_key=True, serialize=False)),
                ('pro_nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('pro_direccion', models.CharField(blank=True, max_length=70, null=True)),
                ('pro_celular', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'proveedor_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('rec_id', models.IntegerField(primary_key=True, serialize=False)),
                ('rec_fecha', models.DateField(blank=True, null=True)),
                ('rec_hora', models.TimeField(blank=True, null=True)),
                ('rec_total', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'db_table': 'recibo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsuarioTb',
            fields=[
                ('usu_id', models.AutoField(primary_key=True, serialize=False)),
                ('usu_nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('usu_contra', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'usuario_tb',
                'managed': False,
            },
        ),
    ]
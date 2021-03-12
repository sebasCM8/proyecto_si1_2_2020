from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import EmpleadoTb, UsuarioTb, CargoTb, EmpleadoxcargoTb, ProveedorTb, AccionTb, BitacoraTb, NitTb, ProductoTb, NotacompraTb, NcompraxproductoTb, NotaentradaTb, NentradaxproductoTb, AlmacenTb, LoteTb, MovimientoloteTb, NotasalidaTb, NsalidaxproductoTb, CategoriaTb, MenuTb, ConversionVenta, StockVenta, PedidoTb, Pedidoxmenu, Recibo
import datetime
import re

# Create your views here.


def home_page(request):
    if 'userid' in request.session:
        if request.method == 'GET':
            return render(request, 'restaurant/home_page.html')
        elif request.method == 'POST':
            if 'logout' in request.POST:
                return HttpResponseRedirect(reverse('restaurant:logout'))
            elif 'perfil' in request.POST:
                usuario=UsuarioTb.objects.filter(usu_id = request.session['userid'])[0]
                empleado = usuario.emp
                cargos = empleado.cargotb_set.all()
                return render(request, 'restaurant/perfil.html', {'user':usuario, 'empleado':empleado, 'cargos':cargos})
    else:
        return render(request, 'restaurant/errorPage.html')
# =====================
# GESTIONAR EMPLEADO
# =====================
def registrar_empleados(request):
    if 'userid' in request.session:
        ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
        if ue.es_admin() == False:
            return render(request, 'restaurant/errorPage.html')
    else: 
        return render(request, 'restaurant/errorPage.html')

    if request.method == 'GET':
        cargos = CargoTb.objects.all()
        return render(request, 'restaurant/empleado_form.html', {'cargos':cargos})
    elif request.method == 'POST':
        emp_nombre = request.POST['emp_nombre']
        emp_ap = request.POST['emp_ap']
        emp_am = request.POST['emp_am']
        emp_ci = request.POST['emp_ci']
        emp_cel = request.POST['emp_cel']
        emp_dir = request.POST['emp_dir']
        emp_sueldo= request.POST['emp_sueldo']

        cargos = CargoTb.objects.all()
        tiene_cargo = False 
        for c in cargos:
            if c.car_nombre in request.POST: 
                tiene_cargo = True
                break

        if (emp_nombre!="" and emp_sueldo.isnumeric() and emp_ap!="" and emp_am!="" and emp_ci.isnumeric() and emp_cel!="" and emp_dir!="" and tiene_cargo):
            empleados = EmpleadoTb.objects.all()
            emp_ci = int(emp_ci)
            emp_sueldo = int(emp_sueldo)
            nuevo = True
            for emp in empleados:
                if emp.emp_ci == emp_ci: 
                    nuevo = False
                    break
            if nuevo:
                nuevo_emp = EmpleadoTb(emp_nombre = emp_nombre, emp_apellidop = emp_ap, emp_apellidom = emp_am, emp_ci = emp_ci, emp_direccion = emp_dir, emp_celular = emp_cel, emp_estado = 1, emp_sueldo=emp_sueldo)
                nuevo_emp.save()

                fecha = datetime.date.today()
                hora = datetime.datetime.now().time()
                accion = AccionTb.objects.filter(acc_id=1)[0]
                eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
                registrarAccion.save()

                for c in cargos:
                    if c.car_nombre in request.POST:
                        newCargo = EmpleadoxcargoTb(car=c, emp=nuevo_emp)
                        newCargo.save()

                msg = "Empleado registrado exitosamente"
                return render(request, 'restaurant/empleado_form.html',{'msg':msg, 'mcolor':'green', 'cargos':cargos})
            else:
                msg = "Empleado ya registrado"
                return render(request, 'restaurant/empleado_form.html',{'msg':msg, 'mcolor':'red', 'cargos':cargos})
        else:
            msg = "Datos invalidos, tambien asegurese de rellenar todos los campos para registrar el empleado"
        return render(request, 'restaurant/empleado_form.html',{'msg':msg, 'mcolor':'red', 'cargos':cargos})

def vista_empleados(request):
    if 'userid' in request.session:
        ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
        if ue.es_admin() == False:
            return render(request, 'restaurant/errorPage.html')
    else: 
        return render(request, 'restaurant/errorPage.html')

    empleados = EmpleadoTb.objects.filter(emp_estado = 1)
    if request.method == 'GET':
        return render(request, 'restaurant/vista_empleados.html' ,{'emps':empleados})
    else:
        if 'ver' in request.POST:
            empleado = EmpleadoTb.objects.filter(emp_id = request.POST['ver'])[0]
            usuario = UsuarioTb.objects.filter(emp=empleado)
            tiene_usuario = False
            if len(usuario)>0:
                usuario = usuario[0]
                tiene_usuario = True                

            cargos = empleado.cargotb_set.all()

            return render(request, 'restaurant/ver_emp.html', {'user':usuario, 'emp':empleado, 'tieneUser':tiene_usuario, 'cargos':cargos})
        if 'editar' in request.POST:
            emp_selected = EmpleadoTb.objects.filter(emp_ci=request.POST['editar'])[0]
            cargos = CargoTb.objects.all()
            exc = emp_selected.cargotb_set.all()
            nu_cargos = list()
            for c in cargos:
                cargo_est = dict()
                if c in exc:
                    cargo_est['estado'] = True 
                else: 
                    cargo_est['estado'] = False 
                cargo_est['cargo'] = c
                nu_cargos.append(cargo_est)

            return render(request, 'restaurant/editar_emp.html', {'emp':emp_selected, 'cargos':nu_cargos})
        if 'eliminar' in request.POST:
            emp_selected = EmpleadoTb.objects.filter(emp_ci = request.POST['eliminar'])[0]
            return render(request, 'restaurant/eliminar_emp.html', {'emp':emp_selected})

def eliminar_emp(request):
    if request.method == 'POST':
        if 'cancelar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:vistaemps'))
        elif 'eliminar' in request.POST:
            emp = EmpleadoTb.objects.filter(emp_ci=request.POST['eliminar'])[0]
            emp.emp_estado = 0
            emp.save()
            return HttpResponseRedirect(reverse('restaurant:vistaemps'))
    else: 
        return render(request, 'restaurant/errorPage.html')        

def empleado_editado(request):
    if request.method=='POST':
        emp = EmpleadoTb.objects.filter(emp_ci = request.POST['emp_selected'])[0]
        
        emp_sueldo = emp.emp_sueldo
        nuevo_sueldo = request.POST['sueldo']
        if nuevo_sueldo.isnumeric() and nuevo_sueldo != emp_sueldo:
            nuevo_sueldo = int(nuevo_sueldo)
            if nuevo_sueldo >= 0:
                emp.emp_sueldo = nuevo_sueldo            
                emp.save()

        emp_cargos = emp.cargotb_set.all()
        cargos = CargoTb.objects.all()
        for c in cargos:
            if c.car_nombre in request.POST:
                if not (c in emp_cargos):
                    nuevo_cargo = EmpleadoxcargoTb(car = c, emp = emp)
                    nuevo_cargo.save()
            else:
                if c in emp_cargos:
                    cargo_antiguo = EmpleadoxcargoTb.objects.filter(car= c, emp=emp)
                    cargo_antiguo.delete()

        return render(request, 'restaurant/guardar_cambios_emp.html', {'empleado':emp})
    else: 
        return render(request, 'restaurant/errorPage.html')
# =====================
# GESTIONAR USUARIO
#======================
def registrar_usuario(request):
    if 'userid' in request.session:
        ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
        if ue.es_admin() == False:
            return render(request, 'restaurant/errorPage.html')
    else: 
        return render(request, 'restaurant/errorPage.html')

    empleados = EmpleadoTb.objects.filter(emp_estado=1)
    emps_sin_usuario = list()
    for emp in empleados:
        usuario_emp = UsuarioTb.objects.filter(emp_id = emp.emp_id)
        if len(usuario_emp) == 0:
            emps_sin_usuario.append(emp)
    hay_emps = True
    if len(emps_sin_usuario) == 0:
        hay_emps = False


    if request.method == 'GET':
        return render(request, 'restaurant/usuario_form.html' ,{'empleados':emps_sin_usuario, 'hayemps':hay_emps})
    else:
        usu_nombre = request.POST['usu_nombre']
        usu_contra = request.POST['usu_contra']
        
        if usu_contra != "" and usu_nombre != "" and 'emp_id' in request.POST:

            usuarios_mismoUsername = UsuarioTb.objects.filter(usu_nombre = usu_nombre)
            if len(usuarios_mismoUsername)>0:
                msg = "Nombre de usuario ocupado, ingrese uno diferente"
                return render(request, 'restaurant/usuario_form.html' ,{'empleados':emps_sin_usuario, 'msg':msg, 'colo':'red', 'hayemps':hay_emps})

            emp_selec = EmpleadoTb.objects.filter(emp_id = request.POST['emp_id'])[0]
            nuevo_usuario = UsuarioTb(usu_nombre = usu_nombre, usu_contra= usu_contra, emp=emp_selec)
            nuevo_usuario.save()
            msg = "Usuario registrado con exito.."

            fecha = datetime.date.today()
            hora = datetime.datetime.now().time()
            accion = AccionTb.objects.filter(acc_id=4)[0]
            eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
            registrarAccion.save()

            emps_sin_usuario.remove(emp_selec)
            if len(emps_sin_usuario) == 0: hay_emps = False

            return render(request, 'restaurant/usuario_form.html' ,{'empleados':emps_sin_usuario, 'msg':msg, 'colo':'green', 'hayemps':hay_emps})

        msg = "Rellene todos los campos para registrar al nuevo usuario"
        return render(request, 'restaurant/usuario_form.html' ,{'empleados':emps_sin_usuario, 'msg':msg, 'colo':'red', 'hayemps':hay_emps})

def perfil_view(request):
    if request.method=='POST':
        if 'editar' in request.POST:
            usuario = UsuarioTb.objects.filter(usu_id = request.POST['editar'])[0]
            empleado = usuario.emp
            return render(request, 'restaurant/editarPerfil.html', {'user': usuario, 'empleado': empleado})
        
        if 'cancelar' in request.POST:
            usuario = UsuarioTb.objects.filter(usu_id = request.POST['cancelar'])[0]
            empleado = usuario.emp
            cargos = empleado.cargotb_set.all()
            return render(request, 'restaurant/perfil.html', {'user':usuario, 'empleado':empleado, 'cargos':cargos})
        
        if 'guardar' in request.POST:
            user_nombre = request.POST['usu_nombre']
            user_contra = request.POST['usu_contra']

            emp_nombre = request.POST['emp_nombre']
            emp_ap = request.POST['emp_ap']
            emp_am = request.POST['emp_am']
            emp_celular = request.POST['emp_celular']
            emp_direccion = request.POST['emp_direccion']

            usuario = UsuarioTb.objects.filter(usu_id = request.POST['guardar'])[0]

            if user_nombre != "" and user_nombre != usuario.usu_nombre:
                usuario.usu_nombre = user_nombre
                usuario.save()
            if user_contra != "" and user_contra != usuario.usu_contra:
                usuario.usu_contra = user_contra
                usuario.save()
            
            empleado = usuario.emp
            if emp_nombre != "" and emp_nombre != empleado.emp_nombre:
                empleado.emp_nombre = emp_nombre
                empleado.save()
            if emp_ap != "" and emp_ap != empleado.emp_apellidop:
                empleado.emp_apellidop = emp_ap
                empleado.save()
            if emp_am != "" and emp_am != empleado.emp_apellidom:
                empleado.emp_apellidom = emp_am
                empleado.save()
            if emp_celular != "" and emp_celular != empleado.emp_celular:
                empleado.emp_celular = emp_celular
                empleado.save()
            if emp_direccion != "" and emp_direccion != empleado.emp_direccion:
                empleado.emp_direccion = emp_direccion
                empleado.save()
            
            cargos = empleado.cargotb_set.all() 

            return render(request, 'restaurant/perfil.html', {'user':usuario, 'empleado':empleado, 'cargos':cargos})
    else:
        return render(request, 'restaurant/errorPage.html')
# ============================
# ====== GESTIONAR CARGO =====
#= ===========================
def registrar_cargo(request):
    if request.method == 'POST':
        car_nombre = request.POST['car_nombre']
        car_desc = request.POST['car_desc']
        if car_nombre != "" and car_desc != "":
            cargos = CargoTb.objects.filter(car_nombre = car_nombre)
            if len(cargos) == 0:
                nuevo_cargo = CargoTb(car_nombre = car_nombre, car_desc = car_desc)
                nuevo_cargo.save()
                msg = "Cargo registrado exitosamente"

                fecha = datetime.date.today()
                hora = datetime.datetime.now().time()
                accion = AccionTb.objects.filter(acc_id=2)[0]
                eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
                registrarAccion.save()

                good_msg =True
            else:
                msg = "El cargo ya  existe"
                good_msg =False
            return render(request, 'restaurant/cargo_form.html', {'msg':msg, 'gm':good_msg})
        else:
            msg = "Rellene todos los campos para registrar"
            good_msg = False 
        return render(request, 'restaurant/cargo_form.html', {'msg':msg, 'gm':good_msg})
    elif request.method == 'GET':
        if 'userid' in request.session:
            ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if ue.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else: 
            return render(request, 'restaurant/errorPage.html')

        return render(request, 'restaurant/cargo_form.html')

def vista_cargos(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if ue.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else: 
            return render(request, 'restaurant/errorPage.html')

        cargos = CargoTb.objects.all()
        return render(request, 'restaurant/vista_cargos.html', {'cargos':cargos})
    if request.method == 'POST':
        if 'editar' in request.POST:
            cargo = CargoTb.objects.filter(car_id = request.POST['editar'])[0]
            return render(request, 'restaurant/editarCargo.html', {'cargo':cargo})
        elif 'eliminar' in request.POST:
            cargo = CargoTb.objects.filter(car_id = request.POST['eliminar'])[0]
            return render(request, 'restaurant/eliminarCargo.html', {'cargo':cargo})

def editar_cargo(request):
    if request.method == 'POST':
        car_nombre = request.POST['car_nombre']
        car_desc = request.POST['car_desc']
        cargo = CargoTb.objects.filter(car_id=request.POST['guardar'])[0]
        if car_nombre != "" and car_desc != "" and (car_nombre != cargo.car_nombre or car_desc != cargo.car_desc):
            cargo.car_nombre = car_nombre
            cargo.car_desc = car_desc 
            cargo.save()
        return HttpResponseRedirect(reverse('restaurant:vercargos'))
    else: 
        return render(request, 'restaurant/errorPage.html')

def eliminar_cargo(request):
    if request.method == 'POST':
        if 'eliminar' in request.POST:
            cargo = CargoTb.objects.filter(car_id=request.POST['eliminar'])[0]

            cargo.puestos.clear()
            
            cargo.delete()
            return HttpResponseRedirect(reverse('restaurant:vercargos'))
        elif 'cancelar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:vercargos'))
    else: 
        return render(request, 'restaurant/errorPage.html')
# ======================
# == GESTIONAR LOGIN === 
# ======================
def login_view(request):
    if request.method == 'GET':
        return render(request, 'restaurant/login.html')
    else:
        usu_nombre = request.POST['username']
        usu_contra = request.POST['contra']
        if usu_contra != "" and usu_nombre != "":
            usuario = UsuarioTb.objects.filter(usu_nombre=usu_nombre)
            if len(usuario)>0:
                eluser = usuario[0]
                if eluser.usu_contra == usu_contra:
                    useremp = eluser.emp
                    if useremp.emp_estado == 1:
                        request.session['userid'] = eluser.usu_id

                        fecha = datetime.date.today()
                        hora = datetime.datetime.now().time()
                        accion = AccionTb.objects.filter(acc_id=5)[0]
                        registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
                        registrarAccion.save()

                        return render(request, 'restaurant/home_page.html')
                    else:
                        msg = "Usuario no valido"
                        return render(request, 'restaurant/login.html', {'msg':msg, 'msgcolor':'red'})
                    
                else:
                    msg = "Contraseña incorrecta"
                    return render(request, 'restaurant/login.html', {'msg':msg, 'msgcolor':'red'})    
            else:
                msg = "El usuario {} no esta registrado..".format(usu_nombre)
                return render(request, 'restaurant/login.html', {'msg':msg, 'msgcolor':'red'})
        else:
            msg = "Rellene todos los campos para ingresar"
            return render(request, 'restaurant/login.html', {'msg':msg, 'msgcolor':'red'})
# ======================
# == GESTIONAR LOGOUT === 
# ======================
def logoutAction(request):
    if 'userid' in request.session:
        eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
        fecha = datetime.date.today()
        hora = datetime.datetime.now().time()
        accion = AccionTb.objects.filter(acc_id=6)[0]
        registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
        registrarAccion.save()
        
        request.session.flush()

        return HttpResponseRedirect(reverse('restaurant:login'))
    else:
        return render(request, 'restaurant/errorPage.html')
#========================
#== GESTIONAR PROVEEDOR ==
#========================
def gestionar_proveedor_vista(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if ue.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else: 
            return render(request, 'restaurant/errorPage.html')

        proveedores = ProveedorTb.objects.all()
        return render(request, 'restaurant/gestProveedor.html', {'provs':proveedores})
    elif request.method == 'POST':
        if 'registrar' in request.POST:
            return render(request, 'restaurant/registrarProveedor.html')
        elif 'registrarProv' in request.POST:
            prov_nombre = request.POST['pro_nombre']
            prov_celular = request.POST['pro_celular']
            prov_direccion = request.POST['pro_direccion']
            if prov_nombre!="" and prov_celular.isnumeric() and prov_direccion!="":
                nuevoProveedor = ProveedorTb(pro_nombre=prov_nombre, pro_direccion=prov_direccion, pro_celular=prov_celular)
                nuevoProveedor.save()
                msg = "Proveedor registrado exitosamente.."

                fecha = datetime.date.today()
                hora = datetime.datetime.now().time()
                accion = AccionTb.objects.filter(acc_id=3)[0]
                eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
                registrarAccion.save()                    

                return render(request, 'restaurant/registrarProveedor.html', {'msg':msg, 'exito':True})
            msg = "Rellene todos los campos correctamente para registrar al proveedor..."
            return render(request, 'restaurant/registrarProveedor.html', {'msg':msg, 'exito':False})
        elif 'editar' in request.POST:
            p = ProveedorTb.objects.filter(pro_id=request.POST['editar'])[0]
            return render(request, 'restaurant/editarProveedor.html', {'prv':p})
        elif 'editarProv' in request.POST:
            p = ProveedorTb.objects.filter(pro_id = request.POST['editarProv'])[0]
            nu_nombre = request.POST['pro_nombre']
            nu_direccion = request.POST['pro_direccion']
            nu_celular = request.POST['pro_celular']
            if nu_celular.isnumeric() and nu_celular != p.pro_celular:
                p.pro_celular = nu_celular
                p.save()
            if nu_nombre != "" and nu_nombre != p.pro_nombre:
                p.pro_nombre = nu_nombre
                p.save()
            if nu_direccion != "" and nu_direccion != p.pro_direccion:
                p.pro_direccion = nu_direccion
                p.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarProveedores'))
        elif 'eliminar' in request.POST:
            p = ProveedorTb.objects.filter(pro_id=request.POST['eliminar'])[0]
            return render(request, 'restaurant/eliminarProveedor.html', {'prv':p})
        elif 'eliminarProv' in request.POST:
            p = ProveedorTb.objects.filter(pro_id=request.POST['eliminarProv'])[0]
            notas = NotacompraTb.objects.filter(pro=p)
            if len(notas)>0:
                msg = "Este proveedor tiene notas de compra, primero elimina esas notas de compra"
                return render(request, 'restaurant/eliminarProveedor.html', {'prv':p, 'msg':msg})
            p.delete()
            return HttpResponseRedirect(reverse('restaurant:gestionarProveedores'))
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarProveedores'))
#========================
#== GESTIONAR ACCION ==
#========================
def gest_accion_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if ue.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else: 
            return render(request, 'restaurant/errorPage.html')

        acciones = AccionTb.objects.all()
        return render(request, 'restaurant/gestionarAccion.html', {'acciones':acciones})    
#========================
#== GESTIONAR BITACORA ==
#========================
def gest_bitacora(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            ue = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if ue.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else: 
            return render(request, 'restaurant/errorPage.html')

        bitacora = BitacoraTb.objects.all()
        historial = list()
        for b in bitacora:
            record = dict()
            record['usuario'] = b.usu.usu_nombre
            record['accion'] = b.acc.acc_nombre
            record['fecha'] = b.bit_fecha
            record['hora'] = b.bit_hora  
            historial.append(record)
        acs = AccionTb.objects.all()
        usuarios = UsuarioTb.objects.all()
        hay = True
        return render(request, 'restaurant/gestBitacora.html', {'bitacora':historial, 'acciones':acs, 'usuarios':usuarios, 'hay':hay})
    else:
        registros = None
        if 'acc_id' in request.POST and request.POST['acc_id'] != "0":
            af_id = int(request.POST['acc_id'])
            af = AccionTb.objects.filter(acc_id=af_id)[0]
            registros = BitacoraTb.objects.filter(acc=af)
        else:
            registros = BitacoraTb.objects.all()
        
        if 'usu_nombre' in request.POST and request.POST['usu_nombre'] != "todos":
            unombre = request.POST['usu_nombre']
            registros_finales = list()
            for reg in registros:
                if reg.usu.usu_nombre == unombre:
                    registros_finales.append(reg)
            registros = registros_finales

        historial = list()
        for b in registros:
            record = dict()
            record['usuario'] = b.usu.usu_nombre
            record['accion'] = b.acc.acc_nombre
            record['fecha'] = b.bit_fecha
            record['hora'] = b.bit_hora  
            historial.append(record)
        acs = AccionTb.objects.all()
        usuarios = UsuarioTb.objects.all()

        hayregistros = True
        if len(historial) == 0: hayregistros = False

        return render(request, 'restaurant/gestBitacora.html', {'bitacora':historial, 'acciones':acs, 'usuarios':usuarios, 'hay':hayregistros})

# ======================
# == GESTIONAR NIT =====
# =====================
def gest_nit_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            empleado = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if (not empleado.es_admin()) and (not empleado.es_cajero()):
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')

    if request.method == 'GET':
        nits = NitTb.objects.all() 
        return render(request, 'restaurant/gestionarNit.html', {'nits':nits})
    else:
        if 'registrarBtn' in request.POST:
            return render(request, 'restaurant/registrarNit.html')
        elif 'registrarNit' in request.POST:
            nit_nro = request.POST['nit_numero']
            nit_nombre = request.POST['nit_nombre']
            if nit_nro.isnumeric() and nit_nombre != "":
                nit_nro = int(nit_nro)
                nitdoble_num = NitTb.objects.filter(nit_numero=nit_nro)
                nitdoble_nom = NitTb.objects.filter(nit_dueno=nit_nombre)
                if len(nitdoble_num) == 0 and len(nitdoble_nom) == 0:
                    nuevonit = NitTb(nit_dueno=nit_nombre, nit_numero=nit_nro)
                    nuevonit.save()
                    fecha = datetime.date.today()
                    hora = datetime.datetime.now().time()
                    accion = AccionTb.objects.filter(acc_id=7)[0]
                    eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                    registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
                    registrarAccion.save()
                    msg = "Nit registrado.."
                    goodmsg = True
                    return render(request, 'restaurant/registrarNit.html', {'msg':msg, 'e':goodmsg})            
                else:
                    msg = "El numero de nit ya esta registrado.."
                    goodmsg = False
                    return render(request, 'restaurant/registrarNit.html', {'msg':msg, 'e':goodmsg})            
            else:
                msg = "Rellene todos los campos correctamente.."
                goodmsg = False
                return render(request, 'restaurant/registrarNit.html', {'msg':msg, 'e':goodmsg})            
        elif 'editarBtn' in request.POST:
            nit = NitTb.objects.filter(nit_id=request.POST['editarBtn'])[0]
            return render(request, 'restaurant/editarNit.html', {'n':nit})
        elif 'editarNit' in request.POST:
            nu_nombre = request.POST['nit_nombre']
            nu_numero = request.POST['nit_numero']

            elnit = NitTb.objects.filter(nit_id=request.POST['editarNit'])[0]
            if nu_nombre != "" and nu_nombre != elnit.nit_dueno:
                elnit.nit_dueno = nu_nombre
                elnit.save()
            if nu_numero.isnumeric():
                nu_numero = int(nu_numero)
                if nu_numero != elnit.nit_numero:
                    elnit.nit_numero = nu_numero
                    elnit.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarNit'))
# ============================
# == GESTIONAR PRODUCTOS =====
# ===========================
def gest_producto_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            empleado = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if empleado.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
        
    if request.method == 'GET':
        productos = ProductoTb.objects.all()
        return render(request, 'restaurant/gestionarProducto.html',{'productos':productos})
    else:
        if 'registrarBtn' in request.POST:
            return render(request, 'restaurant/registrarProducto.html')
        elif 'registrarProducto' in request.POST:
            pnombre = request.POST['prod_nombre']
            pduracion = request.POST['prod_duracion']

            if pduracion.isnumeric() and pnombre != "":
                esrepetido = ProductoTb.objects.filter(prod_nombre=pnombre)
                if len(esrepetido) > 0:
                    msg= "Producto ya registrado"
                    return render(request, 'restaurant/registrarProducto.html', {'msg':msg, 'e':False})
                nuevo_producto = ProductoTb(prod_nombre=pnombre, prod_duracion=pduracion)
                nuevo_producto.save()
                msg= "Producto registrado exitosamente.."

                fecha = datetime.date.today()
                hora = datetime.datetime.now().time()
                accion = AccionTb.objects.filter(acc_id=8)[0]
                eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=eluser, acc=accion)
                registrarAccion.save()    

                return render(request, 'restaurant/registrarProducto.html', {'msg':msg, 'e':True})
            else:
                msg= "Rellene todos los campos correctamente.."
                return render(request, 'restaurant/registrarProducto.html', {'msg':msg, 'e':False})
        elif 'editarBtn' in request.POST:
            producto = ProductoTb.objects.filter(prod_id=request.POST['editarBtn'])[0]
            return render(request, 'restaurant/editarProducto.html', {'producto':producto})
        elif 'editarProducto' in request.POST:
            pnombre = request.POST['prod_nombre']
            pduracion = request.POST['prod_duracion']
            elprod = ProductoTb.objects.filter(prod_id=request.POST['editarProducto'])[0]
            if pnombre!="" and pnombre!=elprod.prod_nombre:
                elprod.prod_nombre = pnombre
                elprod.save()
            if pduracion.isnumeric() and pduracion!=elprod.prod_duracion:
                elprod.prod_duracion = pduracion
                elprod.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarProducto'))
        elif 'eliminarBtn' in request.POST:
            producto = ProductoTb.objects.filter(prod_id=request.POST['eliminarBtn'])[0]
            return render(request, 'restaurant/eliminarProducto.html', {'producto':producto})
        elif 'eliminarProducto' in request.POST:
            producto = ProductoTb.objects.filter(prod_id=request.POST['eliminarProducto'])[0]
            notasc = NcompraxproductoTb.objects.filter(prod=producto)
            racion = ConversionVenta.objects.filter(prod=producto)
            if len(racion) > 0:
                msg = "Este producto tiene una racion asignada, no puede ser eliminado"
                return render(request, 'restaurant/eliminarProducto.html', {'producto':producto, 'msg':msg})
            lotes = LoteTb.objects.filter(prod=producto)
            if len(lotes)>0:
                msg = "Este producto tiene lotes en almacen, no puede ser eliminado"
                return render(request, 'restaurant/eliminarProducto.html', {'producto':producto, 'msg':msg})
            if len(notasc)>0:
                msg = "Este producto tiene notas de compra, primero elimine esas notas si desea eliminar el producto"
                return render(request, 'restaurant/eliminarProducto.html', {'producto':producto, 'msg':msg})
            notase = NentradaxproductoTb.objects.filter(prod=producto)
            if len(notase)>0:
                msg = "Este producto tiene notas de entrada, primero elimine esas notas si desea eliminar el producto"
                return render(request, 'restaurant/eliminarProducto.html', {'producto':producto, 'msg':msg})
            producto.delete()
            return HttpResponseRedirect(reverse('restaurant:gestionarProducto'))
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarProducto'))

# =================================
# == GESTIONAR NOTA DE COMPRA =====
# ================================
def gest_nota_compra_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            empleado = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if empleado.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
    
    if request.method == 'GET':
        ncompras = NotacompraTb.objects.all()
        return render(request, 'restaurant/gestionarNC.html', {'ncompras':ncompras})
    else:
        if 'registrarBtn' in request.POST:
            productos = ProductoTb.objects.all()
            proveedores = ProveedorTb.objects.all()
            return render(request, 'restaurant/registrarNC.html', {'productos':productos, 'proveedores':proveedores, 'seccion1':True})
        elif 'registrarBtn2' in request.POST: 
            productos = ProductoTb.objects.all()
            proveedores = ProveedorTb.objects.all()
            plista = list()
            for p in productos:
                if p.prod_nombre in request.POST:
                    plista.append(p)
            
            if len(plista)>0 and 'pro_id' in request.POST:
                proveedor = ProveedorTb.objects.filter(pro_id=request.POST['pro_id'])[0]
                return render(request, 'restaurant/registrarNC.html', {'plista':plista, 'proveedor':proveedor, 'seccion2':True})
            else:
                msg = "Seleccione el proveedor y almenos un producto para seguir.."
                return render(request, 'restaurant/registrarNC.html', {'productos':productos, 'proveedores':proveedores, 'seccion1':True, 'msg':msg})
        elif 'registrarBtn3' in request.POST:
            proveedor = ProveedorTb.objects.filter(pro_nombre=request.POST['prov'])[0]
            fecha = datetime.date.today()
            plista = list()
            productos = ProductoTb.objects.all()
            for p in productos:
                if p.prod_nombre in request.POST:
                    plista.append(p)

            pdlista = list()
            for p in plista:
                pdatos = dict()
                pdatos['prod']=p
                cantidad_name=p.prod_nombre+"C"
                pdatos['cantidad']=request.POST[cantidad_name]
                if not pdatos['cantidad'].isnumeric():
                    msg = "Rellene correctamente los campos para continuar"
                    return render(request, 'restaurant/registrarNC.html', {'plista':plista, 'proveedor':proveedor, 'seccion2':True, 'msg':msg})
                precio_name = p.prod_nombre+"P"
                pdatos['precio']=request.POST[precio_name]
                if not pdatos['precio'].isnumeric():
                    msg = "Rellene correctamente los campos para continuar"
                    return render(request, 'restaurant/registrarNC.html', {'plista':plista, 'proveedor':proveedor, 'seccion2':True, 'msg':msg})
                pu=float(pdatos['precio'])*float(pdatos['cantidad'])
                pdatos['subtotal']=pu
                pdlista.append(pdatos)

            total = 0
            for pd in pdlista:
                total+=pd['subtotal']
            return render(request, 'restaurant/registrarNC.html', {'seccion3':True, 'proveedor':proveedor, 'fecha':fecha, 'plista':pdlista, 'total':total})
        elif 'registrarNC' in request.POST:
            proveedor = ProveedorTb.objects.filter(pro_nombre=request.POST['prov'])[0]
            fecha = datetime.date.today()
            usuario = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            total = float(request.POST['total'])
            nueva_nc = NotacompraTb(notc_fecha=fecha, notc_total=total, usu=usuario, pro=proveedor)
            nueva_nc.save()

            plista = list()
            productos = ProductoTb.objects.all()
            for p in productos:
                if p.prod_nombre in request.POST:
                    cantidadname = p.prod_nombre+"C"
                    cantidad = int(request.POST[cantidadname])
                    precioname = p.prod_nombre+"P"
                    precio = float(request.POST[precioname])
                    subtotalname = p.prod_nombre+"S"
                    subtotal = float(request.POST[subtotalname])
                    ncxprod = NcompraxproductoTb(ncp_cantidad=cantidad, ncp_precio=precio, ncp_subt=subtotal, nc=nueva_nc, prod=p)
                    ncxprod.save()
            hora = datetime.datetime.now().time()
            accion = AccionTb.objects.filter(acc_id=9)[0]
            registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=usuario, acc=accion)
            registrarAccion.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarNC'))
        elif 'eliminarBtn' in request.POST:
            nc = NotacompraTb.objects.filter(notc_id=request.POST['eliminarBtn'])[0]
            return render(request, 'restaurant/eliminarNC.html', {'nc':nc})
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarNC'))
        elif 'eliminarNC' in request.POST:
            nc = NotacompraTb.objects.filter(notc_id=request.POST['eliminarNC'])[0]
            nc.detalle.clear()
            nc.delete()

            usuario = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            fecha = datetime.date.today()
            hora = datetime.datetime.now().time()
            accion = AccionTb.objects.filter(acc_id=10)[0]
            registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=usuario, acc=accion)
            registrarAccion.save()

            return HttpResponseRedirect(reverse('restaurant:gestionarNC'))
        elif 'verBtn' in request.POST:
            nc = NotacompraTb.objects.filter(notc_id=request.POST['verBtn'])[0]
            prds = nc.detalle.all()
            pdatos = list()
            for p in prds:
                det = NcompraxproductoTb.objects.filter(nc=nc, prod=p)[0]
                datos = dict()
                datos['prd']=p
                datos['cantidad']=det.ncp_cantidad
                datos['precio']=det.ncp_precio
                datos['subt']=det.ncp_subt
                pdatos.append(datos)
            return render(request, 'restaurant/verNC.html', {'detalle':pdatos, 'nc':nc})
# =================================
# == GESTIONAR NOTA DE ENTRADA =====
# ================================
def gest_nota_entrada_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            empleado = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if empleado.es_admin() == False:
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
    
    if request.method == 'GET':
        notas = NotaentradaTb.objects.all()
        return render(request, 'restaurant/gestionarNE.html', {'notase':notas})
    else:
        if 'registrarBtn' in request.POST:
            productos = ProductoTb.objects.all()
            return render(request, 'restaurant/registrarNE.html', {'productos':productos, 'seccion1':True})
        elif 'registrarBtn2' in request.POST:
            productos = ProductoTb.objects.all()
            plista = list()
            for p in productos:
                if p.prod_nombre in request.POST:
                    plista.append(p)
            if len(plista) == 0:
                return render(request, 'restaurant/registrarNE.html', {'seccion1':True, 'productos':productos, 'msg':"Debe seleccionar almenos un producto"})
            return render(request, 'restaurant/registrarNE.html', {'seccion2':True, 'plista':plista})
        elif 'registrarNE' in request.POST:
            productos = ProductoTb.objects.all()
            plista = list()
            for p in productos:
                if p.prod_nombre in request.POST:
                    plista.append(p)
            pdatos = list()
            for prd in plista:
                datos = dict()
                datos['prod'] = prd
                cantidadname = prd.prod_nombre+"C"
                cantidad = request.POST[cantidadname]
                if not cantidad.isnumeric():
                    return render(request, 'restaurant/registrarNE.html', {'seccion2':True, 'msg':"Introduzca las cantidades correcatmente", 'plista':plista})
                datos['cantidad']=int(cantidad)
                pdatos.append(datos)
            fecha = datetime.date.today()
            usuario = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            nueva_ne = NotaentradaTb(note_fecha=fecha, usu=usuario)
            nueva_ne.save()

            hora = datetime.datetime.now().time()
            accion = AccionTb.objects.filter(acc_id=11)[0]
            registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=usuario, acc=accion)
            registrarAccion.save()

            for det in pdatos:
                prod = det['prod']
                cantidad = det['cantidad']
                nu_det = NentradaxproductoTb(nep_cantidad=cantidad, prod=prod, ne=nueva_ne)
                nu_det.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarNE'))
        elif 'verBtn' in request.POST:
            note = NotaentradaTb.objects.filter(note_id=request.POST['verBtn'])[0]
            prds = note.detalle.all()
            detalle_list = list()
            for p in prds:
                det = NentradaxproductoTb.objects.filter(prod=p, ne=note)[0]
                datos = dict()
                datos['p'] = p
                datos['cantidad'] = det.nep_cantidad
                detalle_list.append(datos)
            return render(request, 'restaurant/verNE.html', {'note':note, 'detalle':detalle_list})
        elif 'eliminarBtn' in request.POST:
            note = NotaentradaTb.objects.filter(note_id=request.POST['eliminarBtn'])[0]
            return render(request, 'restaurant/eliminarNE.html', {'ne':note})
        elif 'eliminarNE' in request.POST:
            note = NotaentradaTb.objects.filter(note_id=request.POST['eliminarNE'])[0]
            note.detalle.clear()
            note.delete()

            usuario = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            fecha = datetime.date.today()
            hora = datetime.datetime.now().time()
            accion = AccionTb.objects.filter(acc_id=12)[0]
            registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=usuario, acc=accion)
            registrarAccion.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarNE'))
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarNE'))
# =================================
# == GESTIONAR ALMACEN =====
# ================================
def gest_almacen(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            emp = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if not emp.es_admin():
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
        
    if request.method == 'GET':
        almacenes = AlmacenTb.objects.all()
        return render(request, 'restaurant/gestionarAlmacen.html', {'almacenes':almacenes})
    else:
        if 'registrarBtn' in request.POST:
            return render(request, 'restaurant/registrarAlmacen.html')
        elif 'registrarAlmacen' in request.POST:
            alm_nombre = request.POST['alm_nombre']
            alm_ubicacion = request.POST['alm_ubicacion']
            if alm_nombre != "" and alm_ubicacion != "":
                almacenes = AlmacenTb.objects.filter(alm_nombre=alm_nombre)
                if len(almacenes)>0:
                    return render(request, 'restaurant/registrarAlmacen.html',{'msg':"Almacen ya registrado"})
                nu_almacen = AlmacenTb(alm_nombre=alm_nombre, alm_ubicacion=alm_ubicacion)
                nu_almacen.save()

                usuario = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                fecha = datetime.date.today()
                hora = datetime.datetime.now().time()
                accion = AccionTb.objects.filter(acc_id=13)[0]
                registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=usuario, acc=accion)
                registrarAccion.save()

                return render(request, 'restaurant/registrarAlmacen.html',{'msg':"Almacen registrado", 'ok':True})
            else:
                return render(request, 'restaurant/registrarAlmacen.html',{'msg':"Rellene todos los campos correctamente"})
        elif 'eliminarBtn' in request.POST:
            almacen = AlmacenTb.objects.filter(alm_id=request.POST['eliminarBtn'])[0]
            return render(request, 'restaurant/eliminarAlmacen.html', {'alm':almacen})
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarAlmacen'))
        elif 'eliminarAlm' in request.POST:
            almacen = AlmacenTb.objects.filter(alm_id=request.POST['eliminarAlm'])[0]
            lotes = LoteTb.objects.filter(alm=almacen)
            if len(lotes)>0:
                msg = 'Este almacen tiene lotes, no puede ser eliminado'
                return render(request, 'restaurant/eliminarAlmacen.html', {'alm':almacen, 'msg':msg})
            almacen.delete()
            return HttpResponseRedirect(reverse('restaurant:gestionarAlmacen'))
# =================================
# == GESTIONAR LOTES =====
# ================================
def obtener_entradas():
    entradas = NentradaxproductoTb.objects.all()
    elista = list()
    for e in entradas:
        lotes = LoteTb.objects.filter(nep=e)
        usados = 0
        for l in lotes:
            usados += l.lot_canti
        saldo = e.nep_cantidad - usados
        if saldo > 0:
            datos = dict()
            datos['entrada'] = e
            datos['saldo'] = saldo
            elista.append(datos)
    return elista

def registrarAccion(accion_id, usuario):
    fecha = datetime.date.today()
    hora = datetime.datetime.now().time()
    accion = AccionTb.objects.filter(acc_id=accion_id)[0]
    registrarAccion = BitacoraTb(bit_fecha=fecha, bit_hora=hora, usu=usuario, acc=accion)
    registrarAccion.save()

def gest_lote_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            emp = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if not emp.es_admin():
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
    
    if request.method == 'GET':
        lotes = LoteTb.objects.filter(lot_estado=1)
        return render(request, 'restaurant/gestionarLotes.html', {'lotes':lotes})
    else:
        if 'registrarBtn' in request.POST:
            elista = obtener_entradas()
            almacenes = AlmacenTb.objects.all()
            return render(request, 'restaurant/registrarLote.html', {'entradas':elista, 'almacenes':almacenes})
        elif 'registrarLote' in request.POST:
            lote_canti = request.POST['lote_canti']
            if 'alm_nombre' in request.POST and 'nep_id' in request.POST and lote_canti.isnumeric():
                almacen = AlmacenTb.objects.filter(alm_id=request.POST['alm_nombre'])[0]
                nep = NentradaxproductoTb.objects.filter(nep_id=request.POST['nep_id'])[0]
                lotecanti = int(lote_canti)
                sname = str(nep.nep_id)+"S"
                saldo = int(request.POST[sname])
                if lotecanti <= saldo:
                    fecha = datetime.date.today()
                    nu_lote = LoteTb(lot_canti=lote_canti, lot_fecha=fecha, lot_estado=1, prod=nep.prod, alm=almacen, nep=nep)
                    nu_lote.save()
                    primer_mov = MovimientoloteTb(lot=nu_lote, cant=lote_canti)
                    primer_mov.save()

                    usuario = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                    registrarAccion(14, usuario)

                    return HttpResponseRedirect(reverse('restaurant:gestionarLote'))
                else:
                    elista = obtener_entradas()
                    almacenes = AlmacenTb.objects.all()
                    msg = "La cantidad no debe ser mayor al saldo en la entrada"
                    return render(request, 'restaurant/registrarLote.html', {'entradas':elista, 'almacenes':almacenes, 'msg':msg}) 
            else:
                elista = obtener_entradas()
                almacenes = AlmacenTb.objects.all()
                msg = "Rellene correctamente la cantidad, ademas seleccione un almacen y entrada"
                return render(request, 'restaurant/registrarLote.html', {'entradas':elista, 'almacenes':almacenes, 'msg':msg})
        elif 'verBtn' in request.POST:
            lote = LoteTb.objects.filter(lot_id=request.POST['verBtn'])[0]
            movs = MovimientoloteTb.objects.filter(lot=lote)
            cant = 0
            for m in movs:
                cant += m.cant
            return render(request, 'restaurant/verLote.html', {'lote':lote, 'cantidad':cant})
        elif 'eliminarBtn' in request.POST:
            lote = LoteTb.objects.filter(lot_id=request.POST['eliminarBtn'])[0]
            return render(request, 'restaurant/eliminarLote.html', {'lote':lote})
        elif 'eliminarLote' in request.POST:
            lote = LoteTb.objects.filter(lot_id=request.POST['eliminarLote'])[0]
            lote.lot_estado = 0
            lote.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarLote'))
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarLote'))
# =================================
# == GESTIONAR NOTAS DE SALIDA =====
# ================================
def obtener_lote_cant(lote):
    movs = MovimientoloteTb.objects.filter(lot=lote)
    cant = 0
    for m in movs:
        cant += m.cant
    return cant

def obtener_almacenes_detalle():
    almacenes = AlmacenTb.objects.all()
    result = list()
    for a in almacenes:
        datos = dict()
        datos['alm'] = a
        lotes = LoteTb.objects.filter(lot_estado=1, alm=a)
        prds = dict()
        for l in lotes:
            if not l.prod.prod_nombre in prds:
                prds[l.prod.prod_nombre]=dict()
                prds[l.prod.prod_nombre]['prod']=l.prod
                prds[l.prod.prod_nombre]['cantidad']=obtener_lote_cant(l)
            else:
                prds[l.prod.prod_nombre]['cantidad']+=obtener_lote_cant(l)
        datos['prds'] = prds
        result.append(datos)
    almacenesf = list()
    for ele in result:
        datos = dict()
        datos['alm'] = ele['alm']
        datos['prds'] = list()
        for p in ele['prds']:
            datos['prds'].append(ele['prds'][p])
        almacenesf.append(datos)
    return almacenesf

def obtener_almacend(alm):
    lotes = LoteTb.objects.filter(lot_estado=1, alm=alm)
    prods_cants = dict()
    for l in lotes:
        if not l.prod.prod_nombre in prods_cants:
            prods_cants[l.prod.prod_nombre] = dict()
            prods_cants[l.prod.prod_nombre]['prod'] = l.prod
            prods_cants[l.prod.prod_nombre]['cantidad'] = obtener_lote_cant(l)
        else:
            prods_cants[l.prod.prod_nombre]['cantidad'] += obtener_lote_cant(l)
    stock_list = list()
    for dkey in prods_cants:
        stock_list.append(prods_cants[dkey])
    return stock_list    

def gest_ns_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            emp = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if not emp.es_admin():
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
    
    if request.method == 'GET':
        notas = NotasalidaTb.objects.filter(nots_estado = 1)
        return render(request, 'restaurant/gestionarNS.html', {'notass':notas})
    else:
        if 'registrarBtn' in request.POST:
            almacenes = obtener_almacenes_detalle()
            return render(request, 'restaurant/registrarNS.html', {'almacenes':almacenes, 'seccion1':True})
        elif 'registrar2' in request.POST:
            if 'alm' in request.POST:
                almacen = AlmacenTb.objects.filter(alm_id=request.POST['alm'])[0]
                astock = obtener_almacend(almacen)
                return render(request, 'restaurant/registrarNS.html', {'almacen':almacen, 'stock':astock, 'seccion2':True})
            else:
                almacenes = obtener_almacenes_detalle()
                msg="Seleccione un almacen antes de continuar"
                return render(request, 'restaurant/registrarNS.html', {'almacenes':almacenes, 'seccion1':True, 'msg':msg})
        elif 'registrarNS' in request.POST:
            almacen = AlmacenTb.objects.filter(alm_nombre=request.POST['almacen'])[0]
            productos = ProductoTb.objects.all()
            plista = list()
            for p in productos:
                datos = dict()
                if p.prod_nombre in request.POST:
                    datos['prd'] = p
                    sname = p.prod_nombre + 'S'
                    datos['stock'] = int(request.POST[sname])
                    cname = p.prod_nombre + 'C'
                    cantidad = request.POST[cname]
                    if cantidad.isnumeric() and int(cantidad)<=datos['stock']:
                        datos['cantidad'] = int(cantidad)
                    else:
                        astock = obtener_almacend(almacen)
                        msg = "Rellene correctamente las cantidades, recuerde que no debe superar el stock"
                        return render(request, 'restaurant/registrarNS.html', {'almacen':almacen, 'stock':astock, 'seccion2':True, 'msg':msg})
                    plista.append(datos)
            if len(plista)>0:
                eluser = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                fecha = datetime.date.today()
                nu_ns = NotasalidaTb(nots_fecha=fecha, nots_estado=1, usu=eluser, alm=almacen)
                nu_ns.save()
                for det in plista:
                    lotes = LoteTb.objects.filter(lot_estado=1, prod=det['prd'], alm=almacen)
                    saldo = det['cantidad']
                    for l in lotes:
                        lsaldo = obtener_lote_cant(l)
                        if lsaldo >= saldo:
                            numov = MovimientoloteTb(lot=l, cant=-saldo)
                            numov.save()
                            saldo = 0
                            if obtener_lote_cant(l) == 0:
                                l.lot_estado = 0 
                                l.save()
                            nu_detalla_nsp = NsalidaxproductoTb(nsp_cantidad=det['cantidad'], prod=l.prod, nots=nu_ns)
                            nu_detalla_nsp.save()
                            break
                        else:
                            saldo -= lsaldo
                            numov = MovimientoloteTb(lot=l, cant=-lsaldo)
                            numov.save()
                            l.lot_estado = 0 
                            l.save()
                registrarAccion(15, eluser)

                for p in plista:
                    racion = ConversionVenta.objects.filter(prod=p['prd'])
                    if len(racion)>0:
                        ra = racion[0]
                        nsp = NsalidaxproductoTb.objects.filter(prod=p['prd'], nots=nu_ns)[0]
                        cantidad = ra.cv_cantidad * nsp.nsp_cantidad
                        nu_stockventa = StockVenta(sv_cantidad=cantidad, cv=ra, ns=nu_ns)
                        nu_stockventa.save()

                return HttpResponseRedirect(reverse('restaurant:gestionarNS'))
            else:
                astock = obtener_almacend(almacen)
                msg = "Seleccione almenos un producto para registrar la nota de salida a produccion"
                return render(request, 'restaurant/registrarNS.html', {'almacen':almacen, 'stock':astock, 'seccion2':True, 'msg':msg})                
        elif 'verBtn' in request.POST:
            ns = NotasalidaTb.objects.filter(nots_id=request.POST['verBtn'])[0]
            stock = StockVenta.objects.filter(ns=ns)
            detalle = NsalidaxproductoTb.objects.filter(nots=ns)
            return render(request, 'restaurant/verNS.html', {'ns':ns, 'detalle':detalle, 'stock':stock})
        elif 'eliminarBtn' in request.POST:
            ns = NotasalidaTb.objects.filter(nots_id=request.POST['eliminarBtn'])[0]
            return render(request, 'restaurant/eliminarNS.html', {'ns':ns})
        elif 'eliminarNS' in request.POST:
            ns = NotasalidaTb.objects.filter(nots_id=request.POST['eliminarNS'])[0]
            ns.nots_estado = 0
            ns.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarNS'))
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarNS'))
# =================================
# == GESTIONAR CATEGORIA =====
# ================================
def gest_categoria_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            user = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            if not user.emp.es_admin():
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')

    if request.method == 'GET':
        cats = CategoriaTb.objects.filter(cat_estado=1)
        return render(request, 'restaurant/gestionarCategoria.html', {'cats':cats})
    else:
        if 'registrarBtn' in request.POST:
            return render(request, 'restaurant/registrarCategoria.html')
        elif 'registrarCategoria' in request.POST:
            cat_nombre = request.POST['cat_nombre']
            if cat_nombre != "":
                categorias = CategoriaTb.objects.filter(cat_nombre=cat_nombre)
                if len(categorias) > 0:
                    msg = "Categoria ya registrada.."
                    return render(request, 'restaurant/registrarCategoria.html', {'msg':msg})
                nu_cat = CategoriaTb(cat_nombre=cat_nombre, cat_estado=1)
                nu_cat.save()
                
                user = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                registrarAccion(16, user)

                msg = "Categoria registrada correctamente"
                return render(request, 'restaurant/registrarCategoria.html', {'msg':msg, 'ok':True})
            else:
                msg = "Rellene los campos para registrar la categoria.."
                return render(request, 'restaurant/registrarCategoria.html', {'msg':msg})
        elif 'editarBtn' in request.POST:
            cat = CategoriaTb.objects.filter(cat_id=request.POST['editarBtn'])[0]
            return render(request, 'restaurant/editarCategoria.html', {'cat':cat})
        elif 'editarCategoria' in request.POST:
            cat = CategoriaTb.objects.filter(cat_id=request.POST['editarCategoria'])[0]
            nu_nombre = request.POST['cat_nombre']
            if nu_nombre != "" and nu_nombre != cat.cat_nombre:
                cat.cat_nombre = nu_nombre
                cat.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarCategoria'))
# =================================
# == GESTIONAR MENU =====
# ================================
def es_decimal(cadena):
    if '.' in cadena:
        x = re.findall('^[0-9][0-9]*[.]{1}[0-9]*[1-9]+$', cadena)
        if len(x)>0: return True
        else: return False
    else:
        x = re.findall('^[1-9][0-9]*$', cadena)
        if len(x)>0: return True
        else: return False

def es_natural(cadena):
    x = re.findall('^[1-9][0-9]*$', cadena)
    if len(x)>0: return True
    else: return False

def gest_menu_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            user = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            if not user.emp.es_admin():
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
    
    if request.method == 'GET':
        menus = MenuTb.objects.filter(men_estado=1)
        return render(request, 'restaurant/gestionarMenu.html', {'menus':menus})
    else:
        if 'registrarBtn' in request.POST:
            categorias = CategoriaTb.objects.filter(cat_estado=1)
            return render(request, 'restaurant/registrarMenu.html', {'categorias':categorias})
        elif 'registrarMenu' in request.POST:
            categorias = CategoriaTb.objects.filter(cat_estado=1)
            if 'cat' in request.POST:
                categoria = CategoriaTb.objects.filter(cat_id=request.POST['cat'])[0]
                m_nombre = request.POST['men_nombre']
                m_desc = request.POST['men_desc']
                m_precio = request.POST['men_precio']
                if m_nombre != "" and m_desc != "" and es_decimal(m_precio):
                    menus = MenuTb.objects.filter(men_nombre=m_nombre)
                    if len(menus) > 0:
                        msg = "Menu ya registrado"
                        return render(request, 'restaurant/registrarMenu.html', {'categorias':categorias, 'msg':msg})
                    precio = float(m_precio)
                    nu_menu = MenuTb(cat=categoria, men_nombre=m_nombre, men_desc=m_desc, men_precio=precio, men_estado=1)
                    nu_menu.save()

                    user = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
                    registrarAccion(17, user)
                    
                    msg = "Menu registrado con exito.."
                    return render(request, 'restaurant/registrarMenu.html', {'categorias':categorias, 'msg':msg, 'ok':True})
                else:
                    msg = "Rellene los campos correctamente"
                    return render(request, 'restaurant/registrarMenu.html', {'categorias':categorias, 'msg':msg})
            else:
                msg = "Seleccione un almacen"
                return render(request, 'restaurant/registrarMenu.html', {'categorias':categorias, 'msg':msg})
        elif 'verBtn' in request.POST:
            men = MenuTb.objects.filter(men_id=request.POST['verBtn'])[0]
            return render(request, 'restaurant/verMenu.html', {'me':men})
        elif 'eliminarBtn' in request.POST:
            men = MenuTb.objects.filter(men_id=request.POST['eliminarBtn'])[0]
            return render(request, 'restaurant/eliminarMenu.html', {'me':men})
        elif 'eliminarMenu' in request.POST:
            men = MenuTb.objects.filter(men_id=request.POST['eliminarMenu'])[0]
            men.men_estado = 0
            men.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarMenu'))
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarMenu'))
        elif 'editarBtn' in request.POST:
            men = MenuTb.objects.filter(men_id=request.POST['editarBtn'])[0]
            return render(request, 'restaurant/editarMenu.html', {'me':men})
        elif 'editarMenu' in request.POST:
            men = MenuTb.objects.filter(men_id=request.POST['editarMenu'])[0]
            nu_nombre = request.POST['men_nombre']
            nu_desc = request.POST['men_desc']
            nu_precio = request.POST['men_precio']
            if nu_nombre != "" and nu_nombre != men.men_nombre:
                men.men_nombre = nu_nombre
                men.save()
            if nu_desc != "" and nu_desc != men.men_desc:
                men.men_desc = nu_desc
                men.save()
            if es_decimal(nu_precio) and nu_precio != men.men_precio:
                men.men_precio = float(nu_precio)
                men.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarMenu'))
# =====================================
# == GESTIONAR RACION DE PRODUCTO =====
# =====================================
def prods_sinracion():
    productos = ProductoTb.objects.all()
    plista = list()
    for p in productos:
        racion = ConversionVenta.objects.filter(prod=p)
        if len(racion)==0: plista.append(p)
    return plista

def gest_racion_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            user = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            if not user.emp.es_admin():
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
    
    if request.method == 'GET':
        raciones = ConversionVenta.objects.all()
        return render(request, 'restaurant/gestConversion.html', {'conversiones':raciones})
    else:
        if 'registrarBtn' in request.POST:
            prods = prods_sinracion()
            return render(request, 'restaurant/registrarConversion.html', {'productos':prods})
        elif 'registrarCon' in request.POST:
            prods = prods_sinracion()
            if 'prd' in request.POST:
                producto = ProductoTb.objects.filter(prod_id=request.POST['prd'])[0]
                cantidad = request.POST['cv_cantidad']
                if cantidad.isnumeric():
                    cantidad = int(cantidad)
                    nu_racion = ConversionVenta(cv_cantidad=cantidad, prod=producto)
                    nu_racion.save()
                    msg = "Racion registrada correctamente"
                    prods = prods_sinracion()
                    return render(request, 'restaurant/registrarConversion.html', {'productos':prods, 'msg':msg, 'ok':True})
                else:
                    msg = "Llene correctamente la cantidad"
                    return render(request, 'restaurant/registrarConversion.html', {'productos':prods, 'msg':msg})
            else:
                msg = "Seleccione un producto"
                return render(request, 'restaurant/registrarConversion.html', {'productos':prods, 'msg':msg})
        elif 'editarBtn' in request.POST:
            racion = ConversionVenta.objects.filter(cv_id=request.POST['editarBtn'])[0]
            return render(request, 'restaurant/editarConversion.html', {'racion':racion})
        elif 'editarCon' in request.POST:
            racion = ConversionVenta.objects.filter(cv_id=request.POST['editarCon'])[0]
            nu_cantidad = request.POST['cv_cantidad']
            if nu_cantidad.isnumeric():
                nu_cantidad = int(nu_cantidad)
                if nu_cantidad != racion.cv_cantidad and nu_cantidad > 0:
                    racion.cv_cantidad = nu_cantidad
                    racion.save()
            return HttpResponseRedirect(reverse('restaurant:gestionarCon'))
# =================================
# == GESTIONAR PEDIDO =====
# ================================
def gest_pedido_view(request):
    if request.method == 'GET':
        if 'userid' in request.session:
            empleado = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0].emp
            if (not empleado.es_admin()) and (not empleado.es_cajero()):
                return render(request, 'restaurant/errorPage.html')
        else:
            return render(request, 'restaurant/errorPage.html')
    
    if request.method == 'GET':
        pedidos = PedidoTb.objects.filter(ped_estado=1)
        return render(request, 'restaurant/gestionarPedidos.html', {'pedidos':pedidos})
    else:
        if 'registrarBtn' in request.POST:
            nits = NitTb.objects.all()
            menus = MenuTb.objects.filter(men_estado=1)
            return render(request, 'restaurant/registrarPedido.html', {'seccion1':True, 'menus':menus, 'nits':nits})
        elif 'siguiente' in request.POST:
            menus = MenuTb.objects.filter(men_estado=1)
            nits = NitTb.objects.all()
            menulista = list()
            total = 0
            for m in menus:
                datos = dict()
                if m.men_nombre in request.POST:
                    datos['menu'] = m
                    cantidadname = str(m.men_id)+'C'
                    cantidad = request.POST[cantidadname]
                    if es_natural(cantidad):
                        datos['cantidad'] = int(cantidad)
                        datos['subtot'] = m.men_precio * datos['cantidad']
                        total += datos['subtot']
                    else:
                        msg = "Rellene correctamente las cantidades"
                        return render(request, 'restaurant/registrarPedido.html', {'seccion1':True, 'menus':menus, 'msg':msg, 'nits':nits})
                    menulista.append(datos)
            if len(menulista)>0:
                elnit = None
                if 'nit' in request.POST:
                    elnit = NitTb.objects.filter(nit_numero=request.POST['nit'])[0]
                else:
                    elnit = NitTb.objects.filter(nit_dueno='sin nit')[0]
                return render(request, 'restaurant/registrarPedido.html', {'detallepedido': menulista, 'elnit':elnit, 'seccion2':True, 'total':total})
            else:
                msg = "Seleccione almenos un producto para realizar un pedido"
                return render(request, 'restaurant/registrarPedido.html', {'seccion1':True, 'menus':menus, 'msg':msg, 'nits':nits})
        elif 'confirmarpedido' in request.POST:
            fecha = datetime.date.today()
            hora = datetime.datetime.now().time()
            tipopedido = request.POST['tipop']
            total = float(request.POST['totalp'])
            nu_pedido = PedidoTb(ped_fecha=fecha, ped_hora=hora, ped_tipo=tipopedido, ped_total=total, ped_estado=1)
            nu_pedido.save()
            menus = MenuTb.objects.filter(men_estado=1)

            user = UsuarioTb.objects.filter(usu_id=request.session['userid'])[0]
            registrarAccion(18, user)

            for m in menus:
                name = 'm'+str(m.men_id)
                if name in request.POST:
                    cantname = 'c'+ str(m.men_id)
                    subtotname = 's'+ str(m.men_id)
                    cantidad = int(request.POST[cantname])
                    subtot = float(request.POST[subtotname])
                    nu_pm = Pedidoxmenu(pm_cantidad=cantidad, pm_subtotal=subtot, men=m, ped=nu_pedido)
                    nu_pm.save()

            thenit = NitTb.objects.filter(nit_numero=request.POST['thenit'])[0]
            nu_recibo = Recibo(rec_fecha=fecha, rec_hora=hora, rec_total=total, nit=thenit, ped=nu_pedido)
            nu_recibo.save()

            return HttpResponseRedirect(reverse('restaurant:gestionarPedido'))
        elif 'verBtn' in request.POST:
            pedido = PedidoTb.objects.filter(ped_id=request.POST['verBtn'])[0]
            detalle = Pedidoxmenu.objects.filter(ped=pedido)
            recib = Recibo.objects.filter(ped=pedido)
            if len(recib) > 0:
                recib = recib[0]
            return render(request, 'restaurant/verPedido.html', {'pedido':pedido, 'detalle':detalle, 'recibo':recib})
        elif 'seleccionarReporte' in request.POST:
            return render(request, 'restaurant/seleccionarReporte.html')
        elif 'verReporte' in request.POST:
            theyear = request.POST['yearR']
            themonth = request.POST['monthR']
            theday = request.POST['dayR']

            msg = "Datos incorrectos.."
            if es_natural(theyear):
                theyear = int(theyear)
                if not (theyear > 2000 and theyear <= 2021):
                    msg = "El año es incorrecto"
                    return render(request, 'restaurant/seleccionarReporte.html', {'msg':msg})
            else: return render(request, 'restaurant/seleccionarReporte.html', {'msg':msg})

            if es_natural(themonth):
                themonth = int(themonth)
                if not (themonth > 0 and themonth <= 12):
                    msg = "El mes es incorrecto"
                    return render(request, 'restaurant/seleccionarReporte.html', {'msg':msg})
            else: return render(request, 'restaurant/seleccionarReporte.html', {'msg':msg})

            if es_natural(theday):
                theday = int(theday)
                if not (theday > 0 and theday <= 28):
                    msg = "El dia es incorrecto"
                    return render(request, 'restaurant/seleccionarReporte.html', {'msg':msg})
            else: return render(request, 'restaurant/seleccionarReporte.html', {'msg':msg})

            request.session['lafecha'] = str(theyear) + '-' + str(themonth) + '-' + str(theday)

            return HttpResponseRedirect(reverse('restaurant:verReporte'))
        elif 'imprimirRecibo' in request.POST:
            request.session['pedrec'] = request.POST['imprimirRecibo']
            return HttpResponseRedirect(reverse('restaurant:repRecibo'))
# ===========================
# ==== CREATING THE REPORT ==
# ===========================
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def reporte_emps_view(request):
    fecha = request.session['lafecha']
    pedidos = PedidoTb.objects.filter(ped_estado=1, ped_fecha=fecha)
    pedlista = list()
    totalventas = 0
    for ped in pedidos:
        detalle = Pedidoxmenu.objects.filter(ped=ped)
        datos = dict()
        datos['ped'] = ped
        datos['detalle'] = detalle
        pedlista.append(datos)
        totalventas += ped.ped_total

    data = {
        'totaldia':totalventas,
        'pedidos':pedlista,
        'fecha':fecha
        }
    pdf = render_to_pdf('restaurant/reporte.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
# ===========================
# ==== CREATING THE RECIBO ==
# ===========================
def reporte_recibo(request):
    pedido = PedidoTb.objects.filter(ped_id=request.session['pedrec'])[0]
    detalle = Pedidoxmenu.objects.filter(ped=pedido)
    recib = Recibo.objects.filter(ped=pedido)
    if len(recib) > 0:
        recib = recib[0]
    data = {
        'pedido':pedido,
        'detalle':detalle,
        'recibo':recib
        }
    pdf = render_to_pdf('restaurant/imprecibo.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import EmpleadoTb, UsuarioTb, CargoTb, EmpleadoxcargoTb, ProveedorTb, AccionTb, BitacoraTb, NitTb, ProductoTb
import datetime

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
            if empleado.es_admin() == False:
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
                nitdoble = NitTb.objects.filter(nit_numero=nit_nro)
                if len(nitdoble) == 0:
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
            producto.delete()
            return HttpResponseRedirect(reverse('restaurant:gestionarProducto'))
        elif 'cancelarEliminar' in request.POST:
            return HttpResponseRedirect(reverse('restaurant:gestionarProducto'))
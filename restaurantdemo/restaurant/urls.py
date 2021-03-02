from django.urls import path 
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('RegistrarEmpleado/', views.registrar_empleados, name='regemp'),
    path('RegistrarUsuario/', views.registrar_usuario, name='regusu'),
    path('Empleados/', views.vista_empleados, name="vistaemps"),
    path('EmpleadoEditado/', views.empleado_editado, name = "empeditado"),
    path('Home/', views.home_page, name="home"),
    path('eliminarEmp/', views.eliminar_emp, name="eliminarEmp"),
    path('RegistrarCargo/', views.registrar_cargo, name="regCargo"),
    path('Cargos/', views.vista_cargos, name="vercargos"),
    path('editarCargo/', views.editar_cargo, name="editarcargo"),
    path('eliminarCargo/', views.eliminar_cargo, name="eliminarcargo"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logoutAction, name="logout"),
    path('Perfil/', views.perfil_view, name="perfil"),
    path('gestProveedores/', views.gestionar_proveedor_vista, name="gestionarProveedores"),
    path('gestAccion/', views.gest_accion_view, name="gestionarAccion"),
    path('gestBitacora/', views.gest_bitacora, name="gestionarBitacora"),
    path('gestNit/', views.gest_nit_view, name="gestionarNit"),
    path('gestProducto/', views.gest_producto_view, name="gestionarProducto"),
    path('gestNC/', views.gest_nota_compra_view, name="gestionarNC"),
    path('gestNE/', views.gest_nota_entrada_view, name="gestionarNE"),
    path('gestAlmacen/', views.gest_almacen, name="gestionarAlmacen"),
    path('gestLotes/', views.gest_lote_view, name="gestionarLote"),
    path('gestNS/', views.gest_ns_view, name="gestionarNS")
]

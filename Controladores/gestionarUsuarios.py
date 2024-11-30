# Importación de módulos necesarios
from PyQt5 import QtWidgets, uic
from Modelo.conexion import Comunicacion
import hashlib



class GestionarUsuarios(QtWidgets.QMainWindow):
    """
    Clase que maneja la interfaz y lógica para la gestión de usuarios del sistema.
    Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre usuarios.
    """

    def __init__(self):
        """
        Constructor de la clase. Inicializa la ventana y conecta todos los botones
        con sus respectivas funciones.
        """
        super().__init__()
        # Carga el archivo UI que contiene el diseño de la interfaz
        self.ventanaGestionarUsuarios = uic.loadUi('Vistas/ventanaGestionarUsuarios/ventanaGestionarUsuarios.ui', self)

        # Conexión de botones de navegación
        self.ventanaGestionarUsuarios.botonBaseDatos.clicked.connect(self.abrirPaginaBaseDatos)
        self.ventanaGestionarUsuarios.botonAgregar.clicked.connect(self.abrirPaginaAgregar)
        self.ventanaGestionarUsuarios.botonActualizar.clicked.connect(self.abrirPaginaActualizar)
        self.ventanaGestionarUsuarios.botonEliminar.clicked.connect(self.abrirPaginaEliminar)

        # Conexión de botones de operaciones CRUD
        self.ventanaGestionarUsuarios.botonRefrescar.clicked.connect(self.refrescarBaseDatos)
        self.ventanaGestionarUsuarios.botonAgregarUsuario.clicked.connect(self.agregarUsuario)
        self.ventanaGestionarUsuarios.botonBuscarActualizar.clicked.connect(self.buscarActualizarUsuario)
        self.ventanaGestionarUsuarios.botonActualizarUsuario.clicked.connect(self.actualizarUsuario)
        self.ventanaGestionarUsuarios.botonBuscarEliminar.clicked.connect(self.buscarEliminarUsuario)
        self.ventanaGestionarUsuarios.botonEliminarUsuario.clicked.connect(self.eliminarUsuario)

        # Conexión de eventos de selección en tablas
        self.ventanaGestionarUsuarios.tablaActualizar.itemClicked.connect(self.seleccionarUsuario)
        self.ventanaGestionarUsuarios.tablaEliminar.itemClicked.connect(self.seleccionarUsuarioEliminar)

        # Diccionario para manejar los campos de actualización
        self.lineEdits = {
            'id': self.ventanaGestionarUsuarios.lineEditIdActualizarUsuario,
            'nombre': self.ventanaGestionarUsuarios.lineEditNombreActualizarUsuario,
            'email': self.ventanaGestionarUsuarios.lineEditEmailActualizarUsuario,
            'contrasena': self.ventanaGestionarUsuarios.lineEditContrasenaActualizarUsuario,
            'rol': self.ventanaGestionarUsuarios.lineEditRolActualizarUsuario
        }

        # Inicialización de la conexión a la base de datos
        self.baseDatos = Comunicacion()

        # Referencias a tablas principales
        self.tablaUsuarios = self.ventanaGestionarUsuarios.tablaUsuarios
        self.tablaEliminar = self.ventanaGestionarUsuarios.tablaEliminar

        # Cargar datos iniciales
        self.refrescarBaseDatos()

    # Métodos de navegación entre páginas
    def abrirPaginaBaseDatos(self):
        """Muestra la página de visualización de la base de datos"""
        self.ventanaGestionarUsuarios.stackedWidget.setCurrentIndex(0)

    def abrirPaginaAgregar(self):
        """Muestra la página para agregar nuevos usuarios"""
        self.ventanaGestionarUsuarios.stackedWidget.setCurrentIndex(1)

    def abrirPaginaActualizar(self):
        """Muestra la página para actualizar usuarios existentes"""
        self.ventanaGestionarUsuarios.stackedWidget.setCurrentIndex(2)

    def abrirPaginaEliminar(self):
        """Muestra la página para eliminar usuarios"""
        self.ventanaGestionarUsuarios.stackedWidget.setCurrentIndex(3)

    # Métodos de operaciones con la base de datos
    def refrescarBaseDatos(self):
        """
        Actualiza la tabla de usuarios con los datos más recientes de la base de datos
        """
        datos = self.baseDatos.mostrarUsuarios()
        self.tablaUsuarios.setRowCount(len(datos))

        for row, usuario in enumerate(datos):
            for col, valor in enumerate(usuario[0:]):
                self.tablaUsuarios.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def agregarUsuario(self):
        """
        Agrega un nuevo usuario a la base de datos con los datos ingresados en el formulario
        """
        # Obtener datos de los campos
        id = self.ventanaGestionarUsuarios.lineEditAgregarId.text()
        nombre = self.ventanaGestionarUsuarios.lineEditAgregarNombre.text()
        email = self.ventanaGestionarUsuarios.lineEditAgregarEmail.text()
        contrasena = self.ventanaGestionarUsuarios.lineEditAgregarContrasena.text()
        rol = self.ventanaGestionarUsuarios.lineEditAgregarRol.text()

        contrasenaHash = self.hashContrasena(contrasena)

        # Intentar agregar el usuario
        agregarUsuarioBD = self.baseDatos.agregarUsuarios(id, nombre, email, contrasenaHash, rol)

        # Limpiar campos después de la operación
        self.ventanaGestionarUsuarios.lineEditAgregarId.setText("")
        self.ventanaGestionarUsuarios.lineEditAgregarNombre.setText("")
        self.ventanaGestionarUsuarios.lineEditAgregarEmail.setText("")
        self.ventanaGestionarUsuarios.lineEditAgregarContrasena.setText("")
        self.ventanaGestionarUsuarios.lineEditAgregarRol.setText("")

        # Mostrar resultado de la operación
        if agregarUsuarioBD:
            print("agregado")
            self.ventanaGestionarUsuarios.signalAgregar.setText("Usuario agregado")
            self.refrescarBaseDatos()
        else:
            print("no agregado")
            self.ventanaGestionarUsuarios.signalAgregar.setText("Usuario NO agregado")

    def buscarActualizarUsuario(self):
        """
        Busca usuarios para actualizar según el criterio ingresado
        """
        usuarioBuscar = self.ventanaGestionarUsuarios.lineEditBuscarActualizar.text()
        buscarUsuarioBD = self.baseDatos.buscarUsuariosActualizar(usuarioBuscar)
        self.ventanaGestionarUsuarios.lineEditBuscarActualizar.clear()

        if len(buscarUsuarioBD) == 0:
            self.ventanaGestionarUsuarios.signalActualizarUsuario.setText("Usuario NO encontrado")
        else:
            self.ventanaGestionarUsuarios.signalActualizarUsuario.setText("Coincidencias encontradas")
            self.tablaActualizarUsuario = self.ventanaGestionarUsuarios.tablaActualizar
            self.tablaActualizarUsuario.setRowCount(len(buscarUsuarioBD))

            for row, usuario in enumerate(buscarUsuarioBD):
                for col, valor in enumerate(usuario[0:]):
                    self.tablaActualizarUsuario.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarUsuario(self, item):
        """
        Maneja la selección de un usuario en la tabla de actualización
        """
        row = item.row()
        columnas = ['id', 'nombre', 'email', 'contrasena', 'rol']
        for col, campo in enumerate(columnas, start=0):
            valor = self.ventanaGestionarUsuarios.tablaActualizar.item(row, col).text()
            self.lineEdits[campo].setText(valor)

    def actualizarUsuario(self):
        """
        Actualiza los datos del usuario seleccionado con la información ingresada
        """
        filaSeleccionada = self.ventanaGestionarUsuarios.tablaActualizar.currentRow()

        if filaSeleccionada < 0:
            self.ventanaGestionarUsuarios.signalActualizarUsuario.setText("Por favor seleccione un usuario")
            return

        idOriginal = self.ventanaGestionarUsuarios.tablaActualizar.item(filaSeleccionada, 0).text()

        # Obtener nuevos valores
        nuevo_id = self.lineEdits['id'].text()
        nuevo_nombre = self.lineEdits['nombre'].text()
        nuevo_email = self.lineEdits['email'].text()
        nueva_contrasena = self.lineEdits['contrasena'].text()
        nueva_contrasena = self.hashContrasena(nueva_contrasena)
        nuevo_rol = self.lineEdits['rol'].text()

        # Verificar campos completos
        if not all([nuevo_id, nuevo_nombre, nuevo_email, nueva_contrasena, nuevo_rol]):
            self.ventanaGestionarUsuarios.signalActualizarUsuario.setText("Por favor complete todos los campos")
            return

        actualizacion_exitosa = self.baseDatos.actualizarUsuariosMismoId(idOriginal, nuevo_id, nuevo_nombre, nuevo_email, nueva_contrasena, nuevo_rol)

        if actualizacion_exitosa:
            self.ventanaGestionarUsuarios.signalActualizarUsuario.setText("Usuario actualizado")
            self.refrescarBaseDatos()

            # Limpiar campos
            for lineEdit in self.lineEdits.values():
                lineEdit.clear()

            self.ventanaGestionarUsuarios.lineEditBuscarActualizar.clear()
            self.ventanaGestionarUsuarios.tablaActualizar.setRowCount(0)
        else:
            self.ventanaGestionarUsuarios.signalActualizarUsuario.setText("Error al actualizar")

    def buscarEliminarUsuario(self):
        """
        Busca usuarios para eliminar según el criterio ingresado
        """
        usuarioBuscar = self.ventanaGestionarUsuarios.lineEditBuscarEliminar.text()
        buscarUsuarioenBD = self.baseDatos.buscarUsuariosActualizar(usuarioBuscar)

        if len(buscarUsuarioenBD) == 0:
            self.ventanaGestionarUsuarios.signalEliminar.setText("Usuario NO encontrado")
        else:
            self.ventanaGestionarUsuarios.signalEliminar.setText("Coincidencias encontradas")
            self.tablaEliminar.setRowCount(len(buscarUsuarioenBD))

            for row, usuario in enumerate(buscarUsuarioenBD):
                for col, valor in enumerate(usuario[0:]):
                    self.tablaEliminar.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarUsuarioEliminar(self, item):
        """
        Maneja la selección de un usuario en la tabla de eliminación
        """
        fila_seleccionada = item.row()
        id_item = self.ventanaGestionarUsuarios.tablaEliminar.item(fila_seleccionada, 0)

        if id_item is not None:
            id_usuarios = id_item.text()
            print(f"ID del usuario seleccionado: {id_usuarios}")
            self.id_usuario_seleccionado = id_usuarios
            self.ventanaGestionarUsuarios.signalEliminar.setText(f"Usuario seleccionado: {id_usuarios}")
            self.ventanaGestionarUsuarios.botonEliminarUsuario.setEnabled(True)
        else:
            print("No se pudo obtener el ID del Usuario")
            self.ventanaGestionarUsuarios.signalEliminar.setText("Error al seleccionar el usuario")
            self.ventanaGestionarUsuarios.botonEliminarUsuario.setEnabled(False)

    def eliminarUsuario(self):
        """
        Elimina el usuario seleccionado de la base de datos
        """
        if not hasattr(self, 'id_usuario_seleccionado'):
            self.ventanaGestionarUsuarios.signalEliminar.setText("Por favor, seleccione un usuario primero")
            return

        try:
            if self.baseDatos.eliminarUsuarios(self.id_usuario_seleccionado):
                self.ventanaGestionarUsuarios.signalEliminar.setText(f"Usuario {self.id_usuario_seleccionado} eliminado con éxito")
                self.refrescarBaseDatos()
                self.ventanaGestionarUsuarios.tablaEliminar.setRowCount(0)
                delattr(self, 'id_usuario_seleccionado')
                self.ventanaGestionarUsuarios.botonEliminarUsuario.setEnabled(False)
                self.ventanaGestionarUsuarios.lineEditBuscarEliminar.clear()
            else:
                self.ventanaGestionarUsuarios.signalEliminar.setText("Error al eliminar el Usuario")

        except Exception as e:
            print(f"Error inesperado: {e}")
            self.ventanaGestionarUsuarios.signalEliminar.setText("Error inesperado al eliminar el Usuario")

        print("Operación de eliminación completada")

    def hashContrasena(self, contrasena):
        return hashlib.sha256(contrasena.encode()).hexdigest()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    menu = GestionarUsuarios()
    menu.show()
    app.exec_()
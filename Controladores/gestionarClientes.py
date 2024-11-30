# Importación de las librerías y las clases de otros archivos
from PyQt5 import QtWidgets, uic
from Modelo.conexion import Comunicacion

# Clase principal para gestionar clientes en una interfaz gráfica con PyQt5
class GestionarClientes(QtWidgets.QMainWindow):

    def __init__(self):
        """
        Constructor de la clase. Inicializa la interfaz y conecta los botones con sus funciones.
        """
        super().__init__()
        self.ventanaGestionarClientes = uic.loadUi('Vistas/ventanaGestionarClientes/ventanaGestionarClientes.ui', self)

        # Conexión de botones de navegación
        self.ventanaGestionarClientes.botonBaseDatos.clicked.connect(self.abrirPaginaBaseDatos)
        self.ventanaGestionarClientes.botonAgregar.clicked.connect(self.abrirPaginaAgregar)
        self.ventanaGestionarClientes.botonActualizar.clicked.connect(self.abrirPaginaActualizar)
        self.ventanaGestionarClientes.botonEliminar.clicked.connect(self.abrirPaginaEliminar)
        #self.ventanaGestionarClientes.botonVolver.clicked.connect(self.abrirPaginaInicio)

        # Conexión de botones de operaciones CRUD
        self.ventanaGestionarClientes.botonRefrescar.clicked.connect(self.refrescarBaseDatos)
        self.ventanaGestionarClientes.botonAgregarCliente.clicked.connect(self.agregarCliente)
        self.ventanaGestionarClientes.botonBuscarActualizar.clicked.connect(self.buscarActualizarCliente)
        self.ventanaGestionarClientes.botonActualizarCliente.clicked.connect(self.actualizarCliente)
        self.ventanaGestionarClientes.botonBuscarEliminar.clicked.connect(self.buscarEliminarCliente)
        self.ventanaGestionarClientes.botonEliminarCliente.clicked.connect(self.eliminarCliente)

        # Conexión de eventos de selección en tablas
        self.ventanaGestionarClientes.tablaActualizar.itemClicked.connect(self.seleccionarCliente)
        self.ventanaGestionarClientes.tablaEliminar.itemClicked.connect(self.seleccionarClienteEliminar)

        # Diccionario para manejar los campos de texto de actualización
        self.lineEdits = {
            'id': self.ventanaGestionarClientes.lineEditIdActualizarCliente,
            'nombre': self.ventanaGestionarClientes.lineEditNombreActualizarCliente,
            'email': self.ventanaGestionarClientes.lineEditEmailActualizarCliente,
            'telefono': self.ventanaGestionarClientes.lineEditTelefonoActualizarCliente,
            'direccion': self.ventanaGestionarClientes.lineEditDireccionActualizarCliente
        }

        # Inicialización de la conexión a la base de datos y referencias a tablas
        self.baseDatos = Comunicacion()
        self.tablaClientes = self.ventanaGestionarClientes.tablaClientes
        self.tablaEliminar = self.ventanaGestionarClientes.tablaEliminar

        self.refrescarBaseDatos()

    # Funciones de navegación entre páginas
    def abrirPaginaBaseDatos(self):
        """Muestra la página de base de datos"""
        self.ventanaGestionarClientes.stackedWidget.setCurrentIndex(0)

    def abrirPaginaAgregar(self):
        """Muestra la página para agregar clientes"""
        self.ventanaGestionarClientes.stackedWidget.setCurrentIndex(1)

    def abrirPaginaActualizar(self):
        """Muestra la página para actualizar clientes"""
        self.ventanaGestionarClientes.stackedWidget.setCurrentIndex(2)

    def abrirPaginaEliminar(self):
        """Muestra la página para eliminar clientes"""
        self.ventanaGestionarClientes.stackedWidget.setCurrentIndex(3)

    '''def abrirPaginaInicio(self):
        """
        Oculta la ventana actual y muestra el menú principal de opciones
        """
        from menuOpciones import MenuOpciones

        self.hide()  # Oculta la ventana actual de MenuOpciones
        self.menu_window = MenuOpciones()
        self.menu_window.showMenuOpciones()  # Muestra la ventana de login
    '''

    # Funciones de operaciones con la base de datos
    def refrescarBaseDatos(self):
        """
        Actualiza la tabla de clientes con los datos más recientes de la base de datos
        """
        datos = self.baseDatos.mostrarClientes()
        self.tablaClientes.setRowCount(len(datos))

        for row, cliente in enumerate(datos):
            for col, valor in enumerate(cliente[0:]):
                self.tablaClientes.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def agregarCliente(self):
        """
        Agrega un nuevo cliente a la base de datos con los datos ingresados en el formulario
        """
        id = self.ventanaGestionarClientes.lineEditAgregarId.text()
        nombre = self.ventanaGestionarClientes.lineEditAgregarNombre.text()
        email = self.ventanaGestionarClientes.lineEditAgregarEmail.text()
        telefono = self.ventanaGestionarClientes.lineEditAgregarTelefono.text()
        direccion = self.ventanaGestionarClientes.lineEditAgregarDireccion.text()

        print(id, nombre, email, telefono, direccion)

        agregarClienteBD = self.baseDatos.agregarCliente(id, nombre, email, telefono, direccion)

        # Limpia los campos del formulario
        self.ventanaGestionarClientes.lineEditAgregarId.setText("")
        self.ventanaGestionarClientes.lineEditAgregarNombre.setText("")
        self.ventanaGestionarClientes.lineEditAgregarEmail.setText("")
        self.ventanaGestionarClientes.lineEditAgregarTelefono.setText("")
        self.ventanaGestionarClientes.lineEditAgregarDireccion.setText("")

        if agregarClienteBD:
            print("agregado")
            self.ventanaGestionarClientes.signalAgregar.setText("Cliente agregado")
            self.refrescarBaseDatos()
        else:
            print("no agregado")
            self.ventanaGestionarClientes.signalAgregar.setText("Cliente NO agregado")

    def buscarActualizarCliente(self):
        """
        Busca clientes en la base de datos y muestra los resultados en la tabla de actualización
        """
        clienteBuscar = self.ventanaGestionarClientes.lineEditBuscarActualizar.text()
        buscarClienteBD = self.baseDatos.buscarClienteActualizar(clienteBuscar)
        self.ventanaGestionarClientes.lineEditBuscarActualizar.clear()

        if len(buscarClienteBD) == 0:
            self.ventanaGestionarClientes.signalActualizarCliente.setText("Cliente NO encontrado")
        else:
            self.ventanaGestionarClientes.signalActualizarCliente.setText("Coincidencias encontradas")

            self.tablaActualizarCliente = self.ventanaGestionarClientes.tablaActualizar
            self.tablaActualizarCliente.setRowCount(len(buscarClienteBD))

            for row, cliente in enumerate(buscarClienteBD):
                for col, valor in enumerate(cliente[0:]):
                    self.tablaActualizarCliente.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarCliente(self, item):
        """
        Maneja la selección de un cliente en la tabla de actualización
        """
        row = item.row()
        columnas = ['id', 'nombre', 'email', 'telefono', 'direccion']
        for col, campo in enumerate(columnas, start=0):
            valor = self.ventanaGestionarClientes.tablaActualizar.item(row, col).text()
            self.lineEdits[campo].setText(valor)

    def actualizarCliente(self):
        """
        Actualiza los datos de un cliente seleccionado en la base de datos
        """
        filaSeleccionada = self.ventanaGestionarClientes.tablaActualizar.currentRow()

        if filaSeleccionada < 0:
            self.ventanaGestionarClientes.signalActualizarCliente.setText("Por favor seleccione un cliente")
            return

        idOriginal = self.ventanaGestionarClientes.tablaActualizar.item(filaSeleccionada, 0).text()

        # Obtener los nuevos valores de los LineEdit
        nuevo_id = self.lineEdits['id'].text()
        nuevo_nombre = self.lineEdits['nombre'].text()
        nuevo_email = self.lineEdits['email'].text()
        nuevo_telefono = self.lineEdits['telefono'].text()
        nueva_direccion = self.lineEdits['direccion'].text()

        # Verificar que todos los campos tengan valor
        if not all([nuevo_id, nuevo_nombre, nuevo_email, nuevo_telefono, nueva_direccion]):
            self.ventanaGestionarClientes.signalActualizarCliente.setText("Por favor complete todos los campos")
            return
        else:
            actualizacion_exitosa = self.baseDatos.actualizarClienteMismoId(idOriginal, nuevo_id, nuevo_nombre, nuevo_email, nuevo_telefono, nueva_direccion)

        if actualizacion_exitosa:
            self.ventanaGestionarClientes.signalActualizarCliente.setText("Cliente actualizado")
            self.refrescarBaseDatos()

            # Limpiar los campos después de actualizar
            for lineEdit in self.lineEdits.values():
                lineEdit.clear()

            self.ventanaGestionarClientes.lineEditBuscarActualizar.clear()
            self.ventanaGestionarClientes.tablaActualizar.setRowCount(0)
        else:
            self.ventanaGestionarClientes.signalActualizarCliente.setText("Error al actualizar")

    def buscarEliminarCliente(self):
        """
        Busca clientes para eliminar y muestra los resultados en la tabla de eliminación
        """
        clienteBuscar = self.ventanaGestionarClientes.lineEditBuscarEliminar.text()
        buscarClienteenBD = self.baseDatos.buscarClienteActualizar(clienteBuscar)

        if len(buscarClienteenBD) == 0:
            self.ventanaGestionarClientes.signalEliminar.setText("Cliente NO encontrado")
        else:
            self.ventanaGestionarClientes.signalEliminar.setText("Coincidencias encontradas")

            self.tablaEliminar.setRowCount(len(buscarClienteenBD))

            for row, cliente in enumerate(buscarClienteenBD):
                for col, valor in enumerate(cliente[0:]):
                    self.tablaEliminar.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarClienteEliminar(self, item):
        """
        Maneja la selección de un cliente en la tabla de eliminación
        """
        fila_seleccionada = item.row()
        id_item = self.ventanaGestionarClientes.tablaEliminar.item(fila_seleccionada, 0)

        if id_item is not None:
            id_clientes = id_item.text()
            print(f"ID del cliente seleccionado: {id_clientes}")

            self.id_cliente_seleccionado = id_clientes
            self.ventanaGestionarClientes.signalEliminar.setText(f"Cliente seleccionado: {id_clientes}")
            self.ventanaGestionarClientes.botonEliminarCliente.setEnabled(True)
        else:
            print("No se pudo obtener el ID del cliente")
            self.ventanaGestionarClientes.signalEliminar.setText("Error al seleccionar el cliente")
            self.ventanaGestionarClientes.botonEliminarCliente.setEnabled(False)

    def eliminarCliente(self):
        """
        Elimina el cliente seleccionado de la base de datos
        """
        if not hasattr(self, 'id_cliente_seleccionado'):
            self.ventanaGestionarClientes.signalEliminar.setText("Por favor, seleccione un cliente primero")
            return

        try:
            if self.baseDatos.eliminarCliente(self.id_cliente_seleccionado):
                self.ventanaGestionarClientes.signalEliminar.setText(
                    f"cliente {self.id_cliente_seleccionado} eliminado con éxito")
                self.refrescarBaseDatos()

                self.ventanaGestionarClientes.tablaEliminar.setRowCount(0)
                delattr(self, 'id_cliente_seleccionado')
                self.ventanaGestionarClientes.botonEliminarCliente.setEnabled(False)
                self.ventanaGestionarClientes.lineEditBuscarEliminar.clear()
            else:
                self.ventanaGestionarClientes.signalEliminar.setText("Error al eliminar el cliente")

        except Exception as e:
            print(f"Error inesperado: {e}")
            self.ventanaGestionarClientes.signalEliminar.setText("Error inesperado al eliminar el cliente")

        print("Operación de eliminación completada")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    menu = GestionarClientes()
    menu.show()
    app.exec_()
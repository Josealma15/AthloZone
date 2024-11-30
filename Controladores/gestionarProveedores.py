# Importación de las librerías y las clases de otros archivos
from PyQt5 import QtWidgets, uic
from Modelo.conexion import Comunicacion

# Clase principal para gestionar proveedores en una interfaz gráfica con PyQt5
class GestionarProveedores(QtWidgets.QMainWindow):

    def __init__(self):
        """
        Constructor de la clase. Inicializa la interfaz y conecta los botones con sus funciones.
        """
        super().__init__()
        self.ventanaGestionarProveedores = uic.loadUi(
            'Vistas/ventanaGestionarProveedores/ventanaGestionarProveedores.ui', self)

        # Conexión de botones de navegación
        self.ventanaGestionarProveedores.botonBaseDatos.clicked.connect(self.abrirPaginaBaseDatos)
        self.ventanaGestionarProveedores.botonAgregar.clicked.connect(self.abrirPaginaAgregar)
        self.ventanaGestionarProveedores.botonActualizar.clicked.connect(self.abrirPaginaActualizar)
        self.ventanaGestionarProveedores.botonEliminar.clicked.connect(self.abrirPaginaEliminar)
        #self.ventanaGestionarProveedores.botonVolver.clicked.connect(self.abrirPaginaInicio)

        # Conexión de botones de operaciones CRUD
        self.ventanaGestionarProveedores.botonRefrescar.clicked.connect(self.refrescarBaseDatos)
        self.ventanaGestionarProveedores.botonAgregarProveedor.clicked.connect(self.agregarProveedor)
        self.ventanaGestionarProveedores.botonBuscarActualizar.clicked.connect(self.buscarActualizarProveedor)
        self.ventanaGestionarProveedores.botonActualizarProveedor.clicked.connect(self.actualizarProveedor)
        self.ventanaGestionarProveedores.botonBuscarEliminar.clicked.connect(self.buscarEliminarProveedor)
        self.ventanaGestionarProveedores.botonEliminarProveedor.clicked.connect(self.eliminarProveedor)

        # Conexión de eventos de selección en tablas
        self.ventanaGestionarProveedores.tablaActualizarProveedor.itemClicked.connect(self.seleccionarProveedor)
        self.ventanaGestionarProveedores.tablaEliminar.itemClicked.connect(self.seleccionarProveedorEliminar)

        # Diccionario para manejar los campos de texto de actualización
        self.lineEdits = {
            'nombre': self.ventanaGestionarProveedores.lineEditNombreActualizarProveedor,
            'email': self.ventanaGestionarProveedores.lineEditEmailActualizarProveedor,
            'telefono': self.ventanaGestionarProveedores.lineEditTelefonoActualizarProveedor,
            'direccion': self.ventanaGestionarProveedores.lineEditDireccionActualizarProveedor
        }

        # Inicialización de la conexión a la base de datos y referencias a tablas
        self.baseDatos = Comunicacion()
        self.tablaProveedores = self.ventanaGestionarProveedores.tablaProveedores
        self.tablaEliminar = self.ventanaGestionarProveedores.tablaEliminar

        self.refrescarBaseDatos()

    # Funciones de navegación entre páginas
    def abrirPaginaBaseDatos(self):
        """Muestra la página de base de datos"""
        self.ventanaGestionarProveedores.stackedWidget.setCurrentIndex(0)

    def abrirPaginaAgregar(self):
        """Muestra la página para agregar proveedores"""
        self.ventanaGestionarProveedores.stackedWidget.setCurrentIndex(1)

    def abrirPaginaActualizar(self):
        """Muestra la página para actualizar proveedores"""
        self.ventanaGestionarProveedores.stackedWidget.setCurrentIndex(2)

    def abrirPaginaEliminar(self):
        """Muestra la página para eliminar proveedores"""
        self.ventanaGestionarProveedores.stackedWidget.setCurrentIndex(3)

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
        Actualiza la tabla de proveedores con los datos más recientes de la base de datos
        """
        datos = self.baseDatos.mostrarProveedores()
        self.tablaProveedores.setRowCount(len(datos))

        for row, proveedor in enumerate(datos):
            for col, valor in enumerate(proveedor[0:]):
                self.tablaProveedores.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def agregarProveedor(self):
        """
        Agrega un nuevo proveedor a la base de datos con los datos ingresados en el formulario
        """
        nombre = self.ventanaGestionarProveedores.lineEditAgregarNombre.text()
        email = self.ventanaGestionarProveedores.lineEditAgregarEmail.text()
        telefono = self.ventanaGestionarProveedores.lineEditAgregarTelefono.text()
        direccion = self.ventanaGestionarProveedores.lineEditAgregarDireccion.text()

        agregarProveedorBD = self.baseDatos.agregarProveedor(nombre, email, telefono, direccion)

        # Limpia los campos del formulario
        self.ventanaGestionarProveedores.lineEditAgregarNombre.setText("")
        self.ventanaGestionarProveedores.lineEditAgregarEmail.setText("")
        self.ventanaGestionarProveedores.lineEditAgregarTelefono.setText("")
        self.ventanaGestionarProveedores.lineEditAgregarDireccion.setText("")

        if agregarProveedorBD:
            print("agregado")
            self.ventanaGestionarProveedores.signalAgregar.setText("Proveedor agregado")
            self.refrescarBaseDatos()
        else:
            print("no agregado")
            self.ventanaGestionarProveedores.signalAgregar.setText("Proveedor NO agregado")

    def buscarActualizarProveedor(self):
        """
        Busca proveedores en la base de datos y muestra los resultados en la tabla de actualización
        """
        proveedorBuscar = self.ventanaGestionarProveedores.lineEditBuscarActualizar.text()
        buscarProveedorBD = self.baseDatos.buscarProveedorActualizar(proveedorBuscar)
        self.ventanaGestionarProveedores.lineEditBuscarActualizar.clear()

        if len(buscarProveedorBD) == 0:
            self.ventanaGestionarProveedores.signalActualizarProveedor.setText("Proveedor NO encontrado")
        else:
            self.ventanaGestionarProveedores.signalActualizarProveedor.setText("Coincidencias encontradas")

            # Mostrar resultados encontrados en la tabla
            self.tablaActualizarProveedor = self.ventanaGestionarProveedores.tablaActualizarProveedor
            self.tablaActualizarProveedor.setRowCount(len(buscarProveedorBD))

            for row, proveedor in enumerate(buscarProveedorBD):
                for col, valor in enumerate(proveedor[0:]):
                    self.tablaActualizarProveedor.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarProveedor(self, item):
        """
        Maneja la selección de un proveedor en la tabla de actualización
        """
        row = item.row()
        columnas = ['nombre', 'email', 'telefono', 'direccion']
        for col, campo in enumerate(columnas, start=1):
            valor = self.ventanaGestionarProveedores.tablaActualizarProveedor.item(row, col).text()
            self.lineEdits[campo].setText(valor)
            print(campo, self.lineEdits[campo], valor)

    def actualizarProveedor(self):
        """
        Actualiza los datos de un proveedor seleccionado en la base de datos
        """
        filaSeleccionada = self.ventanaGestionarProveedores.tablaActualizarProveedor.currentRow()

        if filaSeleccionada < 0:
            self.ventanaGestionarProveedores.signalActualizarProducto.setText("Por favor seleccione un proveedor")
            return

        idOriginal = self.ventanaGestionarProveedores.tablaActualizarProveedor.item(filaSeleccionada, 0).text()

        # Obtener los nuevos valores de los LineEdit
        nuevo_nombre = self.lineEdits['nombre'].text()
        nuevo_email = self.lineEdits['email'].text()
        nuevo_telefono = self.lineEdits['telefono'].text()
        nueva_direccion = self.lineEdits['direccion'].text()

        # Verificar que todos los campos tengan valor
        if not all([nuevo_nombre, nuevo_email, nuevo_telefono, nueva_direccion]):
            self.ventanaGestionarProveedores.signalActualizarProducto.setText("Por favor complete todos los campos")
            return
        else:
            actualizacion_exitosa = self.baseDatos.actualizarProveedorMismoId(idOriginal, nuevo_nombre, nuevo_email,
                                                                              nuevo_telefono, nueva_direccion)

        if actualizacion_exitosa:
            self.ventanaGestionarProveedores.signalActualizarProveedor.setText("Proveedor actualizado")
            self.refrescarBaseDatos()

            # Limpiar los campos después de actualizar
            for lineEdit in self.lineEdits.values():
                lineEdit.clear()

            self.ventanaGestionarProveedores.lineEditBuscarActualizar.clear()
            self.ventanaGestionarProveedores.tablaActualizarProveedor.setRowCount(0)
        else:
            self.ventanaGestionarProveedores.signalActualizarProveedor.setText("Error al actualizar")

    def buscarEliminarProveedor(self):
        """
        Busca proveedores para eliminar y muestra los resultados en la tabla de eliminación
        """
        proveedorBuscar = self.ventanaGestionarProveedores.lineEditBuscarEliminar.text()
        buscarProveedorenBD = self.baseDatos.buscarProveedorActualizar(proveedorBuscar)

        if len(buscarProveedorenBD) == 0:
            self.ventanaGestionarProveedores.signalEliminar.setText("Proveedor NO encontrado")
        else:
            self.ventanaGestionarProveedores.signalEliminar.setText("Coincidencias encontradas")

            # Mostrar resultados encontrados en la tabla
            self.tablaEliminar.setRowCount(len(buscarProveedorenBD))

            for row, proveedor in enumerate(buscarProveedorenBD):
                for col, valor in enumerate(proveedor[0:]):
                    self.tablaEliminar.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarProveedorEliminar(self, item):
        """
        Maneja la selección de un proveedor en la tabla de eliminación
        """
        fila_seleccionada = item.row()
        print(fila_seleccionada)
        id_item = self.ventanaGestionarProveedores.tablaEliminar.item(fila_seleccionada, 0)

        if id_item is not None:
            id_proveedor = id_item.text()
            print(f"ID del proveedor seleccionado: {id_proveedor}")  # Para depuración

            self.id_proveedor_seleccionado = id_proveedor
            self.ventanaGestionarProveedores.signalEliminar.setText(f"Proveedor seleccionado: {id_proveedor}")
            self.ventanaGestionarProveedores.botonEliminarProveedor.setEnabled(True)
        else:
            print("No se pudo obtener el ID del proveedor")
            self.ventanaGestionarProveedores.signalEliminar.setText("Error al seleccionar el proveedor")
            self.ventanaGestionarProveedores.botonEliminarProveedor.setEnabled(False)

    def eliminarProveedor(self):
        """
        Elimina el proveedor seleccionado de la base de datos
        """
        if not hasattr(self, 'id_proveedor_seleccionado'):
            self.ventanaGestionarProveedores.signalEliminar.setText("Por favor, seleccione un proveedor primero")
            return

        try:
            if self.baseDatos.eliminarProveedor(self.id_proveedor_seleccionado):
                self.ventanaGestionarProveedores.signalEliminar.setText(
                    f"Proveedor {self.id_proveedor_seleccionado} eliminado con éxito")
                self.refrescarBaseDatos()

                # Limpiar la tabla y resetear el estado
                self.ventanaGestionarProveedores.tablaEliminar.setRowCount(0)
                delattr(self, 'id_proveedor_seleccionado')
                self.ventanaGestionarProveedores.botonEliminarProveedor.setEnabled(False)
                self.ventanaGestionarProveedores.lineEditBuscarEliminar.clear()
            else:
                self.ventanaGestionarProveedores.signalEliminar.setText("Error al eliminar el proveedor")

        except Exception as e:
            print(f"Error inesperado: {e}")
            self.ventanaGestionarProveedores.signalEliminar.setText("Error inesperado al eliminar el proveedor")

        print("Operación de eliminación completada")  # Para depuración


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    menu = GestionarProveedores()
    menu.show()
    app.exec_()
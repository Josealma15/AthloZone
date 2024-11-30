# Importación de las librerías y las clases de otros archivos
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QHeaderView
from Modelo.conexion import Comunicacion

# Clase principal para gestionar stock en una interfaz gráfica con PyQt5
class ControlarStock(QtWidgets.QMainWindow):
    """
    Clase principal para el control de stock.
    Maneja la interfaz gráfica y las operaciones CRUD de productos.
    """

    def __init__(self):
        """
        Constructor de la clase ControlarStock.
        Inicializa la interfaz gráfica y conecta los eventos de los botones.
        """
        super().__init__()

        # Cargar la interfaz desde el archivo UI
        self.ventanaControlarStock = uic.loadUi('Vistas/ventanaControlarStock/ventanaControlarStock.ui', self)

        # Conexión de botones de navegación
        self.ventanaControlarStock.botonBaseDatos.clicked.connect(self.abrirPaginaBaseDatos)
        self.ventanaControlarStock.botonAgregar.clicked.connect(self.abrirPaginaAgregar)
        self.ventanaControlarStock.botonActualizar.clicked.connect(self.abrirPaginaActualizar)
        self.ventanaControlarStock.botonEliminar.clicked.connect(self.abrirPaginaEliminar)
        #self.ventanaControlarStock.botonVolver.clicked.connect(self.abrirPaginaInicio)

        # Conexión de botones de operaciones CRUD
        self.ventanaControlarStock.botonRefrescar.clicked.connect(self.refrescarBaseDatos)
        self.ventanaControlarStock.botonAgregarProducto.clicked.connect(self.agregarProducto)
        self.ventanaControlarStock.botonBuscarActualizar.clicked.connect(self.buscarActualizarProducto)
        self.ventanaControlarStock.botonActualizarProducto.clicked.connect(self.actualizarProducto)
        self.ventanaControlarStock.botonBuscarEliminar.clicked.connect(self.buscarEliminarProducto)
        self.ventanaControlarStock.botonEliminarProducto.clicked.connect(self.eliminarProducto)

        # Conexión de eventos de selección en tablas
        self.ventanaControlarStock.tablaProductosActualizar.itemClicked.connect(self.seleccionarProducto)
        self.ventanaControlarStock.tablaEliminar.itemClicked.connect(self.seleccionarProductoEliminar)

        # Diccionario para manejar los campos de actualización
        self.lineEdits = {
            'nombre': self.ventanaControlarStock.lineEditNombreActualizarStock,
            'descripcion': self.ventanaControlarStock.lineEditDescripcionActualizarStock,
            'precio': self.ventanaControlarStock.lineEditPrecioActualizarStock,
            'cantidad_stock': self.ventanaControlarStock.lineEditCantidadStockActualizarStock,
            'categoria': self.ventanaControlarStock.lineEditCategoriaActualizarStock
        }

        # Inicialización de componentes
        self.baseDatos = Comunicacion()
        self.tablaProductos = self.ventanaControlarStock.tablaProductos
        self.tablaEliminar = self.ventanaControlarStock.tablaEliminar

        # Configuración de las tablas
        self.tablaProductos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refrescarBaseDatos()

    # ======================================================
    # Funciones de navegación entre páginas
    # ======================================================

    def abrirPaginaBaseDatos(self):
        """Muestra la página de vista de base de datos"""
        self.ventanaControlarStock.stackedWidget.setCurrentIndex(0)

    def abrirPaginaAgregar(self):
        """Muestra la página para agregar productos"""
        self.ventanaControlarStock.stackedWidget.setCurrentIndex(1)

    def abrirPaginaActualizar(self):
        """Muestra la página para actualizar productos"""
        self.ventanaControlarStock.stackedWidget.setCurrentIndex(2)

    def abrirPaginaEliminar(self):
        """Muestra la página para eliminar productos"""
        self.ventanaControlarStock.stackedWidget.setCurrentIndex(3)

    '''def abrirPaginaInicio(self):
        """
        Vuelve a la página de inicio según el rol del usuario.
        Redirige a MenuOpciones para admin o MenuOpcionesVendedor para vendedor.
        """

        #print(self.ventanaControlarStock.signalRol.text())

        if self.signalRol == "Admin":
            self.hide()
            self.menu_window = MenuOpciones()
            self.menu_window.showMenuOpciones()
        else:
            self.hide()
            self.menu_window = MenuOpcionesVendedor()
            self.menu_window.showMenuOpcionesVendedor()
    '''
    # ======================================================
    # Funciones de operaciones con la base de datos
    # ======================================================

    def refrescarBaseDatos(self):
        """
        Actualiza la tabla de productos con los datos más recientes de la base de datos
        """
        datos = self.baseDatos.mostrarProductos()
        self.tablaProductos.setRowCount(len(datos))

        for row, producto in enumerate(datos):
            for col, valor in enumerate(producto[0:]):
                self.tablaProductos.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def agregarProducto(self):
        """
        Agrega un nuevo producto a la base de datos.
        Obtiene los valores de los campos de texto y los envía a la base de datos.
        """
        # Obtener valores de los campos
        nombre = self.ventanaControlarStock.lineEditAgregarNombre.text()
        descripcion = self.ventanaControlarStock.lineEditAgregarDescripcion.text()
        precio = self.ventanaControlarStock.lineEditAgregarPrecio.text()
        cantidad_stock = self.ventanaControlarStock.lineEditAgregarCantidadStock.text()
        categoria = self.ventanaControlarStock.lineEditAgregarCategoria.text()

        # Intentar agregar el producto
        agregarProductoaBD = self.baseDatos.agregarProductoControlarStock(nombre, descripcion, precio, cantidad_stock, categoria)

        # Limpiar campos después de agregar
        self.ventanaControlarStock.lineEditAgregarNombre.setText("")
        self.ventanaControlarStock.lineEditAgregarDescripcion.setText("")
        self.ventanaControlarStock.lineEditAgregarPrecio.setText("")
        self.ventanaControlarStock.lineEditAgregarCantidadStock.setText("")
        self.ventanaControlarStock.lineEditAgregarCategoria.setText("")

        # Mostrar resultado de la operación
        if agregarProductoaBD:
            self.ventanaControlarStock.signalAgregar.setText("Producto agregado")
            self.refrescarBaseDatos()
        else:
            self.ventanaControlarStock.signalAgregar.setText("Producto NO agregado")

    def buscarActualizarProducto(self):
        """
        Busca productos para actualizar según el término de búsqueda.
        Muestra los resultados en la tabla de actualización.
        """
        productoBuscar = self.ventanaControlarStock.lineEditBuscarActualizar.text()
        buscarProductoenBD = self.baseDatos.buscarProductoActualizarControlarStock(productoBuscar)

        if len(buscarProductoenBD) == 0:
            self.ventanaControlarStock.signalActualizarProducto.setText("Producto NO encontrado")
        else:
            self.ventanaControlarStock.signalActualizarProducto.setText("Coincidencias encontradas")

            # Actualizar tabla con resultados
            self.tablaProductosActualizar = self.ventanaControlarStock.tablaProductosActualizar
            self.tablaProductosActualizar.setRowCount(len(buscarProductoenBD))

            for row, producto in enumerate(buscarProductoenBD):
                for col, valor in enumerate(producto[0:]):
                    self.tablaProductosActualizar.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarProducto(self, item):
        """
        Maneja la selección de un producto en la tabla de actualización.
        Rellena los campos de edición con los datos del producto seleccionado.
        """
        row = item.row()
        columnas = ['nombre', 'descripcion', 'precio', 'cantidad_stock', 'categoria']
        for col, campo in enumerate(columnas, start=1):
            valor = self.ventanaControlarStock.tablaProductosActualizar.item(row, col).text()
            self.lineEdits[campo].setText(valor)

    def actualizarProducto(self):
        """
        Actualiza los datos de un producto existente en la base de datos.
        Verifica que todos los campos estén completos antes de actualizar.
        """
        filaSeleccionada = self.ventanaControlarStock.tablaProductosActualizar.currentRow()

        if filaSeleccionada < 0:
            self.ventanaControlarStock.signalActualizarProducto.setText("Por favor seleccione un producto")
            return

        idOriginal = self.ventanaControlarStock.tablaProductosActualizar.item(filaSeleccionada, 0).text()

        # Obtener nuevos valores
        nuevo_nombre = self.lineEdits['nombre'].text()
        nueva_descripcion = self.lineEdits['descripcion'].text()
        nuevo_precio = self.lineEdits['precio'].text()
        nueva_cantidad = self.lineEdits['cantidad_stock'].text()
        nueva_categoria = self.lineEdits['categoria'].text()

        # Verificar campos completos
        if not all([nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_cantidad, nueva_categoria]):
            self.ventanaControlarStock.signalActualizarProducto.setText("Por favor complete todos los campos")
            return

        # Actualizar producto
        actualizacion_exitosa = self.baseDatos.actualizarProductoMismoId(idOriginal, nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_cantidad, nueva_categoria)

        if actualizacion_exitosa:
            self.ventanaControlarStock.signalActualizarProducto.setText("Producto actualizado")
            self.refrescarBaseDatos()

            # Limpiar campos y tabla
            for lineEdit in self.lineEdits.values():
                lineEdit.clear()
            self.ventanaControlarStock.lineEditBuscarActualizar.clear()
            self.ventanaControlarStock.tablaProductosActualizar.setRowCount(0)
        else:
            self.ventanaControlarStock.signalActualizarProducto.setText("Error al actualizar")

    def buscarEliminarProducto(self):
        """
        Busca productos para eliminar según el término de búsqueda.
        Muestra los resultados en la tabla de eliminación.
        """
        productoBuscar = self.ventanaControlarStock.lineEditBuscarEliminar.text()
        buscarProductoenBD = self.baseDatos.buscarProductoActualizarControlarStock(productoBuscar)

        if len(buscarProductoenBD) == 0:
            self.ventanaControlarStock.signalEliminar.setText("Producto NO encontrado")
        else:
            self.ventanaControlarStock.signalEliminar.setText("Coincidencias encontradas")

            # Mostrar resultados en tabla
            self.tablaEliminar.setRowCount(len(buscarProductoenBD))
            for row, producto in enumerate(buscarProductoenBD):
                for col, valor in enumerate(producto[0:]):
                    self.tablaEliminar.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    def seleccionarProductoEliminar(self, item):
        """
        Maneja la selección de un producto en la tabla de eliminación.
        Guarda el ID del producto seleccionado para su posterior eliminación.
        """
        fila_seleccionada = item.row()
        id_item = self.ventanaControlarStock.tablaEliminar.item(fila_seleccionada, 0)

        if id_item is not None:
            id_producto = id_item.text()
            self.id_producto_seleccionado = id_producto
            self.ventanaControlarStock.signalEliminar.setText(f"Producto seleccionado: {id_producto}")
            self.ventanaControlarStock.botonEliminarProducto.setEnabled(True)
        else:
            self.ventanaControlarStock.signalEliminar.setText("Error al seleccionar el producto")
            self.ventanaControlarStock.botonEliminarProducto.setEnabled(False)

    def eliminarProducto(self):
        """
        Elimina el producto seleccionado de la base de datos.
        Verifica que haya un producto seleccionado antes de intentar eliminar.
        """
        if not hasattr(self, 'id_producto_seleccionado'):
            self.ventanaControlarStock.signalEliminar.setText("Por favor, seleccione un producto primero")
            return

        try:
            if self.baseDatos.eliminarProducto(self.id_producto_seleccionado):
                self.ventanaControlarStock.signalEliminar.setText(
                    f"Producto {self.id_producto_seleccionado} eliminado con éxito")

                # Limpiar tabla y selección
                self.ventanaControlarStock.tablaEliminar.setRowCount(0)
                delattr(self, 'id_producto_seleccionado')
                self.ventanaControlarStock.botonEliminarProducto.setEnabled(False)
                self.ventanaControlarStock.lineEditBuscarEliminar.clear()
                self.refrescarBaseDatos()
            else:
                self.ventanaControlarStock.signalEliminar.setText("Error al eliminar el producto de la base de datos")

        except Exception as e:
            print(f"Error inesperado: {e}")
            self.ventanaControlarStock.signalEliminar.setText("Error inesperado al eliminar el producto")


# ======================================================
# Punto de entrada de la aplicación
# ======================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    menu = ControlarStock()
    menu.show()
    app.exec_()
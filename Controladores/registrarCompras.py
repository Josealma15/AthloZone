# Importación de módulos necesarios de PyQt5
from PyQt5 import QtWidgets, uic
from Modelo.conexion import Comunicacion

#CLase principal de realizar ventas
class RegistrarCompras(QtWidgets.QMainWindow):

    # Metodo constructor
    def __init__(self):
        super().__init__()

        # Cargar la interfaz grafica
        self.ventanaRegistrarCompras = uic.loadUi('Vistas/ventanaRegistrarCompras/ventanaRegistrarCompras.ui', self)

        # Hacer la conexion con los botones
        self.ventanaRegistrarCompras.botonBaseDatos.clicked.connect(self.abrirPaginaBaseDatos)
        #self.ventanaRegistrarCompras.botonAgregar.clicked.connect(self.abrirPaginaAgregar)
        self.ventanaRegistrarCompras.botonCrearCompra.clicked.connect(self.crearCompraObtenerId)
        self.ventanaRegistrarCompras.botonAgregarDetalles.clicked.connect(self.abrirPaginaAgregarDetalleCompra)
        self.ventanaRegistrarCompras.botonAgregarProductoCompra.clicked.connect(self.agregarProductoCompra)
        self.ventanaRegistrarCompras.botonActualizar.clicked.connect(self.abrirPaginaActualizar)
        self.ventanaRegistrarCompras.botonActualizarDetalles.clicked.connect(self.abrirPaginaActualizarDetalleCompra)
        self.ventanaRegistrarCompras.botonEliminar.clicked.connect(self.abrirPaginaEliminar)
        self.ventanaRegistrarCompras.botonEliminarDetalleCompra.clicked.connect(self.abrirPaginaEliminarDetalleCompra)
        self.ventanaRegistrarCompras.botonRefrescar.clicked.connect(self.refrescarBaseDatos)
        self.ventanaRegistrarCompras.botonFinalizarDetalleCompra.clicked.connect(self.finalizarCompra)
        self.ventanaRegistrarCompras.botonBuscarEliminar.clicked.connect(self.buscarEliminarCompra)
        self.ventanaRegistrarCompras.botonEliminarCompra.clicked.connect(self.eliminarCompra)
        self.ventanaRegistrarCompras.botonEliminarProductoCompra.clicked.connect(self.eliminarProductoDetalle)
        self.ventanaRegistrarCompras.botonBuscarActualizarCompra.clicked.connect(self.buscarActualizarCompra)
        self.ventanaRegistrarCompras.botonActualizarDetalle.clicked.connect(self.actualizarDetalleCompra)
        self.ventanaRegistrarCompras.botonAgregarProductoActualizar.clicked.connect(self.agregarProductoDetalleCompraActualizar)
        self.ventanaRegistrarCompras.botonActualizarCompra.clicked.connect(self.actualizarCompra)
        self.ventanaRegistrarCompras.botonSalirDetalles.clicked.connect(self.salirDetalleCompra)
        self.ventanaRegistrarCompras.botonVolverEliminar.clicked.connect(self.salirEliminarDetalleCompra)

        self.ventanaRegistrarCompras.tablaActualizarCompra.itemClicked.connect(self.seleccionarActualizarCompra)
        self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.itemClicked.connect(self.seleccionarActualizarDetalleCompra)
        self.ventanaRegistrarCompras.tablaEliminar.itemClicked.connect(self.seleccionarEliminarCompra)
        self.ventanaRegistrarCompras.tablaEliminarDetalleCompra.itemClicked.connect(self.seleccionarEliminarProductoDetalle)

        # Definir las tablas de la interfaz
        self.tablaCompras = self.ventanaRegistrarCompras.tablaCompras
        self.tablaAgregarDetalleCompra = self.ventanaRegistrarCompras.tablaAgregarDetalleCompra
        self.tablaActualizarCompra = self.ventanaRegistrarCompras.tablaActualizarCompra
        self.tablaActualizarDetalleCompra = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra
        self.tablaEliminar = self.ventanaRegistrarCompras.tablaEliminar
        self.tablaEliminarDetalleCompra = self.ventanaRegistrarCompras.tablaEliminarDetalleCompra

        # Diccionario para manejar los campos de actualización
        self.lineEdits = {
            'fecha': self.ventanaRegistrarCompras.lineEditFechaActualizarCompra,
            'id_proveedor': self.ventanaRegistrarCompras.lineEditIdProveedorActualizarCompra
        }

        # Diccionario para manejar los campos de actualización detalles
        self.lineEditsDetalles = {
            'id_producto': self.ventanaRegistrarCompras.lineEditIdProductoActualizarDetalleCompra,
            'cantidad': self.ventanaRegistrarCompras.lineEditCantidadActualizarDetalleCompra,
            'precio_unitario': self.ventanaRegistrarCompras.lineEditPrecioUnitarioActualizarDetalleCompra
        }

        # Establecer conexion con la base de datos
        self.baseDatos = Comunicacion()

        # Ejecutar el metodo refrescar base datos para mostrar las ventas
        self.refrescarBaseDatos()

    # Funciones de navegación entre páginas

    def abrirPaginaBaseDatos(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(0)

    def abrirPaginaAgregar(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(1)

    def abrirPaginaEliminar(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(2)

    def abrirPaginaAgregarDetalleCompra(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(3)

    def abrirPaginaActualizar(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(4)

    def abrirPaginaActualizarDetalleCompra(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(5)
        id_venta = self.id_seleccionado_actualizar
        self.refrescarBaseDatosDetallesCompraActualizar(id_venta)
        self.ventanaRegistrarCompras.lineEditFechaActualizarCompra.setText("")
        self.ventanaRegistrarCompras.lineEditIdProveedorActualizarCompra.setText("")
        self.ventanaRegistrarCompras.tablaActualizarCompra.setRowCount(0)

    def abrirPaginaEliminarDetalleCompra(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(6)
        self.actualizarDetalleCompraEliminar(self.id_compra_seleccionada)
        self.ventanaRegistrarCompras.lineEditBuscarEliminar.clear()
        self.ventanaRegistrarCompras.tablaEliminar.setRowCount(0)



    ################################### AQUI SE AGREGAN LAS FUNCIONES PARA HACERLOS CON LA BASE DE DATOS ###################################

    # Mostrar compras de la base de datos
    def refrescarBaseDatos(self):

        datos = self.baseDatos.mostrarCompras()
        self.tablaCompras.setRowCount(len(datos))

        for row, compra in enumerate(datos):
            for col, valor in enumerate(compra[0:]):
                self.tablaCompras.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    # Mostrar los detalles de las compras
    def refrescarBaseDatosDetallesCompra(self, id_compra):

        total_compra = 0
        datos = self.baseDatos.mostrarDetallesCompras(id_compra)
        self.tablaAgregarDetalleCompra.setRowCount(len(datos))
        print(f" REFRESCAR BASE DATOS DETALLES COMPRA {id_compra}")
        print(datos)

        for row, detalle in enumerate(datos):
            total_compra += int(detalle[3] * detalle[4])
            for col, valor in enumerate(detalle[0:]):
                self.tablaAgregarDetalleCompra.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

        self.ventanaRegistrarCompras.signalTotalDetalleCompra.setText(str(total_compra))
        self.refrescarBaseDatos()
        self.baseDatos.actualizarTotalCompra(id_compra, total_compra)
        self.total_compra = total_compra

    # Mostrar los detalles de compras despues de actualizar alguno
    def refrescarBaseDatosDetallesCompraActualizar(self, id_compra):

        total_compra = 0
        datos = self.baseDatos.mostrarDetallesCompras(id_compra)
        self.tablaActualizarDetalleCompra.setRowCount(len(datos))
        print(f" REFRESCAR BASE DATOS DETALLES COMPRA {id_compra}")
        print(datos)

        for row, detalle in enumerate(datos):
            total_compra += int(detalle[3] * detalle[4])
            for col, valor in enumerate(detalle[0:]):
                self.tablaActualizarDetalleCompra.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

        self.ventanaRegistrarCompras.siganlTotalVentaActualizar.setText(str(total_compra))
        self.refrescarBaseDatos()
        self.baseDatos.actualizarTotalCompra(id_compra, total_compra)
        self.total_compra = total_compra

    # Crear el id para la compra que se va a realizar
    def crearCompraObtenerId(self):

        fecha = self.ventanaRegistrarCompras.lineEditFechaDetalleCompra.text()
        id_proveedores = self.ventanaRegistrarCompras.lineEditIdProveedorDetalleCompra.text()

        # Inicialmente, el total será 0
        total = 0

        # Crear una compra con total 0
        id_compra = self.baseDatos.agregarCompra(fecha, id_proveedores, total)

        if id_compra:
            print("Compra iniciada")
            self.ventanaRegistrarCompras.signalAgregarProductoDetalle.setText(f"Venta iniciada {id_compra}")
            self.refrescarBaseDatos()
            self.ventanaRegistrarCompras.botonCrearCompra.setEnabled(False)
            self.id_creado = id_compra

        else:
            print("Error al iniciar la compra")
            self.ventanaRegistrarCompras.signalAgregarProductoDetalle.setText("Error al iniciar la compra")

        #self.ventanaRegistrarCompras.lineEditFechaDetalleCompra.setText("")
        #self.ventanaRegistrarCompras.lineEditIdProveedorDetalleCompra.setText("")
        #self.ventanaRegistrarCompras.signalTotalVenta.setText("")

    # Agregar un producto a la compra
    def agregarProductoCompra(self):

        id_producto = self.ventanaRegistrarCompras.lineEditIdProductoDetalleCompra.text()
        cantidad = self.ventanaRegistrarCompras.lineEditCantidadDetalleCompra.text()
        precio_unitario = self.ventanaRegistrarCompras.lineEditPrecioUnitarioDetalleCompra.text()
        #precio_unitario = self.baseDatos.obtenerValorProducto(id_producto)

        agregarProductoCompraBD = self.baseDatos.agregarProductoCompra(self.id_creado, id_producto, cantidad, precio_unitario)

        # actualizar stock
        actualizar_stock = self.baseDatos.actualizarStockProducto(id_producto, cantidad, precio_unitario)

        if agregarProductoCompraBD != False and actualizar_stock != False:
            self.refrescarBaseDatosDetallesCompra(self.id_creado)
            self.ventanaRegistrarCompras.lineEditIdProductoDetalleCompra.setText("")
            self.ventanaRegistrarCompras.lineEditCantidadDetalleCompra.setText("")
            self.ventanaRegistrarCompras.lineEditPrecioUnitarioDetalleCompra.setText("")
            self.ventanaRegistrarCompras.signalAgregarProductoDetalle.setText("Producto agregado a la compra")




            # Actualizar el valor total de la venta
            tabla = self.ventanaRegistrarCompras.tablaAgregarDetalleCompra
            total = 0

            for fila in range(tabla.rowCount()):
                cantidad = tabla.item(fila, 3)  # Columna de Cantidad
                precio_unitario = tabla.item(fila, 4)  # Columna de Precio Unitario

                if cantidad and precio_unitario:
                    cantidad_valor = float(cantidad.text())
                    precio_unitario_valor = float(precio_unitario.text())
                    total += cantidad_valor * precio_unitario_valor

                    self.ventanaRegistrarCompras.signalTotalDetalleCompra.setText(str(total))

            self.baseDatos.actualizarTotalCompra(self.id_creado, total)

        else:
            self.ventanaRegistrarCompras.signalAgregarProductoDetalle.setText("Error al agregar producto a la compra")


        self.refrescarBaseDatosDetallesCompra(self.id_creado)
        self.ventanaRegistrarCompras.lineEditIdProductoDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditCantidadDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditPrecioUnitarioDetalleCompra.setText("")

    # Finalizar la compra y agregarla a la base de datos
    def finalizarCompra(self):

        id_compra = self.ventanaRegistrarCompras.tablaAgregarDetalleCompra.item(0, 1).text()
        total = self.ventanaRegistrarCompras.signalTotalDetalleCompra.text()

        finalizarCompraBD = self.baseDatos.actualizarTotalCompra(id_compra, total)

        if finalizarCompraBD:
            print("Compra finalizada")
            print(f"Total fue {total}")
            self.ventanaRegistrarCompras.signalAgregarProductoDetalle.setText("Compra finalizada")
        else:
            print("Error al finalizar la compra")
            self.ventanaRegistrarCompras.signalAgregarProductoDetalle.setText("Error al finalizar la Compra")

        # Quitar los valores ingresados de los line edit
        self.ventanaRegistrarCompras.lineEditFechaDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditIdProveedorDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditIdProductoDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditCantidadDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditPrecioUnitarioDetalleCompra.setText("")
        self.ventanaRegistrarCompras.signalTotalDetalleCompra.setText("0")

        # Limpiar la tabla
        self.ventanaRegistrarCompras.tablaAgregarDetalleCompra.setRowCount(0)

        # Activar de nuevo boton de crear venta y obtener id
        self.ventanaRegistrarCompras.botonCrearCompra.setEnabled(True)

        # Refrescar base de datos de Comras
        self.refrescarBaseDatos()

    # Buscar una compra para actualizarla
    def buscarActualizarCompra(self):

        compra_buscar = self.ventanaRegistrarCompras.lineEditBuscarActualizarCompra.text()
        buscar_compra_bd = self.baseDatos.buscarCompraActualizar(compra_buscar)
        self.ventanaRegistrarCompras.lineEditBuscarActualizarCompra.clear()

        if len(buscar_compra_bd) == 0:
            self.ventanaRegistrarCompras.signalActualizarCompra.setText("Compra NO encontrada")

        else:
            self.ventanaRegistrarCompras.signalActualizarCompra.setText("Coincidencias encontradas")

            # MOSTRAR RESULTADOS ENCONTRADOS CUANDO SE DA A BOTON BUSCAR
            self.tablaActualizarCompra.setRowCount(len(buscar_compra_bd))

            for row, compra in enumerate(buscar_compra_bd):
                for col, valor in enumerate(compra[0:]):
                    self.tablaActualizarCompra.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    # Seleccionar una compra para actualizarla
    def seleccionarActualizarCompra(self, item):
        row = item.row()
        self.id_seleccionado_actualizar = self.ventanaRegistrarCompras.tablaActualizarCompra.item(row, 0).text()
        columnas = ['fecha', 'id_proveedor']
        for col, campo in enumerate(columnas, start=1):
            valor = self.ventanaRegistrarCompras.tablaActualizarCompra.item(row, col).text()
            self.lineEdits[campo].setText(valor)

    # Actualizar la compra (finalizar proceso)
    def actualizarCompra(self, item):

        fila_seleccionada = self.ventanaRegistrarCompras.tablaActualizarCompra.currentRow()
        id_item = self.ventanaRegistrarCompras.tablaActualizarCompra.item(fila_seleccionada, 0)

        self.id_compra_seleccionada = id_item

        if id_item is not None:
            id_compra = id_item.text()
            print(f"ID de la compra seleccionada: {id_compra}")  # Para depuración

            self.id_compra_seleccionada = id_item

            self.ventanaRegistrarCompras.signalActualizarCompra.setText(f"Compra seleccionada: {id_compra}")
            self.ventanaRegistrarCompras.botonActualizarCompra.setEnabled(True)
        else:
            print("No se pudo obtener el ID de la compra")
            self.ventanaRegistrarCompras.signalActualizarCompra.setText("Error al seleccionar la compra")
            self.ventanaRegistrarCompras.botonActualizarCompra.setEnabled(False)

        if fila_seleccionada < 0:
            self.ventanaRegistrarCompras.signalActualizarCompra.setText("Por favor seleccione una compra")
            return

        id_original = self.ventanaRegistrarCompras.tablaActualizarCompra.item(fila_seleccionada, 0).text()

        # Obtener los nuevos valores de los LineEdit
        nueva_fecha = self.lineEdits['fecha'].text()
        nuevo_id_proveedor = self.lineEdits['id_proveedor'].text()


        # Verificar que todos los campos tengan valor
        if not all([nueva_fecha, nuevo_id_proveedor]):
            self.ventanaRegistrarCompras.signalActualizarCompra.setText("Por favor complete todos los campos")
            return

        else:
            # Si el ID no cambió, solo actualizar los otros campos
            actualizacion_exitosa = self.baseDatos.actualizarCompraMismoId(id_original, nueva_fecha, nuevo_id_proveedor)

        if actualizacion_exitosa:
            self.ventanaRegistrarCompras.signalActualizarCompra.setText("Compra actualizado")
            self.baseDatos.actualizarVenta(id_original, nueva_fecha, nuevo_id_proveedor)
            self.refrescarBaseDatos()

            # Limpiar los campos después de actualizar
            for lineEdit in self.lineEdits.values():
                lineEdit.clear()

            self.ventanaRegistrarCompras.lineEditBuscarActualizarCompra.clear()

            # Limpiar la tabla
            self.ventanaRegistrarCompras.tablaActualizarCompra.setRowCount(0)

        else:
            self.ventanaRegistrarCompras.signalActualizarCompra.setText("Error al actualizar")

    # Seleccionar un detalle de la compra para actualizarlo
    def seleccionarActualizarDetalleCompra(self, item):
        row = item.row()
        fila_seleccionada = item.row()

        columnas = ['id_producto', 'cantidad', 'precio_unitario']
        for col, campo in enumerate(columnas, start=2):
            valor = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.item(row, col).text()
            self.lineEditsDetalles[campo].setText(valor)

    # Agregar un producto al detalle de la compra
    def agregarProductoDetalleCompraActualizar(self):

        id_compra = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.item(0, 1).text()
        id_producto = self.ventanaRegistrarCompras.lineEditIdProductoActualizarDetalleCompra.text()
        cantidad = self.ventanaRegistrarCompras.lineEditCantidadActualizarDetalleCompra.text()
        precio_unitario = self.ventanaRegistrarCompras.lineEditPrecioUnitarioActualizarDetalleCompra.text()
        print(f"{id_compra} {id_producto} {cantidad} {precio_unitario}")

        agregar_producto_detalle = self.baseDatos.agregarProductoCompra(id_compra, id_producto, cantidad, precio_unitario)

        # actualizar stock
        actualizar_stock = self.baseDatos.actualizarStockProducto(id_producto, cantidad, precio_unitario)

        if agregar_producto_detalle != False and actualizar_stock != False:
            self.refrescarBaseDatosDetallesCompra(id_compra)
            self.ventanaRegistrarCompras.lineEditIdProductoActualizarDetalleCompra.setText("")
            self.ventanaRegistrarCompras.lineEditCantidadActualizarDetalleCompra.setText("")
            self.ventanaRegistrarCompras.lineEditPrecioUnitarioActualizarDetalleCompra.setText("")
            self.ventanaRegistrarCompras.signalActualizarDetalleCompra.setText("Producto agregado a la compra")


            # Actualizar el valor total de la venta
            tabla = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra
            total = 0

            for fila in range(tabla.rowCount()):
                cantidad = tabla.item(fila, 3)  # Columna de Cantidad
                precio_unitario = tabla.item(fila, 4)  # Columna de Precio Unitario

                if cantidad and precio_unitario:
                    cantidad_valor = float(cantidad.text())
                    precio_unitario_valor = float(precio_unitario.text())
                    total += cantidad_valor * precio_unitario_valor

                    self.ventanaRegistrarCompras.siganlTotalVentaActualizar.setText(str(total))

            self.baseDatos.actualizarTotalCompra(id_compra, total)

        else:
            self.ventanaRegistrarCompras.signalActualizarDetalleCompra.setText("Error al agregar producto a la compra")


        self.refrescarBaseDatosDetallesCompra(id_compra)
        self.ventanaRegistrarCompras.lineEditIdProductoActualizarDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditCantidadActualizarDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditPrecioUnitarioActualizarDetalleCompra.setText("")
        self.refrescarBaseDatosDetallesCompraActualizar(id_compra)
        self.refrescarBaseDatos()

    # Actualizar el detalle de la compra (finalizar proceso)
    def actualizarDetalleCompra(self):

        filaSeleccionada = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.currentRow()

        if filaSeleccionada < 0:
            self.ventanaRegistrarCompras.signalDetalleActualizado.setText("Por favor seleccione un producto")
            return

        id_detalle = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.item(filaSeleccionada, 0).text()

        id_compra = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.item(filaSeleccionada, 1).text()

        id_producto_viejo = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.item(filaSeleccionada, 2).text()
        id_producto_nuevo = self.ventanaRegistrarCompras.lineEditIdProductoActualizarDetalleCompra.text()

        vieja_cantidad = int(self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.item(filaSeleccionada, 3).text())
        nueva_cantidad = int(self.ventanaRegistrarCompras.lineEditCantidadActualizarDetalleCompra.text())

        precio_unitario_viejo = self.ventanaRegistrarCompras.tablaActualizarDetalleCompra.item(filaSeleccionada, 4).text()
        precio_unitario_nuevo = self.ventanaRegistrarCompras.lineEditPrecioUnitarioActualizarDetalleCompra.text()

        diferencia = 0
        suma = False

        # Verificar que todos los campos tengan valor
        if not all([id_producto_nuevo, nueva_cantidad, precio_unitario_nuevo]):
            self.ventanaRegistrarCompras.signalActualizarDetalleCompra.setText("Por favor complete todos los campos")
            return


        else:

            if nueva_cantidad > vieja_cantidad:
                diferencia = nueva_cantidad - vieja_cantidad
                suma = True
                # Tengo que sumarle la diferencia

            if vieja_cantidad > nueva_cantidad:
                diferencia = vieja_cantidad - nueva_cantidad
                # Tengo que restarle la diferencia

            if id_producto_nuevo == id_producto_viejo:
                actualizacion_exitosa = self.baseDatos.actualizarProductoDetalleCompraMismoId(id_detalle,id_producto_viejo,nueva_cantidad, precio_unitario_nuevo, diferencia, suma)

            else:
                actualizacion_exitosa = self.baseDatos.actualizarProductoDetalleCompraDiferenteId(id_detalle,id_producto_nuevo,id_producto_viejo,nueva_cantidad,vieja_cantidad, precio_unitario_viejo, precio_unitario_nuevo)

            if actualizacion_exitosa:
                self.ventanaRegistrarCompras.signalActualizarDetalleCompra.setText("Producto de detalle actualizado")
                self.refrescarBaseDatosDetallesCompraActualizar(id_compra)
                total = self.ventanaRegistrarCompras.siganlTotalVentaActualizar.text()
                self.refrescarBaseDatos()
                self.baseDatos.actualizarTotalCompra(id_compra, total)


            else:
                self.ventanaRegistrarCompras.signalActualizarDetalleCompra.setText("No se pudo actualizar el producto")


        self.ventanaRegistrarCompras.lineEditIdProductoActualizarDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditCantidadActualizarDetalleCompra.setText("")
        self.ventanaRegistrarCompras.lineEditPrecioUnitarioActualizarDetalleCompra.setText("")

    # Buscar una compra para eliminarla
    def buscarEliminarCompra(self):

        compra_Buscar = self.ventanaRegistrarCompras.lineEditBuscarEliminar.text()
        buscar_compra_bd = self.baseDatos.buscarCompraActualizar(compra_Buscar)

        if len(buscar_compra_bd) == 0:
            self.ventanaRegistrarCompras.signalEliminar.setText("Compra NO encontrado")

        else:
            self.ventanaRegistrarCompras.signalEliminarCompra.setText("Coincidencias encontradas")

            # MOSTRAR RESULTADOS ENCONTRADOS CUANDO SE DA A BOTON BUSCAR
            self.tablaEliminar.setRowCount(len(buscar_compra_bd))

            for row, compra in enumerate(buscar_compra_bd):
                for col, valor in enumerate(compra[0:]):
                    self.tablaEliminar.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

    # Seleccionar la compra para eliminarla
    def seleccionarEliminarCompra(self, item):
        fila_seleccionada = item.row()
        id_item = self.ventanaRegistrarCompras.tablaEliminar.item(fila_seleccionada, 0)

        if id_item is not None:
            id_compra = id_item.text()
            print(f"ID de la compra seleccionada: {id_compra}")  # Para depuración

            self.id_compra_seleccionada = id_compra

            self.ventanaRegistrarCompras.signalEliminarCompra.setText(f"Compra seleccionada: {id_compra}")
            self.ventanaRegistrarCompras.botonEliminarCompra.setEnabled(True)
        else:
            print("No se pudo obtener el ID de la compra")
            self.ventanaRegistrarCompras.signalEliminarCompra.setText("Error al seleccionar la compra")
            self.ventanaRegistrarCompras.botonEliminarCompra.setEnabled(False)

    # Eliminar la compra (finalizar proceso)
    def eliminarCompra(self):

        if not hasattr(self, 'id_compra_seleccionada'):
            self.ventanaRegistrarCompras.signalEliminarCompra.setText("Por favor, seleccione una compra primero")
            return

        try:
            if self.baseDatos.eliminarCompra(self.id_compra_seleccionada):
                self.ventanaRegistrarCompras.signalEliminarCompra.setText(f"Compra {self.id_compra_seleccionada} eliminada con éxito")
                self.refrescarBaseDatos()

                self.ventanaRegistrarCompras.tablaEliminar.setRowCount(0)
                delattr(self, 'id_compra_seleccionada')
                self.ventanaRegistrarCompras.botonEliminarCompra.setEnabled(False)
                self.ventanaRegistrarCompras.lineEditBuscarEliminar.clear()
            else:
                self.ventanaRegistrarCompras.signalEliminarCompra.setText("Error al eliminar la compra")

        except Exception as e:
            print(f"Error inesperado: {e}")
            self.ventanaRegistrarCompras.signalEliminar.setText("Error inesperado al eliminar la compra")

        print("Operación de eliminación completada")  # Para depuración

    # Actualizar detalle de la compra en la ventana eliminar
    def actualizarDetalleCompraEliminar(self, id_compra):

        total_compra = 0
        datos = self.baseDatos.mostrarDetallesCompras(id_compra)
        self.tablaEliminarDetalleCompra.setRowCount(len(datos))

        for row, detalle in enumerate(datos):
            total_compra += int(detalle[3] * detalle[4])
            for col, valor in enumerate(detalle[0:]):
                self.tablaEliminarDetalleCompra.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

        self.ventanaRegistrarCompras.signalTotalVenta.setText(str(total_compra))
        self.refrescarBaseDatos()

    # Seleccionar producto en el detalle para eliminarlo
    def seleccionarEliminarProductoDetalle(self, item):

        fila_seleccionada = item.row()
        id_detalle = self.ventanaRegistrarCompras.tablaEliminarDetalleCompra.item(fila_seleccionada, 0).text()
        id_compra = self.ventanaRegistrarCompras.tablaEliminarDetalleCompra.item(fila_seleccionada, 1).text()
        id_producto = self.ventanaRegistrarCompras.tablaEliminarDetalleCompra.item(fila_seleccionada, 2).text()
        cantidad_detalle_eliminar = self.ventanaRegistrarCompras.tablaEliminarDetalleCompra.item(fila_seleccionada, 3).text()

        if id_detalle is not None:
            self.detalle_seleccionado = {
                'id_detalle': id_detalle,
                'cantidad_detalle_eliminar': cantidad_detalle_eliminar,
                'id_producto': id_producto,
                'id_compra': id_compra
            }
            self.ventanaRegistrarCompras.botonEliminarProductoCompra.setEnabled(True)
            self.ventanaRegistrarCompras.signalEliminarDetalle.setText(f"Producto seleccionado para eliminar {id_detalle}")
        else:
            print("No se pudo obtener el ID de la compra")
            self.ventanaRegistrarCompras.signalEliminarDetalle.setText("Error al seleccionar la compra")
            self.ventanaRegistrarCompras.botonEliminarProductoCompra.setEnabled(False)

    # Eliminar el producto del detalle de la compra (finalizar el proceso)
    def eliminarProductoDetalle(self):
        if self.detalle_seleccionado:
            datos = self.baseDatos.eliminarDetalleCompra(
                self.detalle_seleccionado['id_detalle'],
                self.detalle_seleccionado['cantidad_detalle_eliminar'],
                self.detalle_seleccionado['id_producto']
            )

            if datos:
                self.actualizarDetalleCompraEliminar(self.detalle_seleccionado['id_compra'])
                print("eliminado")
                self.ventanaRegistrarCompras.signalEliminarDetalle.setText("Producto eliminado")
                self.detalle_seleccionado = None  # Resetear la selección
                self.ventanaRegistrarCompras.botonEliminarProductoCompra.setEnabled(False)
                self.refrescarBaseDatosDetallesCompra(self.id_compra_seleccionada)
                self.refrescarBaseDatos()
            else:
                print("no eliminado")
                self.ventanaRegistrarCompras.signalEliminarDetalle.setText("Producto NO eliminado")
        else:
            print("No hay producto seleccionado para eliminar")
            self.ventanaRegistrarCompras.signalEliminarDetalle.setText("Seleccione un producto para eliminar")

    # Salir de la interfaz de detalle de compra
    def salirDetalleCompra(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(4)

    # Salir de la interfaz de eliminar un detalle de la compra
    def salirEliminarDetalleCompra(self):
        self.ventanaRegistrarCompras.stackedWidget.setCurrentIndex(2)


# Bloque principal para ejecutar la aplicación de forma independiente
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    menu = RegistrarCompras()
    menu.show()
    app.exec_()

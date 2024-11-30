# Importación de módulos necesarios de PyQt5
from PyQt5 import QtWidgets, uic
from Modelo.conexion import Comunicacion

#CLase principal de realizar ventas
class RealizarVentas(QtWidgets.QMainWindow):

    # Metodo constructor
    def __init__(self):
        super().__init__()

        # Cargar la interfaz grafica
        self.ventanaRealizarVentas = uic.loadUi('Vistas/ventanaRealizarVentas/ventanaRealizarVentas.ui', self)

        # Hacer la conexion con los botones
        self.ventanaRealizarVentas.botonBaseDatos.clicked.connect(self.abrirPaginaBaseDatos)
        #self.ventanaRealizarVentas.botonAgregar.clicked.connect(self.abrirPaginaAgregar)
        self.ventanaRealizarVentas.botonEliminar.clicked.connect(self.abrirPaginaEliminar)
        self.ventanaRealizarVentas.botonRealizarVenta.clicked.connect(self.abrirPaginaRealizarVenta)
        self.ventanaRealizarVentas.botonActualizar.clicked.connect(self.abrirPaginaActualizarVenta)
        self.ventanaRealizarVentas.botonActualizarDetallesVenta.clicked.connect(self.abrirPaginaActualizarDetalles)
        self.ventanaRealizarVentas.botonAgregarProductoActualizarDetalle.clicked.connect(self.agregarProductoActualizarDetalleVenta)
        self.ventanaRealizarVentas.botonEliminarDetalles.clicked.connect(self.abrirPaginaEliminarDetalles)

        self.ventanaRealizarVentas.botonRefrescar.clicked.connect(self.refrescarBaseDatos)
        self.ventanaRealizarVentas.botonCrearVentaObtenerId.clicked.connect(self.crearVentaObtenerId)
        #self.ventanaRealizarVentas.botonAgregarVenta.clicked.connect(self.agregarVenta)
        self.ventanaRealizarVentas.botonAgregarProductoVenta.clicked.connect(self.agregarProductoVenta)
        self.ventanaRealizarVentas.botonFinalizarVenta.clicked.connect(self.finalizarVenta)

        self.ventanaRealizarVentas.botonBuscarVentaActualizar.clicked.connect(self.buscarActualizarVenta)
        self.ventanaRealizarVentas.botonActualizarVenta.clicked.connect(self.actualizarVenta)
        self.ventanaRealizarVentas.botonBuscarEliminar.clicked.connect(self.buscarEliminarVenta)
        self.ventanaRealizarVentas.botonEliminarVenta.clicked.connect(self.eliminarVenta)

        self.ventanaRealizarVentas.botonActualizarDetalleProducto.clicked.connect(self.actualizarProductoDetalleVenta)

        #self.ventanaRealizarVentas.botonActualizarDetalle.clicked.connect(self.actualizarDetalleVenta)
        self.ventanaRealizarVentas.botonSalirDetalle.clicked.connect(self.salirDetalleVenta)
        self.ventanaRealizarVentas.botonVolverEliminarDetalleVenta.clicked.connect(self.salirDetalleVentaEliminar)
        self.ventanaRealizarVentas.botonEliminarProductoDetalleVenta.clicked.connect(self.eliminarProductoDetalle)

        self.ventanaRealizarVentas.tablaActualizarVentas.itemClicked.connect(self.seleccionarActualizarVenta)
        self.ventanaRealizarVentas.tablaActualizarDetallesVenta.itemClicked.connect(self.seleccionarActualizarDetalleVenta)
        self.ventanaRealizarVentas.tablaEliminar.itemClicked.connect(self.seleccionarEliminarVenta)
        self.ventanaRealizarVentas.tablaEliminarProductoDetalleVenta.itemClicked.connect(self.seleccionarEliminarProductoDetalle)

        # Diccionario para manejar los campos de actualización
        self.lineEdits = {
            #'id': self.ventanaRealizarVentas.lineEditBuscarIdVenta,
            'fecha': self.ventanaRealizarVentas.lineEditBuscarFechaVenta,
            'id_cliente': self.ventanaRealizarVentas.lineEditBuscarIdCliente
            #'total': self.ventanaRealizarVentas.lineEditBuscarTotalVenta,
        }

        # Diccionario para manejar los campos de actualización detalles
        self.lineEditsDetalles = {
            'id_producto': self.ventanaRealizarVentas.lineEditIdProductoDetalle,
            'cantidad': self.ventanaRealizarVentas.lineEditCantidadDetalle
            #'precio_unitario': self.ventanaRealizarVentas.lineEditPrecioUnitarioDetalle,
        }

        # Establecer conexion con la base de datos
        self.baseDatos = Comunicacion()

        # Definir las tablas de la interfaz
        self.tablaVentas = self.ventanaRealizarVentas.tablaVentas
        self.tablaEliminar = self.ventanaRealizarVentas.tablaEliminar
        self.tablaRealizarVentaProductos = self.ventanaRealizarVentas.tablaRealizarVentaProductos
        self.tablaActualizarVentas = self.ventanaRealizarVentas.tablaActualizarVentas
        self.tablaActualizarDetallesVenta = self.ventanaRealizarVentas.tablaActualizarDetallesVenta
        self.tablaEliminarProductoDetalleVenta = self.ventanaRealizarVentas.tablaEliminarProductoDetalleVenta

        # Ejecutar el metodo refrescar base datos para mostrar las ventas
        self.refrescarBaseDatos()

    # Funciones de navegación entre páginas

    def abrirPaginaBaseDatos(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(0)

    #def abrirPaginaAgregar(self):
        #self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(1)

    def abrirPaginaEliminar(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(2)

    def abrirPaginaRealizarVenta(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(4)

    def abrirPaginaActualizarVenta(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(5)

    def abrirPaginaActualizarDetalles(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(6)
        id_venta = self.id_seleccionado_actualizar
        self.refrescarBaseDatosDetallesActualizar(id_venta)
        self.ventanaRealizarVentas.lineEditBuscarFechaVenta.setText("")
        self.ventanaRealizarVentas.lineEditBuscarIdCliente.setText("")
        self.ventanaRealizarVentas.tablaActualizarVentas.setRowCount(0)

    def abrirPaginaEliminarDetalles(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(3)
        self.actualizarDetalleVentaEliminar(self.id_venta_seleccionada)
        self.ventanaRealizarVentas.lineEditBuscarEliminar.clear()
        self.ventanaRealizarVentas.tablaEliminar.setRowCount(0)


    '''def abrirPaginaInicio(self):
        from menuOpciones import MenuOpciones

        self.hide()  # Oculta la ventana actual de MenuOpciones
        self.menu_window = MenuOpciones()
        self.menu_window.showMenuOpciones()  # Muestra la ventana de opciones
    '''


    ################################# AQUI SE AGREGAN LAS FUNCIONES PARA HACERLOS CON LA BASE DE DATOS #################################

    # Mostrar ventas de la base de datos
    def refrescarBaseDatos(self):

        datos = self.baseDatos.mostrarVentas()
        self.tablaVentas.setRowCount(len(datos))

        for row, venta in enumerate(datos):
            for col, valor in enumerate(venta[0:]):
                self.tablaVentas.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))


    # Mostrar los detalles de las ventas
    def refrescarBaseDatosDetallesVenta(self, id_venta):

        totalVenta = 0
        datos = self.baseDatos.mostrarDetallesVentas(id_venta)
        self.tablaRealizarVentaProductos.setRowCount(len(datos))

        for row, detalle in enumerate(datos):
            totalVenta += int(detalle[3] * detalle[4])
            for col, valor in enumerate(detalle[0:]):
                self.tablaRealizarVentaProductos.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

        self.ventanaRealizarVentas.signalTotalVentaDetalles.setText(str(totalVenta))
        self.refrescarBaseDatos()
        self.baseDatos.actualizarTotalVenta(id_venta, totalVenta)
        self.total_venta = totalVenta


    # Mostrar los detalles de ventas despues de actualizar alguno
    def refrescarBaseDatosDetallesActualizar(self, id_venta):

        totalVenta = 0
        datos = self.baseDatos.mostrarDetallesVentas(id_venta)
        self.tablaActualizarDetallesVenta.setRowCount(len(datos))

        for row, detalle in enumerate(datos):
            totalVenta += int(detalle[3] * detalle[4])
            for col, valor in enumerate(detalle[0:]):
                self.tablaActualizarDetallesVenta.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

        self.ventanaRealizarVentas.signalTotalVentaDetalles.setText(str(totalVenta))
        self.refrescarBaseDatos()
        self.baseDatos.actualizarTotalVenta(id_venta, totalVenta)
        self.total_venta = totalVenta


    # Crear el id para la venta que se va a realizar
    def crearVentaObtenerId(self):

        fecha = self.ventanaRealizarVentas.lineEditIdVentaRealizarVentaFecha.text()
        id_clientes = self.ventanaRealizarVentas.lineEditIdVentaRealizarVentaIdCliente.text()

        # Inicialmente, el total será 0
        total = 0

        # Crear una venta con total 0
        id_venta = self.baseDatos.agregarVenta(fecha, id_clientes, total)

        if id_venta:
            print("Venta iniciada")
            self.ventanaRealizarVentas.signalRealizarVenta.setText(f"Venta iniciada con id {id_venta}")
            #self.ventanaRealizarVentas.lineEditIdVentaRealizarVenta.setText(str(id_venta))
            self.refrescarBaseDatos()
            self.ventanaRealizarVentas.botonCrearVentaObtenerId.setEnabled(False)
            self.id_creado = id_venta

        else:
            print("Error al iniciar la venta")
            self.ventanaRealizarVentas.signalRealizarVenta.setText("Error al iniciar la venta")

        self.ventanaRealizarVentas.lineEditAgregarFechaVenta.setText("")
        self.ventanaRealizarVentas.lineEditAgregarIdCliente.setText("")
        self.ventanaRealizarVentas.signalTotalVenta.setText("")


    # Agregar un producto a la venta
    def agregarProductoVenta(self):

        id_producto = self.ventanaRealizarVentas.lineEditIdProductoRealizarVenta.text()
        cantidad = self.ventanaRealizarVentas.lineEditCantidadRealizarVenta.text()
        precio_unitario = self.baseDatos.obtenerValorProducto(id_producto)


        if precio_unitario != False:

            # Primero verificamos si hay suficiente stock
            if self.baseDatos.actualizarTablaProductos(id_producto, cantidad):
                agregarProductoVentaBD = self.baseDatos.agregarProductoVenta(self.id_creado, id_producto, cantidad, precio_unitario)

                if agregarProductoVentaBD != False:
                    self.refrescarBaseDatosDetallesVenta(self.id_creado)
                    self.ventanaRealizarVentas.lineEditCantidadRealizarVenta.setText("")
                    self.ventanaRealizarVentas.lineEditIdProductoRealizarVenta.setText("")
                    self.ventanaRealizarVentas.lineEditCantidadRealizarVenta.setText("")
                    self.ventanaRealizarVentas.signalRealizarVenta.setText("Producto agregado a la venta")


                    # Actualizar el valor total de la venta
                    tabla = self.ventanaRealizarVentas.tablaRealizarVentaProductos
                    total = 0

                    for fila in range(tabla.rowCount()):
                        cantidad = tabla.item(fila, 3)  # Columna de Cantidad
                        precio_unitario = tabla.item(fila, 4)  # Columna de Precio Unitario

                        if cantidad and precio_unitario:
                                cantidad_valor = float(cantidad.text())
                                precio_unitario_valor = float(precio_unitario.text())
                                total += cantidad_valor * precio_unitario_valor

                    self.ventanaRealizarVentas.signalTotalVenta.setText(str(total))

                else:
                    self.ventanaRealizarVentas.signalRealizarVenta.setText("Error al agregar producto a la venta")

            else:
                self.ventanaRealizarVentas.signalRealizarVenta.setText("No hay suficiente stock para este producto")

        else:
            self.ventanaRealizarVentas.signalRealizarVenta.setText("Error al obtener el precio del producto")

        self.refrescarBaseDatosDetallesVenta(self.id_creado)
        self.ventanaRealizarVentas.lineEditIdProductoRealizarVenta.setText("")
        self.ventanaRealizarVentas.lineEditCantidadRealizarVenta.setText("")


    # Finalizar la venta y agregarla a la base de datos
    def finalizarVenta(self):

        id_venta = self.ventanaRealizarVentas.tablaRealizarVentaProductos.item(0, 1).text()
        total = self.ventanaRealizarVentas.signalTotalVenta.text()

        finalizarVentaBD = self.baseDatos.actualizarVentaDespuesDeDetalles(id_venta, total)

        if finalizarVentaBD:
            print("Venta finalizada")
            self.ventanaRealizarVentas.signalAgregar.setText("Venta finalizada")
        else:
            print("Error al finalizar la venta")
            self.ventanaRealizarVentas.signalAgregar.setText("Error al finalizar la venta")

        # Quitar los valores ingresados de los line edit
        self.ventanaRealizarVentas.lineEditIdProductoRealizarVenta.setText("")
        self.ventanaRealizarVentas.lineEditCantidadRealizarVenta.setText("")
        self.ventanaRealizarVentas.lineEditIdVentaRealizarVentaFecha.setText("")
        self.ventanaRealizarVentas.lineEditIdVentaRealizarVentaIdCliente.setText("")
        self.ventanaRealizarVentas.signalTotalVenta.setText("0")

        # Limpiar la tabla
        self.ventanaRealizarVentas.tablaRealizarVentaProductos.setRowCount(0)

        # Activar de nuevo boton de crear venta y obtener id
        self.ventanaRealizarVentas.botonCrearVentaObtenerId.setEnabled(True)

        # Refrescar base de datos de ventas
        self.refrescarBaseDatos()


    # Buscar una venta para actualizarla
    def buscarActualizarVenta(self):

        ventaBuscar = self.ventanaRealizarVentas.lineEditBuscarVentaActualizar.text()
        buscaVentaBD = self.baseDatos.buscarVentaActualizar(ventaBuscar)
        self.ventanaRealizarVentas.lineEditBuscarVentaActualizar.clear()

        if len(buscaVentaBD) == 0:
            self.ventanaRealizarVentas.signalVentaActualizada.setText("Cliente NO encontrado")

        else:
            self.ventanaRealizarVentas.signalVentaActualizada.setText("Coincidencias encontradas")

            # MOSTRAR RESULTADOS ENCONTRADOS CUANDO SE DA A BOTON BUSCAR
            self.tablaActualizarVentas.setRowCount(len(buscaVentaBD))

            for row, venta in enumerate(buscaVentaBD):
                for col, valor in enumerate(venta[0:]):
                    self.tablaActualizarVentas.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))


    # Seleccionar una venta para actualizarla
    def seleccionarActualizarVenta(self, item):
        row = item.row()
        self.id_seleccionado_actualizar = self.ventanaRealizarVentas.tablaActualizarVentas.item(row, 0).text()
        columnas = ['fecha', 'id_cliente']
        for col, campo in enumerate(columnas, start=1):
            valor = self.ventanaRealizarVentas.tablaActualizarVentas.item(row, col).text()
            self.lineEdits[campo].setText(valor)


    # Actualizar la venta (finalizar proceso)
    def actualizarVenta(self, item):
        #filaSeleccionada = self.ventanaRealizarVentas.tablaActualizarVentas.currentRow()

        fila_seleccionada = self.ventanaRealizarVentas.tablaActualizarVentas.currentRow()
        id_item = self.ventanaRealizarVentas.tablaEliminar.item(fila_seleccionada, 0)

        self.id_venta_seleccionada = id_item

        if id_item is not None:
            id_venta = id_item.text()
            print(f"ID de la venta seleccionada: {id_venta}")  # Para depuración

            self.id_venta_seleccionada = id_item

            self.ventanaRealizarVentas.signalEliminar.setText(f"Venta seleccionada: {id_venta}")
            self.ventanaRealizarVentas.botonEliminarVenta.setEnabled(True)
        else:
            print("No se pudo obtener el ID de la venta")
            self.ventanaRealizarVentas.signalEliminar.setText("Error al seleccionar la venta")
            self.ventanaRealizarVentas.botonEliminarVenta.setEnabled(False)

        if fila_seleccionada < 0:
            self.ventanaRealizarVentas.signalVentaActualizada.setText("Por favor seleccione una venta")
            return

        idOriginal = self.ventanaRealizarVentas.tablaActualizarVentas.item(fila_seleccionada, 0).text()

        # Obtener los nuevos valores de los LineEdit
        #nuevo_id = self.lineEdits['id'].text()
        nueva_fecha = self.lineEdits['fecha'].text()
        nuevo_id_cliente = self.lineEdits['id_cliente'].text()
        #nuevo_total = self.lineEdits['total'].text()


        # Verificar que todos los campos tengan valor
        if not all([nueva_fecha, nuevo_id_cliente]):
            self.ventanaRealizarVentas.signalVentaActualizada.setText("Por favor complete todos los campos")
            return

        else:
            # Si el ID no cambió, solo actualizar los otros campos
            actualizacion_exitosa = self.baseDatos.actualizarVentaMismoId(idOriginal, nueva_fecha, nuevo_id_cliente)

        if actualizacion_exitosa:
            self.ventanaRealizarVentas.signalVentaActualizada.setText("Venta actualizado")
            self.refrescarBaseDatos()
            self.refrescarBaseDatosDetallesVenta(idOriginal)

            # Limpiar los campos después de actualizar
            for lineEdit in self.lineEdits.values():
                lineEdit.clear()

            self.ventanaRealizarVentas.lineEditBuscarVentaActualizar.clear()

            # Limpiar la tabla
            self.ventanaRealizarVentas.tablaActualizarVentas.setRowCount(0)

        else:
            self.ventanaRealizarVentas.signalVentaActualizada.setText("Error al actualizar")


    # Agregar un producto al detalle de la venta
    def agregarProductoActualizarDetalleVenta(self):

        id_venta = self.ventanaRealizarVentas.tablaActualizarDetallesVenta.item(0, 1).text()
        id_producto = self.ventanaRealizarVentas.lineEditIdProductoDetalle.text()
        cantidad = self.ventanaRealizarVentas.lineEditCantidadDetalle.text()
        precio_unitario = self.baseDatos.obtenerValorProducto(id_producto)
        print(f"{id_venta} {id_producto} {cantidad} {precio_unitario}")

        if precio_unitario != False:
            print("1")

            # Primero verificamos si hay suficiente stock
            if self.baseDatos.actualizarTablaProductos(id_producto, cantidad):
                print("2")
                agregarProductoVentaBD = self.baseDatos.agregarProductoVenta(id_venta, id_producto, cantidad, precio_unitario)

                if agregarProductoVentaBD != False:
                    print("3")
                    self.refrescarBaseDatosDetallesVenta(id_venta)
                    self.ventanaRealizarVentas.lineEditIdProductoDetalle.setText("")
                    self.ventanaRealizarVentas.lineEditCantidadDetalle.setText("")
                    self.ventanaRealizarVentas.signalDetalleActualizado.setText("Producto agregado a la venta")

                    # Actualizar el valor total de la venta
                    tabla = self.ventanaRealizarVentas.tablaActualizarDetallesVenta
                    total = 0

                    for fila in range(tabla.rowCount()):
                        cantidad = tabla.item(fila, 3)  # Columna de Cantidad
                        precio_unitario = tabla.item(fila, 4)  # Columna de Precio Unitario

                        if cantidad and precio_unitario:
                            cantidad_valor = float(cantidad.text())
                            precio_unitario_valor = float(precio_unitario.text())
                            total += cantidad_valor * precio_unitario_valor


                    #self.ventanaRealizarVentas.signalTotalVentaDetalles.setText(str(total))
                    self.baseDatos.actualizarTotalVenta(id_venta, total)
                    self.refrescarBaseDatos()
                    self.refrescarBaseDatosDetallesVenta(id_venta)
                    self.refrescarBaseDatosDetallesActualizar(id_venta)

                else:
                    print("4")
                    self.ventanaRealizarVentas.signalDetalleActualizado.setText("Error al agregar producto a la venta")

            else:
                print("5")
                self.ventanaRealizarVentas.signalDetalleActualizado.setText("No hay suficiente stock para este producto")

        else:
            print("6")
            self.ventanaRealizarVentas.signalDetalleActualizado.setText("Error al obtener el precio del producto")

        self.refrescarBaseDatosDetallesVenta(id_venta)
        self.refrescarBaseDatosDetallesActualizar(id_venta)
        self.ventanaRealizarVentas.lineEditIdProductoDetalle.setText("")
        self.ventanaRealizarVentas.lineEditCantidadDetalle.setText("")


    # Seleccionar un detalle de la venta para actualizarlo
    def seleccionarActualizarDetalleVenta(self, item):
        row = item.row()
        fila_seleccionada = item.row()

        columnas = ['id_producto', 'cantidad']
        for col, campo in enumerate(columnas, start=2):
            valor = self.ventanaRealizarVentas.tablaActualizarDetallesVenta.item(row, col).text()
            self.lineEditsDetalles[campo].setText(valor)


    # Actualizar el detalle de la venta (finalizar proceso)
    def actualizarDetalleVenta(self, id_venta):

        if id_venta == False:
            self.ventanaRealizarVentas.signalDetalleActualizado.setText("Seleccione una venta para actualizar los detalles")

        else:
            self.ventanaRealizarVentas.signalDetalleActualizado.setText(f"Actualizando detalles venta id = {id_venta}")
            datos = self.baseDatos.mostrarDetallesVentas(id_venta)
            totalVenta = 0
            self.tablaActualizarDetallesVenta.setRowCount(len(datos))

            for row, detalle in enumerate(datos):
                totalVenta += int(detalle[2] * detalle[3])
                for col, valor in enumerate(detalle[0:]):
                    self.tablaActualizarDetallesVenta.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

            self.ventanaRealizarVentas.signalTotalVentaDetalles.setText(str(totalVenta))
            self.baseDatos.actualizarTotalVenta(id_venta, totalVenta)
            self.refrescarBaseDatosDetallesVenta(id_venta)
            self.refrescarBaseDatos()
            #datos = self.baseDatos.actualizarVentaDespuesDeDetalles(id_venta,totalVenta)
            #print(totalVenta)


    # Actualizar el producto en el detalle de la venta (cantidad, precio)
    def actualizarProductoDetalleVenta(self):

        filaSeleccionada = self.ventanaRealizarVentas.tablaActualizarDetallesVenta.currentRow()

        if filaSeleccionada < 0:
            self.ventanaRealizarVentas.signalDetalleActualizado.setText("Por favor seleccione un producto")
            return

        id_detalle = self.ventanaRealizarVentas.tablaActualizarDetallesVenta.item(filaSeleccionada, 0).text()
        id_venta = self.ventanaRealizarVentas.tablaActualizarDetallesVenta.item(filaSeleccionada, 1).text()
        id_producto_viejo = self.ventanaRealizarVentas.tablaActualizarDetallesVenta.item(filaSeleccionada, 2).text()
        id_producto_nuevo = self.ventanaRealizarVentas.lineEditIdProductoDetalle.text()
        vieja_cantidad = int(self.ventanaRealizarVentas.tablaActualizarDetallesVenta.item(filaSeleccionada, 3).text())
        nueva_cantidad = int(self.ventanaRealizarVentas.lineEditCantidadDetalle.text())
        precio_unitario_nuevo = self.baseDatos.obtenerValorProducto(id_producto_nuevo)
        diferencia = 0
        resta = False


        # Verificar que todos los campos tengan valor
        if not all([id_producto_nuevo, nueva_cantidad]):
            self.ventanaRealizarVentas.signalDetalleActualizado.setText("Por favor complete todos los campos")
            return


        else:

            if nueva_cantidad > vieja_cantidad:

                diferencia = nueva_cantidad - vieja_cantidad
                resta = True
                # Tengo que restarle la diferencia

            if vieja_cantidad > nueva_cantidad:

                diferencia = vieja_cantidad - nueva_cantidad
                # Tengo que sumarle la diferencia


            if id_producto_nuevo == id_producto_viejo:
                actualizacion_exitosa = self.baseDatos.actualizarProductoDetalleVentaMismoId(id_detalle, id_producto_viejo, nueva_cantidad, diferencia, resta)

            else:
                actualizacion_exitosa = self.baseDatos.actualizarProductoDetalleVentaDiferenteId(id_detalle, id_producto_nuevo, id_producto_viejo, nueva_cantidad, vieja_cantidad)


            if actualizacion_exitosa:
                self.ventanaRealizarVentas.signalDetalleActualizado.setText("Producto de detalle actualizado")
                self.refrescarBaseDatosDetallesActualizar(id_venta)
                total = self.ventanaRealizarVentas.signalTotalVentaDetalles.text()
                self.baseDatos.actualizarTotalVenta(id_venta, total)
                self.refrescarBaseDatos()


            else:
                self.ventanaRealizarVentas.signalDetalleActualizado.setText("No se pudo actualizar el producto")


    # Buscar una venta para eliminarla
    def buscarEliminarVenta(self):

        ventaBuscar = self.ventanaRealizarVentas.lineEditBuscarEliminar.text()
        buscarVentaenBD = self.baseDatos.buscarVentaActualizar(ventaBuscar)

        if len(buscarVentaenBD) == 0:
            self.ventanaRealizarVentas.signalEliminar.setText("Venta NO encontrado")

        else:
            self.ventanaRealizarVentas.signalEliminar.setText("Coincidencias encontradas")

            # MOSTRAR RESULTADOS ENCONTRADOS CUANDO SE DA A BOTON BUSCAR
            self.tablaEliminar.setRowCount(len(buscarVentaenBD))

            for row, venta in enumerate(buscarVentaenBD):
                for col, valor in enumerate(venta[0:]):
                    self.tablaEliminar.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))


    # Seleccionar la venta para eliminarla
    def seleccionarEliminarVenta(self, item):
        fila_seleccionada = item.row()
        id_item = self.ventanaRealizarVentas.tablaEliminar.item(fila_seleccionada, 0)

        if id_item is not None:
            id_venta = id_item.text()
            print(f"ID de la venta seleccionada: {id_venta}")  # Para depuración

            self.id_venta_seleccionada = id_venta

            self.ventanaRealizarVentas.signalEliminar.setText(f"Venta seleccionada: {id_venta}")
            self.ventanaRealizarVentas.botonEliminarVenta.setEnabled(True)
        else:
            print("No se pudo obtener el ID de la venta")
            self.ventanaRealizarVentas.signalEliminar.setText("Error al seleccionar la venta")
            self.ventanaRealizarVentas.botonEliminarVenta.setEnabled(False)


    # Eliminar la venta (finalizar proceso)
    def eliminarVenta(self):

        if not hasattr(self, 'id_venta_seleccionada'):
            self.ventanaRealizarVentas.signalEliminar.setText("Por favor, seleccione una venta primero")
            return

        try:
            if self.baseDatos.eliminarVenta(self.id_venta_seleccionada):
                self.ventanaRealizarVentas.signalEliminar.setText(f"Venta {self.id_venta_seleccionada} eliminada con éxito")
                self.refrescarBaseDatos()

                self.ventanaRealizarVentas.tablaEliminar.setRowCount(0)
                delattr(self, 'id_venta_seleccionada')
                self.ventanaRealizarVentas.botonEliminarVenta.setEnabled(False)
                self.ventanaRealizarVentas.lineEditBuscarEliminar.clear()
            else:
                self.ventanaRealizarVentas.signalEliminar.setText("Error al eliminar la venta")

        except Exception as e:
            print(f"Error inesperado: {e}")
            self.ventanaRealizarVentas.signalEliminar.setText("Error inesperado al eliminar la venta")

        print("Operación de eliminación completada")  # Para depuración


    # Actualizar detalle de la venta (este metodo es una copia de uno anterior, se creo porque hay un conflicto que no se logro resolver)
    def actualizarDetalleVenta(self, idVenta):

        self.id_venta_seleccionada = idVenta
        totalVenta = 0
        datos = self.baseDatos.mostrarDetallesVentas(idVenta)
        self.tablaEliminarProductoDetalleVenta.setRowCount(len(datos))

        for row, detalle in enumerate(datos):
            totalVenta += int(detalle[3] * detalle[4])
            for col, valor in enumerate(detalle[0:]):
                self.tablaActualizarDetallesVenta.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

        self.ventanaRealizarVentas.signalTotalVentaEliminar.setText(str(totalVenta))
        self.refrescarBaseDatos()


    # Actualizar detalle de la venta en la ventana eliminar
    def actualizarDetalleVentaEliminar(self, idVenta):

        #idVenta = self.id_venta_seleccionada
        totalVenta = 0
        datos = self.baseDatos.mostrarDetallesVentas(idVenta)
        self.tablaEliminarProductoDetalleVenta.setRowCount(len(datos))

        for row, detalle in enumerate(datos):
            totalVenta += int(detalle[3] * detalle[4])
            for col, valor in enumerate(detalle[0:]):
                self.tablaEliminarProductoDetalleVenta.setItem(row, col, QtWidgets.QTableWidgetItem(str(valor)))

        self.ventanaRealizarVentas.signalTotalVentaEliminar.setText(str(totalVenta))
        self.refrescarBaseDatos()


    # Seleccionar producto en el detalle para eliminarlo
    def seleccionarEliminarProductoDetalle(self, item):

        fila_seleccionada = item.row()
        id_detalle = self.ventanaRealizarVentas.tablaEliminarProductoDetalleVenta.item(fila_seleccionada, 0).text()
        idVenta = self.ventanaRealizarVentas.tablaEliminarProductoDetalleVenta.item(fila_seleccionada, 1).text()
        id_producto = self.ventanaRealizarVentas.tablaEliminarProductoDetalleVenta.item(fila_seleccionada, 2).text()
        cantidad_detalle_eliminar = self.ventanaRealizarVentas.tablaEliminarProductoDetalleVenta.item(fila_seleccionada, 3).text()
        idVentaEliminar = idVenta

        if id_detalle is not None:
            self.detalle_seleccionado = {
                'id_detalle': id_detalle,
                'cantidad_detalle_eliminar': cantidad_detalle_eliminar,
                'id_producto': id_producto,
                'idVenta': idVenta
            }
            self.ventanaRealizarVentas.botonEliminarProductoDetalleVenta.setEnabled(True)
            self.ventanaRealizarVentas.signalProductoEliminar.setText("Producto seleccionado para eliminar")
        else:
            print("No se pudo obtener el ID de la venta")
            self.ventanaRealizarVentas.signalProductoEliminar.setText("Error al seleccionar la venta")
            self.ventanaRealizarVentas.botonEliminarProductoDetalleVenta.setEnabled(False)


    # Eliminar el producto del detalle de la venta (finalizar el proceso)
    def eliminarProductoDetalle(self):
        if self.detalle_seleccionado:
            datos = self.baseDatos.eliminarDetalle(
                self.detalle_seleccionado['id_detalle'],
                self.detalle_seleccionado['cantidad_detalle_eliminar'],
                self.detalle_seleccionado['id_producto']
            )

            if datos:
                self.actualizarDetalleVentaEliminar(self.detalle_seleccionado['idVenta'])
                print("eliminado")
                self.ventanaRealizarVentas.signalProductoEliminar.setText("Producto eliminado")
                self.detalle_seleccionado = None  # Resetear la selección
                self.ventanaRealizarVentas.botonEliminarProductoDetalleVenta.setEnabled(False)
                self.refrescarBaseDatosDetallesVenta(self.id_venta_seleccionada)
                self.refrescarBaseDatos()
            else:
                print("no eliminado")
                self.ventanaRealizarVentas.signalProductoEliminar.setText("Producto NO eliminado")
        else:
            print("No hay producto seleccionado para eliminar")
            self.ventanaRealizarVentas.signalProductoEliminar.setText("Seleccione un producto para eliminar")


    # Salir de la interfaz de detalle de venta
    def salirDetalleVenta(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(5)


    # Salir de la interfaz de eliminar un detalle de la venta
    def salirDetalleVentaEliminar(self):
        self.ventanaRealizarVentas.stackedWidget.setCurrentIndex(2)


# Bloque principal para ejecutar la aplicación de forma independiente
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    menu = RealizarVentas()
    menu.show()
    app.exec_()
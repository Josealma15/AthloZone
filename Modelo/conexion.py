# IMPORTAR MODULO
import psycopg2
from psycopg2 import OperationalError

class Comunicacion:

    def __init__(self):
        # None se usan para indicar que inicialmente no hay una conexión establecida ni un cursor creado.
        # Estos valores se actualizarán más tarde cuando se establezca la conexión real a la base de datos.

        self.conexion = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        try:
            self.conexion = psycopg2.connect(
                user="postgres",
                password="athlozone",
                host="127.0.0.1",
                port="5432",
                database="AthlozoneV2"
            )
            self.cursor = self.conexion.cursor()
            print("Conexión exitosa a la base de datos")
        except OperationalError as e:
            print(f"Error al conectar a la base de datos: {e}")

# --------------------------------------------- FUNCIONES BASE DE DATOS PARA LA INTERFAZ DE CONTROLAR STOCK ---------------------------------------------

    def mostrarProductos(self):
        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM productos ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def agregarProductoControlarStock(self, nombre, descripcion, precio, cantidad_stock, categoria):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = """
                INSERT INTO productos (nombre, descripcion, precio, cantidad_stock, categoria)
                VALUES (%s, %s, %s, %s, %s)
                """

            # Crear una tupla con los valores a insertar
            valores = (nombre, descripcion, precio, cantidad_stock, categoria)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Confirmar la transacción
            self.conexion.commit()

            print(
                f"Producto agregado exitosamente: {nombre} : {descripcion} : {precio} : {cantidad_stock} : {categoria}")
            return True

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar el producto: {e}")
            return False


    def buscarProductoActualizarControlarStock(self, productoBuscar):

        try:
            # Crear una consulta SQL flexible que busque en todos los campos relevantes
            sql = """
                SELECT * FROM productos
                WHERE id::text ILIKE %s
                OR nombre ILIKE %s
                OR precio::text ILIKE %s
                OR cantidad_stock::text ILIKE %s
                OR categoria ILIKE %s
                """

            # Preparar el valor de búsqueda para que funcione con ILIKE
            valor_busqueda = f"%{productoBuscar}%"

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, [valor_busqueda] * 5)

            # Obtener todos los resultados
            resultados = self.cursor.fetchall()

            if resultados:
                return resultados
            else:
                return []

        except psycopg2.Error as e:
            print(f"Error al buscar el producto: {e}")
            return []


    def actualizarProductoMismoId(self, id_producto, nombre, descripcion, precio, cantidad_stock, categoria):

        print(id_producto, nombre, descripcion, precio, cantidad_stock, categoria)
        try:
            cursor = self.conexion.cursor()
            sql = """UPDATE productos SET 
                     nombre = %s, 
                     descripcion = %s, 
                     precio = %s, 
                     cantidad_stock = %s, 
                     categoria = %s 
                     WHERE id = %s"""

            valores = (nombre, descripcion, precio, cantidad_stock, categoria, id_producto)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False


    def eliminarProducto(self, id_producto):
        try:
            sql = "DELETE FROM productos WHERE id = %s"
            self.cursor.execute(sql, (id_producto,))
            self.conexion.commit()
            print(f"Producto con ID {id_producto} eliminado de la base de datos")
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar el producto: {e}")
            self.conexion.rollback()
            return False


# --------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------- FUNCIONES BASE DE DATOS PARA LA INTERFAZ DE GESTIONAR PROVEEDORES ---------------------------------------------

    def mostrarProveedores(self):

        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM proveedores ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def agregarProveedor(self, nombre, email, telefono, direccion):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = """
                INSERT INTO proveedores (nombre, email, telefono, direccion)
                VALUES (%s, %s, %s, %s)
                """

            # Crear una tupla con los valores a insertar
            valores = (nombre, email, telefono, direccion)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Confirmar la transacción
            self.conexion.commit()

            print(
                f"Producto agregado exitosamente: {nombre} : {email} : {telefono} : {direccion}")
            return True

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar el proveedor: {e}")
            return False


    def buscarProveedorActualizar(self, proveedorBuscar):

        try:
            # Crear una consulta SQL flexible que busque en todos los campos relevantes
            sql = """
                SELECT * FROM proveedores
                WHERE id::text ILIKE %s
                OR nombre ILIKE %s
                OR email::text ILIKE %s
                OR telefono::text ILIKE %s
                OR direccion ILIKE %s
                """

            # Preparar el valor de búsqueda para que funcione con ILIKE
            valor_busqueda = f"%{proveedorBuscar}%"

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, [valor_busqueda] * 5)

            # Obtener todos los resultados
            resultados = self.cursor.fetchall()

            if resultados:
                return resultados
            else:
                return []

        except psycopg2.Error as e:
            print(f"Error al buscar el proveedor: {e}")
            return []


    def actualizarProveedorMismoId(self, idOriginal,nombre, email, telefono, direccion):

        try:
            cursor = self.conexion.cursor()
            sql = """UPDATE proveedores SET 
                     nombre = %s, 
                     email = %s, 
                     telefono = %s, 
                     direccion = %s 
                     WHERE id = %s"""

            valores = (nombre, email, telefono, direccion, idOriginal)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar proveedor: {e}")
            return False


    def eliminarProveedor(self, id_proveedor):
        try:
            sql = "DELETE FROM proveedores WHERE id = %s"
            self.cursor.execute(sql, (id_proveedor,))
            self.conexion.commit()
            print(f"Proveedor con ID {id_proveedor} eliminado de la base de datos")
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar el proveedor: {e}")
            self.conexion.rollback()
            return False

# --------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------- FUNCIONES BASE DE DATOS PARA LA INTERFAZ DE GESTIONAR CLIENTES -------------------------------------------

    def mostrarClientes(self):

        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM clientes ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def agregarCliente(self, id, nombre, email, telefono, direccion):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = """INSERT INTO clientes (id, nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s)"""

            # Crear una tupla con los valores a insertar
            valores = (id, nombre, email, telefono, direccion)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Confirmar la transacción
            self.conexion.commit()

            print(
                f"cliente agregado exitosamente: {id} {nombre} : {email} : {telefono} : {direccion}")
            return True

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar el cliente: {e}")
            return False


    def buscarClienteActualizar(self, clienteBuscar):

        try:
            # Crear una consulta SQL flexible que busque en todos los campos relevantes
            sql = """
                SELECT * FROM clientes
                WHERE id::text ILIKE %s
                OR nombre ILIKE %s
                OR email::text ILIKE %s
                OR telefono::text ILIKE %s
                OR direccion ILIKE %s
                """

           #Preparar el valor de búsqueda para que funcione con ILIKE
            valor_busqueda = f"%{clienteBuscar}%"

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, [valor_busqueda] * 5)

            # Obtener todos los resultados
            resultados = self.cursor.fetchall()

            if resultados:
                return resultados
            else:
                return []

        except psycopg2.Error as e:
            print(f"Error al buscar el cliente: {e}")
            return []


    def actualizarClienteMismoId(self, idOriginal, nuevo_id, nuevo_nombre, nuevo_email, nuevo_telefono, nueva_direccion):

        try:
            cursor = self.conexion.cursor()
            sql = """UPDATE clientes SET id = %s, nombre = %s, email = %s, telefono = %s, direccion = %s WHERE id = %s"""

            valores = (nuevo_id, nuevo_nombre, nuevo_email, nuevo_telefono, nueva_direccion, idOriginal)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False


    def eliminarCliente(self, id_clientes):
        try:
            sql = "DELETE FROM clientes WHERE id = %s"
            self.cursor.execute(sql, (id_clientes,))
            self.conexion.commit()
            print(f"Cliente con ID {id_clientes} eliminado de la base de datos")
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar el cliente: {e}")
            self.conexion.rollback()
            return False


# --------------------------------------------------------------------------------------------------------------------------------------------------------




# --------------------------------------------- FUNCIONES BASE DE DATOS PARA LA INTERFAZ DE REALIZAR VENTAS ---------------------------------------------

    def mostrarVentas(self):

        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM ventas ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def agregarVenta(self, fecha, id_clientes, total):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = "INSERT INTO ventas (fecha, cliente_id, total) VALUES (%s, %s, %s) RETURNING id"

            # Crear una tupla con los valores a insertar
            valores = (fecha, id_clientes, total)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Obtener el ID de la venta recién creada
            id_creado = self.cursor.fetchone()[0]

            # Confirmar la transacción
            self.conexion.commit()


            print(f"venta agregado exitosamente: {id_creado} : {fecha} : {id_clientes} : {total}")
            return id_creado

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar la venta: {e}")
            return e


    def agregarProductoVenta(self, id_venta, id_producto, cantidad, precio_unitario):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = """ INSERT INTO detalles_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s) """

            # Crear una tupla con los valores a insertar
            valores = (id_venta, id_producto, cantidad, precio_unitario)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Confirmar la transacción
            self.conexion.commit()

            print(
                f"venta agregado exitosamente: {id_venta} : {id_producto} : {cantidad} : {precio_unitario}")
            return True

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar producto a la venta: {e}")
            return False


    def obtenerValorProducto(self, id_producto):

        sql_select = "SELECT precio FROM productos WHERE id = %s;"
        self.cursor.execute(sql_select, (id_producto,))
        resultado = self.cursor.fetchone()

        if resultado is None:
            return False

        else:
            precio_producto = resultado[0]
            return precio_producto


    def actualizarTablaProductos(self, id_producto, cantidad ):

        sql_select = "SELECT cantidad_stock FROM productos WHERE id = %s;"
        self.cursor.execute(sql_select, (id_producto,))
        resultado = self.cursor.fetchone()

        if resultado is None:
            return False  # El producto no existe

        cantidad_actual = int(resultado[0])
        cantidad = int(cantidad)

        if cantidad_actual > 0:
            if cantidad <= cantidad_actual:
                # Calculamos la nueva cantidad
                nueva_cantidad = cantidad_actual - cantidad
                # Actualizamos la tabla con la nueva cantidad
                sql_update = "UPDATE productos SET cantidad_stock = %s WHERE id = %s;"
                self.cursor.execute(sql_update, (nueva_cantidad, id_producto))
                # Commit para guardar los cambios
                self.conexion.commit()
                return True
            else:
                return False  # No hay suficiente stock
        else:
            return False  # No hay stock disponible


    def mostrarDetallesVentas(self, idventa):

        #print(f"DESDE CONEXION {idventa}")
        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM detalles_venta WHERE venta_id = %s ORDER BY id", (idventa,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def actualizarVentaMismoId(self, idOriginal, nueva_fecha, nuevo_id_cliente):

        try:
            cursor = self.conexion.cursor()
            sql = """UPDATE ventas SET 
                     fecha = %s, 
                     cliente_id = %s
                     WHERE id = %s"""

            valores = (nueva_fecha, nuevo_id_cliente, idOriginal)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar venta: {e}")
            return False


    def actualizarTotalVenta(self, id_venta, total):
        print(f"ACTUALIZANDO VENTA EN CONEXIO {total}")
        try:
            cursor = self.conexion.cursor()
            sql = """UPDATE ventas SET 
                     total = %s  WHERE id = %s """

            valores = (total, id_venta)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar nuevo total de venta: {e}")
            return False


    def obtenerCantidadProducto(self, id_producto):

        sql_select = "SELECT cantidad_stock FROM productos WHERE id = %s;"
        self.cursor.execute(sql_select, (id_producto,))
        resultado = self.cursor.fetchone()

        if resultado is None:
            return False

        else:
            precio_producto = resultado[0]
            return precio_producto


    def actualizarProductoDetalleVentaMismoId(self, id_detalle, id_producto, nueva_cantidad, diferencia, resta):

        try:
            cantidad = self.obtenerCantidadProducto(id_producto)
            if cantidad >= nueva_cantidad:

                cursor = self.conexion.cursor()
                sql = "UPDATE detalles_venta SET cantidad = %s WHERE id = %s"
                valores = (nueva_cantidad, id_detalle)
                cursor.execute(sql, valores)
                self.conexion.commit()

                if resta:
                    if cantidad < diferencia:
                        return False
                    else:
                        cantidad -= diferencia
                else:
                    cantidad += diferencia

                sql2 = "UPDATE productos SET cantidad_stock = %s WHERE id = %s"
                valores2 = (cantidad, id_producto)
                cursor.execute(sql2, valores2)
                self.conexion.commit()
                return True
            else:
                return False

        except Exception as e:
            print(f"Error al actualizar producto de detalle venta: {e}")
            return False


    def actualizarProductoDetalleVentaDiferenteId(self, id_detalle, id_producto_nuevo, id_producto_viejo, nueva_cantidad, vieja_cantidad):

        try:
            cantidad_producto_nuevo = self.obtenerCantidadProducto(id_producto_nuevo)
            cantidad_producto_viejo = self.obtenerCantidadProducto(id_producto_viejo)
            valor_producto_nuevo = self.obtenerValorProducto(id_producto_nuevo)

            if cantidad_producto_nuevo >= nueva_cantidad:
                cursor = self.conexion.cursor()
                sql = "UPDATE detalles_venta SET cantidad = %s, producto_id = %s, precio_unitario = %s WHERE id = %s"
                valores = (nueva_cantidad, id_producto_nuevo, valor_producto_nuevo, id_detalle)
                cursor.execute(sql, valores)
                self.conexion.commit()
                cantidad_producto_nuevo -= nueva_cantidad
                cantidad_producto_viejo += vieja_cantidad

                sql2 = "UPDATE productos SET cantidad_stock = %s WHERE id = %s"
                valores2 = (cantidad_producto_viejo, id_producto_viejo)
                cursor.execute(sql2, valores2)
                self.conexion.commit()

                sql22 = "UPDATE productos SET cantidad_stock = %s WHERE id = %s"
                valores22 = (cantidad_producto_nuevo, id_producto_nuevo)
                cursor.execute(sql22, valores22)
                self.conexion.commit()
                return True
            else:
                return False

        except Exception as e:
            print(f"Error al actualizar producto de detalle venta: {e}")
            return False


    def buscarVentaActualizar(self, ventaBuscar):

        try:
            # Crear una consulta SQL flexible que busque en todos los campos relevantes
            sql = """
                         SELECT * FROM ventas WHERE id::text ILIKE %s OR CAST(fecha AS TEXT) ILIKE %s OR cliente_id::text ILIKE %s OR total::text ILIKE %s
                 """

            # Preparar el valor de búsqueda para que funcione con ILIKE
            valor_busqueda = f"%{ventaBuscar}%"

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, [valor_busqueda] * 4)

            # Obtener todos los resultados
            resultados = self.cursor.fetchall()

            if resultados:
                return resultados
            else:
                return []

        except psycopg2.Error as e:
            print(f"Error al buscar la venta: {e}")
            return []


    def actualizarVentaDespuesDeDetalles(self, id_venta, total_venta):

        try:
            cursor = self.conexion.cursor()
            sql = """UPDATE ventas SET 
                      total = %s  WHERE id = %s """

            valores = (total_venta, id_venta)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar nuevo total de venta: {e}")
            return False


    def eliminarVenta(self, id_venta):
        try:
            sql = "DELETE FROM ventas WHERE id = %s"
            self.cursor.execute(sql, (id_venta,))
            self.conexion.commit()
            print(f"Venta con ID {id_venta} eliminada de la base de datos")
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar la venta: {e}")
            self.conexion.rollback()
            return False


    def eliminarDetalle(self, id_detalle, cantidad_detalle_eliminar, id_producto):

        try:
            sql = "DELETE FROM detalles_venta WHERE id = %s AND cantidad = %s AND producto_id = %s"
            self.cursor.execute(sql, (id_detalle, cantidad_detalle_eliminar, id_producto))
            self.conexion.commit()
            print(f"Producto con ID {id_detalle} eliminada de la base de datos")

            # Ls sumamos al producto en stock la cantidad a eliminar porque no se va a vender
            cantidad = int(self.obtenerCantidadProducto(id_producto))
            cantidad += int(cantidad_detalle_eliminar)

            # Actualizamos esa cantidad en el stock
            sql2 = """UPDATE productos SET cantidad_stock = %s WHERE id = %s"""
            valores2 = (cantidad, id_producto)
            self.cursor.execute(sql2, valores2)
            self.conexion.commit()

            return True

        except psycopg2.Error as e:
            print(f"Error al eliminar el producto: {e}")
            self.conexion.rollback()
            return False


# --------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------- FUNCIONES BASE DE DATOS PARA LA INTERFAZ DE REGISTRAR COMPRAS ---------------------------------------------

    def mostrarCompras(self):

        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM compras ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def mostrarDetallesCompras(self, compra_id):

        #print(f"DESDE CONEXION {idventa}")
        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM detalles_compra WHERE compra_id = %s ORDER BY id", (compra_id,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def mostrarDetallesCompras(self, id_compra):

        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM detalles_compra WHERE compra_id = %s ORDER BY id", (id_compra,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def agregarCompra(self, fecha, proveedor_id, total):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = "INSERT INTO compras (fecha, proveedor_id, total) VALUES (%s, %s, %s) RETURNING id"

            # Crear una tupla con los valores a insertar
            valores = (fecha, proveedor_id, total)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Obtener el ID de la venta recién creada
            id_creado = self.cursor.fetchone()[0]

            # Confirmar la transacción
            self.conexion.commit()

            print(f"compra agregada exitosamente: {id_creado} : {fecha} : {proveedor_id} : {total}")
            return id_creado

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar la venta: {e}")
            return e


    def agregarProductoCompra(self, id_compra, id_producto, cantidad, precio_unitario):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = """ INSERT INTO detalles_compra (compra_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s) """

            # Crear una tupla con los valores a insertar
            valores = (id_compra, id_producto, cantidad, precio_unitario)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Confirmar la transacción
            self.conexion.commit()

            print(f"Producto agregado a compra exitosamente: {id_compra} : {id_producto} : {cantidad} : {precio_unitario}")
            return True

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar producto a la compra: {e}")
            return False


    def actualizarStockProducto(self, producto_id, cantidad, precio_unitario):

        try:
            stock = self.obtenerCantidadProducto(producto_id)
            total = int(stock) + int(cantidad)
            cursor = self.conexion.cursor()
            sql = "UPDATE productos SET cantidad_stock = %s, precio = %s  WHERE id = %s "
            valores = (total, precio_unitario, producto_id)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True

        except Exception as e:
            print(f"Error al actualizar nuevo total de compra: {e}")
            return False


    def actualizarTotalCompra(self, compra_id, total):
        print(f"ACTUALIZANDO COMPRA EN CONEXION {total}")

        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE compras SET total = %s  WHERE id = %s "
            valores = (total, compra_id)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True

        except Exception as e:
            print(f"Error al actualizar nuevo total de compra: {e}")
            return False


    def actualizarVenta(self, id_compra, fecha, proveedor_id):

        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE compras SET fecha = %s  AND proveedor_id WHERE id = %s "
            valores = (fecha, proveedor_id, id_compra)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True

        except Exception as e:
            print(f"Error al actualizar nuevo total de compra: {e}")
            return False


    def buscarCompraActualizar(self, compra_buscar):

        try:
            # Crear una consulta SQL flexible que busque en todos los campos relevantes
            sql = "SELECT * FROM compras WHERE id::text ILIKE %s OR CAST(fecha AS TEXT) ILIKE %s OR proveedor_id::text ILIKE %s OR total::text ILIKE %s ORDER BY id"


            # Preparar el valor de búsqueda para que funcione con ILIKE
            valor_busqueda = f"%{compra_buscar}%"

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, [valor_busqueda] * 4)

            # Obtener todos los resultados
            resultados = self.cursor.fetchall()

            if resultados:
                return resultados
            else:
                return []

        except psycopg2.Error as e:
            print(f"Error al buscar la compra: {e}")
            return []


    def actualizarCompraMismoId(self, id_original, nueva_fecha, nuevo_id_proveedor):

        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE compras SET fecha = %s, proveedor_id = %s WHERE id = %s"

            valores = (nueva_fecha, nuevo_id_proveedor, id_original)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar compra: {e}")
            return False


    def actualizarProductoDetalleCompraMismoId(self, id_detalle, id_producto_viejo, nueva_cantidad, precio_unitario_nuevo, diferencia, suma):

        try:
            cantidad = self.obtenerCantidadProducto(id_producto_viejo)

            if cantidad >= nueva_cantidad:

                cursor = self.conexion.cursor()
                sql = "UPDATE detalles_compra SET cantidad = %s, precio_unitario = %s WHERE id = %s"

                valores = (nueva_cantidad, precio_unitario_nuevo, id_detalle)
                cursor.execute(sql, valores)
                self.conexion.commit()

                if not suma:
                    if cantidad < diferencia:
                        return False
                    else:
                        cantidad -= diferencia

                else:
                    cantidad += diferencia

                sql2 = "UPDATE productos SET cantidad_stock = %s, precio = %s WHERE id = %s"

                valores2 = (cantidad, precio_unitario_nuevo, id_producto_viejo)
                cursor.execute(sql2, valores2)
                self.conexion.commit()

                return True

            else:
                return False

        except Exception as e:
            print(f"Error al actualizar producto de detalle venta: {e}")
            return False


    def actualizarProductoDetalleCompraDiferenteId(self, id_detalle,id_producto_nuevo,id_producto_viejo,nueva_cantidad,vieja_cantidad, viejo_precio, nuevo_precio):


        try:
            cantidad_producto_nuevo = self.obtenerCantidadProducto(id_producto_nuevo)
            cantidad_producto_viejo = self.obtenerCantidadProducto(id_producto_viejo)

            #nuevo_precio = self.obtenerValorProducto(id_producto_nuevo)

            if cantidad_producto_nuevo >= nueva_cantidad:

                cantidad_producto_nuevo += nueva_cantidad
                cantidad_producto_viejo -= vieja_cantidad


                cursor = self.conexion.cursor()
                sql = "UPDATE detalles_compra SET cantidad = %s, producto_id = %s, precio_unitario = %s WHERE id = %s"
                valores = (nueva_cantidad, id_producto_nuevo, nuevo_precio, id_detalle)
                cursor.execute(sql, valores)
                self.conexion.commit()

                sql2 = "UPDATE productos SET cantidad_stock = %s WHERE id = %s"
                valores2 = (cantidad_producto_viejo, id_producto_viejo)
                cursor.execute(sql2, valores2)
                self.conexion.commit()

                sql22 = "UPDATE productos SET cantidad_stock = %s, precio = %s WHERE id = %s"
                valores22 = (cantidad_producto_nuevo, nuevo_precio, id_producto_nuevo)
                cursor.execute(sql22, valores22)
                self.conexion.commit()


                return True

            else:
                return False

        except Exception as e:
            print(f"Error al actualizar producto de detalle venta: {e}")
            return False


    def eliminarCompra(self, id_compra):
        try:
            sql = "DELETE FROM compras WHERE id = %s"
            self.cursor.execute(sql, (id_compra,))
            self.conexion.commit()
            print(f"Compra con ID {id_compra} eliminada de la base de datos")
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar la compra: {e}")
            self.conexion.rollback()
            return False


    def eliminarDetalleCompra(self, id_detalle, cantidad_detalle_eliminar, id_producto):

        try:
            sql = "DELETE FROM detalles_compra WHERE id = %s AND cantidad = %s AND producto_id = %s"
            self.cursor.execute(sql, (id_detalle, cantidad_detalle_eliminar, id_producto))
            self.conexion.commit()
            print(f"Producto con ID {id_detalle} eliminada de la base de datos")

            # Ls sumamos al producto en stock la cantidad a eliminar porque no se va a vender
            cantidad = int(self.obtenerCantidadProducto(id_producto))
            cantidad -= int(cantidad_detalle_eliminar)

            # Actualizamos esa cantidad en el stock
            sql2 = """UPDATE productos SET cantidad_stock = %s WHERE id = %s"""
            valores2 = (cantidad, id_producto)
            self.cursor.execute(sql2, valores2)
            self.conexion.commit()

            return True

        except psycopg2.Error as e:
            print(f"Error al eliminar el producto: {e}")
            self.conexion.rollback()
            return False


# --------------------------------------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------ FUNCIONES BASE DE DATOS PARA LA INTERFAZ DE GESTIONAR USUARIOS ----------------------------------------------

    def mostrarUsuarios(self):

        if self.conexion is None or self.cursor is None:
            print("No hay conexión a la base de datos")
            return []

        try:
            self.cursor.execute("SELECT * FROM usuarios ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []


    def agregarUsuarios(self, id, nombre, email, contrasena, rol):

        try:
            # Crear la consulta SQL para insertar el nuevo producto
            sql = "INSERT INTO usuarios (id, nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s, %s)"

            # Crear una tupla con los valores a insertar
            valores = (id, nombre, email, contrasena, rol)

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, valores)

            # Confirmar la transacción
            self.conexion.commit()

            print(
                f"Usuario agregado exitosamente: {id} {nombre} : {email} : {contrasena} : {rol}")
            return True

        except psycopg2.Error as e:

            # Si ocurre un error, hacer rollback y mostrar el error
            self.conexion.rollback()
            print(f"Error al agregar el usuario: {e}")
            return False


    def buscarUsuariosActualizar(self, usuarioBuscar):

        try:
            # Crear una consulta SQL flexible que busque en todos los campos relevantes
            sql = "SELECT * FROM usuarios WHERE id::text ILIKE %s OR nombre::text ILIKE %s OR email::text ILIKE %s OR contraseña::text ILIKE %s OR rol::text ILIKE %s"

            # Preparar el valor de búsqueda para que funcione con ILIKE
            valor_busqueda = f"%{usuarioBuscar}%"

            # Ejecutar la consulta SQL
            self.cursor.execute(sql, [valor_busqueda] * 5)

            # Obtener todos los resultados
            resultados = self.cursor.fetchall()

            if resultados:
                return resultados
            else:
                return []

        except psycopg2.Error as e:
            print(f"Error al buscar el usuario: {e}")
            return []


    def actualizarUsuariosMismoId(self, idOriginal, nuevo_id, nuevo_nombre, nuevo_email, nueva_contrasena, nuevo_rol):

        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE usuarios SET id = %s, nombre = %s, email = %s, contraseña = %s, rol = %s WHERE id = %s"

            valores = (nuevo_id, nuevo_nombre, nuevo_email, nueva_contrasena, nuevo_rol, idOriginal)
            cursor.execute(sql, valores)
            self.conexion.commit()
            return True

        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False


    def eliminarUsuarios(self, id_usuario):
        try:
            sql = "DELETE FROM usuarios WHERE id = %s"
            self.cursor.execute(sql, (id_usuario,))
            self.conexion.commit()
            print(f"Usuario con ID {id_usuario} eliminado de la base de datos")
            return True

        except psycopg2.Error as e:
            print(f"Error al eliminar el usuario: {e}")
            self.conexion.rollback()
            return False

# --------------------------------------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------ FUNCIONES BASE DE DATOS PARA GESTIONAR EL ROL DEL USUARIO  ----------------------------------------------

    def obtenerRolLogin(self, name, password):
        try:
            cursor = self.conexion.cursor()
            sql = "SELECT rol FROM usuarios WHERE nombre = %s AND contraseña = %s"
            cursor.execute(sql, (name, password))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]  # Devuelve el rol si se encuentra
            else:
                return None  # Retorna None si no se encuentra el usuario
        except Exception as e:
            print(f"Error al obtener el rol: {e}")
            return None

# --------------------------------------------------------------------------------------------------------------------------------------------------------



    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada")

    def __del__(self):
        self.cerrar_conexion()

if __name__ == "__main__":
    conec = Comunicacion()
    conec.cerrar_conexion()

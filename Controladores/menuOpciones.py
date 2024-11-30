# Importación de módulos necesarios de PyQt5
from PyQt5 import QtWidgets, uic

class MenuOpciones(QtWidgets.QMainWindow):
    """
    Clase que representa el menú principal de opciones para usuarios administradores.
    Hereda de QMainWindow para crear una ventana principal.
    """

    def __init__(self):
        """
        Constructor de la clase. Inicializa la ventana y conecta los botones
        con sus respectivas funciones.
        """
        super().__init__()
        # Carga el archivo UI que contiene el diseño de la interfaz
        self.ventanaMenuOpciones = uic.loadUi("Vistas/ventanaMenuOpciones/ventanaMenuOpciones.ui", self)

        # Conexión de señales de los botones con sus respectivos métodos
        self.ventanaMenuOpciones.botonSalirMenuOpciones.clicked.connect(self.salir)
        self.ventanaMenuOpciones.botonRegresarMenuOpciones.clicked.connect(self.volveraVentanaLogin)
        self.ventanaMenuOpciones.botonControlarStock.clicked.connect(self.irControlarStock)
        self.ventanaMenuOpciones.botonGestionarProveedores.clicked.connect(self.irGestionarProveedores)
        self.ventanaMenuOpciones.botonGestionarClientes.clicked.connect(self.irGestionarClientes)
        self.ventanaMenuOpciones.botonGestionarUsuarios.clicked.connect(self.irGestionarUsuarios)
        self.ventanaMenuOpciones.botonRealizarVentas.clicked.connect(self.irRealizarVentas)
        self.ventanaMenuOpciones.botonRegistrarCompras.clicked.connect(self.irRegistrarCompras)

    def showMenuOpciones(self):
        """Método para mostrar la ventana del menú de opciones"""
        self.show()

    def hideMenuOpciones(self):
        """Método para ocultar la ventana del menú de opciones"""
        self.hide()

    def volveraVentanaLogin(self):
        """
        Método para volver a la ventana de login.
        Oculta la ventana actual y muestra la ventana de inicio de sesión.
        """
        # Importa VentanaLogin y crea una nueva instancia
        from principal import VentanaLogin

        self.hide()  # Oculta la ventana actual de MenuOpciones

        self.login_window = VentanaLogin()
        self.login_window.ventanaLogin.show()  # Muestra la ventana de login

    def salir(self):
        """Método para cerrar la aplicación"""
        self.close()

    def irControlarStock(self):
        """
        Método para abrir la ventana de control de stock.
        Crea y muestra una nueva instancia de la ventana ControlarStock.
        """
        from controlarStock import ControlarStock
        # self.hide()
        self.stock_window = ControlarStock()
        self.stock_window.show()

    def irGestionarProveedores(self):
        """
        Método para abrir la ventana de gestión de proveedores.
        Crea y muestra una nueva instancia de la ventana GestionarProveedores.
        """
        from gestionarProveedores import GestionarProveedores

        # self.hide()
        self.proveedores_window = GestionarProveedores()
        self.proveedores_window.show()

    def irGestionarClientes(self):
        """
        Método para abrir la ventana de gestión de clientes.
        Crea y muestra una nueva instancia de la ventana GestionarClientes.
        """
        from gestionarClientes import GestionarClientes

        # self.hide()
        self.clientes_window = GestionarClientes()
        self.clientes_window.show()

    def irGestionarUsuarios(self):
        """
        Método para abrir la ventana de gestión de usuarios.
        Crea y muestra una nueva instancia de la ventana GestionarUsuarios.
        """
        from gestionarUsuarios import GestionarUsuarios

        # self.hide()
        self.clientes_window = GestionarUsuarios()
        self.clientes_window.show()

    def irRealizarVentas(self):
        """
        Método para abrir la ventana de realización de ventas.
        Crea y muestra una nueva instancia de la ventana RealizarVentas.
        """
        from realizarVentas import RealizarVentas
        # self.hide()
        self.clientes_window = RealizarVentas()
        self.clientes_window.show()

    def irRegistrarCompras(self):
        """
        Método para abrir la ventana de registro de compras.
        Crea y muestra una nueva instancia de la ventana RegistrarCompras.
        """
        from registrarCompras import RegistrarCompras

        # self.hide()
        self.clientes_window = RegistrarCompras()
        self.clientes_window.show()


# Bloque principal para ejecutar la aplicación de forma independiente
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    menu = MenuOpciones()
    menu.show()
    app.exec_()
# Importación de módulos necesarios de PyQt5
from PyQt5 import QtWidgets, uic

class MenuOpcionesVendedor(QtWidgets.QMainWindow):
    """
    Clase que representa el menú de opciones para usuarios vendedores.
    Hereda de QMainWindow para crear una ventana principal.
    Esta versión tiene funcionalidades limitadas comparada con el menú de administrador.
    """

    def __init__(self):
        """
        Constructor de la clase. Inicializa la ventana y conecta los botones
        con sus respectivas funciones.
        """
        super().__init__()

        # Carga el archivo UI que contiene el diseño de la interfaz para vendedores
        self.ventanaMenuOpcionesVendedor = uic.loadUi("Vistas/ventanaMenuOpciones/ventanaMenuOpcionesVendedor.ui", self)

        # Conexión de señales de los botones con sus respectivos métodos
        self.ventanaMenuOpcionesVendedor.botonRegresarMenuOpcionesVendedor.clicked.connect(self.volveraVentanaLogin)
        self.ventanaMenuOpcionesVendedor.botonSalirMenuOpcionesVendedor.clicked.connect(self.salir)
        self.ventanaMenuOpcionesVendedor.botonControlarStock.clicked.connect(self.irControlarStock)
        self.ventanaMenuOpcionesVendedor.botonRealizarVentas.clicked.connect(self.irRealizarVentas)
        self.ventanaMenuOpcionesVendedor.botonRegistrarCompras.clicked.connect(self.irRegistrarCompras)

    def showMenuOpcionesVendedor(self):
        """Método para mostrar la ventana del menú de opciones del vendedor"""
        self.show()

    def hideMenuOpciones(self):
        """Método para ocultar la ventana del menú de opciones del vendedor"""
        self.hide()

    def volveraVentanaLogin(self):
        """
        Método para volver a la ventana de login.
        Crea y muestra una nueva instancia de la ventana de inicio de sesión.
        """
        # Importa VentanaLogin y crea una nueva instancia
        from principal import VentanaLogin

        # self.hide()  # Oculta la ventana actual de MenuOpciones

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
    menu = MenuOpcionesVendedor()
    menu.show()
    app.exec_()
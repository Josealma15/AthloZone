# Importar librerías necesarias
from PyQt5 import QtWidgets, uic
from menuOpciones import MenuOpciones
from menuOpcionesVendedor import MenuOpcionesVendedor
from Modelo.conexion import Comunicacion
import hashlib


class VentanaLogin:
    """
    Clase que maneja la ventana de inicio de sesión de la aplicación.
    Gestiona la autenticación de usuarios y redirecciona según el rol.
    """

    def __init__(self):
        """
        Constructor de la clase. Inicializa la aplicación y carga las interfaces gráficas.
        También configura las conexiones de los botones y la base de datos.
        """
        # Crear instancia de la aplicación PyQt
        self.app = QtWidgets.QApplication([])

        # Cargar las interfaces gráficas desde archivos .ui
        self.ventanaLogin = uic.loadUi("Vistas/ventanaLogin/ventanaLogin1.ui")  # Ventana principal de login
        self.ventanaLoginIncorrecto = uic.loadUi("Vistas/ventanaLogin/ventanaLogin2-inicioIncorrecto.ui")  # Ventana de error

        # Configurar las conexiones de los botones con sus respectivas funciones
        self.ventanaLogin.pushButton.clicked.connect(self.guiVentanaLogin)  # Botón de inicio de sesión
        self.ventanaLogin.pushButton_3.clicked.connect(self.salir)  # Botón de salir
        self.ventanaLoginIncorrecto.pushButton_4.clicked.connect(self.regresardeventanaLoginInCorrecto)  # Botón de regresar
        self.ventanaLoginIncorrecto.pushButton_3.clicked.connect(self.salir)  # Botón de salir en ventana de error

        # Inicializar la conexión con la base de datos
        self.baseDatos = Comunicacion()

        # Iniciar la aplicación
        self.ejecutarApp()

    def guiVentanaLogin(self):
        """
        Maneja el proceso de autenticación cuando el usuario intenta iniciar sesión.
        Verifica las credenciales y redirecciona según el rol del usuario.
        """
        # Obtener datos ingresados por el usuario
        name = self.ventanaLogin.lineEdit.text()
        password = self.ventanaLogin.lineEdit_2.text()
        password = hashlib.sha256(password.encode()).hexdigest()

        # Verificar el rol del usuario en la base de datos
        rol = self.baseDatos.obtenerRolLogin(name, password)

        # Validar campos vacíos
        if len(name) == 0 or len(password) == 0:
            self.ventanaLogin.label_4.setText("Ingrese todos los datos")

        # Validar si las credenciales son correctas
        elif rol is None:
            self.ventanaLogin.label_4.setText("Usuario o contraseña incorrectos")

        # Redireccionar según el rol del usuario
        elif rol == "admin":
            self.ventanaLogin.hide()
            menu_opciones = MenuOpciones()
            menu_opciones.showMenuOpciones()

        elif rol == "empleado":
            self.ventanaLogin.hide()
            menu_opciones_vendedor = MenuOpcionesVendedor()
            menu_opciones_vendedor.showMenuOpcionesVendedor()

        else:
            self.ventanaLogin.hide()
            self.guiventanaLoginIncorrecto()

    def guiventanaLoginIncorrecto(self):
        """
        Muestra la ventana de error cuando el inicio de sesión es incorrecto.
        """
        self.ventanaLogin.hide()
        self.ventanaLoginIncorrecto.show()

    def regresardeventanaMenuOpciones(self):
        """
        Maneja el retorno desde el menú de opciones a la ventana de login.
        Limpia los campos de entrada y mensajes de error.
        """
        MenuOpciones().hideMenuOpciones()

        # Limpiar campos de entrada
        name = self.ventanaLogin.lineEdit
        password = self.ventanaLogin.lineEdit_2
        name.setText("")
        password.setText("")

        # Limpiar mensaje de error
        self.ventanaLogin.label_4.setText("")

        self.ventanaLogin.show()

    def regresardeventanaLoginInCorrecto(self):
        """
        Maneja el retorno desde la ventana de error a la ventana principal de login.
        Limpia los campos de entrada y mensajes de error.
        """
        self.ventanaLoginIncorrecto.hide()

        # Limpiar campos de entrada
        name = self.ventanaLogin.lineEdit
        password = self.ventanaLogin.lineEdit_2
        name.setText("")
        password.setText("")

        # Limpiar mensaje de error
        self.ventanaLogin.label_4.setText("")

        self.ventanaLogin.show()

    def salir(self):
        """
        Cierra la aplicación.
        """
        self.app.exit()

    def conectarBotones(self):
        """
        Configura las conexiones entre los botones y sus funciones correspondientes.
        """
        # Conectar botones de la ventana principal
        self.ventanaLogin.pushButton.clicked.connect(self.guiVentanaLogin)
        self.ventanaLogin.pushButton_3.clicked.connect(self.salir)

        # Conectar botones de la ventana de error
        self.ventanaLoginIncorrecto.pushButton_4.clicked.connect(self.regresardeventanaLoginInCorrecto)
        self.ventanaLoginIncorrecto.pushButton_3.clicked.connect(self.salir)

    def ejecutarApp(self):
        """
        Inicia la ejecución de la aplicación mostrando la ventana de login.
        """
        self.ventanaLogin.show()
        self.app.exec_()


# Punto de entrada de la aplicación
if __name__ == "__main__":
    login = VentanaLogin()  # Crear instancia de la ventana de login
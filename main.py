import clientes
import conexion
import eventos
import styles
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        eventos.Eventos.cargarProv(self)

        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        EVENTOS DE BOTONES
        '''

        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)

        '''
        EVENTOS DE CAJAS DE TEXTO
        '''

        var.ui.txtDnicli.editingFinished.connect(lambda : clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
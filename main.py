import clientes
import conexion
import eventos
import styles
from venAux import Calendar
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        eventos.Eventos.cargarProv(self)
        eventos.Eventos.cargarMunicipios(self)
        clientes.Clientes.cargaTablaClientes(self)

        '''
        EVENTOS DEL MENUBAR
        '''

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        EVENTOS DE BOTONES
        '''

        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))

        '''
        EVENTOS DE CAJAS DE TEXTO
        '''

        var.ui.txtDnicli.editingFinished.connect(lambda : clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda : clientes.Clientes.checkEmail(var.ui.txtEmailcli.text()))

        '''
        EVENTOS COMOBOX
        '''

        var.ui.cmbProvinciacli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipios)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
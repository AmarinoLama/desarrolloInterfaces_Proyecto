import clientes
import conexion
import styles
from venAux import *
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.dlgabrir = FileDialogAbrir()
        var.dlggestion = dlgGestionProp()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        var.historico = 0
        #conexionserver.ConexionServer.crear_conexion(self)

        '''
        EVENTOS DE TABLAS
        '''

        clientes.Clientes.cargaTablaClientes(self)
        eventos.Eventos.resizeTablaClientes(self)
        eventos.Eventos.resizeTablaPropiedades(self)
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        var.ui.tablaPropiedades.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)
        propiedades.Propiedades.cargarTablaPropiedades(self)

        '''
        EVENTOS DEL MENUBAR
        '''

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionCargar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_Propiedades.triggered.connect(eventos.Eventos.abrirTipoProp)

        '''
        EVENTOS DE BOTONES
        '''

        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnBajacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))
        var.ui.btnPublicacionPro.clicked.connect(lambda: eventos.Eventos.abrirCalendar(2))
        var.ui.btnBajaPro.clicked.connect(lambda: eventos.Eventos.abrirCalendar(3))
        var.ui.btnModifcli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelcli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnGrabarPro.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModificarPro.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnEliminarPro.clicked.connect(propiedades.Propiedades.bajaPropiedad)

        '''
        EVENTOS DE CAJAS DE TEXTO
        '''

        var.ui.txtDnicli.editingFinished.connect(lambda : clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda : clientes.Clientes.checkEmail(var.ui.txtEmailcli.text()))
        var.ui.txtMovilcli.editingFinished.connect(lambda : clientes.Clientes.checkTelefono(var.ui.txtMovilcli.text()))
        var.ui.txtMovilPro.editingFinished.connect(lambda : propiedades.Propiedades.checkTelefono(var.ui.txtMovilPro.text()))

        '''
        EVENTOS COMBOBOX
        '''

        eventos.Eventos.cargarProv(self)
        var.ui.cmbProvinciacli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipiosCli)
        var.ui.cmbProvinciaPro.currentIndexChanged.connect(eventos.Eventos.cargarMunicipiosPro)
        eventos.Eventos.cargarTipoPropiedad(self)

        '''
        EVENTOS TOOLBAR
        '''

        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionTipoPropiedad.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionBuscar.triggered.connect(propiedades.Propiedades.filtrarPropiedades)

        '''
        EVENTOS DE CHECKBOX
        '''

        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
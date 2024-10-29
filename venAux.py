from datetime import datetime

from PyQt6.QtWidgets import QDialog

import propiedades
from dlgCalendar import *
import var
import eventos
from dlgGestionProp import *


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano,mes,dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

class dlgGestionProp(QtWidgets.QDialog):
    def __init__(self):
        super(dlgGestionProp, self).__init__()
        self.ui = Ui_dlg_Tipoprop()
        self.ui.setupUi(self)
        self.ui.btnAnadirtipoprop.clicked.connect(propiedades.Propiedades.altaTipoPropiedad)
        self.ui.btnDeltipoprop.clicked.connect(propiedades.Propiedades.bajaTipoPropiedad)
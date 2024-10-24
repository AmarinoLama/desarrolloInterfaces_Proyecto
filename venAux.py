from datetime import datetime

from PyQt6.QtWidgets import QDialog

from dlgCalendar import *
import var
import eventos
from dlgGestionProp import Ui_dlg_TipoProp


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

class dlg_Tipo_prop(QtWidgets, QDialog):
    def __init__(self):
        super(dlg_Tipo_prop, self).__init__()
        var.dlggestion = Ui_dlg_TipoProp()
        var.dlggestion.setupUi(self)
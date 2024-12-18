from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
import os, shutil
import var

class Informes:

    def reportClientes(self):
        try:
            fecha = datetime.today().strftime('%d/%m/%Y')
            nomepdfcli = fecha + "_listadoclientes.pdf"
            self.report = canvas.Canvas('informes/', nomepdfcli)
            titulo = "Listado Clientes"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)
            items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
            self.report.setFont('Helvetica-Bold', size=10)
            self.report.drawString(50, 650, str(items[0]))
            self.report.drawString(120, 650, str(items[1]))
            self.report.drawString(170, 650, str(items[2]))
            self.report.drawString(285, 650, str(items[3]))
            self.report.drawString(390, 650, str(items[4]))
            self.report.drawString(460, 650, str(items[5]))
            self.report.line(50, 645, 525, 645)

            var.report.save()
            rootPath = '.\\informes'
            for file in os.endswith(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(file)('%s\\%s' % (rootPath, file))
        except Exception as e:
            print(e)

    def topInforme(titulo):
        try:
            ruta_logo = '.\\img\\logo.ico'
            logo = Image.open(ruta_logo)

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'Transportes Teis')
                var.report.drawString(230, 670, titulo)
                var.report.line(50, 665, 525, 665)

                # Dibuja la imagen en el informe
                var.report.drawImage(ruta_logo, 480, 725, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 770, 'CIF: A12345678')
                var.report.drawString(55, 755, 'Avda. Galicia - 101')
                var.report.drawString(55, 740, 'Vigo - 36216 - España')
                var.report.drawString(55, 725, 'Teléfono: 986 132 456')
                var.report.drawString(55, 710, 'e-mail: cartesteisr@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def footInforme(titulo):
        try:
            total_pages = 0
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)
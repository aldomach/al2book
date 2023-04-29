import PySimpleGUI as sg
from PyPDF2 import PdfFileReader, PdfFileWriter

# Creamos la interfaz gráfica con PySimpleGUI
layout = [[sg.Text('Selecciona un archivo PDF')],
          [sg.Input(key='archivo'), sg.FileBrowse()],
          [sg.Button('Abrir'), sg.Button('Guardar')]]

window = sg.Window('Dividir PDF', layout)

# Esperamos a que el usuario seleccione un archivo y haga clic en el botón Abrir
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Abrir':
        archivo = values['archivo']
        # Leemos el archivo PDF y creamos un objeto PdfFileReader
        pdf_reader = PdfFileReader(open(archivo, 'rb'))
        # Creamos un objeto PdfFileWriter para escribir el nuevo archivo PDF
        pdf_writer = PdfFileWriter()

        # Iteramos sobre las páginas del archivo PDF original
        for pagina in range(pdf_reader.getNumPages()):
            # Agregamos cada página al objeto PdfFileWriter
            pdf_writer.addPage(pdf_reader.getPage(pagina))
            # Si ya hemos agregado cuatro páginas, creamos una nueva hoja
            if (pagina + 1) % 4 == 0:
                pdf_writer.addBlankPage()

        # Guardamos el nuevo archivo PDF
        nuevo_archivo = archivo.split('.')[0] + '_nuevo.pdf'
        with open(nuevo_archivo, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
            sg.popup(f'Se ha guardado el archivo {nuevo_archivo}')

    # Si el usuario hace clic en el botón Guardar sin haber seleccionado un archivo primero
    elif event == 'Guardar' and not values['archivo']:
        sg.popup('Por favor selecciona un archivo PDF primero')

window.close()

import PySimpleGUI as sg
from PyPDF2 import PdfFileReader, PdfFileWriter
from math import ceil


def combine_pages(pdf_reader):
    pdf_writer = PdfFileWriter()
    num_pages = pdf_reader.getNumPages()

    for i in range(0, num_pages, 4):
        # Crear una nueva página con las 4 páginas
        new_page = pdf_reader.getPage(i)
        if i+1 < num_pages:
            new_page.mergeTransformedPage(pdf_reader.getPage(i+1), [0.5, 0, 0, 0.5, new_page.mediaBox.getWidth()/2, 0], expand=False)
        if i+2 < num_pages:
            new_page.mergeTransformedPage(pdf_reader.getPage(i+2), [0.5, 0, 0, 0.5, 0, new_page.mediaBox.getHeight()/2], expand=False)
        if i+3 < num_pages:
            new_page.mergeTransformedPage(pdf_reader.getPage(i+3), [0.5, 0, 0, 0.5, new_page.mediaBox.getWidth()/2, new_page.mediaBox.getHeight()/2], expand=False)

        pdf_writer.addPage(new_page)

    return pdf_writer


def open_and_save_file(filepath):
    # Abrir archivo PDF
    pdf_reader = PdfFileReader(filepath, 'rb')

    # Ordenar las páginas
    pdf_writer = combine_pages(pdf_reader)

    # Agregar "_book" al final del nombre del archivo
    output_filename = filepath[:-4] + "_book.pdf"

    # Guardar el archivo PDF combinado
    with open(output_filename, 'wb') as output:
        pdf_writer.write(output)


def main():
    # Definir el diseño de la ventana
    layout = [[sg.Text("Seleccione un archivo PDF para combinar y ordenar:")],
              [sg.Input(key='filepath', enable_events=True), sg.FileBrowse()],
              [sg.Button("Guardar archivo PDF combinado", disabled=True)]]

    # Crear la ventana
    window = sg.Window("PDF Book Maker", layout)

    # Loop principal de la ventana
    while True:
        event, values = window.read()

        # Salir del loop si se cierra la ventana
        if event == sg.WINDOW_CLOSED:
            break

        # Actualizar el botón si se selecciona un archivo
        if event == 'filepath':
            if values['filepath'].lower().endswith('.pdf'):
                window['Guardar archivo PDF combinado'].update(disabled=False)
            else:
                window['Guardar archivo PDF combinado'].update(disabled=True)

        # Guardar el archivo PDF combinado si se hace clic en el botón
        if event == 'Guardar archivo PDF combinado':
            open_and_save_file(values['filepath'])
            # window.close()

    # Cerrar la ventana
    window.close()


if __name__ == '__main__':
    main()

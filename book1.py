import PySimpleGUI as sg
from PyPDF2 import PdfFileWriter, PdfFileReader

# Función para dividir un PDF en 4 páginas por hoja
def split_pdf(filename):
    pdf_reader = PdfFileReader(open(filename, "rb"))
    pdf_writer = PdfFileWriter()
    num_pages = pdf_reader.getNumPages()
    # Secuencia de páginas para reordenar
    seq = [32,1,31,2,30,3,29,4,28,5,27,6,26,7,25,8,
           24,9,23,10,22,11,21,12,20,13,19,14,
           18,15,17,16]
    # Índice para recorrer la secuencia
    i = 0
    # Bucle para crear las nuevas páginas
    while i < num_pages:
        # Crear una nueva página vacía
        new_page = pdf_writer.addBlankPage()
        # Obtener las 4 páginas originales según la secuencia
        page1 = pdf_reader.getPage(seq[i]-1)
        page2 = pdf_reader.getPage(seq[i+1]-1)
        page3 = pdf_reader.getPage(seq[i+2]-1)
        page4 = pdf_reader.getPage(seq[i+3]-1)
        # Escalar y rotar las páginas originales
        page1.scaleBy(0.5)
        page1.rotateClockwise(90)
        page2.scaleBy(0.5)
        page2.rotateClockwise(90)
        page3.scaleBy(0.5)
        page3.rotateClockwise(90)
        page4.scaleBy(0.5)
        page4.rotateClockwise(90)
        # Fusionar las páginas originales en la nueva página
        new_page.mergeTranslatedPage(page1, 0, 421)
        new_page.mergeTranslatedPage(page2, 0, 0)
        new_page.mergeTranslatedPage(page3, 297.5 ,421)
        new_page.mergeTranslatedPage(page4 ,297.5 ,0)
        # Avanzar el índice en 4 posiciones
        i += 4
    # Devolver el objeto PdfFileWriter con las nuevas páginas
    return pdf_writer

# Layout de la GUI con dos botones y dos entradas de texto
layout = [[sg.Button("Abrir PDF", key="open", image_filename="open.png", button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0),
           sg.InputText(key="input", size=(40,1), disabled=True)],
          [sg.Button("Guardar PDF", key="save", image_filename="save.png", button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0),
           sg.InputText(key="output", size=(40,1), disabled=True)]]

# Crear la ventana con el layout
window = sg.Window("PySimpleGUI PDF Splitter", layout)

# Bucle de eventos de la ventana
while True:
    event, values = window.read()
    # Si se cierra la ventana o se pulsa Escape, salir del bucle
    if event == sg.WINDOW_CLOSED or event == "Escape":
        break
    # Si se pulsa el botón de abrir PDF
    elif event == "open":
        # Abrir un diálogo para elegir el archivo PDF
        filename = sg.popup_get_file("Elige un archivo PDF", file_types=(("PDF Files", "*.pdf"),))
        # Si se ha elegido un archivo
            if filename:
            # Mostrar el nombre del archivo en la entrada de texto
            window["input"].update(filename)
            # Dividir el archivo PDF en 4 páginas por hoja
            pdf_writer = split_pdf(filename)
            # Guardar el objeto PdfFileWriter en una variable global
            global output_pdf
            output_pdf = pdf_writer
    # Si se pulsa el botón de guardar PDF y hay un objeto PdfFileWriter
    elif event == "save" and output_pdf:
        # Abrir un diálogo para elegir el nombre y la ubicación del nuevo PDF
        filename = sg.popup_get_file("Guardar como", save_as=True, file_types=(("PDF Files", "*.pdf"),))
        # Si se ha elegido un nombre y una ubicación
        if filename:
            # Asegurarse de que el nombre termina con .pdf
            if not filename.endswith(".pdf"):
                filename += ".pdf"
            # Mostrar el nombre del archivo en la entrada de texto
            window["output"].update(filename)
            # Escribir el nuevo PDF en el disco
            with open(filename, "wb") as f:
                output_pdf.write(f)
# Cerrar la ventana al salir del bucle
window.close()

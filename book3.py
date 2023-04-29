import PySimpleGUI as sg
from PyPDF2 import PageObject
import PyPDF2

def reorder_pdf(input_file):
    pdf_reader = PyPDF2.PdfReader(input_file)
    num_pages = len(pdf_reader.pages)
    pdf_writer = PyPDF2.PdfWriter()


    sequence = [32,1,31,2,30,3,29,4,28,5,27,6,26,7,25,8,24,9,23,10,22,11,21,12,20,13,19,14,18,15,17,16]
    for i in range(0, num_pages, 32):
        for j in range(i, min(i+32, num_pages)):
            page = pdf_reader.pages[sequence[j%32]-1]

            if j%4 == 0:
                new_page = PyPDF2.pdf.PageObject.create_blank_page(None, page.mediaBox.getWidth()/2, page.mediaBox.getHeight()/2)
                new_page = PyPDF2.pdf.Page.create_blank_page(None, page.mediaBox.getWidth()/2, page.mediaBox.getHeight()/2)
                new_page.mergeScaledTranslatedPage(page, 0.5, 0, 0, 0.5, 0, page.mediaBox.getHeight()/2)
                page = new_page
            elif j%4 == 2:
                page.rotateClockwise(180)
            pdf_writer.addPage(page)

    output_file = input_file[:-4] + '_book.pdf'
    with open(output_file, 'wb') as out_file:
        pdf_writer.write(out_file)

sg.theme('DefaultNoMoreNagging')
layout = [[sg.Text('Selecciona el archivo PDF a reordenar:')],
          [sg.Input(key='-INPUT-'), sg.FileBrowse()],
          [sg.Button('Reordenar'), sg.Button('Cancelar')]]

window = sg.Window('Reordenar PDF', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break
    elif event == 'Reordenar':
        input_file = values['-INPUT-']
        reorder_pdf(input_file)
        sg.popup('PDF reordenado correctamente.', title='Reordenar PDF')
        break

window.close()


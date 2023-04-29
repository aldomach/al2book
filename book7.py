import os
import PySimpleGUI as sg
import fitz

def create_book(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count
    new_doc = fitz.open()
    for i in range(0, num_pages, 4):
        for j in range(2):
            for k in range(2):
                if i+j*2+k < num_pages:
                    page = doc[i+j*2+k]
                    new_page = new_doc.new_page()
                    new_page.show_pdf_page(page, matrix=fitz.Matrix(0.5, 0.5), clip=None, rotate=0)
    new_pdf_path = os.path.splitext(pdf_path)[0] + '_book.pdf'
    new_doc.save(new_pdf_path)
    sg.popup(f"El nuevo PDF se ha guardado en:\n{new_pdf_path}")

sg.theme('DefaultNoMoreNagging')

layout = [[sg.Text('Selecciona un archivo PDF:')],
          [sg.Input(key='-PDF-'), sg.FileBrowse()],
          [sg.Button('Crear libro', key='-CREATE-')]]

window = sg.Window('PDF Book Maker', layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    elif event == '-CREATE-':
        pdf_path = values['-PDF-']
        if pdf_path:
            create_book(pdf_path)

window.close()

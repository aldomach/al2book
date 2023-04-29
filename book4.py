import fitz
import os.path 
import PySimpleGUI as sg

def reorder_pdf(input_path, output_path):
    # open PDF file
    with fitz.open(input_path) as doc:
        total_pages = doc.page_count
        pages_per_sheet = 4
        if total_pages % pages_per_sheet != 0:
            # add blank pages if needed to make total_pages a multiple of pages_per_sheet
            blank_pages = pages_per_sheet - total_pages % pages_per_sheet
            for _ in range(blank_pages):
                doc.insert_page(-1)
            total_pages += blank_pages

        # create new PDF with reordered pages
        new_doc = fitz.open()
        for i in range(0, total_pages, pages_per_sheet):
            sheet = fitz.Matrix2d(2, 2).preRotate(0)
            rect = fitz.Rect(0, 0, 297, 210)
            new_page = new_doc.new_page(width=rect.width, height=rect.height)
            new_page.show_pdf_page(
                rect,
                doc,
                i + 31
            )
            new_page.show_pdf_page(
                rect,
                doc,
                i,
                matrix=sheet
            )
            new_page.show_pdf_page(
                rect,
                doc,
                i + 30,
                matrix=sheet
            )
            new_page.show_pdf_page(
                rect,
                doc,
                i + 1,
                matrix=sheet
            )

        # save new PDF
        new_doc.save(output_path)
        new_doc.close()

sg.theme('DarkGrey6')
layout = [[sg.Text('Selecciona un archivo PDF')],
          [sg.Input(key='_FILEBROWSE_', visible=False)],
          [sg.Button('Browse'), sg.Button('Reordenar'), sg.Button('Exit')]]

window = sg.Window('Reordenar PDF', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Browse':
        input_path = sg.popup_get_file('Selecciona un archivo PDF', file_types=(('PDF', '*.pdf'),))
        if input_path:
            window.Element('_FILEBROWSE_').Update(input_path)
    elif event == 'Reordenar':
        input_path = values['_FILEBROWSE_']
        if not input_path:
            sg.popup('Selecciona un archivo PDF primero')
        else:
            output_path = os.path.splitext(input_path)[0] + '_book.pdf'
            reorder_pdf(input_path, output_path)
            sg.popup('Archivo guardado como:\n\n{}'.format(output_path))

window.close()

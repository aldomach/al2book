import PyPDF2
import PySimpleGUI as sg

def merge_pdf(input_path, output_path):
    input_pdf = PyPDF2.PdfReader(open(input_path, "rb"))
    # num_pages = input_pdf.getNumPages()
    num_pages = len(input_pdf.pages)
    output_pdf = PyPDF2.PdfWriter()
    page_numbers = []


    if num_pages > 32:
        for i in range(0, num_pages, 32):
            page_numbers += list(range(i+31, i-1, -1))
    else:
        page_numbers = list(range(num_pages, 0, -1))
    for page_num in page_numbers:
        page = input_pdf.getPage(page_num-1)
        page.scale(0.5)
        if page_num % 4 == 1:
            output_page = PyPDF2.pdf.PageObject.createBlankPage(None, 792, 612)
            output_canvas = PyPDF2.pdf.ContentStream([0, 0, 792, 0, 0, 612], output_pdf)
        page.mergePage(output_page)
        x = 0 if page_num % 2 == 1 else 396
        y = 0 if page_num % 4 in [1, 2] else 306
        output_canvas.addXObject(page.pdfFormXObject, x, y)
        if page_num % 4 == 0:
            output_canvas.close()
            output_pdf.add_page(output_page)
    if page_num % 4 != 0:
        output_canvas.close()
        output_pdf.add_page(output_page)
    output_file = open(output_path, "wb")
    output_pdf.write(output_file)
    output_file.close()

sg.theme('DarkAmber')
layout = [[sg.Text('Seleccione el archivo PDF a procesar')],
          [sg.Input(key='-FILE-', change_submits=True), sg.FileBrowse()],
          [sg.Button('Procesar'), sg.Button('Salir')]]
window = sg.Window('PDF Booklet', layout)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Salir':
        break
    if event == 'Procesar':
        input_path = values['-FILE-']
        output_path = input_path[:-4] + '_book.pdf'
        merge_pdf(input_path, output_path)
        sg.popup('El archivo ha sido procesado y guardado en la misma carpeta con el nombre:\n\n' + output_path)
window.close()

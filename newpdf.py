import os
import PySimpleGUI as sg
from reportlab.pdfgen import canvas

def create_pdf(num_pages):
    filename = 'document.pdf'
    if os.path.exists(filename):
        counter = 1
        while os.path.exists(f"{os.path.splitext(filename)[0]}_{counter:02d}{os.path.splitext(filename)[1]}"):
            counter += 1
        filename = f"{os.path.splitext(filename)[0]}_{counter:02d}{os.path.splitext(filename)[1]}"

    c = canvas.Canvas(filename)
    width, height = c._pagesize

    for i in range(num_pages):
        c.drawString(width/2, height/2, str(num_pages))
        c.rect(0, 0, width, height)
        c.showPage()

    c.save()

sg.theme('DefaultNoMoreNagging')

layout = [[sg.Text('Número de páginas:'), sg.InputText(key='-NUMPAGES-')],
          [sg.Button('Crear')]]

window = sg.Window('Generar PDF', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Crear':
        try:
            num_pages = int(values['-NUMPAGES-'])
            create_pdf(num_pages)
            sg.popup(f"Se ha creado el PDF con {num_pages} páginas.")
        except ValueError:
            sg.popup("Por favor, ingrese un número entero válido.")

window.close()

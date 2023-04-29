import PySimpleGUI as sg
import os
from fpdf import FPDF

# Define la función para generar el PDF
def generate_pdf(filename, num_pages):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(80)
            # self.cell(30, 10, f'Página {str(self.page_no())}', 0, 1, 'C')
            self.ln(20)
    
    pdf = PDF()
    for i in range(num_pages):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 96)
        pdf.cell(0, pdf.h/2, f' {i+1}', 0, 0, 'C')
    pdf.output(filename, 'F')

# Define la ventana
layout = [[sg.Text('Número de páginas:'), sg.Input(key='-NUMPAGES-')],
          [sg.Button('Crear'), sg.Button('Salir')]]

# Crea la ventana
window = sg.Window('Generador de PDFs', layout)

# Loop principal
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Salir':
        break
    elif event == 'Crear':
        num_pages = int(values['-NUMPAGES-'])
        filename = f'pdf_{num_pages}.pdf'
        i = 0
        while os.path.isfile(filename):
            i += 1
            filename = f'pdf_{num_pages}_{i:02d}.pdf'
        generate_pdf(filename, num_pages)
        sg.popup(f'Se ha generado el archivo {filename}')

# Cierra la ventana
window.close()

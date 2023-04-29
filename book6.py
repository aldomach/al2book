# Importar las bibliotecas
import PySimpleGUI as sg
import fitz

# Crear la interfaz gráfica
layout = [
    [sg.Text("Selecciona un PDF para reordenar sus páginas")],
    [sg.Button("Abrir PDF", key="-OPEN-")]
]

window = sg.Window("Reordenador de PDF", layout)

# Crear la secuencia de páginas
sequence = [32, 1, 31, 2, 30, 3, 29, 4, 28, 5, 27, 6, 26, 7, 25, 8,
            24, 9, 23, 10, 22, 11, 21, 12, 20, 13, 19, 14, 18, 15,
            17, 16]

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-OPEN-":
        # Abrir una ventana de selección de archivos
        filename = sg.popup_get_file("Elige un PDF", file_types=(("PDF Files", "*.pdf"),))
        if filename:
            # Abrir el PDF con PyMuPDF
            doc = fitz.open(filename)
            # Ajustar la secuencia al número de páginas del PDF
            sequence = [n for n in sequence if n <= doc.page_count]
            # Seleccionar las páginas según la secuencia
            doc.select(sequence)
            # Guardar el nuevo PDF con el mismo nombre agregando _book al final
            new_filename = filename[:-4] + "_book.pdf"
            doc.save(new_filename)
            # Mostrar un mensaje de confirmación
            sg.popup(f"Se ha guardado el nuevo PDF como {new_filename}")

window.close()

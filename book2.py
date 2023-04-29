import PySimpleGUI as sg
import PyPDF2

# Crear la ventana de la aplicación
sg.theme('DarkBlue')
layout = [[sg.Text('Seleccione el archivo PDF a procesar:')],
          [sg.Input(key='-FILE-', enable_events=True, visible=False), sg.FileBrowse()],
          [sg.Text('Seleccione la ubicación del archivo de salida:')],
          [sg.Input(key='-OUTPUT-', enable_events=True, visible=False), sg.FolderBrowse()],
          [sg.Button('Procesar PDF', disabled=True, key='-PROCESS-')],
          [sg.Output(size=(60,10))]]
window = sg.Window('Procesador de PDF', layout)

# Loop de eventos de la ventana
while True:
    event, values = window.read()
    
    # Si se selecciona un archivo, se habilita el botón de procesamiento
    if event == '-FILE-':
        if values['-FILE-'].endswith('.pdf'):
            window['-PROCESS-'].update(disabled=False)
        else:
            sg.popup('El archivo seleccionado no es un PDF', title='Error')
            window['-PROCESS-'].update(disabled=True)
    
    # Si se selecciona una carpeta de salida, se actualiza el texto de la ruta de salida
    if event == '-OUTPUT-':
        window['-OUTPUT-'].update(values['-OUTPUT-'])
    
    # Si se presiona el botón de procesamiento, se procesa el PDF
    if event == '-PROCESS-':
        # Se abre el archivo PDF y se crea un objeto de escritura para el PDF de salida
        pdf_reader = PyPDF2.PdfFileReader(values['-FILE-'], strict=False)
        pdf_writer = PyPDF2.PdfFileWriter()
        
        # Se establece el orden de las páginas
        num_pages = pdf_reader.getNumPages()
        page_order = [32,1,31,2,30,3,29,4,28,5,27,6,26,7,25,8,24,9,23,10,22,11,21,12,20,13,19,14,18,15,17,16]
        page_order.extend(list(range(33, num_pages+1)))
        
        # Se procesan las páginas del PDF
        for page_num in page_order:
            page = pdf_reader.getPage(page_num - 1)
            page.rotateClockwise(90)
            pdf_writer.addPage(page)
        
        # Se escribe el PDF de salida en el archivo especificado
        output_path = values['-OUTPUT-'] + '/output.pdf'
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
        
        # Se muestra un mensaje de éxito y se limpian los campos
        sg.popup(f'El archivo PDF ha sido procesado exitosamente.\nSe ha guardado en {output_path}.', title='Proceso finalizado')
        window['-FILE-'].update('')
        window['-OUTPUT-'].update('')
        window['-PROCESS-'].update(disabled=True)
    
    # Si se cierra la ventana, se detiene el loop
    if event == sg.WINDOW_CLOSED:
        break

# Se cierra la ventana
window.close()

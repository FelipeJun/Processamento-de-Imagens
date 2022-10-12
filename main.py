from multiprocessing.sharedctypes import Value
from turtle import position
import PySimpleGUI as sg
import os
from func import *
import tempfile


sg.theme("DarkBlue6")

menu_def = [
['Imagem', ['Carregar imagem', 'Carregar URL',
'Salvar', ['Salvar Thumbnail','Salvar com qualidade reduzida',
'Salvar Imagem como',['JPEG', 'PNG','BMP']]]],
['Filtros',['Efeitos', ['Normal','P/B', 'QTD Cor','Sepia','Brilho','Cores','Contraste','Nitidez'],
'Blur',['SBlur','BoxBlur','GaussianBlur'],
'Contour','Detail','Edge Enhance','Emboss','Find Edges','Sharpen','Smooth']],
['Editar Imagem',['Mirror',['FLIP_TOP_BOTTOM','FLIP_LEFT_RIGHT','TRANSPOSE']]],
['Ajuda', ['Sobre a imagem','Mostrar Localização']],
]
tmp_file = tempfile.NamedTemporaryFile(suffix=".png").name

def main():
    layout = [
        [sg.Menu(menu_def)],
        [sg.Text('TEST',text_color='WHITE',key="-TEXTO-")],
        [sg.Graph(key="-IMAGE-", canvas_size=(500,500), graph_bottom_left=(0, 0),
                 graph_top_right=(400, 400), change_submits=True, drag_submits=True)],
        [sg.Slider(range=(0, 5), default_value=2, resolution=0.1, orientation="h", enable_events=True, key="-FATOR-")],
    ]

    window = sg.Window("Visualizador de Imagem",layout = layout)
    dragging = False
    ponto_inicial = ponto_final = retangulo = None
    filename = None
    actualeffect =''
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
        try:
            # Abrir a imagem
            if event in ["Carregar imagem","Carregar URL"]:
                filename = open_image(tmp_file,event,window)


            if event == "Salvar Thumbnail":
                save_thumbnail(tmp_file,"Thumbnail.png","png",75,75,75)
            if event == "Salvar com qualidade reduzida":
                save_redux(tmp_file,"Redux.png")

            # TEM Q ARRUMAR AQ AINDA A PARTE DE SALVAR
            if event in ["JPEG","PNG","BMP"]:
                image_converter(tmp_file,'saved',event)
    
            # infos da imagem
            if event == "Sobre a imagem":
                openInfoWindow(filename,window)
            if event == "Mostrar Localização":
                GPSLocation(filename)


            # Eventos para edição da imagem
            if event in ["P/B","QTD Cor","Sepia",
            'Brilho','Cores','Contraste','Nitidez']:
                window.Element('-TEXTO-').update(event)
                actualeffect = event
                

            if event in ['SBlur','BoxBlur','GaussianBlur','Contour','Detail',
            'Edge Enhance','Emboss','Find Edges','Sharpen','Smooth',
            'TRANSPOSE','FLIP_TOP_BOTTOM','FLIP_LEFT_RIGHT']:
                filter(tmp_file,event,window)

            if event == "-FATOR-":
               applyEffect(filename,tmp_file,actualeffect,values,window)
            
            if event == "-IMAGE-":
                x, y = values["-IMAGE-"]
                if not dragging:
                    ponto_inicial = (x, y)
                    dragging = True
                else:
                    ponto_final = (x, y)
                if retangulo:
                    window["-IMAGE-"].delete_figure(retangulo)
                if None not in (ponto_inicial, ponto_final):
                    retangulo = window["-IMAGE-"].draw_rectangle(ponto_inicial, ponto_final, line_color='red')
            elif event.endswith('+UP'):
                dragging = False
            

    
        except Exception as e:
            sg.popup_error(e)

    window.close()
    os.remove('temp.png')


if __name__ == "__main__":
    main()




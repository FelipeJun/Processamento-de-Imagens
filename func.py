import io
import os
import PySimpleGUI as sg
from PIL import Image
import requests
from PIL import ImageFilter
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
import webbrowser
from PIL import ImageEnhance

flips = {
'FLIP_TOP_BOTTOM': Image.FLIP_TOP_BOTTOM,
'FLIP_LEFT_RIGHT': Image.FLIP_LEFT_RIGHT,
'TRANSPOSE': Image.TRANSPOSE
}

filtros = {
    'SBlur': ImageFilter.BLUR,
    'BoxBlur': ImageFilter.BoxBlur(radius=9),
    'GaussianBlur': ImageFilter.GaussianBlur,
    'Contour': ImageFilter.CONTOUR,
    'Detail': ImageFilter.DETAIL,
    'Edge Enhance': ImageFilter.EDGE_ENHANCE,
    'Emboss': ImageFilter.EMBOSS,
    'Find Edges': ImageFilter.FIND_EDGES,
    'Sharpen': ImageFilter.SHARPEN,
    'Smooth': ImageFilter.SMOOTH
}

fields = {
"File name" : "File name",
"File size" : "File size",
"Model" : "Camera Model",
"ExifImageWidth" : "Width",
"ExifImageHeight" : "Height",
"DateTime" : "Creating Date",
"static_line" : "*",
"MaxApertureValue" : "Aperture",
"ExposureTime" : "Exposure",
"FNumber" : "F-Stop",
"Flash" : "Flash",
"FocalLength" : "Focal Length",
"ISOSpeedRatings" : "ISO",
"ShutterSpeedValue" : "Shutter Speed",
}



def abre_url(window):
    url = sg.popup_get_text("Coloque a URL")
    imagem = requests.get(url)
    imagem = Image.open(io.BytesIO(imagem.content))
    mostrar_imagem(imagem, window) 
    return imagem
def salvar_url(url):
    imagem = requests.get(url)
    imagem = Image.open(io.BytesIO(imagem.content))
    imagem.save("daweb.png", format="PNG", optimize=True)

def mostrar_imagem(imagem, window):
    imagem.thumbnail((500,500))
    bio = io.BytesIO()
    imagem.save(bio, "PNG")
    window["-IMAGE-"].erase()
    window["-IMAGE-"].draw_image(data=bio.getvalue(), location=(0,400))

def carrega_imagem(window,temp_file):
    filename = sg.popup_get_file('Get File')
    if os.path.exists(filename):
        imagem = Image.open(filename)
        imagem.save(temp_file)
        mostrar_imagem(imagem, window)
    return filename
    
def GPSLocation(filename):
    image_path = Path(filename)
    exif_data = get_exif_data(image_path.absolute())
    north = exif_data["GPSInfo"]["GPSLatitude"]
    east = exif_data["GPSInfo"]["GPSLongitude"]
    latitude = round(float(((north[0] * 60 + north[1]) * 60 + north[2]) / 3600),7)
    longitude = round(float(((east[0] * 60 + east[1]) * 60 + east[2]) / 3600),7)
    url = f'https://www.google.com.br/maps/@{latitude},-{longitude},15z'
    webbrowser.open(url)


def openInfoWindow(filename, window):
    layout = []
    image_path = Path(filename)
    exif_data = get_exif_data(image_path.absolute())
    for field in fields:
        if field == "File name":
            layout.append([sg.Text(fields[field], size=(10,1)),sg.Text(image_path.name,size = (25,1))]) 
        elif field == "File size":
            layout.append([sg.Text(fields[field], size=(10,1)),sg.Text(image_path.stat().st_size,size = (25,1))]) 
        else:
            layout.append([sg.Text(fields[field], size=(10,1)),sg.Text(exif_data.get(field, "No data"),size = (25,1))]) 

    window = sg.Window("Second Window", layout, modal=True)
    while True:
        event,values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
            
        
    window.close()


def get_exif_data(path):
    exif_data = {}
    try:
        image = Image.open(path)
        info = image._getexif()
    except OSError:
        info = {}

    #Se não encontrar o arquivo
    if info is None:
        info = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_data = {}
            for gps_tag in value:
                sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                gps_data[sub_decoded] = value[gps_tag]
            exif_data[decoded] = gps_data
        else:
            exif_data[decoded] = value

    return exif_data



def save_thumbnail(input_file,output_file,format,qualit,width, height):
    imagem = Image.open(input_file)
    imagem.save(output_file, format=format, optmize = True, quality = qualit)
    imagem.thumbnail((width,height))
    imagem.save(output_file)

def save_redux(input_file,output_file):
    imagem = Image.open(input_file)
    imagem.save(output_file,format = "JPEG",optmize = True,quality=1)

def image_converter(input_file,output_file,format):
    imagem = Image.open(input_file)
    imagem.save(output_file, format = format,optmize =True)

def crop_image(input_image, coords, window):
    if os.path.exists(input_image):
        image = Image.open(input_image)
        cropped_image = image.crop(coords)
        mostrar_imagem(cropped_image, window)

def resize(input_image, coords, window):
    if os.path.exists(input_image):
        image = Image.open(input_image)
        resized_image = image.crop(coords)
        mostrar_imagem(resized_image, window)




def applyEffect(tmp_file,event,window):

    Effects[event](tmp_file)

    imagem = Image.open(tmp_file)
    imagem.thumbnail((500,500))
    bio = io.BytesIO()
    imagem.save(bio, "png")
    window["-IMAGE-"].erase()
    window["-IMAGE-"].draw_image(data=bio.getvalue(), location=(0,400))



def filter(tmp_file,filter,window):
    image = Image.open(tmp_file)
    if filter in ["TRANSPOSE","FLIP_TOP_BOTTOM","FLIP_LEFT_RIGHT"]:
        image = image.transpose(flips[filter])
    else:
        image = image.filter(filtros[filter])
        
    image.save(tmp_file)
    image.thumbnail((500,500))
    bio = io.BytesIO()
    image.save(bio, "png")
    window["-IMAGE-"].erase()
    window["-IMAGE-"].draw_image(data=bio.getvalue(), location=(0,400))

def convertToPb(filename):
    image = Image.open(filename)
    image = image.convert("L")
    image.save(filename)

def convertToQtdColor(filename):
    if os.path.exists(filename):
        qtdCores = sg.popup_get_text("Digite a quantidade de cores")
        image = Image.open(filename)
        image = image.convert("P", palette=Image.Palette.ADAPTIVE,colors = int(qtdCores))
        image.save(filename)

def calcula_paleta(cor):
    paleta = []
    r,g,b = cor
    for i in range(255):
        new_red = r * i // 255
        new_green = g * i // 255
        new_blue = b * i // 255
        paleta.extend((new_red,new_green,new_blue))
    return paleta

def convertTosepia(filename):
    if os.path.exists(filename):
        branco = (255,240,192)
        paleta = calcula_paleta(branco)
        image = Image.open(filename)
        image = image.convert("L")
        image.putpalette(paleta)
        sepia = image.convert("RGB")
        image.save(filename)

def brilho(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Brightness(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def contraste(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Contrast(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def cores(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Color(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def nitidez(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Sharpness(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)


Effects = {
"P/B" : convertToPb,
"QTD Cor" : convertToQtdColor,
"Sepia": convertTosepia,
}
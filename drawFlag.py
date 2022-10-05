from PIL import Image,ImageDraw

# Bandeira do Japão
image = Image.new('RGBA', (300, 200),'White')
draw = ImageDraw.Draw(image)
draw.ellipse((100, 50, 200, 150), fill = 'red', outline ='red')
draw.point((150, 100), 'red')
image.save('japan.png')

# # Bandeira antiga de Portugal
image = Image.new('RGBA', (300, 200),'White')
draw = ImageDraw.Draw(image)
draw.rectangle((0, 80, 300, 120), fill="blue")
draw.rectangle((130,0, 170, 300), fill="blue")
image.save('Portugal.png')

#Bandeira do Mato Grosso
image = Image.new('RGBA', (300, 200),'blue')
draw = ImageDraw.Draw(image)
draw.polygon(((20, 100), (150, 20), (280, 100),(150,180)), fill="white")
draw.ellipse((100, 50, 200, 150), fill = 'green')

draw.polygon(((150, 50),(160,85),
              (198,85),(165,105),
              (180,140),(150,120),
              (120,140),(135,105),
              (102,85),(140,85)),
              fill="yellow")

image.save('MatoGrosso.png')

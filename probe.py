from PIL import Image, ImageOps

# creating an image object 
img = Image.open("cats.png").convert("L")

# image colorize function 
img1 = ImageOps.colorize(img, black="blue", white="white")
img1.show() 
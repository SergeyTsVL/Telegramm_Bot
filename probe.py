from PIL import Image

img = Image.open("cats.jpg")
img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
img.save("cats_new.jpg")
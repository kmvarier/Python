#To draw fibonacci squares and spiral
#Program written by Prof K. M. Varier
from PIL import Image, ImageFont, ImageDraw, ImageFile
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from sys import argv

def readFile (fileName):
    fileObj = open (fileName, "r")
    lines = fileObj.read ().splitlines ()
    fileObj.close ()
    return lines

def readPrimes (filename) :
    lines = readFile (filename)
    primes = []
    for line in lines :
        columns = line.split ()
        primes.append (columns [1])
    return primes
    
def readFibonacci (filename) :
    lines = readFile (filename)
    data = []
    for line in lines :
        columns = line.split ()
        data.append (columns [3])
    return data
    
    
def main () :   
    x1 = [0, 0,   0,  -2, -2,  1,   -2, -15, -15]
    y1 = [0, -1, -2, -2,  0, -2, -10, -10, 3]
    x2 = [0, 1, 1, 1, 1, 6, 6, -2, 6]
    y2 = [0, 0, -1, 0, 3, 3, -2, 3, 24]
    quad_no = [0, 3, 0, 1, 2, 3, 0, 1, 2]
    bbox = [(0, 0, 0, 0), (-1, -2, 1, 0), (-1, -2, 1, 0), (-2, -2, 2, 2), (-2, -3, 4, 3), (-2, -5, 6, 3), (-10, -10, 6, 6), (-15, -10, 11, 16), (-15, -18, 27, 24)]
    x0 = 920
    y0 = 350
    W = 1920
    H = 1080
    factor = 25
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    dataType = int (argv [1])
    if dataType == 0 :
        #Primes
        data = readPrimes ("data.dat")
        of = "PrimeSpiral.mp4"
        text0 = "Prime Spiral"
    else :
        #Fibonaacci numbers
        data = readFibonacci ("data.dat")
        of = "FibSpiral.mp4"
        text0 = "Fibonacci Spiral"
    frames = []
    bg0 = Image.open ('bgGreenBorder.png')
    fig = plt.figure ()
    fig.set_size_inches (19.2, 10.8)
    plt.axis ("off")
    bgi = bg0.copy ()
    f0 = ImageFont.truetype ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 60)
    f = ImageFont.truetype ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 30)
    for i in range (1, 9) :
        side = int (data [i]) *factor
        w = side
        xi1 = x0 + x1 [i] * factor
        yi1 = y0 + y1 [i] * factor
        xi2 = x0 + x2 [i] * factor
        yi2 = y0 + y2 [i] * factor
        img = bgi.copy ()
        draw = ImageDraw.Draw (img)
        draw.rectangle ((xi1, yi1, xi2, yi2), fill=None, outline=(255, 0, 0), width = 2)
        text = str (data [i])
        xt = int ((xi1+ xi2)/2) - 10
        yt = int ((yi1+ yi2)/2) - 20
        draw.text ((xt, yt), text, (0, 0, 0), font = f)
        draw.text ((1300, 100), text0, (255, 0, 0), font = f0)
        imgplot = plt.imshow (img, origin='upper')             
        frames.append ([imgplot])
        bgi = img.copy ()
    for i in range (1, 9) :
        if quad_no [i] == 0 :
            angle1 = 270
            angle2 = 360
        elif quad_no [i] == 1 :
            angle1 = 180
            angle2 = 270
        elif quad_no [i] == 2 :
            angle1 = 90
            angle2 = 180
        elif quad_no [i] == 3 :
            angle1 = 0
            angle2 = 90
        xi1, yi1, xi2, yi2 = bbox [i]
        xi1 *= factor
        yi1 *= factor
        xi2 *= factor
        yi2 *= factor
        xi1 += x0
        yi1 += y0
        xi2 += x0
        yi2 += y0        
        draw.arc ((xi1, yi1, xi2, yi2), start = angle1, end = angle2, fill ="blue", width = 2)
        imgplot = plt.imshow (img, origin='upper')             
        frames.append ([imgplot])
        bgi = img.copy ()
    plt.show ()
    ani = animation.ArtistAnimation (fig, frames, interval=5,    blit=True, repeat_delay=100000)
    ani.save (of, fps = 5)
    print ("Output video saved as ", of)
        
    
if __name__ == '__main__':
    main ()

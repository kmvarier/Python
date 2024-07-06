#To animate the spinning Top
from PIL import Image, ImageDraw
from matplotlib import animation
from math import pi, cos, sin, sqrt, fabs, asin, acos
import numpy as np
from random import random, randint
import cv2
from sys import argv, exit

global j
def ColorDistance (rgb1,rgb2):
    '''d = {} distance between two colors(3)'''
    rm = 0.5* (rgb1[0]+rgb2[0])
    d = sum ((2+rm,4,3-rm)*(rgb1-rgb2)**2)**0.5
    return d

def random_color ():
    r = randint (0, 255)
    g = randint (0, 255)
    b = randint (0, 255)
    return (r, g, b)

def image_split (img, m, n) :
    w, h = img.size
    xw = int (w / m)
    yh = int (h / n)
    out_img = []
    for i in range (0, m) :
        x0 = i * xw
        for j in range (0, n) :
            y0 = j * xw
            box = (x0, y0, x0 + xw, y0 + yh)
            im = img.crop (box)
            out_img.append (im)
    return out_img
 
def generate_transparent_frame (img, c1, c2) :
    draw = ImageDraw.Draw (img)
    shape = [(0,  0), (1920, 24)]
    draw.rectangle(shape, fill =c1)
    shape = [(0,  24), (24, 1080)]
    draw.rectangle(shape, fill =c1)
    shape = [(25,  1055), (1920, 1080)]
    draw.rectangle(shape, fill =c1)
    shape = [(1894,  25), (1920, 1080)]
    draw.rectangle(shape, fill =c1)
    shape = [(25,  25), (1894, 49)]
    draw.rectangle(shape, fill =c2)
    shape = [(25,  49), (49, 1055)]
    draw.rectangle(shape, fill =c2)
    shape = [(25,  1030), (1894, 1055)]
    draw.rectangle(shape, fill =c2)
    shape = [(1870,  25), (1894, 1055)]
    draw.rectangle(shape, fill =c2)
    return (img)

def get_ellipse (cx, cy, a, b, t) :
    global j
    x = []
    y = []
    ax = cx - a
    ac = ax - cx
    ay = (cy + b * sqrt (1.0 - ac * ac / a / a))
    ct = cos (t)
    st = sin (t)
    x1 = int (ax * ct + ay * st)
    y1 = int (-ax * st + ay * ct)
    x.append (x1)
    y.append (y1)
    j = 0
    while ac < a :
        j += 1
        ax += 5
        ac = ax - cx
        if  ( fabs (ac) > a) :
            break
        ay = (cy + b * sqrt (1.0 - ac * ac / a / a))
        x1 = int (ax * ct + ay * st)
        y1 = int (-ax * st + ay * ct)
        x.append (x1)
        y.append (y1)
    ax -= 5
    ac = ax - cx
    while ac < a :
        j += 1
        ac = ax - cx
        if  ( fabs (ac) > a) :
            break
        ay = (cy - b * sqrt (1.0 - ac * ac / a / a))
        x1 = int (ax * ct + ay * st)
        y1 = int (-ax * st + ay * ct)
        x.append (x1)
        y.append (y1) 
        ax -= 5  
    return x, y
    
images_folder = 'images/'

c1 = (r1, g1, b1) = random_color ()
c2 = (r2, g2, b2) = random_color ()
color1 = np.array ([r1, g1, b1])
color2 = np.array ([r2, g2, b2])
img = Image.new ('RGB', (1920, 1080))
bg = generate_transparent_frame (img, c1, c2)
W = bg.width
H = bg.height
W2 = int (W/2)
H2 = int (H/2)
n = randint (0, 16)
top_file = images_folder + "top1.png"
top = Image.open (top_file)
w = top.width
h = top.height
w2 = int (w / 2)
h2 = int (h / 2)
centre = (int (w/2), h)
padx = 48
pady = 27
table0 = Image.open (images_folder + "tabletop.png")
ws = table0.width
hs = table0.height
table = table0.resize ((ws - 2 * padx, hs - 2 * pady), 0)
out = bg.copy ()
tops = []
tops.append (images_folder + "top0.png")
tops.append (images_folder + "top1.png")
tops.append (images_folder + "top2.png")
tops.append (images_folder + "top3.png")
tops.append (images_folder + "top4.png")

slides = []
angle0 = 25.0
xpad = int ((W - w) / 2)
ypad = int ((H - h) / 2)
xtip = W2
ytip = ypad + h
a = h * sin (angle0 * pi / 180.0)
b = a / 3
print ("a = ", a, "b = ", b)
x0 = W2
y0 = ypad + b + 15
xe, ye = get_ellipse (x0, y0, a, b, 0)
npts = len (xe)
npts2 = int (npts / 2) + 1
i1 = 0
i2 = 3 * npts
outf = "top.avi"
xtopbox = W2 - w2
ytopbox = ypad
out = bg.copy ()
angle_old = angle0
img = out.paste (table, (padx, pady), mask = table)
img = out.paste (top, (xtopbox, ytopbox), mask = top)
j = -1
i3 = int (npts / 2)
for i in range (i1, i2) :
    out = bg.copy ()
    j += 1
    k = i % 4
    img = out.paste (table, (padx, pady), mask = table)
    n = j % npts
    x = xe [n]
    y = ye [n]
    length = sqrt ((x - xtip) * (x - xtip) + (y - ytip) * (y - ytip))
    angle = asin ((x - xtip) /  length) * 180.0 / pi
    diff = angle_old - angle
    top = Image.open (tops [k])
    topz = top.resize ((w, int (length)), 0)
    wz, hz = topz.size
    topr = topz.rotate (angle, resample=Image.BICUBIC, expand=True, center=centre) 
    wr, hr = topr.size
    wr2 = int (wr / 2)
    hr2 = int (hr /2)
    wz2 = int (wz / 2)
    hz2 = int (hz /2)
    
    xtopbox = W2 - wr2
    ytopbox = ypad + (h2 - hr2)
    
    print ("Length :%5.2f"%length, "angle :%5.2f"%angle, "wr :%6.2f"%wr, "hr :%5.2f"%hr, "xt :%5.2f"%xtopbox, "xt :%5.2f"%ytopbox)
    
    if (n >= i3) :
        xtopbox = W2 - wr2
        ytopbox = ypad + (h2 - hr2)
        img = out.paste (topr, (xtopbox, ytopbox), mask = topr)
        print ("i < i3")
    
    else :
        print (i)
        #n = npts - i - 1
        print ("i > i3")
        y = ye [n]
        xtopbox = W2 - wr2
        ytopbox = ypad + (h2 - hr2 ) + int (y - y0)
        img = out.paste (topr, (xtopbox, ytopbox), mask = topr)

    for l in range (0, npts) :
        out.putpixel ((xe [l], ye [l]), (255, 0, 0))
        out.putpixel ((xe [l] - 1, ye [l]), (255, 0, 0))
        out.putpixel ((xe [l] - 1, ye [l] - 1), (255, 0, 0))
        out.putpixel ((xe [l], ye [l] - 1), (255, 0, 0))
    slides.append (out)
    angle_old = angle
    
    of = "dummy/"+ "%03d"%i + ".png"
    topr.save (of)
print ("No of points = ", j)

print ("Making the video... ", outf)
video = cv2.VideoWriter(outf, cv2.VideoWriter_fourcc(*'XVID'), 30, (1920,1080))
for slide in slides :
    nparr = np.array (slide)
    cvimg = cv2.cvtColor (nparr, cv2.COLOR_RGB2BGR)
    video.write (cvimg)	
exit ()

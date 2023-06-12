import turtle
import numpy as np
import pandas as pd
import colorsys

def point_track(obj, t):
    
    inipos = t.pos()
    
    color0 = t.pencolor()
    size0 = t.pensize()
    
    points = obj.points
    scalepx = obj.scalepx
    scalepy = obj.scalepy
    fcolor = obj.fcolor
    fline = obj.fline
    drawornot = obj.drawornot
    
    fmod = obj.fmod
    argsf = obj.argsf
    
    if drawornot == None:
        drawornot = [False] * len(points[:,0])
    
    objdp = obj.objdp
    penup = obj.penup
    objd = obj.objd
    
    tol = 1e-6
        
    if objdp == 0.:
        objdp = tol
    elif objdp == 1.:
        objdp = 1. - tol
    
    
    ############################
    ## Scale
    ############################

    if scalepx != None:
        xmin = np.min(points[:,0])
        xmax = np.max(points[:,0])
        points[:,0] = (points[:,0] - xmin) / (xmax - xmin) * scalepx
    if scalepy != None:
        ymin = np.min(points[:,1])         
        ymax = np.max(points[:,1])
        points[:,1] = (points[:,1] - ymin) / (ymax - ymin) * scalepy  
        
    ############################
    ## Turtle
    ############################    
  
    dv = np.zeros(len(points[:,0]))
    dx = np.zeros(len(points[:,0]))
    dy = np.zeros(len(points[:,0]))
    le = [True] * len(points[:,0])
    up = [True] * len(points[:,0])
    an = np.zeros(len(points[:,0]))    
    
    for i in range(len(dv)):
        if i == 0:
            dx[i] = points[i,0]
            dy[i] = points[i,1]
        else:
            dx[i] = points[i,0] - points[i - 1,0]
            dy[i] = points[i,1] - points[i - 1,1]
        dv[i] = np.sqrt(dx[i]**2 + dy[i]**2)

        if dx[i] < 0 and dy[i] > 0:
            le[i] = True
            up[i] = True
            an[i] = np.arctan(dx[i] / dy[i]) * 180. / np.pi
        elif dx[i] > 0 and dy[i] > 0: 
            le[i] = False
            up[i] = True 
            an[i] = np.arctan(dx[i] / dy[i]) * 180. / np.pi
        elif dx[i] > 0 and dy[i] < 0:
            le[i] = True
            up[i] = False
            an[i] = np.arctan(dx[i] / dy[i]) * 180. / np.pi
        elif dx[i] < 0 and dy[i] < 0:
            le[i] = False
            up[i] = False
            an[i] = np.arctan(dx[i] / dy[i]) * 180. / np.pi
        elif dy[i] == 0 and dx[i] < 0:
            le[i] = False
            up[i] = 0
            an[i] = 90
        elif dy[i] == 0 and dx[i] > 0:
            le[i] = True
            up[i] = 0
            an[i] = 90   
        elif dy[i] == 0 and dx[i] == 0:
            le[i] = 0
            up[i] = True
            an[i] = 0
            dv[i] = 0
        else:
            le[i] = False
            up[i] = True 
            an[i] = np.arctan(dx[i] / dy[i]) * 180. / np.pi     
            
    if obj.center:
        xmin = np.min(points[:,0])
        xmax = np.max(points[:,0])
        t.penup()
        t.left(90)
        t.forward(np.abs(xmax - xmin) * 0.5)
        t.right(90)
        #t.pendown()

        ymin = np.min(points[:,1])
        ymax = np.max(points[:,1])
        t.penup()
        t.left(180)
        t.forward(np.abs(ymax - ymin) * 0.5)
        t.right(180)
    else:
        xmin = np.min(points[:,0])
        xmax = np.max(points[:,0])
        t.penup()
        t.left(90)
        t.forward(np.abs(xmax - xmin) * 0.5)
        t.right(90)        
        
            
    for i in range(len(points[:,0])):
        
        if fmod != None:
            fmod(t, i, obj, objd, argsf)
        
        if i >= 1:
            t.pendown()
        
        if fcolor != None:
            color = fcolor(i, obj)
            t.pencolor(color)   
        else:
            t.pencolor(obj.linecolor)   
            
        if fline != None:
            pens = fline(i, obj)     
            t.pensize(pens)
        else:
            t.pensize(obj.linewidth)

        ###########################
        if up[i] == False:
            t.left(180)

        if le[i] == True:
            t.left(np.abs(an[i]))    
        else:
            t.right(np.abs(an[i]))

        ###########################
        #t.forward(dv[i])

        if penup:
            t.penup()
            ########################
            t.forward(dv[i] * objdp)
            ########################
            
            if drawornot[i]:
                if objd != None:
                    for ob in objd:
                        ob.draw()
            
            t.penup()
            ########################
            t.forward(dv[i] * (1. - objdp))
            ########################
            t.pendown()     
            #t.write(str(i), font=("Verdana", 5, "normal"))
        
        
        else:
            ########################
            t.forward(dv[i] * objdp)
            ########################
            
            if drawornot[i]:
                if objd != None:
                    for ob in objd:
                        ob.draw()
                    
            ########################    
            t.forward(dv[i] * (1. - objdp))  
            ########################    
            #t.write(str(i), font=("Verdana", 5, "normal"))

        ###########################        
        if le[i] == True:
            t.right(np.abs(an[i]))    
        else:
            t.left(np.abs(an[i]))    

        if up[i] == False:
            t.right(180)            
            
    t.pencolor(color0)
    t.pensize(size0)
    t.penup()
    t.goto(inipos)
    t.pendown()
    return




def deltoid(obj, t, begin_end = None):
    # valores iniciales
 
    if begin_end != None:
        begin_end(obj, t, True)
    
    color0 = t.pencolor()
    size0 = t.pensize()
    t.pencolor(obj.linecolor)
    t.pensize(obj.linewidth)
    
    if obj.colorRelleno != None:
        t.fillcolor(obj.colorRelleno)
        t.begin_fill()   
        
    l = obj.l
    c = obj.c
    f = obj.f
        
    d1 = np.sqrt((l * f)**2 + (c * 0.5)**2)
    d2 = np.sqrt((l * (1. - f))**2 + (c * 0.5)**2)

    alpha = np.arctan(c * 0.5 / (l * f)) * 180. / np.pi
    beta = np.arctan(l * (1. - f) / (c * 0.5)) * 180. / np.pi        
    
    if obj.center:
        t.penup()
        t.backward(l * 0.5)
        t.pendown()
    
    t.left(alpha)
    t.forward(d1)
    t.right(90. - beta + alpha)
    t.forward(d2)
    t.right(beta * 2)
    t.forward(d2)
    t.right(90 - beta + alpha)
    t.forward(d1)
    t.right(180 - alpha)        
        
    if obj.colorRelleno != None:
        t.end_fill()
        
    if obj.center:
        t.penup()
        t.forward(l * 0.5)
        t.pendown()
    
    # volver a los valores iniciales
    t.pencolor(color0)
    t.pensize(size0)
    
    if begin_end != None:
        begin_end(obj, t, False)
    return

    
def circulo(obj, t, begin_end = None):

    if begin_end != None:
        begin_end(obj, t, True)
        
    # color y tamaño de linea    
    # valores iniciales
    color0 = t.pencolor()
    size0 = t.pensize()

    t.pencolor(obj.linecolor)
    t.pensize(obj.linewidth)

    t.rt(90)
    t.fd(obj.radio)
    t.left(90)
    t.pendown()  

    if obj.colorRelleno != None:
        t.fillcolor(obj.colorRelleno)
        t.begin_fill()   

    t.circle(obj.radio, steps = obj.steps)
    t.penup()    
    t.left(90)
    t.fd(obj.radio)
    t.right(90)

    if obj.colorRelleno != None:
        t.end_fill()
    t.pendown()

    # volver a los valores iniciales
    t.pencolor(color0)
    t.pensize(size0)
    
    if begin_end != None:
        begin_end(obj, t, False)
    return


def circulo2(obj, t, begin_end = None):
    
    if begin_end != None:
        begin_end(obj, t, True)
        
    # color y tamaño de linea
    # valores iniciales
    color0 = t.pencolor()
    size0 = t.pensize()

    t.pencolor(obj.linecolor)
    t.pensize(obj.linewidth)
    
    angini = 360. / float(obj.steps)

    t.penup()
    t.rt(90)
    
    fact = 1.
    if obj.vertex == False:
        t.rt(angini * 0.5)
        fact = np.cos(angini * 0.5 * np.pi / 180.)
    
    t.fd(obj.radio * fact)
    t.left(90)
    t.pendown()  

    if obj.colorRelleno != None:
        t.fillcolor(obj.colorRelleno)
        t.begin_fill()   

    t.circle(obj.radio * fact, steps = obj.steps)
    t.penup()    
    t.left(90)
    t.fd(obj.radio * fact)
    t.right(90)
    
    if obj.vertex == False:
        t.left(angini * 0.5)

    if obj.colorRelleno != None:
        t.end_fill()
    t.pendown()

    # volver a los valores iniciales
    t.pencolor(color0)
    t.pensize(size0)
    
    if begin_end != None:
        begin_end(obj, t, False)
    return
    
    
def polarArray(obj, t, begin_end = None):
    
    if begin_end != None:
        begin_end(obj, t, True)    
    
    # valores iniciales
    color0 = t.pencolor()
    size0 = t.pensize()
    t.penup()

    if obj.nrad == 1:
        obj.radio0 = obj.radio

    if obj.l0r1 == 0:
        t.left(obj.ang0)
    else:
        t.right(obj.ang0)    

    if obj.ang == 360:
        dangle = obj.ang / obj.nang
    else:
        dangle = obj.ang / (obj.nang - 1)

    drad = (obj.radio - obj.radio0) / obj.nrad

    for i in range(obj.nang):

        t.forward(obj.radio0)
        for j in range(obj.nrad):
            t.pendown()
            
            #if obj.objd != None:
            #    for ob in obj.objd:
            #        ob.draw()
            if obj.objd != None:
                if obj.fmod != None:
                    obj.fmod(obj, i, j)
                for ob in obj.objd:
                    ob.draw()            
  
            else:
                t.dot(10)
            t.penup()
            t.forward(drad)
        t.backward(obj.radio)

        if obj.l0r1 == 0:
            t.left(dangle)
        else:
            t.right(dangle) 

    if obj.ang == 360:
        if obj.l0r1 == 0:
            t.right(obj.ang0 + obj.ang)
        else:
            t.left(obj.ang0 + obj.ang)  
    else:
        if obj.l0r1 == 0:
            t.right(obj.ang0 + obj.ang + dangle)
        else:
            t.left(obj.ang0 + obj.ang + dangle)  

    # volver a los valores iniciales
    t.pencolor(color0)
    t.pensize(size0)
    t.pendown()
    
    if begin_end != None:
        begin_end(obj, t, False)
        
    return 


def poligon(obj, t, begin_end = None):
    
    if begin_end != None:
        begin_end(obj, t, True)
        
    angi = (obj.n - 2) * 180 / obj.n
    ange = 180 - angi

    # valores iniciales
    color0 = t.pencolor()
    size0 = t.pensize()

    t.color(obj.linecolor)
    t.pensize(obj.linewidth)

    if obj.colorRelleno != None:
        t.fillcolor(obj.colorRelleno)
        t.begin_fill()   

    if obj.vertex:
        # inicio de polígono
        t.left(angi / 2)
        for i in range(obj.n):
            t.forward(obj.lado)
            t.right(ange)

        t.right(angi / 2)   
    else: 
        # inicio de polígono
        t.left(90)
        t.forward(obj.lado / 2)

        for i in range(obj.n - 1):
            t.right(ange)
            t.forward(obj.lado)

        t.right(ange)
        t.forward(obj.lado / 2)
        t.right(90)

    if obj.colorRelleno != None:
        t.end_fill()

    # volver a los valores iniciales
    t.pencolor(color0)
    t.pensize(size0)    
    
    if begin_end != None:
        begin_end(obj, t, False)
        
    return 




def xyarray(obj, t):

    dx = obj.lx / (obj.nx - 1)
    dy = obj.ly / (obj.ny - 1)

    t.penup()
    if obj.center:
        t.backward(obj.ly / 2)
        t.right(90)
        t.backward(obj.lx / 2)
        t.left(90)
    else:
        t.left(90)
        t.forward(obj.lx / 2)
        t.right(90)

    for i in range(obj.nx):
        t.pendown()
        if obj.objd != None:
            for ob in obj.objd:
                ob.draw()
            #obj.objd.draw()
        else:
            t.dot(10)        
        t.penup()
        for j in range(obj.ny - 1):
            t.forward(dy)
            t.pendown()
            if obj.objd != None:
                for ob in obj.objd:
                    ob.draw()
                #obj.objd.draw()
            else:
                t.dot(10)
            t.penup()
        if i == obj.nx - 1: break 
        t.backward(obj.ly)
        t.right(90)
        t.forward(dx)
        t.left(90)

    if obj.center:
        t.backward(obj.ly / 2)
        t.right(90)
        t.backward(obj.lx / 2)
        t.left(90)
    else:
        t.backward(obj.ly)
        t.right(90)
        t.backward(obj.lx / 2)
        t.left(90)
    t.pendown()
    return 


def linearray(obj, t, begin_end = None):
    
    if begin_end != None:
        begin_end(obj, t, True)
        
    # valores iniciales
    color0 = t.pencolor()
    size0 = t.pensize()

    t.pensize(obj.linewidth)
    t.color(obj.linecolor)
    if obj.l0r1 == 0:
        t.left(obj.startangle)
    else:
        t.right(obj.startangle)

    if obj.totalangle == 360:
        dangle = obj.totalangle / obj.nlines
    else:
        dangle = obj.totalangle / (obj.nlines - 1)

    for i in range(obj.nlines):
        t.forward(obj.lline)

        t.backward(obj.lline)
        if obj.l0r1 == 0:
            t.left(dangle)
        else:
            t.right(dangle)   

    if obj.totalangle == 360:
        if obj.l0r1 == 0:
            t.right(obj.startangle + obj.totalangle)
        else:
            t.left(obj.startangle + obj.totalangle)  
    else:
        if obj.l0r1 == 0:
            t.right(obj.startangle + obj.totalangle + dangle)
        else:
            t.left(obj.startangle + obj.totalangle + dangle)  
    # volver a los valores iniciales
    t.pencolor(color0)
    t.pensize(size0)
    
    if begin_end != None:
        begin_end(obj, t, False)
    return 


def fractaltree(obj, t):     #, objd = None, objdp = 0.5, fmod = None):
    fractalTree2(t, obj, obj.niter, obj.nact)
    return


def fractalTree2(t, obj, niter, nact):
    if (niter < 1):
        return
    else:
        for i in range(obj.nact):
            obj.turtleActions(t, obj, niter, i, True)
            fractalTree2(t, obj, niter - 1, nact)
            obj.turtleActions(t, obj, niter, i, False)
    return 


def turtleAct(t, obj, niter, nact, goback):
    
    niter0 = obj.niter0
    nit = invn(niter, niter0) - 1
    size = obj.size
    
    if nact == 0:
        dec = 0.5
        d = size * dec**nit
        if goback:
            t.left(45)
            t.forward(d)
        else:
            t.penup()
            t.backward(d)
            t.right(45)
            t.pendown()
    if nact == 1:
        dec = 0.8
        d = size * dec**nit    
        if goback:
            t.right(45)
            t.forward(d)
        else:
            t.penup()
            t.backward(d)
            t.left(45)
            t.pendown()
    return 



def generatelsystem(obj, t):
    for i in obj.lcode:
        obj.lvariables(i, obj, t)
           

class SuperTurtle():
    def __init__(self, t, drawtype = None, objd = None, fmod = None, argsf = None, fdraw = None):
        
        # Circulo
        self.radio = 10
        self.steps = 10
        self.colorRelleno = None
        
        # Point tracking
        self.points = np.array([[0,0], [0,1]])
        self.scalepx = None
        self.scalepy = None
        self.fcolor = None
        self.fline = None
        self.drawornot = None
        
        # Deltoid
        self.l = 200
        self.c = 100
        self.f = 1. / 3.
        self.angap = np.arctan(self.c * 0.5 / (self.f * self.l)) * 180 / np.pi * 2.
        
        # Polar Array
        self.nrad = 1
        self.nang = 4
        self.l0r1 = 0
        self.ang = 360
        self.ang0 = 0
        self.radio0 = 0
            
        # Poligon
        self.n = 3
        self.lado = 100
        self.vertex = True
        
        # XY Array
        self.lx = 100
        self.ly = 100
        self.nx = 2
        self.ny = 2
        self.center = True
        
        # LineArray
        self.nlines = 5
        self.lline = 10
        self.startangle = 0
        self.totalangle = 360
        self.l0r1 = 0
        
        # Fractal 3
        self.nact = 1
        self.turtleActions = turtleAct
        self.angle = 90
        self.size = 10
        
        # L
        self.turtleStatus = []
        self.lvariables = LVARIABLES
        self.rules = {"F" : "F + F - F - F F + F + F - F"}
        self.axiom = "F + F + F + F"
        self.niter = 3
        self.lcode = self.axiom
        self.multsize = 1.5
        self.divsize = 1.5
        self.multangle = 1.5
        self.divangle = 1.5
        

        # Tortuga
        self.t = t
        self.linewidth = 1
        self.linecolor = "Black"
        self.linewidthmult = 1.5
        self.linewidthdiv = 1.5
        
        # Modificar
        self.objd = objd
        self.fmod = fmod
        self.argsf = argsf
        self.fdraw = fdraw
        self.begin_end = None
        
        # Tipo
        self.tipo = drawtype
                
    def genlcode(self):
        lcode = self.axiom
        for i in range(self.niter):
            lcode = apply_rules(self, lcode)
        self.lcode = lcode
        return 
            
    def draw(self):
        
        if self.tipo == "circle":
            circulo(self, self.t, self.begin_end)
        if self.tipo == "circle2":
            circulo2(self, self.t, self.begin_end)        
        elif self.tipo == "polararray":
            polarArray(self, self.t, self.begin_end)
        elif self.tipo == "poligon":
            poligon(self, self.t)
        elif self.tipo == "xyarray":
            xyarray(self, self.t)
        elif self.tipo == "linearray":
            linearray(self, self.t)
        elif self.tipo == "fractaltree":
            fractaltree(self, self.t)
        elif self.tipo == "lsystem":
            generatelsystem(self, self.t)
        elif self.tipo == "deltoid":
            deltoid(self, self.t, self.begin_end)
        elif self.tipo == "pointtrack":
            point_track(self, self.t)
        else:
            self.t.dot(20)
        return 

    
def LVARIABLES(var, obj, t):
    if var in ["A", "B", "C", "D", "E", "F"]:
        t.forward(obj.size)
    elif var in ["G", "H", "I", "J", "K", "L"]:
        t.penup()
        t.forward(obj.size)
        t.pendown()
    elif var == "+":
        t.left(obj.angle)
    elif var == "-":
        t.right(obj.angle)
    elif var == "[":
        now = {}
        now["pos"] = t.pos()
        now["heading"] = t.heading()
        now["pen"] = t.pen()
        obj.turtleStatus.append(now)
    elif var == "]":
        t.pen(obj.turtleStatus[-1]["pen"])
        t.penup()
        t.setpos(obj.turtleStatus[-1]["pos"])
        t.setheading(obj.turtleStatus[-1]["heading"])
        t.pendown()
        if len(obj.turtleStatus) <= 1:
            obj.turtleStatus = []
        else:
            obj.turtleStatus.pop()
    else:
        t.forward(obj.size)
    return
    
 # Función para aplicar las reglas
def apply_rules(obj, lcode):
    return "".join([obj.rules.get(ch, ch) for ch in lcode])

# Función para generar la cadena de iteraciones
def generate_string(obj):
    for i in range(obj.niter):
        obj.lcode = apply_rules(obj, lcode)
    return 


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in degrees.
    """
    ox, oy = origin[0], origin[1]
    px, py = point[0], point[1]
    
    angle *= np.pi / 180.

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return [qx, qy]


def rgb_to_hex(rgb):
    """Converts an rgb tuple to hex string for web.
    
    >>> rgb_to_hex((204, 0, 0))
    'CC0000'
    """
    return ''.join(["%0.2X" % c for c in rgb])

cc = ["Nose", "Green Antique", "Ghost Boy", "Purple Memoiry", "Green Pip Boy", 
            "IHS - Death", "Dull Vibrancy", "Red Devil or Demon", "Monochrome Pallet", 
            "Weirwood I Color Palette", "Profundo Color", "Cool Dark",
            "Foggy London by Entropy", "SIPI", "Lavvy", "CD1ColorYB", 
            "IHS - Dream", "An orange shades", "Beccas Rainbow Part 1", 
            "Rainbow Flag", "PBI", "5HEX", "Victoria origin", "Pokemon", 
            "at-pc", "Just Messing Around", "Electric Bumblebee"]

def colorpalette(name):
    
    if type(name) == int:
        cc = ["Nose", "Green Antique", "Ghost Boy", "Purple Memoiry", "Green Pip Boy", 
                "IHS - Death", "Dull Vibrancy", "Red Devil or Demon", "Monochrome Pallet", 
                "Weirwood I Color Palette", "Profundo Color", "Cool Dark",
                "Foggy London by Entropy", "SIPI", "Lavvy", "CD1ColorYB", 
                "IHS - Dream", "An orange shades", "Beccas Rainbow Part 1", 
                "Rainbow Flag", "PBI", "5HEX", "Victoria origin", "Pokemon", 
                "at-pc", "Just Messing Around", "Electric Bumblebee"]  # 27 valores
        if name <= len(cc) - 1:
            name = cc[name]
        else:
            name = "Nose"

    colorp = [["Nose", 
                (255, 247, 244),
                (229, 219, 218),
                (200, 191, 184),
                (195, 176, 169),
                (162, 152, 153)],
              ["Green Antique", 
                (23, 21, 16),
                (106, 106, 69),
                (209, 204, 189),
                (228, 226, 219),
                (242, 240, 236)],      
              ["Ghost Boy", 
                (0, 0, 0),
                (72, 72, 72),
                (111, 110, 110),
                (154, 154, 154),
                (228, 228, 228)],
              ["Purple Memoiry",        
                (220, 207, 232),
                (218, 196, 239),
                (177, 148, 204),
                (150, 111, 186),
                (120, 64, 173)],
              ["Green Pip Boy",          
                (0, 238, 0),
                (0, 142, 0),
                (0, 95, 0),
                (0, 47, 0),
                (0, 0, 0)],
              ["IHS - Death",           
                (243, 246, 244),
                (196, 196, 214),
                (17, 31, 75),
                (3, 15, 55),
                (0, 0, 0)],    
              ["Dull Vibrancy",              
                (28, 0, 53),
                (50, 3, 92),
                (69, 4, 127),
                (87, 3, 162),
                (112, 0, 212)],
              ["Red Devil or Demon",               
                (255, 0, 0),
                (191, 0, 0),
                (128, 0, 0),
                (64, 0, 0),
                (0, 0, 0)],      
              ["Monochrome Pallet",            
                (161, 23, 244),
                (149, 24, 224),
                (139, 28, 206),
                (129, 28, 190),
                (119, 25, 176)],
              ["Weirwood I Color Palette",             
                (237, 238, 240),
                (239, 241, 240),
                (240, 242, 241),
                (233, 233, 233),
                (219, 220, 221)],
              ["Profundo Color",            
                (1, 0, 0),
                (26, 32, 97),
                (1, 1, 1),
                (11, 0, 17),
                (50, 50, 52)],
              ["Cool Dark",           
                (18, 52, 86),
                (137, 11, 128),
                (115, 121, 121),
                (14, 110, 97),
                (106, 50, 159)],
              ["Foggy London by Entropy",                 
                (12, 11, 11),
                (38, 38, 36),
                (89, 84, 72),
                (182, 177, 155),
                (254, 251, 253)],
              ["SIPI",   
                (102, 0, 0),
                (204, 0, 0),
                (56, 118, 29),
                (106, 168, 79),
                (0, 0, 0)],
              ["Lavvy",            
                (131, 112, 168),
                (31, 27, 26),
                (68, 58, 57),
                (134, 114, 107),
                (203, 193, 183)],   
              ["CD1ColorYB",                
                (62,38,0),
                (116,71,0),
                (157,103,18),
                (182,125,34),
                (208,148,54)],
              ["IHS - Dream",    
                (241,194,50),
                (191,144,0),
                (127,96,0),
                (61,44,5),
                (0,0,0)],
              ["An orange shades",    
                (255,170,0),
                (204,136,0),
                (153,102,0),
                (102,68,0),
                (51,34,0)],
              ["Beccas Rainbow Part 1",    
                (222,0,0),
                (255,102,0),
                (255,233,26),
                (122,226,0),
                (18,151,41)],
              ["Rainbow Flag",    
                (228,3,3),
                (255,140,0),
                (255,237,0),
                (0,128,38),
                (0,77,255)],
              ["PBI",    
                (102,102,255),
                (102,178,102),
                (255,201,102),
                (255,102,102),
                (178,102,178)],
              ["5HEX",    
                (41,134,204),
                (141,167,59),
                (255,192,0),
                (250,130,27),
                (244,67,54)],
              ["Victoria origin",    
                (238,201,0),
                (179,17,17),
                (207,17,120),
                (75,0,131),
                (65,105,225)],
              ["Pokemon",    
                (255,0,0),
                (204,0,0),
                (59,76,202),
                (255,222,0),
                (179,161,37)],
              ["at-pc",    
                (56,110,211),
                (255,102,0),
                (244,54,54),
                (91,194,40),
                (255,150,0)],
              ["Just Messing Around",    
                (229,229,11),
                (70,183,23),
                (195,44,169),
                (63,26,232),
                (108,15,136)],
              ["Electric Bumblebee",    
                (255,224,37),
                (255,231,88),
                (255,238,137),
                (255,246,192),
                (255,253,240)]]
    
    colorpal = pd.DataFrame(colorp)
    colorpal.columns = ["Name", "Color1", "Color2", "Color3", "Color4", "Color5"]
    return colorpal.loc[colorpal['Name'] == name].values.tolist()[0][1:]


def rgb_to_hex(rgb):
    """Converts an rgb tuple to hex string for web.
    
    >>> rgb_to_hex((204, 0, 0))
    'CC0000'
    """
    return ''.join(["%0.2X" % c for c in rgb])
    
    
def invn(n, niter0):
    return -1. * (n - niter0) + 1.

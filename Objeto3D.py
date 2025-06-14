from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

import random

class Objeto3D:
        
    def __init__(self):
        self.vertices = []
        self.faces    = []
        self.speed    = []
        self.angle    = []
        self.radius   = []
        self.position = Ponto(0,0,0)
        self.rotation = (0,0,0,0)
        self.fase = 0
        self.amplitude = 0.025
        self.estados = ""
        self.z_inicial = []
        
        pass

    def LoadFile(self, file:str):
        f = open(file, "r")

        # leitor de .obj baseado na descrição em https://en.wikipedia.org/wiki/Wavefront_.obj_file    
        for line in f:
            values = line.split(' ')
            # dividimos a linha por ' ' e usamos o primeiro elemento para saber que tipo de item temos

            if values[0] == 'v': 
                # item é um vértice, os outros elementos da linha são a posição dele
                self.vertices.append(Ponto(float(values[1]),
                                           float(values[2]),
                                           float(values[3])))
                self.speed.append((random.random() + 0.1))
                

                self.angle.append(math.atan2(float(values[3]), float(values[1])))
                self.radius.append(math.hypot(float(values[1]), float(values[3])))


            if values[0] == 'f':
                # item é uma face, os outros elementos da linha são dados sobre os vértices dela
                self.faces.append([])
                for fVertex in values[1:]:
                    fInfo = fVertex.split('/')
                    # dividimos cada elemento por '/'
                    self.faces[-1].append(int(fInfo[0]) - 1) # primeiro elemento é índice do vértice da face
                    # ignoramos textura e normal
                
        # calcular o centro da cabeça
        soma_x, soma_y, soma_z = 0, 0, 0
        contador = 0
        for v in self.vertices:
            if 0.4 < v.y < 0.6:
                soma_x += v.x
                soma_y += v.y
                soma_z += v.z
                contador += 1
                
        self.centro = Ponto(soma_x/ contador, soma_y/contador, soma_z/contador)
        pass

    def DesenhaVertices(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(.0, .0, .0)
        glPointSize(8)

        # glBegin(GL_POINTS)
        for v in self.vertices:
            glPushMatrix()
            glTranslate(v.x, v.y, v.z)
            glutSolidSphere(.05, 20, 20)
            glPopMatrix()
            # glVertex(v.x, v.y, v.z)
        # glEnd()
        
        glPopMatrix()
        pass

    def DesenhaWireframe(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0, 0, 0)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_LINE_LOOP)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass

    def Desenha(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0.34, .34, .34)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_TRIANGLE_FAN)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass



    # Movimento de "sim"
    def MovimentoSim(self):
        self.fase += 0.1
        angulo = self.amplitude * math.sin(self.fase)
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            y = v.y - self.centro.y
            z = v.z - self.centro.z
               
            v.y = math.cos(angulo) * y - math.sin(angulo) * z + self.centro.y
            v.z = math.sin(angulo) * y + math.cos(angulo) * z + self.centro.z
            
        if  self.fase > 2*math.pi and -0.01 < angulo < 0.01:
            self.estados = "finalizado"
            self.fase  = 0
    

    # Estrutura que faz os pontos descerem 
    def QuedaCabeca(self):
     self.estados = ""
     finalizou = True
    
     for i in range(len(self.vertices)):
            self.angle[i] += self.speed[i] * (1/30)

            x = self.radius[i] * math.cos(self.angle[i])
            z = self.radius[i] * math.sin(self.angle[i])

            self.vertices[i].x = x
            self.vertices[i].z = z

            if self.vertices[i].y > 0:
                self.vertices[i].y -= 0.25
                
            finalizou = False                
            if finalizou:
                self.estados = "finalizado"
                     
    def Quicar(self):
     
     # Ir sempre até a metade da altura e atualizar até que ela seja igual a 0
     for i in range(len(self.vertices)):
        #if self.vertices[i].y <= 0.25:
            self.angle[i] += self.speed[i] * (1/30)
            novaAltura = self.vertices[i].y /2
            self.vertices[i].y = novaAltura

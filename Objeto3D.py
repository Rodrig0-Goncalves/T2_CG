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
        self.estadoTrasFrente = ""
        self.estadoQueda = ""
        self.estadoQuicar = ""
        self.estadoTornado = ""
        self.verticesOriginais= []
        self.alturaVertices = []
        self.direcaoVertice = []
        
        pass

    def LoadFile(self, file:str):
        f = open(file, "r")

        # leitor de .obj baseado na descrição em https://en.wikipedia.org/wiki/Wavefront_.obj_file    
        for line in f:
            values = line.split(' ')
            # dividimos a linha por ' ' e usamos o primeiro elemento para saber que tipo de item temos

            if values[0] == 'v': 
                # item é um vértice, os outros elementos da linha são a posição dele
                vertices = Ponto(float(values[1]),
                                           float(values[2]),
                                           float(values[3]))
                self.speed.append((random.random() + 0.1))
                
                self.vertices.append(vertices)
                self.verticesOriginais.append(Ponto(vertices.x, vertices.y, vertices.z))

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
                    
            for i in self.vertices: # para pegar a altura de cada vértice e as direções dele
                self.alturaVertices.append(i.y/2)
                self.direcaoVertice.append(-1)   
                                    
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



    # Movimento de ir para tras e para frente
    def MovimentoTrasFrente(self):
        self.fase += 0.1
        angulo = self.amplitude * math.sin(self.fase)
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            y = v.y - self.centro.y
            z = v.z - self.centro.z
               
            v.y = math.cos(angulo) * y - math.sin(angulo) * z + self.centro.y
            v.z = math.sin(angulo) * y + math.cos(angulo) * z + self.centro.z
            
        if  self.fase > 2*math.pi and -0.01 < angulo < 0.01:
            self.estadoTrasFrente = "finalizado"
            self.fase  = 0
            print("Finalizou movimento tras frente")
            
    

    # Estrutura que faz os pontos descerem 
    
    def QuedaCabeca(self):
        finalizou = True
        # Ir sempre até a metade da altura e atualizar até que ela seja igual a 0
        for i in range(len(self.vertices)):
            verticeAtual = self.vertices[i]
            direcao = self.direcaoVertice[i]
            altura = self.alturaVertices[i] 
                    
            if altura <= 0.1:
                verticeAtual.y = 0
                continue
            
            finalizou = False
            
            if direcao == -1: #significa que ele esta descendo
                verticeAtual.y -= 0.2
                if verticeAtual.y <= 0:
                    verticeAtual.y = 0
                    self.direcaoVertice[i] = 1 # sobe os vértices
            
            elif direcao == 1:
                verticeAtual.y += 0.2
                if verticeAtual.y >= altura:
                    self.alturaVertices[i] = altura/2
                    if self.alturaVertices[i] <= 0.01:
                        self.direcaoVertice[i] = 0
                    else:
                        self.direcaoVertice[i] = -1
                    
        if finalizou:
            self.estadoQuicar = "finalizou"
            
        

    # Quarda os vértices inicias para usar quando resetar em "b" - porém resetando programa desde o ínicio, ajustar
    def resetarVertices(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x = self.verticesOriginais[i].x
            self.vertices[i].y = self.verticesOriginais[i].y
            self.vertices[i].z = self.verticesOriginais[i].z
            
            self.fase = 0
            self.estadoQueda = ""
            self.estadoTrasFrente = ""
        
         #self.angle[i] += self.speed[i] * (1/30) faz os vértices girarem 

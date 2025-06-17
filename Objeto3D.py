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
        self.verticesOriginais= []
        self.alturaVertices = []
        self.direcaoVertice = []
        self.tornadoAltura = []
        self.anguloTornado = []
        self.raioTornado = []
        self.tornadoFinal = []
        self.explosaoDirecao = []
        self.aneisInicio = []
        self.aneisRaio =[]
        self.aneisAngulo = []
        self.fasesUniverso = "compresao" 
        self.tempoUniverso = 0
        self.planetaRaio = 0.1
        self.position = Ponto(0,0,0)
        self.rotation = (0,0,0,0)
        self.fase = 0
        self.amplitude = 0.025
        self.estadoTrasFrente = ""
        self.estadoQueda = ""
        self.estadoTornado = ""
        self.estadoReforma = ""
        self.estadoUniverso = ""
       
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
                self.verticesOriginais.append(Ponto(vertices.x, vertices.y, vertices.z)) #Guarda todas as posições dos vértices para utilizar posteriormente

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
                
                # define o eixo em que o tornado vai girar e subir
            for i in self.vertices:
                self.anguloTornado.append(math.atan2(i.z, i.x)) # retorna o angulo entre os vetores em relação no plano 2D, define o angulo do circulo
                self.raioTornado.append(math.hypot(i.x, i.z)) # retorna a distância do ponto em relação a origem 
                self.tornadoAltura.append(i.y)
                
                # define um raio para cada vertice subir no tornado
                offset = random.uniform(-1.5,2.5)
                self.tornadoFinal.append(i.y +  offset)
                
            # randoriza as direções das explosões
            for i in range(len(self.vertices)):
                angulo = random.uniform(0,2*math.pi)
                verticeX = math.cos(angulo)
                verticeZ = math.sin(angulo)
                self.explosaoDirecao.append(Ponto(verticeX, 0, verticeZ))
                
            for i in range(len(self.vertices)):
                raio = random.uniform(4,5)
                angulo = random.uniform(0,2*math.pi)
                self.aneisRaio.append(raio)
                self.aneisAngulo.append(angulo)
                                                
        # calcular o centro da cabeça - pega a coordenada de cada vértice, soma e dívide pelo total, assim conseguido a médias dos pontos que estão no centro
        soma_x, soma_y, soma_z = 0, 0, 0
        contador = 0
        for i in self.vertices:
            if 0.4 < i.y < 0.6:
                soma_x += i.x
                soma_y += i.y
                soma_z += i.z
                contador += 1
                
        self.centro = Ponto(soma_x/ contador, soma_y/contador, soma_z/contador)

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

    # ==================================== PARTE NOVA DO PROJETO ==============================================
    # Movimento de ir para tras e para frente
    def MovimentoTrasFrente(self):
        self.fase += 0.1
        angulo = self.amplitude * math.sin(self.fase)
        for i in range(len(self.vertices)):
            vertice = self.vertices[i]
            verticeY = vertice.y - self.centro.y
            verticeZ = vertice.z - self.centro.z
               
            vertice.y = math.cos(angulo) * verticeY - math.sin(angulo) * verticeZ + self.centro.y
            vertice.z = math.sin(angulo) * verticeY + math.cos(angulo) * verticeZ + self.centro.z
            
        if  self.fase > 2*math.pi and -0.01 < angulo < 0.01:
            self.estadoTrasFrente = "finalizado"
            self.fase  = 0            
    
    # Estrutura que faz os pontos descerem 
    def QuedaCabeca(self):
        finalizou = True
        for i in range(len(self.vertices)):
            verticeAtual = self.vertices[i]
            direcao = self.direcaoVertice[i]
            altura = self.alturaVertices[i] 
                    
            if altura == 0 or altura <= 0.1:
                verticeAtual.y = 0
                continue
            
            finalizou = False
            
            # blocos executas o quicar dos vértices até a altura
            if direcao == -1: 
                verticeAtual.y -= 0.2
                if verticeAtual.y <= 0:
                    verticeAtual.y = 0
                    self.direcaoVertice[i] = 1 # sobe os vértices
            
            elif direcao == 1: 
                verticeAtual.y += 0.2
                if verticeAtual.y >= altura: # sempre indo até a metade da altura anterior
                    self.alturaVertices[i] = altura/2
                    if self.alturaVertices[i] <= 0.01:
                        self.direcaoVertice[i] = 0
                    else:
                        self.direcaoVertice[i] = -1
        
        if finalizou:
            self.estadoQueda = "finalizado"
        
    def Tornado(self):
        finalizou = True
        for i in range(len(self.vertices)):
            self.anguloTornado[i] += self.speed[i] * (1/30)
                        
            # responsável por  subir os vértices
            if self.vertices[i].y < self.tornadoFinal[i]:
                self.vertices[i].y += 0.05               
                finalizou = False
                
            # responsavel por fazer as partícualas girarem
            x = self.raioTornado[i] * math.cos(self.anguloTornado[i])
            z = self.raioTornado[i] * math.sin(self.anguloTornado[i])
                
            self.vertices[i].x = x
            self.vertices[i].z = z
                
        if finalizou:
            self.estadoTornado = "finalizado"
            
    def ReconstruirCabeca(self):
        finalizou = True
        
        # Resposavel por fazer a animação retornar a posição original aos poucos, interpolanod os vértices
        for i in range(len(self.vertices)):
            atual = self.vertices[i]
            final = self.verticesOriginais[i]
            
            # identifica se os vértices já estão na posição original, vai colocanso eles proximos dos pontos originais 
            fx = final.x - atual.x
            fy = final.y - atual.y
            fz = final.z - atual.z
            
            if abs(fx) > 0.01:
                atual.x += fx *0.1
                finalizou = False
            
            if abs(fy) > 0.01:
                atual.y += fy *0.1
                finalizou = False
                
            if abs(fz) > 0.01:   
                atual.z += fz *0.1
                finalizou = False
                
        if finalizou:
            self.estadoReforma = "finalizado"
         
    def Universo(self):
        self.tempoUniverso += 1 # temoporizador para mudança de estados
        
        if self.fasesUniverso == "compresao":
            finalizou = True
            comprimir = Ponto(2,0,2) # coordenadas onde os pontos serão comprimidos
                
            for i in range(len(self.vertices)): # comprime todos os vértices em um unico ponto
                vertice = self.vertices[i]
                compX = comprimir.x - vertice.x
                compY = comprimir.y - vertice.y
                compZ = comprimir.z - vertice.z
                
                # verifica se todos já estão no ponto de compresao
                if abs(compX) > 0.01 or abs(compY) > 0.01 or abs(compZ) > 0.01:
                    vertice.x += compX * 0.4
                    vertice.z += compZ * 0.4 
                    vertice.y += compY * 0.4 
                    finalizou = False
            if finalizou:
                self.fasesUniverso = "explosao" # passa para a próxima etapa
                self.tempoUniverso = 0
          
        elif self.fasesUniverso == "explosao":
            for i in range(len(self.vertices)): # espalha os vértices na horizontal
                vertice = self.vertices[i] 
                vertice.x += self.explosaoDirecao[i].x * 0.1
                vertice.y += self.explosaoDirecao[i].y * 0.1
                vertice.z += self.explosaoDirecao[i].z * 0.1
            
            if self.tempoUniverso > 120: # apos o numero de tempo, passa para a proxima etapa
                self.aneisInicio = [Ponto(vertice.x, vertice.y, vertice.z) for vertice in self.vertices]
                self.fasesUniverso = "aneis"
                self.tempoUniverso = 0
                
                
        elif self.fasesUniverso == "aneis":
            finalizou = True
            for i in range(len(self.vertices)):
                self.aneisAngulo[i] += 0.02
                
                # calculos responsaveis por fazer os vértices girarem no formato desejado
                raio = self.aneisRaio[i]
                angulo = self.aneisAngulo[i]
                
                # não mexe em y para não ter aneis na vertical
                destinoX = raio * math.cos(angulo)
                destinoY = 0
                destinoZ = raio * math.sin(angulo)
                
                # interpolação dos vértices para fazer uma transição suave -  tem relação com a velocidade em que os vértices vão retornar
                
                atual = self.vertices[i]             
                destX =  destinoX - atual.x
                destY = destinoY -  atual.y
                destZ = destinoZ - atual.z   
                # separação dos cálculo para otimizar a computação
                atual.x += destX  *0.03
                atual.y += destY *0.03
                atual.z += destZ *0.03
                
                if abs(destX) > 0.01 or abs(destY) > 0.01 or abs(destZ) > 0.01: # abs ignora o sinal e verifica o quão longe os vértices estão do destino
                    finalizou = False
                
            if self.tempoUniverso > 120:
                self.planetaInicio = [Ponto(vertice.x, vertice.y, vertice.z) for vertice in self.vertices]
                self.fasesUniverso = "planeta"
        # parte não esta sendo executada, trava o processamento -- OLHAR
        
        elif self.fasesUniverso == "planeta":
            raio = 2
            for i in range(len(self.vertices)):
                angulo = self.angle[i]
                altura = (i/len(self.vertices))*math.pi
                self.angle[i] += self.speed[i] * (1/60)
                
                # coordenadas do planete
                coordX = raio * math.sin(altura) * math.cos(angulo)
                coordY = raio * math.cos(altura)
                coordZ = raio * math.sin(altura) * math.sin(angulo)
                
                vertice = self.vertices[i]
                vertice.x += (coordX - vertice.x) * 0.50
                vertice.y += (coordY - vertice.y) * 0.50
                vertice.z += (coordZ - vertice.z) * 0.50
                  
    # Guarda os vértices inicias para usar quando resetar em "b" - porém resetando programa desde o ínicio, ajustar
    def ResetarVertices(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x = self.verticesOriginais[i].x
            self.vertices[i].y = self.verticesOriginais[i].y
            self.vertices[i].z = self.verticesOriginais[i].z
            
            self.fase = 0
            self.estadoQueda = ""
            self.estadoTrasFrente = ""
            self.estadoTornado = ""
            self.estadoReforma = ""
            self.estadoUniverso = ""
          

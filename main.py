from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import time
from Objeto3D import *

o:Objeto3D
tempo_antes = time.time()
soma_dt = 0

estado  = "iniciado"
estados = ["trasFrente", "quedaCabeca", "tornado", "reformaCabeca", "parteNova"]
fase = 0

def init():
    global o
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o = Objeto3D()
    o.LoadFile('Human_Head.obj')

    DefineLuz()
    PosicUser()


def DefineLuz():
    # Define cores para um objeto dourado
    luz_ambiente = [0.4, 0.4, 0.4]
    luz_difusa = [0.7, 0.7, 0.7]
    luz_especular = [0.9, 0.9, 0.9]
    posicao_luz = [2.0, 3.0, 0.0]  # PosiÃ§Ã£o da Luz
    especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable(GL_COLOR_MATERIAL)

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT, GL_SHININESS, 51)

def PosicUser():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Configura a matriz da projeção perspectiva (FOV, proporção da tela, distância do mínimo antes do clipping, distância máxima antes do clipping
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml
    gluPerspective(60, 16/9, 0.01, 50)  # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #Especifica a matriz de transformação da visualização
    # As três primeiras variáveis especificam a posição do observador nos eixos x, y e z
    # As três próximas especificam o ponto de foco nos eixos x, y e z
    # As três últimas especificam o vetor up
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    gluLookAt(-2, 6, -8, 0, 0, 0, 0, 1.0, 0)

def DesenhaLadrilho():
    glColor3f(0.5, 0.5, 0.5)  # desenha QUAD preenchido
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

    glColor3f(1, 1, 1)  # desenha a borda da QUAD
    glBegin(GL_LINE_STRIP)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20, -1, -10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()

def DesenhaCubo():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslated(0, 0.5, 0)
    glutSolidCube(1)

    glColor3f(0.5, 0.5, 0)
    glTranslated(0, 0.5, 0)
    glRotatef(90, -1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glutSolidCone(1, 1, 4, 4)
    glPopMatrix()


# controle de todos as etapas do programa
def Animacao():
    global soma_dt, tempo_antes, estado, fase

    tempo_agora = time.time()
    delta_time = tempo_agora - tempo_antes
    tempo_antes = tempo_agora

    soma_dt += delta_time

    if soma_dt > 1.0/30: # Aprox 30 quadros por segundo
        soma_dt = 0
        
        etapa = estados[fase]
        
        # Controle dos estados a serem executados
        if estado in ["iniciado", "play"]:
            if etapa == "trasFrente":
                o.MovimentoTrasFrente()
                if o.estadoTrasFrente == "finalizado":
                    avancaFase()
                    print("Finalizou primeiro movimento")
                    
            elif etapa == "quedaCabeca":
                o.QuedaCabeca()
                if o.estadoQueda  == "finalizado":
                    avancaFase()
                    print("Finalizou segundo movimento")
                    
            elif etapa == "tornado":
                o.Tornado()
                if o.estadoTornado == "finalizado":
                    avancaFase()
                    print("Finalizou terceiro movimento")
            elif etapa == "reformaCabeca":
                o.ReconstruirCabeca()
                if o.estadoReforma == "finalizado":
                    avancaFase()
                    print("Recontrui cabeça")
                    
            elif etapa == "parteNova":
                o.Universo() # fazer a parte nova, diferente do projeto
                if o.estadoUniverso == "finalizado":
                    print("Fim.")
                    estado = "stop"
                
        elif estado == "back":
            if fase > 0:
                fase -= 1
                o.fase = 0
                o.ResetarVertices()
            estado = "play"
            
        elif estado == "next":
            if fase < len(estados)- 1:
                fase += 1
            estado = "play"
                     
        glutPostRedisplay()

# Controle das fases a serem feitas, sempre indo para o próximo e cuidado para não passar do limite
def avancaFase():
    global fase, estado
    fase = min (fase+1, len(estados)-1)
    estado = "iniciado"

def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    #DesenhaCubo()    

    # classes que desenham as faces
    #o.Desenha() 
    #o.DesenhaWireframe()

    o.DesenhaVertices()

    glutSwapBuffers()
    pass

# movimentos das teclas
def play():
    global estado
    estado = "play"
    o.fase = 0
    o.estadoQueda = ""
    o.estadoTrasFrente = ""
    o.estadoReforma = ""
    o.estadoTornado = ""
    
def back():
    global estado, etapa
    if etapa > 0:
        etapa -= 1
        estado = "play"
        o.fase = 0
        o.estadoQueda = ""
        o.estadoTrasFrente = ""
        o.estadoReforma = ""
        o.estadoTornado = ""
    
def next():
    global estado, etapa
    if etapa < len(estado):
        etapa += 1
        estado = "play"
        o.fase = 0
        o.estadoQueda = ""
        o.estadoTrasFrente = ""
        o.estadoReforma = ""
        o.estadoTornado = ""

# Teclas a serem usadas
def teclado(key, x, y):
    global estado, etapa, fase

    if key == b'p':        
        estado  = "play"
    elif key == b'b':
        estado = "back"
    elif key == b'n':       
        estado = "next"
    elif key == b's':
        estado = "stop"
        
    glutPostRedisplay()
    pass

def main():

    glutInit(sys.argv)

    # Define o modelo de operacao da GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)

    # Especifica o tamnho inicial em pixels da janela GLUT
    glutInitWindowSize(740, 580)

    # Especifica a posição de início da janela
    glutInitWindowPosition(200, 200)

    # Cria a janela passando o título da mesma como argumento
    glutCreateWindow(b'Computacao Grafica - 3D')

    # Função responsável por fazer as inicializações
    init()
    

    # Registra a funcao callback de redesenho da janela de visualizacao
    glutDisplayFunc(desenha)

    # Registra a funcao callback para tratamento das teclas ASCII
    glutKeyboardFunc(teclado)
    
    glutIdleFunc(Animacao)

    try:
        # Inicia o processamento e aguarda interacoes do usuario
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()

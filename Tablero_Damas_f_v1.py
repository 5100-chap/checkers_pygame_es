"""----------------------------------Modulos--------------------------------"""
try:
    import pygame as pg
    from pygame import *
    import sys
    import os
    from time import sleep
except ImportError:
    print('Error: Instale la libreria con -pip install pygame')
    sys.exit(0)

"""---------------------------------Definir---------------------------------"""
"""------------------------Variables---------------------------"""
"""------------------Tamaño pantalla-------------------"""
"""Esta es la resolucion de nuestro juego, hasta el momento los valores se...
...deben de acercar a un cuadrado para evitar errores"""
LARGO = 800
ANCHO = 800
"""Tamaño de nuestro tablero en especifico"""
JANCHO = ANCHO - 200
"""------------------------Tablero-----------------------"""
"""Indica las filas y columnas de nuestro tablero"""
FILAS = 8
COLUMNAS = 8
"""----------------------Colores (RGB)-------------------"""
"""Variables que indican los colores en base al codigo RGB"""
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CAFE_OSCURO = (102, 51, 0)
NARANJA_CREMA = (255, 204, 153)
AMARILLO = (255, 255, 102)
AZUL = (0, 0, 255)
AZUL_CREMA = (102,102,153)
"""-------------------Tamaño del cuadrado----------------"""
"""El tamaño de los cuadrados"""
TAMAÑO_CDD = JANCHO//COLUMNAS
"""--------------Espacio entre el cuadrado y las fichas---------"""
ESPACIO_ECP = 18
"""---------------------Radio-------------------------"""
RADIO = TAMAÑO_CDD//2 - ESPACIO_ECP
"""----------------------FPS (reloj)-----------------------"""
"""Esta variable permite sincronizar la ventana con un...
...tiempo predefinido"""
reloj = pg.time.Clock()
FPS = 60
"""--------------------llamar ventana desde pygame---------------"""
SCREEN = pg.display.set_mode((ANCHO, LARGO))
pg.display.set_caption("Juegos Cognitivos: Damas")
"""------------------------------Funciones----------------------------------"""
"""Esta funcion nos ayuda a obtener posicion respecto al mouse para...
...interactuar"""
def pos_mouse(pos):
    x, y = pos
    fila = y // TAMAÑO_CDD
    col = x // TAMAÑO_CDD
    return fila, col


"""Crea una función que limpia la consola"""
def limpiar_consola():
    if os.name == 'posix':
        _ = os.system('clear')  # Sistemas basados en UNIX (Mac o Linux)
    else:
        _ = os.system('cls')  # Windows

"""---------------------------------Clases----------------------------------"""
"""-------------------------------------------------------------------------"""
class tablero:
    """Esta clase va a manejar el tablero"""
    """Declaramos los datos que almacenara esta clase
    En este caso declararemos ___init___ que es un tipo indice"""
    def __init__(self):
        """Declaramos una lista la cual nos ayudara a almacenar los datos de...
        ...nuestra matriz que controlara el juego"""
        self.tabla = []
        """Aqui se declara las piezas negras y blancas que tiene un jugador"""
        self.negro_rest = 12
        self.blanco_rest = 12
        """Aqui se declaran las piezas reyes que tienen los jugadores"""
        self.rey_negro = 0
        self.rey_blanco = 0
        """Aqui se llama a la variable que crea nuestra tabla"""
        self.crear_tabla()
    """Declaramos una variable que se encargue de dibujar los cuadrados"""
    def cuadros_tab(self, screen):
        """Rellenamos la pantalla de cafe oscuro"""
        screen.fill(CAFE_OSCURO)
        """Hacemos una matriz, primero se crean las filas con loop for"""
        """Como aqui queremos dibujar cuadrados en esta matriz solo se...
        ...tomaran en cuenta para dibujar los cuadrados en filas...
        ...las posiciones que son impares y la posiciones de las...
        ...columnas que sean pares con respecto al punto de origen"""
        for fila in range(FILAS):
            for col in range(fila % 2, COLUMNAS, 2):
                calculo_cdds = (fila*TAMAÑO_CDD,
                                col * TAMAÑO_CDD, TAMAÑO_CDD, TAMAÑO_CDD)
                pg.draw.rect(screen, NARANJA_CREMA, calculo_cdds )
    """Declararemos una variable que se encargue de crear nuestra tabla"""
    def crear_tabla(self):
        for fila in range(FILAS):
            self.tabla.append([])
            for col in range(COLUMNAS):
                if col % 2 == ((fila + 1) % 2):
                    """Estas dos condiciones ubican las fichas"""
                    if fila < 3:
                        self.tabla[fila].append(
                            damas_piezas(fila, col, BLANCO))
                    elif fila > 4:
                        self.tabla[fila].append(
                            damas_piezas(fila, col, NEGRO))
                        """Estos else definen los espacios en blanco"""
                    else:
                        self.tabla[fila].append(0)
                else:
                    self.tabla[fila].append(0)
    """Esta funcion se encarga de dibujar todo a nuestra pantalla"""
    def dibujar(self, screen):
        self.cuadros_tab(screen)
        """Estos for in loops se encargan de dibujar las piezas (Matriz)"""
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                pieza = self.tabla[fila][col]
                if pieza != 0:
                    pieza.dibujar(screen)

    def movimiento(self, pieza, fila, col):
        """intercambiamos las posiciones de nuestra matriz (tabla), la cual...
        ...se declara como un intercambio simple entre coordenadas de una...
        ...lista, declaralas por separado (o sea que se declaren en linea...
        ...diferente sin comas) hara que el programa experimente errores...
        ...a la hora de mover las piezas."""
        self.tabla[pieza.fila][pieza.columna], self.tabla[fila][col] \
        = self.tabla[fila][col], self.tabla[pieza.fila][pieza.columna]
        """Se actualiza la ubicacion de la pieza, y se llama a la funcion...
        encargada del movimiento dentro de la clase piezas."""
        pieza.movimiento(fila, col)
        """Checa si tu pieza cumple con los requisitos para ser rey"""
        if fila == FILAS - 1 or fila == 0:
            pieza.eres_rey()
            if pieza.color == BLANCO:
                self.rey_blanco += 1
            else:
                self.rey_negro += 1
    """Ayuda con poner al tanto de la posicion de nuestras piezas...
    ...en la matriz"""
    def piezas(self, fila, col):
        try:
            return self.tabla[fila][col]
        except IndexError:
            return None
    """Esta funcion se encarga de checar que movimientos estan permitidos...
    ...(O sea que una dama no se pueda mover en linea recta o que no se...
    ...pueda mover hacia atras si no es rey)"""
    def mov_legales(self, pieza):
        """Almacena los movimientos en un diccionario"""
        movimientos = {}
        izquierda = pieza.columna - 1
        derecha = pieza.columna + 1
        fila = pieza.fila
        """Agregamos los movimientos al diccionario dependiendo del color...
        ...o viendo si la pieza es rey"""
        if pieza.color == NEGRO or pieza.rey:
            movimientos.update(self._diagonal_izq(
                fila - 1, max(fila-3, -1), -1, pieza.color, izquierda))
            movimientos.update(self._diagonal_der(
                fila - 1, max(fila-3, -1), -1, pieza.color, derecha))
        if pieza.color == BLANCO or pieza.rey:
            movimientos.update(self._diagonal_izq(
                fila + 1, min(fila+3, FILAS), 1, pieza.color, izquierda))
            movimientos.update(self._diagonal_der(
                fila + 1, min(fila+3, FILAS), 1, pieza.color, derecha))
        """Regresamos lo que se haya guardado en el diccionario"""
        return movimientos
    """Estas funciones son encargada de hacer nuestro movimiento en... 
    ...las lineas horizontales, encargada ademas de checar si una...
    ...dama come o no."""
    """Funcion de diagonal derecha"""
    def _diagonal_der(self, inicio, fin, paso, color, der, skip=[]):
        """Declaramos un diccionario que almacenara el movimiento...
        ...en diagonal"""
        mov = {}
        """Declaramos una lista que guarde el ultimo dato almacenado"""
        ultimo = []
        for i in range(inicio, fin, paso):
            """Checa que nuestra diagonal en derecha no se salga...
            de la matriz"""
            if der >= COLUMNAS:
                break
            actual = self.tabla[i][der]
            """checa si encontramos un cuadro vacio"""
            if actual == 0:
                """No hay lugar para moverse"""
                if skip and not ultimo:
                    break
                    """Condicional para el salto"""
                elif skip:
                    mov[(i, der)] = ultimo + skip
                    """Condicional para el multisalto"""
                else:
                    mov[(i, der)] = ultimo
                if ultimo:
                    if paso == -1:
                        fila = max(i-3, 0)
                    else:
                        fila = min(i+3, FILAS)
                    mov.update(self._diagonal_izq(
                        i+paso, fila, paso, color, der-1, skip=ultimo))
                    mov.update(self._diagonal_der(
                        i+paso, fila, paso, color, der+1, skip=ultimo))
                break
                """Caso de que encontremos una dama del mismo color"""
            elif actual.color == color:
                break
            else:
                ultimo = [actual]
            der += 1
        """Regresa los datos almacenados"""
        return mov
        """Funcion de diagonal izquierda"""
    def _diagonal_izq(self, inicio, fin, paso, color, izq, skip=[]):
        mov = {}
        ultimo = []
        for i in range(inicio, fin, paso):
            if izq < 0:
                break
            actual = self.tabla[i][izq]
            if actual == 0:
                if skip and not ultimo:
                    break
                elif skip:
                    mov[(i, izq)] = ultimo + skip
                else:
                    mov[(i, izq)] = ultimo
                if ultimo:
                    if paso == -1:
                        fila = max(i-3, 0)
                    else:
                        fila = min(i+3, FILAS)
                    mov.update(self._diagonal_izq(
                        i+paso, fila, paso, color, izq-1, skip=ultimo))
                    mov.update(self._diagonal_der(
                        i+paso, fila, paso, color, izq+1, skip=ultimo))
                break
            elif actual.color == color:
                break
            else:
                ultimo = [actual]
            izq -= 1
        return mov
    """Esta funcion remueve las fichas en caso de ser necesario"""
    def remove(self, piezas):
        for pieza in piezas:
            self.tabla[pieza.fila][pieza.columna] = 0
            if pieza != 0:
                if pieza.color == NEGRO:
                    self.negro_rest -= 1
                else:
                    self.blanco_rest -= 1
    """Esta funcion define un ganador"""
    def ganador(self):
        if self.negro_rest <= 0:
            return 'Blanco'
        elif self.blanco_rest <= 0:
            return 'Negro'
        """Mientras no gane nadie regresara None (No hay valor)"""
        return None
"""-------------------------------------------------------------------------"""
class damas_piezas:
    """Esta clase va a manejar las fichas"""
    """variables exclusivas para la clase"""
    def __init__(self, fila, columna, color):
        self.fila = fila
        self.columna = columna
        self.color = color
        self.rey = False
        self.x = 0
        self.y = 0
        self.pos_xy()
    """Esta funcion permite ubicar las piezas en la matriz"""
    def pos_xy(self):
        self.x = TAMAÑO_CDD * self.columna + TAMAÑO_CDD // 2
        self.y = TAMAÑO_CDD * self.fila + TAMAÑO_CDD // 2
    """Esta funcion convierte una pieza a rey"""
    def eres_rey(self):
        self.rey = True
    """Esta funcion se encarga de dibujar las piezas"""
    def dibujar(self, screen):
        if self.rey == False:
            pg.draw.circle(screen, ROJO, (self.x, self.y), RADIO + 7)
            pg.draw.circle(screen, self.color, (self.x, self.y), RADIO)
        else:
            pg.draw.circle(screen, AMARILLO, (self.x, self.y), RADIO + 7)
            pg.draw.circle(screen, self.color, (self.x, self.y), RADIO)
    """Esta funcion se encarga del movimiento de las piezas"""
    def movimiento(self, fila, columna):
        self.columna = columna
        self.fila = fila
        self.pos_xy()
"""-------------------------------------------------------------------------"""
class juego:
    """Esta clase va a ser encargada de las interacciones"""
    def __init__(self, screen):
        self.ficha_select = None
        self.tabla = tablero()
        self.turno_actual = NEGRO
        self.mov_legales = {}
        self.screen = screen
    """Esta funcion actualiza los dibujos en pantalla"""
    def actualizar(self):
        self.tabla.dibujar(self.screen)
        self.dibujar_opciones(self.mov_legales)
        self.turno_di(self.screen)
        pg.display.flip()
    """Esta funcion crea un texto y un vizualizador para ver cual es el... 
    ...turno actual"""
    def turno_di(self, screen):
        cuadrado1 = (0, JANCHO, ANCHO, LARGO)
        cuadrado2 = (JANCHO, 0, ANCHO, LARGO)
        pg.draw.rect(self.screen, AZUL_CREMA, cuadrado1, 0)
        pg.draw.rect(self.screen, AZUL_CREMA, cuadrado2, 0)
        pg.draw.circle(screen, AZUL, (ANCHO//4,
        JANCHO + 100), RADIO+7)
        if self.turno_actual == NEGRO:
            pg.draw.circle(screen, NEGRO, (ANCHO//4,
            JANCHO + 100), RADIO)
        else:
            pg.draw.circle(screen, BLANCO, (ANCHO//4,
            JANCHO + 100), RADIO)
        formato = pg.font.SysFont('Arial', int(ANCHO*(4/60)))
        turno = formato.render("Turno:", False, BLANCO)
        screen.blit(turno, (0, JANCHO))
    """Esta funcion se encarga de la seleccion de las piezas"""
    def seleccion(self, fila, col):
        """Si una ficha es seleccionada entonces..."""
        if self.ficha_select:
            """...se almacena para checar si tiene movimientos validos"""
            result = self._mover(fila, col)
            """Si el movimiento seleccionado no es valido se mantiene en la...
            ultima seleccion"""
            if not result:
                self.ficha_select = None
                self.seleccion(fila, col)
        pieza = self.tabla.piezas(fila, col)
        """Checamos si la seleccion es una pieza y si corresponde al turno"""
        if pieza == None:
            return False
        if pieza != 0 and pieza.color == self.turno_actual:
            self.ficha_select = pieza
            self.mov_legales = self.tabla.mov_legales(pieza)
            return True
        return False
    """Esta funcion determina el movimiento y el cambio de turno"""
    def _mover(self, fila, col):
        pieza = self.tabla.piezas(fila, col)
        if self.ficha_select and pieza == 0 \
            and (fila, col) in self.mov_legales:
            self.tabla.movimiento(self.ficha_select, fila, col)
            skip = self.mov_legales[(fila, col)]
            if skip:
                self.tabla.remove(skip)
            self.cambio_turno()
        else:
            return False
        return True
    """Esta funcion dibuja los movimientos validos"""
    def dibujar_opciones(self, mover):
        for moverse in mover:
            fila, col = moverse
            pg.draw.circle(self.screen, AZUL, (col * TAMAÑO_CDD +
            TAMAÑO_CDD//2, fila * TAMAÑO_CDD + TAMAÑO_CDD//2), 15)
    """Esta funcion define el cambio de turno"""
    def cambio_turno(self):
        self.mov_legales = {}
        if self.turno_actual == NEGRO:
            self.turno_actual = BLANCO
        else:
            self.turno_actual = NEGRO
    """Esta funcion checa al ganador"""
    def ganador(self):
        return self.tabla.ganador()
"""-------------------------------------------------------------------------"""
class menu:
    """Esta clase sera el menu principal"""
    """Variables para la clase"""
    def __init__(self):
        self.fondo = AZUL_CREMA
        self.screen = SCREEN
        self.color_ns = (100, 100, 100)
        self.color_s = (180, 180, 180)
    """Esta funcion crea un boton"""
    def boton(self,texto, x, y):
        ladoc = int(ANCHO*(3/10))
        ladod = int(LARGO*(1.5/10))
        formato = pg.font.SysFont('Arial', int(ANCHO*(4/125)))
        formatot = pg.font.SysFont('Arial', int(ANCHO*(4/60)))
        texto = formato.render(texto, True, BLANCO)
        titulo = formatot.render('Juegos Cognitivos: Damas', True, BLANCO)
        rectangulo = pg.Rect((x, y, ladoc, ladod))
        """Esta condicion le da un efecto al boton cuando el mouse se...
        ...posiciona sobre el"""
        if rectangulo.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(self.screen, self.color_s, rectangulo, 0)         
        else:
            pg.draw.rect(self.screen, self.color_ns, rectangulo, 0)
        """Dibuja el boton con su texto"""
        self.screen.blit(texto, (x, y+(ladoc//6)))
        self.screen.blit(titulo, (int(ANCHO/(20/3)), 0))
        return x, y, ladoc, ladod
    """Esta funcion crea un pantalla si gana alguien"""
    def mensaje_ganador(self,texto):
        """Define la parte de los textos"""
        texto = str(texto)
        self.screen.fill(self.fondo)
        formato = pg.font.SysFont('Arial', int(ANCHO*(4/60)))
        titulo = formato.render('Ganador:', True, BLANCO)
        ganador = formato.render(texto, True, BLANCO)
        """Dibuja los textos"""
        self.screen.blit(titulo, (ANCHO//3, 0))
        self.screen.blit(ganador, (ANCHO//2.6, LARGO//4))
        """Dibuja una ficha del ganador"""
        pg.draw.circle(self.screen, ROJO, (ANCHO//2,
        int(LARGO//1.8)), RADIO*4+(7*4))
        if texto == 'Blanco':
            pg.draw.circle(self.screen, BLANCO, (ANCHO//2,
            int(LARGO//1.8)), RADIO*4)
        elif texto == 'Negro':
            pg.draw.circle(self.screen, NEGRO, (ANCHO//2,
            int(LARGO//1.8)), RADIO*4)
        else:
            pg.draw.circle(self.screen, CAFE_OSCURO, (ANCHO//2,
            int(LARGO//1.8)), RADIO*4)
        pg.display.flip()
    def intrucciones(self):
        texto1 = """Cada jugador tendra 12 fichas ya sean negras o 
        blancas que se colocaran en los cuadros cafes de las primeras 3 
        filas de cada lado, los movimientos para las fichas seran en diagonal 
        y solo se podran mover una casilla cada turno hacia adelante
        (al campo enemigo)"""
        texto2 = """Si una ficha llega al lado contrario del tablero dicha 
        ficha se convertira en dama o reina la cual se podra mover en 
        cualquier dirección en diagonal ya sea atras o adelante pero su 
        movimiento aun se limitara a una casilla, las damas nunca podran 
        saltar encima de sus propias piezas o en dos piezas continuas del 
        lado contrario"""
        texto3 = """Una ficha puede comerse a otra saltando encima de ella 
        siempre y cuando sea diagonal y este en una casilla adelante 
        diagonalmente ademas de que sea su turno,las damas pueden comer 
        en cualquier dirección, el comer fichas es obligatorio si una ficha 
        tiene la oportunidad de comer otra tendra que comerla obligatoriamente
        y no optar por mover otra ficha."""
        print(texto1)
        print(texto2)
        print(texto3)
        read_me = open("read_me.txt", "w")
        read_me.write(texto1)
        read_me.write(texto2)
        read_me.write(texto3)
        read_me.close()
    def main_menu(self):
        """Esto creara nuestro menu principal"""
        self.screen.fill(self.fondo)
        """Creacion de botones"""
        boton1 = self.boton('Iniciar Damas', ANCHO - ANCHO//2, 
        LARGO - LARGO//2)
        boton2 = self.boton('Salir', ANCHO - ANCHO//3,
        LARGO - LARGO//3)
        pg.draw.circle(self.screen, ROJO, (int(ANCHO//2.7), 
        int(LARGO//1.3)), RADIO*4+(7*4))
        pg.draw.circle(self.screen, AMARILLO, (ANCHO//5, 
        int(LARGO//2.5)), RADIO*4+(7*4))
        pg.draw.circle(self.screen, BLANCO, (int(ANCHO//2.7), 
        int(LARGO//1.3)), RADIO*4)
        pg.draw.circle(self.screen, NEGRO, (ANCHO//5, 
        int(LARGO//2.5)), RADIO*4)
        """Colision para los botones"""
        inicio = pg.Rect(boton1)
        salir = pg.Rect(boton2)
        """Accion iniciar el juego"""
        if inicio.collidepoint(pg.mouse.get_pos()) and \
            pg.event.get(MOUSEBUTTONDOWN):
            return False
        """Accion salir del juego"""
        if salir.collidepoint(pg.mouse.get_pos()) and \
                pg.event.get(MOUSEBUTTONDOWN):
            limpiar_consola()
            sys.exit(0)
        pg.display.flip()
    
"""----------------------------Programa principal---------------------------"""
def main():
    """Primero y antes que nada se inicia la libreria con este comando"""
    pg.init()
    """Se declara nuestro tablero, para asi poder usarlo posteriormente"""
    tab = juego(SCREEN)
    m_menu = menu()
    p_damas = False
    principal = True
    while principal:
        reloj.tick(FPS)
        for evento in pg.event.get():
            if evento.type == QUIT:
                sys.exit(0)
        m_menu.main_menu()
        if m_menu.main_menu() == False:
            principal = False
            p_damas = True
    """Este bucle es el encargado de mantener abierto y cerrar la ventana...
    ...del juego como tal."""
    while p_damas:
        reloj.tick(FPS)
        if tab.ganador() != None:
            p_damas = False
        for evento in pg.event.get():
            if evento.type == QUIT:
                sys.exit(0)
                limpiar_consola()
            if evento.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                x, y = pos_mouse(pos)
                tab.seleccion(x, y)
        """Ordenamos al progama al actualizarse por cada cuadro por segundo"""
        tab.actualizar()
    m_menu.mensaje_ganador(tab.ganador())
"""----------------------------------Codigo---------------------------------"""
limpiar_consola()
instrucciones = menu()
instrucciones.intrucciones()
while True:
    main()
    sleep(5)

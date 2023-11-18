import os
import pygame
import random





def get_absolute_path_of( path ):
    return os.getcwd() + '/' + path

relative_paths = [ 'img', 'temp' ]

paths = {}

for a_relative_path in relative_paths:
    complete_path = get_absolute_path_of( a_relative_path )
    paths[ a_relative_path ] = complete_path













# Game
#TODO Une classe Game qui gère la partie et le déroulement du jeu (les règles déroulées dans le temps)
#TODO Méthodes de Game :
#TODO RemoveLine, FallLines, gameover,update_score,







# Line
# TODO Gère le groupement des sprites concernés par une ligne, et le carré concerné, pour supprimer une ligne facilement.







# Board
#TODO Gère le dessin du plateau, ses dimensions.

class Board:

    def __init__( self, size, game ):
        self.size = size
        self.game = game
        self._calculate_size()


    def _calculate_size(self):
        self.third_party = self.size / 3
        self.well_size = self.third_party * 2
        self.start_panel = self.size - self.third_party
        self.bricks_size = self.well_size / 10
        self.start_low_wall_B = self.start_panel - self.bricks_size



    def draw(self):

        # Dessiner une grille

        taille_carre = 20
        epaisseur_grille = 1
        taille_ecran = self.game.resolution[0]
        couleur_grille = (220, 220, 220)

        nb_carres = int( taille_ecran / taille_carre ) + 1

        for hauteur in range( nb_carres):
            posY = hauteur * taille_carre

            for largeur in range( nb_carres ):
                posX = largeur * taille_carre

                carre_grille = pygame.Rect(posX, posY, taille_carre, taille_carre)
                pygame.draw.rect( self.game.screen, couleur_grille, carre_grille, epaisseur_grille )



        # Black Panel
        black_panel = pygame.Rect(self.start_panel, 0, self.third_party, self.size)
        pygame.draw.rect( self.game.screen, (0, 0, 0), black_panel )

        # Bricks
        brick = paths['img'] + '/bricks.png'
        brick_image = pygame.image.load( brick )
        fliped_brick_image = pygame.transform.flip(brick_image, True, False)

        brick_image_rect = brick_image.get_rect()



        repeat = int( self.game.resolution[0]/brick_image_rect.height )

        for i in range( repeat ):
            low_wall_A = pygame.rect.Rect( 0, i*brick_image_rect.height, brick_image_rect.width, brick_image_rect.height)
            self.game.screen.blit( fliped_brick_image, low_wall_A )

            low_wall_B = pygame.rect.Rect( self.start_low_wall_B, i*brick_image_rect.height, brick_image_rect.width, brick_image_rect.height)
            self.game.screen.blit( brick_image, low_wall_B )



class Game:

    def __init__( self, args ):

        size = args['resolution']
        self.resolution = ( size, size )

        self.next_fall = 0
        self.fall_time = 1000

        self.falling_pentamino = False

        self.all_pentaminos = {

            'I' : {
                'color' : (0, 255, 255),
                'display' : [1,1,1,1]
            },

            'O' : {
                'color' : (255, 255, 0),
                'display' : [[1,1], [1,1]]
            },

            'T' : {
                'color' : (170, 0, 255),
                'display' : [[1,1,1], [0,1,0]]
            },

            'L' : {
                'color' : (255, 165, 0),
                'display' : [[1,1,1], [1,0,0]]
            },

            'J' : {
                'color' : (0, 0, 255),
                'display' : [[1,1,1], [0,0,1]]
            },

            'Z' : {
                'color' : (255, 0, 0),
                'display' : [[1,1,0], [0,1,1]]
            },

            'S' : {
                'color' : (0, 255, 0),
                'display' : [[0,1,1], [1,1,0]]
            }

        }

        self.screen_color = args['screen_color']

        self.init_screen()
        self.init_events()
        self.init_board( size )
        self.init_loop()


    def init_screen(self):
        self.screen = pygame.display.set_mode( self.resolution )
        self.clock = pygame.time.Clock()


    def init_events(self):
        self.events = Events( self )
        self.events.new_pentamino()


    def init_board(self, size):
        self.board = Board( size, self )


    def init_loop(self):
        self.loop = Loop( self )





class Events:

    def __init__(self, game):
        self.game = game
        self.list = {}
        self.response = {}
        self.init()

        self.keys_array = {
            'K_UP' : 'up',
            'K_DOWN' : 'down',
            'K_LEFT' : 'left',
            'K_RIGHT' : 'right'
        }


    def init(self):

        self.init_response()

        # Quit Event
        self.list['quit'] = pygame.QUIT
        self.list['keydown'] = pygame.KEYDOWN
        self.list['keyup'] = pygame.KEYUP


    def init_response(self):

        self.response = {
            'quit' : False,
            'keydown' : False,
            'keyup' : False
        }


    def quit(self, event):
        print ('Vous avez décidé de quitter le jeu.')
        self.response['quit'] = True


    def keydown(self, event):

        for a_key in self.keys_array.keys():
            tested_key = getattr( pygame, a_key, False )
            if event.key == tested_key:
                 method = getattr( self, self.keys_array[ a_key ], False )
                 if method: method()

        self.response['keydown'] = True



    def keyup(self, event):
        self.response['keyup'] = True


    def up(self):
        print('UP')


    def down(self):
        print('DOWN')


    def left(self):
        print('LEFT')


    def right(self):
        print('RIGHT')


    def call(self):

        self.init_response()

        for a_pygame_event in pygame.event.get():

            for a_called_event_name in self.list.keys():

                if a_pygame_event.type == self.list[ a_called_event_name ]:
                    method = getattr(self, a_called_event_name, False)
                    if method: method( a_pygame_event )

        return self.response


    def new_pentamino(self):
        all_pentaminos_names = [key for key in self.game.all_pentaminos]
        name = all_pentaminos_names[ random.randint( 0, 6 ) ]
        self.game.falling_pentamino = Tetramino( self.game.all_pentaminos[ name ], name )


    def fall(self, time):
        print('fall')
        self.game.next_fall = time + self.game.fall_time





class Loop:

    def __init__( self, game ):
        self.game = game

        self.screen = self.game.screen
        self.clock = self.game.clock
        self.running = False

        self.init()


    def init(self):

        pygame.init()

        self.running = True
        self.loop()


    def loop(self):

        while self.running:

            now = pygame.time.get_ticks()
            if now >= self.game.next_fall:
                self.game.events.fall( now )

            # Quit event.
            call = self.game.events.call()
            self.running = not call['quit']

            # Our display method.
            self.display()

            # Pygame Display method
            pygame.display.flip()

            # FPS
            self.clock.tick(60)


        pygame.quit()


    def display(self):
        self.screen_color()
        self.game.board.draw()

    def screen_color(self):
        self.screen.fill( self.game.screen_color )






# Tetramino

#TODO Classe abstraite tetramino
#TODO Une classe pour chaque pièce, qui hérite de tetramino


class Tetramino:

    def __init__( self, type, name ):
        print( type )
        self.name = name
        self.color = type['color']
        self.display = type['display']
        self.pos = [ 100, 100 ]
        self.falling = True

        self.draw()


    def draw(self):
        print( 'Dessine')
        print( self.display )





args = {
    "resolution" : 750,
    "screen_color" : "white"
}

Game( args )





# Score
#TODO Une classe Score qui gère le score du joueur



# Interface
#TODO Une classe parente : Interface (abstraite) Puis une classe pour boutons, messages, etc.



# Affichage
#TODO Une classe Display qui gère ce qu'on affiche à l'écran, ce qu'il faut mettre à jour, etc.



# Player
#TODO Une classe pour l'entité player



# Player_Name
#TODO Une classe pour l'entrée du nom

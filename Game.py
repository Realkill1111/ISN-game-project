import pygame
from pygame import *
import os
import tkinter
from threading import Timer

# Detection taille écran
root = tkinter.Tk()
scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
pygame.init()

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((scrwidth, scrheight),pygame.NOFRAME)

if scrwidth >= 1920 and scrheight >= 1080:
    leng = 1
    perso_x = 960
    perso_y = 840
    WIDTH = 48
    h = 48
    w = 52
elif scrwidth <= 1920 and scrheight <= 1080:
    leng = 0.71
    perso_x = 680
    perso_y = 595
    WIDTH = 34
    h = 34
    w = 37

path = os.path.dirname(os.path.abspath(__file__))
combined_size = f"{scrwidth}x{scrheight}"
sprites_dir = f"{path}/sprites"
menu = True
continuer = False

def centering(img):
    global scrwidth,scrheight
    ww=img.get_rect().size
    return (abs(scrwidth-ww[0])/2) , (abs(scrheight-ww[1])/2)

xdisp,ydisp = 0,0

noir  =   0,   0,   0
blanc = 255, 255, 255
rouge = 255,   0,   0
jaune = 255, 220,   0

police = pygame.font.Font('freesansbold.ttf',40)

def bouton(x, y, w, h, backgroundcolor, texte, textcolor, fnt):
    global fenetre
    box = ( (x,y) , (w,h))
    pygame.draw.rect(fenetre, backgroundcolor, box)
    txt = fnt.render(texte, True, textcolor)
    txtpos = txt.get_rect()
    txtpos.x = x+int(w/2) - txtpos.width/2
    txtpos.y = y+int(h/2) - txtpos.height/2
    fenetre.blit(txt, txtpos)
    return ( Rect(x, y, w, h) )

jouer   = bouton((scrwidth-440)/2, (scrheight-200)/2, 440, 75, rouge, "JOUER"  , jaune, police)
quitter = bouton((scrwidth-440)/2, (scrheight+200)/2, 440, 75, rouge, "QUITTER", jaune, police)


ecran = []
salle = []
pn = []
ps = []

#Rafraîchissement de l'écran
pygame.display.flip()

pygame.mixer.music.load(f"{path}/Musique/twimenu.wav")
posx,posy = pygame.mouse.get_pos()
pygame.mixer.music.play()

def dedans(pos, rect) :
    x1 = rect.x
    y1 = rect.y
    x2 = rect.x+rect.w
    y2 = rect.y+rect.h
    if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
        return True
    return False

while menu:
    
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == MOUSEBUTTONUP and dedans(pygame.mouse.get_pos(), quitter) ):
            menu = False
            continuer = False
            
        if event.type == MOUSEMOTION:
            posx,posy = pygame.mouse.get_pos()
            fnt = pygame.font.Font("freesansbold.ttf", 24)
            text = fnt.render(f"x,y: ({posx}, {posy})",1,(255,255,255))
            r = (text.get_rect().x+xdisp, text.get_rect().y+ydisp, text.get_rect().w+20, text.get_rect().h)
            pygame.draw.rect(fenetre, noir, r)
            fenetre.blit(text, (xdisp,ydisp))

        if event.type == MOUSEBUTTONUP and dedans(pygame.mouse.get_pos(), jouer):
            pygame.init()
            fenetre.fill((0,0,0))
            menu = False
            continuer = True
            pygame.mixer.music.stop()
    
            # Chargement et collage du fond + perso
            frame = 0
            """
            arena = pygame.image.load(f"{sprites_dir}/background.png").convert_alpha()
            arena = pygame.transform.scale(arena, (scrwidth,scrheight))
            layer = pygame.image.load(f"{sprites_dir}/layerblit.png").convert_alpha()
            layer = pygame.transform.scale(layer, (scrwidth,scrheight))
            fond = pygame.image.load(f"{sprites_dir}/back.png").convert_alpha()
            fond = pygame.transform.scale(fond, (scrwidth,scrheight))
            perso_up = pygame.image.load(f"{sprites_dir}/move/perso_up.png").convert_alpha()

            fenetre.blit(arena, (xdisp,ydisp))
            fenetre.blit(perso_up, (perso_x,perso_y))

            #perso_run_up = pygame.image.load(f"{sprites_dir}/move/perso_run_up.png").convert_alpha()
            """
            frame_rect = pygame.Rect(frame * WIDTH, 0, h, w)

            clock = pygame.time.Clock()
            

            # Rafraîchissement de l'écran
            pygame.display.flip()

            pygame.key.set_repeat(1,20)

            trigger = 0

        pygame.display.flip()

niveau = 1

arena = 0
echelle=0
layer =0
fond = 0
perso_up =0
perso_run_up = 0

def charge(niveau):
    global ecran, salle, pn, ps
    global echelle, arena, layer,fond, perso_up, perso_run_up, fenetre
    d = f"{sprites_dir}/level{niveau}"
    with open(f"{d}/map.txt", 'r') as map:
        for ligne in map:
            ligne = ligne.rstrip('\n')
            if 'ecran' in ligne: 
                ecran = ligne[ligne.find('=')+1 : len(ligne)].split(',')
                i=0
                for s in range(0, len(ecran)):
                    n = int(ecran[i])
                    ecran[i] = n
                    i=i+1
                #ecran = list(map(int, ecran)) 
            if 'salle' in ligne:
                salle = ligne[ligne.find('=')+1 : len(ligne)].split(',')
                i=0
                for s in range(0, len(salle)):
                    n = int(salle[i])
                    salle[i] = n
                    i=i+1
            if 'porte_nord' in ligne:
                pn = ligne[ligne.find('=')+1 : len(ligne)].split(',')
                i=0
                for s in range(0, len(pn)):
                    n = int(pn[i])
                    pn[i] = n
                    i=i+1
            if 'porte_sud' in ligne:
                ps = ligne[ligne.find('=')+1 : len(ligne)].split(',')
                i=0
                for s in range(0, len(ps)):
                    n = int(ps[i])
                    ps[i] = n
                    i=i+1

    echelle = (ecran[0] / scrwidth , ecran[1] / scrheight)
    arena = pygame.image.load(f"{d}/background.png").convert_alpha()
    arena = pygame.transform.scale(arena, (scrwidth,scrheight))
    layer = pygame.image.load(f"{d}/layerblit.png").convert_alpha()
    layer = pygame.transform.scale(layer, (scrwidth,scrheight))
    fond = pygame.image.load(f"{d}/back.png").convert_alpha()
    fond = pygame.transform.scale(fond, (scrwidth,scrheight))
    perso_up = pygame.image.load(f"{d}/move/perso_up.png").convert_alpha()
    #perso_up = pygame.transform.scale(perso_up, (echelle[0],echelle[1]))
    perso_run_up = pygame.image.load(f"{d}/move/perso_run_up.png").convert_alpha()
    #perso_run_up = pygame.transform.scale(perso_run_up, (echelle[0],echelle[1]))
    fenetre.blit(arena, (xdisp,ydisp))
    fenetre.blit(perso_up, (perso_x,perso_y))

            
while continuer:

    charge(niveau)
     
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            continuer = False

        dt = clock.tick(60) # On ralentit la boucle à 60 FPS
                
        if event.type == KEYDOWN :

            if event.key == K_UP:

                if perso_y >= 490*leng:
                    perso_y -= 8*leng                    
                frame = (frame + 1) % 10
                frame_rect = pygame.Rect(frame * WIDTH, 0, h, w)
                fenetre.blit(arena, xdisp,ydisp)
                fenetre.blit(layer, xdisp,ydisp)
                fenetre.blit(perso_run_up, dest=(perso_x, perso_y), area=frame_rect)

            if event.key == K_DOWN:

                if perso_y <= 904*leng:
                    perso_y += 8*leng
                    
                frame = (frame + 1) % 10
                frame_rect = pygame.Rect(frame * WIDTH, 0, h, w)
                fenetre.blit(arena, (xdisp,ydisp))
                fenetre.blit(layer, (xdisp,ydisp))
                fenetre.blit(perso_run_up, dest=(perso_x, perso_y), area=frame_rect)

            if event.key == K_LEFT:

                if perso_x >= 513*leng:
                    perso_x -= 8*leng
                    
                frame = (frame + 1) % 10
                frame_rect = pygame.Rect(frame * WIDTH, 0, h, w)
                fenetre.blit(arena, (xdisp,ydisp))
                fenetre.blit(layer, (xdisp,ydisp))
                fenetre.blit(perso_run_up, dest=(perso_x, perso_y), area=frame_rect)

            if event.key == K_RIGHT:

                if perso_x <= 1350*leng:
                    perso_x += 8*leng
                    
                frame = (frame + 1) % 10
                frame_rect = pygame.Rect(frame * WIDTH, 0, h, w)
                fenetre.blit(arena, (xdisp,ydisp))
                fenetre.blit(layer, (xdisp,ydisp))
                fenetre.blit(perso_run_up, dest=(perso_x, perso_y), area=frame_rect)
                
        if event.type == KEYUP:

            if event.key == K_UP:
                fenetre.blit(arena, (xdisp,ydisp))
                fenetre.blit(layer, (xdisp,ydisp))
                fenetre.blit(perso_up, (perso_x,perso_y))

            if event.key == K_DOWN:
                fenetre.blit(arena, (xdisp,ydisp))
                fenetre.blit(layer, (xdisp,ydisp))
                fenetre.blit(perso_up, (perso_x,perso_y))

            if event.key == K_LEFT:
                fenetre.blit(arena, (xdisp,ydisp))
                fenetre.blit(layer, (xdisp,ydisp))
                fenetre.blit(perso_up, (perso_x,perso_y))

            if event.key == K_RIGHT:
                fenetre.blit(arena, (xdisp,ydisp))
                fenetre.blit(layer, (xdisp,ydisp))
                fenetre.blit(perso_up, (perso_x,perso_y))
        
        if 900*leng < perso_x < 1020*leng and 480*leng < perso_y < 550*leng and trigger == 0:
            trigger = 1
            pygame.mixer.music.load(f"{path}/Musique/Emerald Dream.wav")
            pygame.mixer.music.play()
            arena = pygame.image.load(f"{sprites_dir}/level1/Hooded_One_arena.png").convert_alpha()
            layer = pygame.image.load(f"{sprites_dir}/level1/Hooded_One_layerblit.png").convert_alpha()
            fond = pygame.image.load(f"{sprites_dir}/level1/Hooded_One_back.png").convert_alpha()
            fenetre.blit(fond, (xdisp,ydisp))
    
    #niveau+=1
    pygame.display.flip()       

pygame.quit()
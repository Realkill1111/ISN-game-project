import pygame
from pygame import *
import os
import tkinter
from threading import Timer


def bouton(fenetre,x, y, w, h, backgroundcolor, texte, textcolor, fnt):
    box = ( (x,y) , (w,h))
    pygame.draw.rect(fenetre, backgroundcolor, box)
    txt = fnt.render(texte, True, textcolor)
    txtpos = txt.get_rect()
    txtpos.x = x+int(w/2) - int(txtpos.width/2)
    txtpos.y = y+int(h/2) - int(txtpos.height/2)
    fenetre.blit(txt, txtpos)
    return ( Rect(x, y, w, h) )

def centering(w,h,img):
    ww=img.get_rect().size
    return (abs(w-ww[0])/2) , (abs(h-ww[1])/2)

def liremap(ligne):
    m=[]
    s = ligne[ligne.find('=')+1 : len(ligne)].split(',')
    for i in s:
        n = int(i)
        m.append(n)
    return m

def dedansPoint(pos, rect) :
    x1 = rect.x
    y1 = rect.y
    x2 = rect.x+rect.w
    y2 = rect.y+rect.h
    if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
        return True
    return False

def dedans(r1, r2):
    r1w = r1.x+r1.w
    r1h = r1.y+r1.h
    r2w = r2.x+r2.w
    r2h = r2.y+r2.h
    if r1.x <= r2.x <= r1w and r1.y <= r2.y <= r1h and r1.x <= r2w <= r1w and r1.y <= r2h <= r1h:
        return True
    return False

def touche(r1,r2):
    r1w = r1.x+r1.w
    r1h = r1.y+r1.h
    r2w = r2.x+r2.w
    r2h = r2.y+r2.h
    print(r1.x , "<=" , r2.x ,'<=', r1w, 'and' ,r1.x , '<=' , r2w , '<=' , r1w , 'and' , r1h ,'>=' , r2.y)
    if r1.x <= r2.x <= r1w and r1.x <= r2w <= r1w and r1h >= r2.y:
        return True
    return False

def coord(pos,orig):
    #posx,posy = pygame.mouse.get_pos()
    fnt = pygame.font.Font("freesansbold.ttf", 24)  # #AnonymousPro-Regular.ttf
    text = fnt.render(f"{pos[0]}, {pos[1]}",1,(255,255,255))
    r = (text.get_rect().x+xdisp, text.get_rect().y+ydisp, text.get_rect().w+20, text.get_rect().h+20)
    pygame.draw.rect(fenetre, noir, r)
    fenetre.blit(text, (xdisp+orig[0],ydisp+orig[1]))

# Detection taille écran
root = tkinter.Tk()
scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
pygame.init()

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((scrwidth, scrheight))

path = os.path.dirname(os.path.abspath(__file__))
combined_size = f"{scrwidth}x{scrheight}"
sprites_dir = f"{path}/sprites"
menu = True
continuer = False

xdisp,ydisp = 0,0

noir  =   0,   0,   0
blanc = 255, 255, 255
rouge = 255,   0,   0
jaune = 255, 220,   0

police = pygame.font.Font('freesansbold.ttf',40)
jouer   = bouton(fenetre, (scrwidth-440)/2, (scrheight-200)/2, 440, 75, rouge, "JOUER"  , jaune, police)
quitter = bouton(fenetre,(scrwidth-440)/2, (scrheight+200)/2, 440, 75, rouge, "QUITTER", jaune, police)

#Rafraîchissement de l'écran
pygame.display.flip()

pygame.mixer.music.load(f"{path}/Musique/twimenu.wav")
posx,posy = pygame.mouse.get_pos()
pygame.mixer.music.play()

menu = False
while menu:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONUP and dedansPoint(pygame.mouse.get_pos(), quitter) ):
            menu = False
            continuer = False
            
        #if event.type == pygame.MOUSEMOTION:

        if event.type == pygame.MOUSEBUTTONUP and dedansPoint(pygame.mouse.get_pos(), jouer):
            pygame.init()
            fenetre.fill((0,0,0))
            menu = False
            continuer = True
            pygame.mixer.music.stop()
    
            # Chargement et collage du fond + perso
            
            clock = pygame.time.Clock()
            

            # Rafraîchissement de l'écran
            pygame.display.flip()

            pygame.key.set_repeat(1,20)

            trigger = 0

        pygame.display.flip()

frame = 0
niveau = 1
arena = 0
echelle=0
layer =0
fond = 0
perso_up =0
perso_run_up = 0
speed = 10
trigger = 0

ecran = []
salle = Rect(0,0,0,0)
pn = Rect(0,0,0,0)
ps = Rect(0,0,0,0)

def charge(niveau):
    global ecran, salle, pn, ps
    global echelle, arena, layer, fond, perso_up, perso_run_up
    d = f"{sprites_dir}/level{niveau}"
    with open(f"{d}/map.txt", 'r') as map:
        for ligne in map:
            ligne = ligne.rstrip('\n')
            if 'ecran' in ligne: 
                ecran = liremap(ligne)
            if 'salle' in ligne:
                msalle=liremap(ligne)
                salle = Rect(msalle[0],msalle[1],msalle[2]-msalle[0],msalle[3]-msalle[1])
            if 'porte_nord' in ligne:
                mpn = liremap(ligne)
                pn = Rect(mpn[0],mpn[1],mpn[2]-mpn[0],mpn[3]-mpn[1])
            if 'porte_sud' in ligne:
                mps = liremap(ligne)
                ps = Rect(mps[0],mps[1],mps[2]-mps[0],mps[3]-mps[1])

    echelle = (scrwidth/ecran[0] , scrheight/ecran[1])
    arena = pygame.image.load(f"{d}/background.png").convert_alpha()
    arena = pygame.transform.scale(arena, (scrwidth,scrheight))
    layer = pygame.image.load(f"{d}/layerblit.png").convert_alpha()
    layer = pygame.transform.scale(layer, (scrwidth,scrheight))
    fond = pygame.image.load(f"{d}/back.png").convert_alpha()
    fond = pygame.transform.scale(fond, (scrwidth,scrheight))
    perso_up = pygame.image.load(f"{d}/move/perso_up.png").convert_alpha()
    perso_run_up = pygame.image.load(f"{d}/move/perso_run_up.png").convert_alpha()

charge(niveau)

pygame.time.Clock().tick(60)
pygame.key.set_repeat(1,10)

perso = Rect(salle.x+salle.w/2,salle.y+salle.h/2,48,52)

continuer = True
while continuer:

    fenetre.blit(arena, (xdisp,ydisp))
    fenetre.blit(layer, (xdisp,ydisp))
    #fenetre.blit(perso_up, ( int(perso.x * echelle[0]), int(perso.y * echelle[1])))
    frame_rect = pygame.Rect(frame * perso.w, 0, perso.h, perso.w)
    fenetre.blit(perso_run_up, dest=( int(perso.x * echelle[0]), int(perso.y * echelle[1])), area=frame_rect)

    for event in pygame.event.get():

        mvtx,mvty = 0,0

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            continuer = False
        
        if event.type == pygame.KEYDOWN :

            if event.key == pygame.K_UP:
                mvty = -speed

            if event.key == pygame.K_DOWN:
                mvty = speed

            if event.key == pygame.K_LEFT:
                mvtx = -speed

            if event.key == pygame.K_RIGHT:
                mvtx = speed

            frame = (frame + 1) % 10

            mvt = Rect(perso.x+mvtx,perso.y+mvty,perso.w,perso.h)
            print('mvt=',mvt)

            if dedans(salle,mvt):
                perso = mvt
            elif mvty == -speed:
                perso = Rect(perso.x,salle.y,perso.w,perso.h)
            elif mvty == speed:
                perso = Rect(perso.x,salle.y+salle.h-perso.h,perso.w,perso.h)
            elif mvtx == -speed:
                perso = Rect(salle.x,perso.y,perso.w,perso.h)
            elif mvtx == speed:
                perso = Rect(salle.x+salle.w-perso.w,perso.y,perso.w,perso.h)

        if touche(pn,perso) and trigger == 0:
            trigger = 1
            pygame.mixer.music.load(f"{path}/Musique/Emerald Dream.wav")
            pygame.mixer.music.play()
            arena = pygame.image.load(f"{sprites_dir}/level1/Hooded_One_arena.png").convert_alpha()
            arena = pygame.transform.scale(arena, (scrwidth,scrheight))
            layer = pygame.image.load(f"{sprites_dir}/level1/Hooded_One_layerblit.png").convert_alpha()
            layer = pygame.transform.scale(layer, (scrwidth,scrheight))
            fond = pygame.image.load(f"{sprites_dir}/level1/Hooded_One_back.png").convert_alpha()
            fond = pygame.transform.scale(fond, (scrwidth,scrheight))
            fenetre.blit(fond, (xdisp,ydisp))

    pygame.display.flip()       

pygame.quit()

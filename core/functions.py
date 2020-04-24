import pygame
from pygame import *
from threading import Thread
from time import sleep
from typing import Union, List, Tuple, Callable


flint = Union[float, int]


def threaded_triggerer(callbacks_list: List[Tuple[flint, Callable]], stop: flint = None, step: flint = None):
    def a(c, stop_, step_):
        t = 1
        for _ in range(round(stop_)):
            for el in c:
                if el[0] <= t:
                    el[1]()
                    del c[c.index(el)]

            sleep(step_)
            t += step_

    # Count
    count = stop if stop else 0
    is_none = stop is None
    for e in callbacks_list:
        if e[0] > count:
            if is_none:
                count = e[0]
            else:
                raise Warning(f'callback at t={e[0]} will be ignored because of stop at t={count}')

    # Step
    step = step if step else 1
    count = count / step

    # Thread
    x = Thread(target=a, args=(callbacks_list, count, step), daemon=True)
    x.start()


def bouton(fenetre, x, y, w, h, backgroundcolor, texte, textcolor, fnt):
    box = ((x, y), (w, h))
    pygame.draw.rect(fenetre, backgroundcolor, box)
    txt = fnt.render(texte, True, textcolor)
    txtpos = txt.get_rect()
    txtpos.x = x + int(w / 2) - int(txtpos.width / 2)
    txtpos.y = y + int(h / 2) - int(txtpos.height / 2)
    fenetre.blit(txt, txtpos)
    return Rect(x, y, w, h)


def centering(w, h, img):
    ww = img.get_rect().size
    return (abs(w - ww[0]) / 2), (abs(h - ww[1]) / 2)


def liremap(ligne):
    m = []
    s = ligne[ligne.find('=') + 1: len(ligne)].split(',')
    for i in s:
        n = int(i)
        m.append(n)
    return m


def dedans_point(pos, rect):
    x1 = rect.x
    y1 = rect.y
    x2 = rect.x + rect.w
    y2 = rect.y + rect.h
    if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
        return True
    return False


def dedans(r1, r2):
    r1w = r1.x + r1.w
    r1h = r1.y + r1.h
    r2w = r2.x + r2.w
    r2h = r2.y + r2.h
    if r1.x <= r2.x <= r1w and r1.y <= r2.y <= r1h and r1.x <= r2w <= r1w and r1.y <= r2h <= r1h:
        return True
    return False


def touche(r1, r2):
    r1w = r1.x + r1.w
    r1h = r1.y + r1.h
    r2w = r2.x + r2.w
    r2h = r2.y + r2.h
    # print(r1.x , "<=" , r2.x ,'<=', r1w, 'and' ,r1.x , '<=' , r2w , '<=' , r1w , 'and' , r1h ,'>=' , r2.y)
    if r1.x <= r2.x <= r1w and r1.x <= r2w <= r1w and r1h >= r2.y:
        return True
    return False


def coord(pos, orig, fenetre, xdisp, ydisp, noir):
    # posx,posy = pygame.mouse.get_pos()
    fnt = pygame.font.Font("freesansbold.ttf", 24)  # #AnonymousPro-Regular.ttf
    text = fnt.render(f"{pos[0]}, {pos[1]}", 1, (255, 255, 255))
    r = (text.get_rect().x + xdisp, text.get_rect().y + ydisp, text.get_rect().w + 20, text.get_rect().h + 20)
    pygame.draw.rect(fenetre, noir, r)
    fenetre.blit(text, (xdisp + orig[0], ydisp + orig[1]))

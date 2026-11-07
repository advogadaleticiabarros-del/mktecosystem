"""Blocos centralizados da versão 2 dos Reels do 13º (aprovada em 06/11/2026: "Aprovadíssimo, com ritmo maravilhoso").
Tudo no eixo x=540, igual à legenda; fotos com rosto ganham desfoque e véu mais escuro; efeitos sonoros v2."""
import motor as m
import som2
from motor import carimbo, centro, kick, pilula, texto

m.sfx = lambda pasta: som2.efeitos_v2(m.AQUI / "sfx2")

CX = 540
VEU_ROSTO = "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.62) 45%, rgba(26,21,17,.92))"


def kc(txt, at, top=350):
    return kick(txt, at, top=top, style=centro(800))


def pc(txt, at, top, w=560, **st):
    return pilula(txt, at, top, style={**centro(w), **st})


def tc(html, at, top, size=110, **kw):
    return texto(html, at, top, size=size, align="center", **kw)


def cc(txt, at, top, size=76, rot=-4):
    w = len(txt) * size * 0.66 + 70
    return carimbo(txt, at, top, int((1080 - w) / 2), rot=rot, size=size)

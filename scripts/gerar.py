"""Gera os SVGs do perfil (assets/). Rodar da raiz do repositório: python scripts/gerar.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = '"Segoe UI",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif'
MONO = '"Cascadia Code",SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace'
# roxo: fundo, pontos, destaque, destaque claro, texto, texto secundário, apagado, rosa
C = dict(bg0="#0b0618", bg1="#160c30", bg2="#2a1452", ponto="#3b2466", ac="#a78bfa", ac2="#c4b5fd",
         txt="#f5f0ff", sub="#c9bde6", mudo="#8a7aab", rosa="#f0abfc", borda="#2e1d55")
ESTILO = f"<style>.s{{font-family:{SANS}}}.m{{font-family:{MONO}}}</style>"


def grava(nome, w, h, corpo, rotulo):
    OUT.mkdir(exist_ok=True)
    (OUT / nome).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{rotulo}">'
        f"{ESTILO}{corpo}</svg>\n", encoding="utf-8")


def fundo(w, h, gid, cx="85%", cy="15%"):
    return (f'<defs><radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="95%"><stop offset="0" stop-color="{C["bg2"]}"/>'
            f'<stop offset=".45" stop-color="{C["bg1"]}"/><stop offset="1" stop-color="{C["bg0"]}"/></radialGradient>'
            f'<pattern id="{gid}p" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{C["ponto"]}"/></pattern>'
            f'<clipPath id="{gid}c"><rect width="{w}" height="{h}" rx="18"/></clipPath></defs>'
            f'<g clip-path="url(#{gid}c)"><rect width="{w}" height="{h}" fill="url(#{gid})"/>'
            f'<rect width="{w}" height="{h}" fill="url(#{gid}p)" opacity=".5"/></g>')


def cabecalho():
    w, h = 1040, 250
    frases = ["APIs com FastAPI e PostgreSQL", "Interfaces em React + TypeScript", "LLMs aplicados a produtos reais"]
    CH, X0, Y, DUR = 13.2, 92, 206, 12   # largura do caractere a 22px, início e baseline da linha digitada
    partes = []
    for k, f in enumerate(frases):
        s = k / len(frases)
        a, b, c, d = s, s + 1.6/DUR, s + 3.4/DUR, s + 3.8/DUR
        lw = len(f) * CH + 2
        if k == 0:
            kt, vw = f"0;{b:.4f};{c:.4f};{d:.4f};1", f"0;{lw:.1f};{lw:.1f};0;0"
        else:
            kt, vw = f"0;{a:.4f};{b:.4f};{c:.4f};{d:.4f};1", f"0;0;{lw:.1f};{lw:.1f};0;0"
        vx = ";".join(f"{X0+float(v)+2:.1f}" for v in vw.split(";"))
        partes.append(
            f'<clipPath id="t{k}"><rect x="{X0}" y="{Y-24}" height="34" width="0">'
            f'<animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" keyTimes="{kt}" values="{vw}"/></rect></clipPath>'
            f'<text x="{X0}" y="{Y}" textLength="{len(f)*CH:.1f}" lengthAdjust="spacing" class="m" font-size="22" fill="{C["txt"]}" clip-path="url(#t{k})">{f}</text>'
            f'<rect y="{Y-19}" width="11" height="24" fill="{C["ac"]}" x="{X0}">'
            f'<animate attributeName="x" dur="{DUR}s" repeatCount="indefinite" keyTimes="{kt}" values="{vx}"/>'
            f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{a:.4f};{min(s+4/DUR, 1):.4f}" values="0;1;0"/></rect>')
    nos = [(780, 62, 7), (870, 112, 9), (830, 192, 7), (950, 82, 6), (985, 178, 8), (905, 222, 6), (745, 150, 6)]
    arestas = [(0, 1), (1, 2), (1, 3), (3, 4), (2, 5), (4, 5), (6, 2), (6, 0)]
    ar = "".join(f'<line x1="{nos[i][0]}" y1="{nos[i][1]}" x2="{nos[j][0]}" y2="{nos[j][1]}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
                 f'<animate attributeName="stroke-dashoffset" values="1;0" dur="1.2s" begin="{0.15*k:.2f}s"/></line>' for k, (i, j) in enumerate(arestas))
    no = "".join(f'<circle cx="{x}" cy="{y}" r="{r}"><animate attributeName="r" values="{r};{r*1.45:.1f};{r}" dur="{2.4+0.35*k:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="1;.55;1" dur="{2.4+0.35*k:.2f}s" repeatCount="indefinite"/></circle>' for k, (x, y, r) in enumerate(nos))
    corpo = (fundo(w, h, "hd") +
             f'<g stroke="{C["ac"]}" stroke-width="1.6" opacity=".45">{ar}</g><g fill="{C["ac"]}">{no}</g>'
             f'<text x="66" y="70" class="m" font-size="17" fill="{C["ac"]}">~/luizfsjunior</text>'
             f'<text x="64" y="124" class="s" font-size="46" font-weight="700" fill="{C["txt"]}">Luiz Fernando</text>'
             f'<text x="66" y="162" class="s" font-size="22" fill="{C["sub"]}">Desenvolvedor <tspan fill="{C["ac2"]}" font-weight="600">Full Stack</tspan>'
             f' · Python &amp; <tspan fill="{C["ac2"]}" font-weight="600">IA aplicada</tspan></text>'
             f'<text x="66" y="{Y}" class="m" font-size="22" fill="{C["rosa"]}">&gt;</text>' + "".join(partes))
    grava("header.svg", w, h, corpo, "Luiz Fernando, Desenvolvedor Full Stack, Python e IA aplicada")


def divisoria(nome, n, titulo):
    w, h = 1040, 36
    rotulo = f"// {n} · {titulo}"
    x = 4 + len(rotulo) * 9.0 + 14   # largura aproximada do rótulo mono a 15px
    corpo = (f'<text x="4" y="24" class="m" font-size="15"><tspan fill="{C["rosa"]}">//</tspan>'
             f'<tspan fill="{C["mudo"]}"> {n} · </tspan><tspan fill="{C["ac2"]}">{titulo}</tspan></text>'
             f'<text x="{x:.0f}" y="24" class="m" font-size="15" fill="{C["borda"]}" textLength="{w-x-4:.0f}" lengthAdjust="spacingAndGlyphs">'
             f'{"─" * 70}</text>')
    grava(nome, w, h, corpo, f"Seção {n}: {titulo}")


def painel_anamnesia():
    """Card compacto: o produto à esquerda, um trecho de entrevista à direita."""
    w, h = 1040, 190
    o = [fundo(w, h, "an", cx="80%", cy="30%"),
         f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{C["borda"]}"/>',
         f'<text x="40" y="58" class="m" font-size="13" fill="{C["mudo"]}"><tspan fill="#4ade80">●</tspan> no ar · anamnes-ia.vercel.app'
         f'<animate attributeName="opacity" values="1;.6;1" dur="2.4s" repeatCount="indefinite"/></text>',
         f'<text x="38" y="104" class="s" font-size="38" font-weight="700" fill="{C["txt"]}">Anamnes.ia</text>',
         f'<text x="40" y="136" class="s" font-size="16.5" fill="{C["sub"]}">Estudantes de medicina treinam anamnese</text>',
         f'<text x="40" y="159" class="s" font-size="16.5" fill="{C["sub"]}">conversando com um paciente simulado por IA.</text>']
    falas = [("aluno", "O que trouxe você aqui hoje?"), ("paciente", "Uma dor no peito que começou há 3 dias.")]
    px, pw, DUR = 560, 440, 8
    for i, (quem, txt) in enumerate(falas):
        bw = len(txt) * 7.6 + 26
        y = 46 + i * 44
        x = px + pw - bw if quem == "aluno" else px
        cor, fill = (C["ac2"], C["bg2"]) if quem == "aluno" else (C["sub"], C["bg1"])
        t0 = 0.06 + i * 0.18
        # sem animação a fala fica visível; com animação ela entra em sequência
        o.append(f'<g><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.2f};{t0+.05:.2f};.93;1" dur="{DUR}s" repeatCount="indefinite"/>'
                 f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="32" rx="11" fill="{fill}" stroke="{cor}" stroke-opacity=".45"/>'
                 f'<text x="{x+13:.0f}" y="{y+20.5}" class="m" font-size="12.5" fill="{cor}">{txt}</text></g>')
    y, t0 = 46 + 2 * 44, 0.06 + 2 * 0.18
    o.append(f'<g><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.2f};{t0+.05:.2f};.93;1" dur="{DUR}s" repeatCount="indefinite"/>'
             f'<rect x="{px+pw-64}" y="{y}" width="64" height="32" rx="11" fill="{C["bg2"]}" stroke="{C["ac2"]}" stroke-opacity=".45"/>'
             + "".join(f'<circle cx="{px+pw-44+j*12}" cy="{y+16}" r="3.2" fill="{C["ac2"]}"><animate attributeName="opacity" values=".25;1;.25" dur="1.1s" begin="{j*.18:.2f}s" repeatCount="indefinite"/></circle>' for j in range(3))
             + "</g>")
    grava("anamnesia.svg", w, h, "".join(o),
          "Anamnes.ia, no ar em anamnes-ia.vercel.app: estudantes de medicina treinam anamnese conversando com um paciente simulado por IA.")


def botao(nome, texto, icone, largura):
    w, h = largura, 44
    corpo = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["bg2"]}"/><stop offset="1" stop-color="{C["bg1"]}"/></linearGradient></defs>'
             f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="url(#g)" stroke="{C["ac"]}" stroke-opacity=".55"/>'
             f'<g transform="translate(16,12)">{icone}</g>'
             f'<text x="46" y="27.5" class="m" font-size="14" fill="{C["txt"]}">{texto}</text>')
    grava(nome, w, h, corpo, texto)


ICONE_LINKEDIN = (f'<rect width="20" height="20" rx="4" fill="{C["ac"]}"/>'
                  f'<text x="10" y="15" class="s" font-size="13" font-weight="700" text-anchor="middle" fill="{C["bg0"]}">in</text>')
ICONE_EMAIL = (f'<rect y="2" width="20" height="16" rx="3" fill="none" stroke="{C["ac"]}" stroke-width="1.8"/>'
               f'<path d="M1.5 4 L10 11 L18.5 4" fill="none" stroke="{C["ac"]}" stroke-width="1.8" stroke-linejoin="round"/>')


if __name__ == "__main__":
    cabecalho()
    painel_anamnesia()
    botao("btn-linkedin.svg", "in/luizfsjunior", ICONE_LINKEDIN, 196)
    botao("btn-email.svg", "luizfsjunior.2002@gmail.com", ICONE_EMAIL, 300)
    for arq, n, titulo in [("sec-agora.svg", "01", "agora"), ("sec-projetos.svg", "02", "projetos"),
                           ("sec-stack.svg", "03", "stack"), ("sec-contato.svg", "04", "contato")]:
        divisoria(arq, n, titulo)

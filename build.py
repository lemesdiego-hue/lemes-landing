#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador das landing pages otimizadas da Lemes Advogados.
Fonte única de verdade: CSS, template e conteúdo de cada página ficam aqui.
Rode:  python3 build.py
Saída: trabalhista.html, civel.html, divorcio.html, inventario.html,
       aereo.html, previdenciario.html, schema-markup.json, home-meta-tags.txt
"""
import json, pathlib
from string import Template

OUT = pathlib.Path(__file__).resolve().parent
WHATS = "https://wa.me/5511995155021?text=Ol%C3%A1%2C%20vim%20pelo%20site%20e%20gostaria%20de%20uma%20consulta"
# Domínio onde as páginas efetivamente ficam hospedadas (landing). O schema/marca
# continua apontando para o site institucional (NAP['url']).
LANDING = "https://landing.lemesadvogados.com"
# ID do Google Ads — embutido em todas as páginas (a landing não tem injeção via Wix).
ADS_ID = "AW-993352616"

# ---- NAP (Name / Address / Phone) — idêntico em todas as páginas (SEO local) ----
NAP = {
    "name": "Lemes Sociedade Individual de Advogados",
    "short": "Lemes Advogados",
    "phone_display": "(11) 99515-5021",
    "phone_tel": "+5511995155021",
    "email": "diego@lemesadvogados.com",
    "street": "Rua Coronel Melo de Oliveira, 557",
    "district": "Perdizes",
    "city": "São Paulo",
    "region": "SP",
    "cep": "05011-040",
    "cnpj": "25.385.186/0001-75",
    "oab": "OAB/SP 255.888",
    "lawyer": "Diego Henrique Lemes",
    "hours": "Seg–Sex, 9h às 18h",
    "url": "https://www.lemesadvogados.com",
}

PRACTICES = [
    ("trabalhista",   "Trabalhista"),
    ("civel",         "Cível"),
    ("divorcio",      "Divórcio"),
    ("inventario",    "Inventário"),
    ("aereo",         "Direito Aéreo"),
    ("previdenciario","Previdenciário"),
]

# ============================================================================ #
#  CSS — sistema de design "Dossiê" (papel / tinta / carimbo / verde-deferido)
#  Inline em cada página para portabilidade e velocidade (1 requisição a menos).
# ============================================================================ #
CSS = r"""
:root{
 --paper:#ECE9E1;--paper2:#E4E0D5;--ink:#1B2420;--ink2:#3C453F;
 --carimbo:#BE3A2B;--ledger:#2E6B52;--muted:#76715F;
 --line:rgba(27,36,32,.16);--line2:rgba(27,36,32,.09);
 --display:"Archivo",system-ui,sans-serif;--body:"Spectral",Georgia,serif;
 --mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;
 --s-1:clamp(.78rem,.76rem + .1vw,.84rem);--s0:clamp(1rem,.97rem + .15vw,1.1rem);
 --s1:clamp(1.18rem,1.1rem + .35vw,1.35rem);--s2:clamp(1.45rem,1.3rem + .7vw,1.85rem);
 --s3:clamp(1.85rem,1.5rem + 1.6vw,2.7rem);--s4:clamp(2.3rem,1.7rem + 2.8vw,3.8rem);
 --gutter:clamp(1.15rem,5vw,4rem);--maxw:1140px;--radius:3px;
}
*,*::before,*::after{box-sizing:border-box;margin:0}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation-duration:.001ms!important;transition-duration:.001ms!important}}
body{background:var(--paper);color:var(--ink);font-family:var(--body);font-size:var(--s0);line-height:1.62;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:hidden}
img{display:block;max-width:100%}a{color:inherit}
:focus-visible{outline:2.5px solid var(--carimbo);outline-offset:3px}
.wrap{width:100%;max-width:var(--maxw);margin-inline:auto;padding-inline:var(--gutter)}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
h1,h2,h3{font-family:var(--display);text-transform:uppercase;line-height:1.02;letter-spacing:-.01em}
.eyebrow{font-family:var(--mono);font-size:var(--s-1);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);overflow-wrap:anywhere}
.eyebrow::before{content:"";display:inline-block;width:1.6em;height:1px;background:currentColor;vertical-align:middle;margin-right:.6em;opacity:.7}
.section{padding-block:clamp(3rem,7vw,5.5rem)}
.lead{font-size:var(--s1);color:var(--ink2);max-width:60ch}
/* header */
.bar{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--paper) 90%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar__in{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:.7rem}
.brand{display:flex;align-items:baseline;gap:.5rem;text-decoration:none;font-family:var(--display);font-weight:800;letter-spacing:.04em;font-size:var(--s1);text-transform:uppercase}
.brand span{font-family:var(--mono);font-size:.58em;letter-spacing:.14em;color:var(--muted);font-weight:400}
.bar__phone{display:none;font-family:var(--mono);font-size:var(--s-1);letter-spacing:.06em;color:var(--ink2)}
@media(min-width:760px){.bar__phone{display:block}}
/* botões */
.btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--display);font-weight:700;font-size:var(--s0);letter-spacing:.02em;text-decoration:none;color:#fff;background:var(--ledger);border:1px solid var(--ledger);padding:.8em 1.3em;border-radius:var(--radius);cursor:pointer;transition:transform .16s,box-shadow .16s;box-shadow:4px 4px 0 var(--ink)}
.btn:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 var(--ink)}
.btn:active{transform:translate(2px,2px);box-shadow:1px 1px 0 var(--ink)}
.btn svg{width:1.1em;height:1.1em}
.btn--ink{background:var(--ink);border-color:var(--ink)}
.btn--ghost{background:transparent;color:var(--ink);border-color:var(--line);box-shadow:none}
.btn--ghost:hover{transform:none;box-shadow:none;background:var(--paper2);border-color:var(--ink)}
.btn--lite{background:var(--paper);color:var(--ink);border-color:var(--paper);box-shadow:4px 4px 0 rgba(0,0,0,.3)}
.btn--lite:hover{box-shadow:6px 6px 0 rgba(0,0,0,.3)}
/* hero */
.hero{padding-top:clamp(2.2rem,5vw,4rem);padding-bottom:clamp(1.5rem,4vw,3rem)}
.hero h1{font-weight:900;font-size:var(--s4);overflow-wrap:break-word}
.hero .lead{margin-top:1.3rem}
.cta{display:flex;flex-wrap:wrap;gap:.8rem;align-items:center;margin-top:1.8rem}
.hero__note{font-family:var(--mono);font-size:var(--s-1);color:var(--muted);margin-top:.9rem}
.trust{display:flex;flex-wrap:wrap;gap:.5rem 1.4rem;margin-top:2rem;padding-top:1.3rem;border-top:1px solid var(--line);font-family:var(--mono);font-size:var(--s-1);letter-spacing:.04em;color:var(--ink2)}
.trust b{color:var(--carimbo);font-weight:700}
/* cards */
.h2wrap{max-width:54ch}
.h2wrap h2{font-weight:800;font-size:var(--s3);margin-top:.6rem}
.h2wrap p{margin-top:.9rem;color:var(--ink2)}
.cards{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:clamp(1.8rem,4vw,2.6rem);border-radius:var(--radius);overflow:hidden}
@media(min-width:640px){.cards{grid-template-columns:1fr 1fr}}
@media(min-width:980px){.cards--3{grid-template-columns:1fr 1fr 1fr}}
.card{background:var(--paper);padding:clamp(1.3rem,2.5vw,1.8rem);display:block;text-decoration:none}
.card:hover{background:var(--paper2)}
.card h3{font-weight:800;font-size:var(--s1);margin-bottom:.5rem}
.card p{color:var(--ink2);font-size:var(--s0)}
.card__more{display:inline-block;margin-top:.7rem;font-family:var(--mono);font-size:var(--s-1);color:var(--carimbo);letter-spacing:.06em}
/* blocos de conteúdo (texto rastreável) */
.prose h2{font-weight:800;font-size:var(--s2);margin-top:clamp(2.2rem,4vw,3rem)}
.prose h2:first-child{margin-top:0}
.prose p{margin-top:1rem;max-width:68ch}
.prose ul{margin-top:1rem;max-width:68ch;padding-left:1.1rem}
.prose li{margin-top:.45rem}
.prose strong{color:var(--ink)}
/* faixa escura: passos */
.dark{background:var(--ink);color:var(--paper)}
.dark .eyebrow{color:rgba(236,233,225,.6)}.dark .eyebrow::before{background:rgba(236,233,225,.6)}
.steps{display:grid;gap:clamp(1.3rem,3vw,2.4rem);grid-template-columns:1fr;margin-top:clamp(1.8rem,4vw,2.6rem)}
@media(min-width:740px){.steps{grid-template-columns:repeat(3,1fr)}}
.step{border-top:1px solid rgba(236,233,225,.25);padding-top:1.2rem}
.step .n{font-family:var(--mono);font-size:var(--s2);color:#8FD3B0;font-weight:700}
.step h3{font-weight:700;font-size:var(--s1);margin:.7rem 0 .5rem}
.step p{color:rgba(236,233,225,.8)}
/* faixa carimbo: CTA */
.band{background:var(--carimbo);color:#fff}
.band__in{display:grid;gap:1.4rem;grid-template-columns:1fr;align-items:center}
@media(min-width:820px){.band__in{grid-template-columns:1.5fr auto}}
.band h2{font-weight:800;font-size:var(--s3)}
.band p{margin-top:.7rem;font-size:var(--s1);color:rgba(255,255,255,.92);max-width:48ch}
/* FAQ — nativo, rastreável, sem JS */
.faq{margin-top:clamp(1.8rem,4vw,2.6rem);border-top:2px solid var(--ink)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;cursor:pointer;padding:1.15rem 2.2rem 1.15rem 0;position:relative;font-family:var(--display);font-weight:700;font-size:var(--s1);text-transform:none;letter-spacing:0}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:.2rem;top:1rem;font-family:var(--mono);font-size:1.5rem;color:var(--carimbo);transition:transform .2s}
.faq details[open] summary::after{content:"\2013"}
.faq__a{padding:0 0 1.3rem;max-width:72ch;color:var(--ink2)}
.faq__a p+p{margin-top:.8rem}
/* sobre / E-E-A-T */
.about{display:grid;gap:1.5rem;grid-template-columns:1fr;align-items:center;border:1px solid var(--line);border-radius:var(--radius);background:var(--paper2);padding:clamp(1.5rem,3.5vw,2.4rem)}
@media(min-width:720px){.about{grid-template-columns:auto 1fr}}
.about__sig{font-family:var(--display);font-weight:900;font-size:var(--s2);text-transform:uppercase;line-height:1;padding-right:1.5rem}
@media(min-width:720px){.about__sig{border-right:1px solid var(--line)}}
.about__sig span{display:block;font-family:var(--mono);font-size:var(--s-1);font-weight:400;color:var(--muted);letter-spacing:.08em;margin-top:.5rem}
.about p{color:var(--ink2)}.about p+p{margin-top:.8rem}
/* contato + formulário */
.contact{display:grid;gap:clamp(1.8rem,4vw,3rem);grid-template-columns:1fr}
@media(min-width:860px){.contact{grid-template-columns:1.05fr .95fr}}
.contact h2{font-weight:800;font-size:var(--s3)}
.napcard{margin-top:1.4rem;font-family:var(--mono);font-size:var(--s0);line-height:1.9;color:var(--ink2)}
.napcard a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.form{background:var(--paper2);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(1.4rem,3vw,2rem)}
.form h3{font-weight:700;font-size:var(--s1);text-transform:none;letter-spacing:0;margin-bottom:1rem}
.field{margin-bottom:.95rem}
.field label{display:block;font-family:var(--mono);font-size:var(--s-1);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:.35rem}
.field input,.field textarea{width:100%;font-family:var(--body);font-size:var(--s0);color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:.7em .8em}
.field textarea{min-height:96px;resize:vertical}
.form .btn{width:100%;justify-content:center;margin-top:.4rem}
.form small{display:block;margin-top:.8rem;color:var(--muted);font-size:var(--s-1)}
/* footer */
.foot{background:var(--ink);color:var(--paper);padding-block:clamp(2.8rem,6vw,4.5rem)}
.foot__grid{display:grid;gap:2.2rem;grid-template-columns:1fr}
@media(min-width:760px){.foot__grid{grid-template-columns:1.4fr 1fr 1fr}}
.foot h2{font-weight:900;font-size:var(--s2);letter-spacing:.02em}
.foot h4{font-family:var(--mono);font-size:var(--s-1);letter-spacing:.12em;text-transform:uppercase;color:#8FD3B0;margin-bottom:.9rem;font-weight:700}
.foot a,.foot p{color:rgba(236,233,225,.82);text-decoration:none;display:block;margin-bottom:.45rem;font-size:var(--s0)}
.foot a:hover{color:#fff;text-decoration:underline;text-underline-offset:3px}
.foot__legal{margin-top:2.4rem;padding-top:1.4rem;border-top:1px solid rgba(236,233,225,.16);font-size:var(--s-1);color:rgba(236,233,225,.55);line-height:1.55;max-width:90ch}
/* FAB */
.fab{position:fixed;right:clamp(.9rem,3vw,1.8rem);bottom:clamp(.9rem,3vw,1.8rem);z-index:60;display:inline-flex;align-items:center;gap:.5em;background:var(--ledger);color:#fff;padding:.75em 1.05em;border-radius:100px;text-decoration:none;font-family:var(--display);font-weight:700;box-shadow:0 8px 24px rgba(27,36,32,.28)}
.fab:hover{transform:translateY(-3px)}.fab span{display:none}
@media(min-width:520px){.fab span{display:inline}}
@media(max-width:560px){.hero .cta .btn{width:100%;justify-content:center}.band .btn{width:100%;justify-content:center}}
"""

JS = r"""
(function(){"use strict";
 var Z="https://wa.me/5511995155021";
 // formulário -> WhatsApp (CTA secundário funciona sem backend)
 var f=document.getElementById("leadform");
 if(f){f.addEventListener("submit",function(e){e.preventDefault();
  var n=(f.nome.value||"").trim(),c=(f.contato.value||"").trim(),m=(f.msg.value||"").trim();
  var t="Olá! Meu nome é "+n+". "+(m||"Gostaria de uma consulta.")+(c?" Meu contato: "+c+".":"");
  window.open(Z+"?text="+encodeURIComponent(t),"_blank","noopener");
 });}
})();
"""

# Ícone WhatsApp (SVG inline, leve)
ZAP_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.5 23.5l1.6-5.8A11.4 11.4 0 1 1 12 23.4a11.5 11.5 0 0 1-5.5-1.4L.5 23.5zM6.8 20l.4.2a9.5 9.5 0 1 0-3.2-3.2l.2.4-1 3.5 3.6-.9z"/></svg>')

# ============================================================================ #
#  Helpers de renderização
# ============================================================================ #
def esc(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def cards_html(cards, three=False):
    cls = "cards cards--3" if three else "cards"
    items = []
    for c in cards:
        href = c.get("href")
        more = '<span class="card__more">Saiba mais &rarr;</span>' if href else ""
        tag = "a" if href else "div"
        attr = f' href="{href}"' if href else ""
        items.append(f'<{tag} class="card"{attr}><h3>{esc(c["t"])}</h3><p>{esc(c["d"])}</p>{more}</{tag}>')
    return f'<div class="{cls}">' + "".join(items) + "</div>"

def prose_html(blocks):
    out = []
    for b in blocks:
        out.append(f'<h2>{esc(b["h2"])}</h2>')
        for p in b.get("p", []):
            out.append(f"<p>{p}</p>")  # p pode conter <strong>/<a> intencionais
        if b.get("ul"):
            out.append("<ul>" + "".join(f"<li>{li}</li>" for li in b["ul"]) + "</ul>")
    return "\n".join(out)

def steps_html(steps):
    out = []
    for i, s in enumerate(steps, 1):
        out.append(f'<div class="step"><p class="n">0{i}</p><h3>{esc(s["t"])}</h3><p>{esc(s["d"])}</p></div>')
    return '<div class="steps">' + "".join(out) + "</div>"

def faq_html(faqs):
    out = ['<div class="faq">']
    for q in faqs:
        ans = "".join(f"<p>{p}</p>" for p in q["a"])
        out.append(f'<details><summary>{esc(q["q"])}</summary><div class="faq__a">{ans}</div></details>')
    out.append("</div>")
    return "".join(out)

def footer_links():
    return "".join(f'<a href="/{slug}">{label}</a>' for slug, label in PRACTICES)

def schema_for(page):
    legal = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "@id": f"{NAP['url']}/{page['slug']}#legalservice",
        "name": NAP["name"],
        "description": page["meta"],
        "url": f"{NAP['url']}/{page['slug']}",
        "telephone": "+55-11-99515-5021",
        "email": NAP["email"],
        "priceRange": "$$",
        "openingHours": "Mo-Fr 09:00-18:00",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": NAP["street"],
            "addressLocality": f"{NAP['district']}, {NAP['city']}",
            "addressRegion": NAP["region"],
            "postalCode": NAP["cep"],
            "addressCountry": "BR",
        },
        "areaServed": "São Paulo, SP",
        "knowsAbout": page["knows"],
        "founder": {"@type": "Person", "name": NAP["lawyer"], "jobTitle": "Advogado", "identifier": NAP["oab"]},
        "sameAs": ["https://www.linkedin.com/in/diego-henrique-lemes-8882b0/"],
    }
    faqpage = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q["q"],
             "acceptedAnswer": {"@type": "Answer", "text": " ".join(_strip(p) for p in q["a"])}}
            for q in page["faqs"]
        ],
    }
    return legal, faqpage

def _strip(s):
    import re
    return re.sub("<[^>]+>", "", s)

# ============================================================================ #
#  Template da página
# ============================================================================ #
TPL = Template(r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<meta name="description" content="$meta">
<link rel="canonical" href="$canonical">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lemes Advogados">
<meta property="og:title" content="$title">
<meta property="og:description" content="$meta">
<meta property="og:url" content="$canonical">
<meta property="og:locale" content="pt_BR">
<meta name="geo.region" content="BR-SP">
<meta name="geo.placename" content="São Paulo">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=Spectral:wght@400;500;600&display=swap" rel="stylesheet">
<!-- Google tag (gtag.js) — Google Ads -->
<script async src="https://www.googletagmanager.com/gtag/js?id=$ads_id"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', '$ads_id');
</script>
<style>$css</style>
<script type="application/ld+json">$schema</script>
</head>
<body>
<header class="bar">
 <div class="wrap bar__in">
  <a class="brand" href="/" aria-label="Lemes Advogados — início"><b>Lemes</b><span>Advogados</span></a>
  <a class="bar__phone" href="tel:$phone_tel">$phone_display</a>
  <a class="btn" href="$whats" target="_blank" rel="noopener">$zap WhatsApp</a>
 </div>
</header>

<main>
 <!-- HERO -->
 <section class="hero wrap" aria-labelledby="h1">
  <p class="eyebrow">$eyebrow</p>
  <h1 id="h1">$h1</h1>
  <p class="lead">$hero_sub</p>
  <div class="cta">
   <a class="btn" href="$whats" target="_blank" rel="noopener">$zap Falar agora no WhatsApp</a>
   <a class="btn--ghost btn" href="#contato">Enviar mensagem</a>
  </div>
  <p class="hero__note">$hero_note</p>
  <div class="trust">
   <span>$lawyer · <b>$oab</b></span><span>$district, $city/$region</span><span>$hours</span>
  </div>
 </section>

 <!-- SITUAÇÕES / SERVIÇOS -->
 <section class="section wrap">
  <div class="h2wrap"><p class="eyebrow">$sit_eyebrow</p><h2>$sit_h2</h2><p>$sit_sub</p></div>
  $cards
 </section>

 <!-- CONTEÚDO RASTREÁVEL -->
 <section class="section wrap prose">
  $prose
 </section>

 <!-- PASSOS -->
 <section class="section dark">
  <div class="wrap">
   <div class="h2wrap"><p class="eyebrow">Como funciona</p><h2 style="color:var(--paper)">$steps_h2</h2></div>
   $steps
  </div>
 </section>

 <!-- FAQ -->
 <section class="section wrap">
  <div class="h2wrap"><p class="eyebrow">Dúvidas frequentes</p><h2>$faq_h2</h2></div>
  $faq
 </section>

 <!-- FAIXA CTA -->
 <section class="section band">
  <div class="wrap band__in">
   <div><h2>$band_h2</h2><p>$band_sub</p></div>
   <a class="btn btn--lite" href="$whats" target="_blank" rel="noopener">$zap Falar no WhatsApp</a>
  </div>
 </section>

 <!-- SOBRE / E-E-A-T -->
 <section class="section wrap">
  <div class="about">
   <p class="about__sig">Diego H. Lemes<span>$oab · $name</span></p>
   <div>
    <p>Atendimento conduzido pelo próprio advogado, do primeiro contato ao desfecho. $about_line</p>
    <p>Escritório em $district, $city, com atuação em todo o estado de $region. CNPJ $cnpj.</p>
   </div>
  </div>
 </section>

 <!-- CONTATO + FORMULÁRIO -->
 <section class="section wrap" id="contato">
  <div class="contact">
   <div>
    <p class="eyebrow">Fale com a Lemes</p>
    <h2>$contact_h2</h2>
    <p class="lead" style="margin-top:1rem">A primeira conversa é sem compromisso. Explico com clareza se há o que fazer e qual o próximo passo.</p>
    <div class="napcard">
     $name<br>
     $street — $district<br>
     $city/$region · CEP $cep<br>
     WhatsApp / Tel: <a href="$whats" target="_blank" rel="noopener">$phone_display</a><br>
     E-mail: <a href="mailto:$email">$email</a><br>
     $hours
    </div>
   </div>
   <form class="form" id="leadform">
    <h3>Conte seu caso</h3>
    <div class="field"><label for="nome">Seu nome</label><input id="nome" name="nome" type="text" required autocomplete="name"></div>
    <div class="field"><label for="contato">Telefone ou e-mail</label><input id="contato" name="contato" type="text" autocomplete="tel"></div>
    <div class="field"><label for="msg">Resumo do seu caso</label><textarea id="msg" name="msg"></textarea></div>
    <button class="btn" type="submit">$zap Enviar pelo WhatsApp</button>
    <small>Ao enviar, você abre uma conversa no WhatsApp com os dados preenchidos. Suas informações não são compartilhadas com terceiros.</small>
   </form>
  </div>
 </section>
</main>

<footer class="foot">
 <div class="wrap foot__grid">
  <div>
   <h2>$name</h2>
   <p style="margin-top:.8rem">Advocacia em $district, $city. Atendimento humano, linguagem clara e foco em resolver o seu caso.</p>
  </div>
  <div>
   <h4>Áreas de atuação</h4>
   $footer_links
  </div>
  <div>
   <h4>Contato</h4>
   <a href="$whats" target="_blank" rel="noopener">WhatsApp $phone_display</a>
   <a href="mailto:$email">$email</a>
   <p>$street</p>
   <p>$district, $city/$region · $cep</p>
   <a href="https://www.linkedin.com/in/diego-henrique-lemes-8882b0/" target="_blank" rel="noopener">LinkedIn</a>
  </div>
 </div>
 <div class="wrap">
  <p class="foot__legal">$name · $cnpj · Advogado responsável: $lawyer ($oab).<br>
  Conteúdo de caráter exclusivamente informativo, em conformidade com o Código de Ética e Disciplina da OAB e o Provimento nº 205/2021. Não constitui oferta de serviços, captação de clientela nem promessa de resultado. Cada caso é analisado individualmente.</p>
 </div>
</footer>

<a class="fab" href="$whats" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">$zap<span>Fale conosco</span></a>
<script>$js</script>
</body>
</html>
""")

# ============================================================================ #
#  CONTEÚDO DE CADA PÁGINA
# ============================================================================ #
PAGES = {}

PAGES["trabalhista"] = {
 "slug":"trabalhista",
 "title":"Advogado Trabalhista em SP | Cálculo de Rescisão | Lemes",
 "meta":"Foi demitido ou tem horas extras não pagas? Calcule sua rescisão e fale com advogado trabalhista em São Paulo pelo WhatsApp. Atendimento direto.",
 "h1":"Advogado Trabalhista em São Paulo",
 "hero_sub":"Foi demitido, está com horas extras não pagas ou quer calcular sua rescisão? Analiso seu caso com clareza e você fala direto comigo pelo WhatsApp.",
 "hero_note":"Cálculo de rescisão · Atendimento direto com o advogado · Sem compromisso",
 "knows":["Direito Trabalhista","Cálculo de rescisão","Rescisão indireta","Horas extras","Verbas rescisórias","Justa causa"],
 "sit_eyebrow":"Em que posso ajudar",
 "sit_h2":"Situações que mais atendo",
 "sit_sub":"Veja se a sua situação aparece abaixo — em todas elas pode haver valores a receber.",
 "cards":[
  {"t":"Cálculo de rescisão","d":"Demitido ou pedindo demissão? Confiro se saldo, aviso prévio, 13º, férias e FGTS foram pagos corretamente."},
  {"t":"Rescisão indireta","d":"Quando a empresa descumpre o contrato — salário atrasado, assédio, desvio de função — você pode sair com os mesmos direitos da demissão sem justa causa."},
  {"t":"Horas extras não pagas","d":"Trabalho além da jornada, intervalo suprimido ou banco de horas irregular geram pagamento com adicional de no mínimo 50%."},
  {"t":"Fui demitido, e agora?","d":"Oriento o passo a passo após a demissão: quais documentos guardar, prazos e o que conferir no acerto."},
  {"t":"Verbas rescisórias","d":"Aviso prévio, 13º proporcional, férias + 1/3, multa de 40% do FGTS e liberação do seguro-desemprego."},
  {"t":"Assédio e danos morais","d":"Humilhação, cobrança abusiva e adoecimento ligado ao trabalho podem gerar indenização por danos morais."},
 ],
 "prose":[
  {"h2":"Fui demitido sem justa causa: quais são meus direitos?",
   "p":["Na demissão sem justa causa, o trabalhador costuma ter direito a <strong>saldo de salário</strong>, <strong>aviso prévio</strong> (30 dias, acrescidos de 3 dias por ano trabalhado, até o limite de 90 dias), <strong>13º salário proporcional</strong>, <strong>férias vencidas e proporcionais acrescidas de 1/3</strong> e <strong>multa de 40% sobre o saldo do FGTS</strong>.",
        "Além disso, surge o direito de <strong>sacar o FGTS</strong> e, conforme o tempo de trabalho, de receber o <strong>seguro-desemprego</strong>. Se alguma dessas parcelas não foi paga ou veio com valor menor, é possível cobrar a diferença."]},
  {"h2":"Como calcular a rescisão trabalhista",
   "p":["O valor da rescisão soma as verbas acima e varia conforme o <strong>salário</strong>, o <strong>tempo de casa</strong> e o <strong>motivo da saída</strong> (demissão sem justa causa, pedido de demissão, acordo ou justa causa). Cada motivo libera um conjunto diferente de direitos.",
        "Por isso, antes de assinar o acerto, vale conferir os cálculos. Posso fazer essa conferência para você gratuitamente: basta enviar o contracheque e a data de admissão e saída pelo WhatsApp."]},
  {"h2":"O que é rescisão indireta e quando cabe",
   "p":["A rescisão indireta é a “justa causa do empregador”: prevista no art. 483 da CLT, ocorre quando a empresa comete faltas graves, como <strong>atraso reiterado de salário</strong>, <strong>exigência de tarefas fora do contrato</strong>, <strong>assédio</strong> ou <strong>ambiente de risco</strong>. Reconhecida na Justiça, o trabalhador sai com os mesmos direitos de uma demissão sem justa causa, mesmo tendo tomado a iniciativa de encerrar o vínculo."]},
  {"h2":"Em quanto tempo preciso entrar com ação trabalhista?",
   "p":["O prazo para ajuizar a ação é de <strong>até 2 anos</strong> contados do fim do contrato. Dentro desse período, é possível cobrar os direitos dos <strong>últimos 5 anos</strong> trabalhados. Quanto antes você buscar orientação, mais fácil reunir provas como holerites, cartões de ponto e mensagens."]},
 ],
 "steps_h2":"Do primeiro contato à ação",
 "steps":[
  {"t":"Você me conta o que houve","d":"Mande uma mensagem no WhatsApp. Sem juridiquês: você explica do seu jeito e eu faço as perguntas certas."},
  {"t":"Analiso e calculo","d":"Confiro documentos e calculo as verbas devidas, dizendo com honestidade o que dá para buscar."},
  {"t":"Buscamos o seu direito","d":"Tentamos acordo ou entramos com a ação, e você acompanha cada passo do processo."},
 ],
 "faq_h2":"Perguntas frequentes sobre direito trabalhista",
 "faqs":[
  {"q":"Fui demitido sem justa causa, quais são meus direitos?","a":["Você tem direito a saldo de salário, aviso prévio, 13º proporcional, férias vencidas e proporcionais com 1/3 e multa de 40% do FGTS, além de poder sacar o FGTS e receber o seguro-desemprego conforme o tempo trabalhado.","Se alguma verba não foi paga corretamente, é possível cobrar a diferença na Justiça do Trabalho."]},
  {"q":"Como funciona a rescisão indireta?","a":["É quando o empregador comete falta grave (salário atrasado, assédio, desvio de função, ambiente de risco). Com base no art. 483 da CLT, o trabalhador pede o reconhecimento na Justiça e, se aceito, sai com os mesmos direitos da demissão sem justa causa."]},
  {"q":"Posso reclamar horas extras não pagas?","a":["Sim. Horas trabalhadas além da jornada, intervalos suprimidos e banco de horas irregular devem ser pagos com adicional de, no mínimo, 50%. Cartões de ponto, escalas e mensagens ajudam a comprovar."]},
  {"q":"Como calcular minha rescisão trabalhista?","a":["O cálculo soma saldo de salário, aviso prévio, 13º e férias proporcionais com 1/3 e a multa de 40% do FGTS, variando conforme salário, tempo de casa e motivo da saída. Posso fazer esse cálculo gratuitamente pelo WhatsApp com base no seu contracheque."]},
  {"q":"Em quanto tempo preciso entrar com ação trabalhista?","a":["O prazo é de até 2 anos após o fim do contrato, e nele você pode cobrar os direitos dos últimos 5 anos trabalhados."]},
 ],
 "band_h2":"Calcule sua rescisão gratuitamente",
 "band_sub":"Envie seu contracheque e as datas de admissão e saída. Confiro se você recebeu tudo a que tem direito.",
 "contact_h2":"Fale com um advogado trabalhista",
 "about_line":"Atuação em Direito do Trabalho e Cível, com a mesma atenção em cada caso — da primeira ação à continuidade de um problema antigo.",
}

PAGES["civel"] = {
 "slug":"civel",
 "title":"Advogado Cível em São Paulo | Lemes Advogados",
 "meta":"Divórcio, inventário, partilha e pequenas causas. Advogado cível perto de você em São Paulo. Fale agora pelo WhatsApp e tire suas dúvidas.",
 "h1":"Advogado Cível em São Paulo",
 "hero_sub":"Divórcio, inventário, partilha, contratos e pequenas causas. Atendimento próximo, com explicação em linguagem que você entende e foco em resolver.",
 "hero_note":"Advogado cível perto de você · Atendimento em todo São Paulo",
 "knows":["Direito Civil","Divórcio","Inventário","Partilha de bens","Pequenas causas","Contratos","Indenizações"],
 "sit_eyebrow":"Áreas do direito cível",
 "sit_h2":"Como podemos ajudar",
 "sit_sub":"Atuo nas principais demandas cíveis das famílias e do dia a dia. Clique para ver a página específica.",
 "cards":[
  {"t":"Divórcio","d":"Consensual ou litigioso, no cartório ou na Justiça. Veja como funciona e quanto custa.","href":"/divorcio"},
  {"t":"Inventário e partilha","d":"Partilha de bens após o falecimento, no cartório ou judicial. Prazos, custos e tabela OAB.","href":"/inventario"},
  {"t":"Pequenas causas","d":"Cobranças, problemas de consumo e conflitos de menor valor no Juizado Especial."},
  {"t":"Contratos e indenizações","d":"Revisão de contratos, descumprimento, danos morais e materiais."},
  {"t":"Cobranças e dívidas","d":"Negociação, defesa em cobranças indevidas e inscrição irregular em cadastros."},
  {"t":"Família e união estável","d":"Reconhecimento e dissolução de união estável, alimentos e guarda."},
 ],
 "prose":[
  {"h2":"Advogado cível perto de você em São Paulo",
   "p":["O escritório fica em <strong>Perdizes, São Paulo</strong>, e atende clientes de toda a cidade e região. O atendimento começa pelo WhatsApp, de forma prática, e segue com a mesma pessoa do início ao fim — você sempre sabe com quem está falando."]},
  {"h2":"Pequenas causas: quando vale a pena",
   "p":["O Juizado Especial Cível resolve conflitos de até 40 salários mínimos, como cobranças indevidas, problemas com produtos e serviços e pequenos contratos. Para causas de até 20 salários mínimos, é possível entrar sem advogado, mas a orientação jurídica aumenta as chances de êxito e evita erros que atrasam o processo."]},
  {"h2":"Divórcio e inventário: as demandas mais comuns",
   "p":["Dois dos atendimentos mais frequentes são o <strong>divórcio</strong> e o <strong>inventário</strong>. Quando há acordo entre as partes, ambos podem ser feitos em cartório, de forma mais rápida e barata. Criamos páginas específicas para explicar cada um em detalhe — veja como funciona o <a href=\"/divorcio\">divórcio</a> e o <a href=\"/inventario\">inventário</a>."]},
 ],
 "steps_h2":"Como começamos",
 "steps":[
  {"t":"Você descreve o caso","d":"Mande sua dúvida pelo WhatsApp. Entendo a situação e digo se há o que fazer."},
  {"t":"Avalio os caminhos","d":"Explico as opções — acordo, cartório ou Justiça — com custos e prazos claros."},
  {"t":"Conduzo o processo","d":"Cuido de toda a parte jurídica e mantenho você informado em cada etapa."},
 ],
 "faq_h2":"Perguntas frequentes sobre direito cível",
 "faqs":[
  {"q":"O que faz um advogado cível?","a":["O advogado cível atua em conflitos do dia a dia entre pessoas e empresas: divórcio, inventário, partilha, contratos, cobranças, indenizações por danos morais e materiais e causas de consumo, entre outros."]},
  {"q":"Tem advogado cível perto de mim em São Paulo?","a":["Sim. O escritório fica em Perdizes, São Paulo, e atende toda a cidade, com início do atendimento pelo WhatsApp para a sua comodidade."]},
  {"q":"Como funciona o Juizado de Pequenas Causas?","a":["O Juizado Especial Cível julga causas de até 40 salários mínimos de forma mais simples e rápida. Até 20 salários mínimos é possível ingressar sem advogado, mas a orientação jurídica ajuda a montar o pedido e reunir provas."]},
  {"q":"Quanto custa um advogado cível?","a":["Depende da complexidade e do tipo de ação. Em muitos casos é possível trabalhar com honorários combinados previamente ou vinculados ao êxito. Na primeira conversa, explico os valores com transparência, sem compromisso."]},
 ],
 "band_h2":"Tire sua dúvida cível agora",
 "band_sub":"Conte sua situação pelo WhatsApp. Explico, sem compromisso, se há o que fazer e qual o caminho.",
 "contact_h2":"Fale com um advogado cível",
 "about_line":"Atuação em Direito Civil e de Família — divórcio, inventário, partilha, contratos e pequenas causas — com atendimento próximo e linguagem clara.",
}

PAGES["divorcio"] = {
 "slug":"divorcio",
 "title":"Advogado de Divórcio em SP | Cartório e Judicial | Lemes",
 "meta":"Divórcio no cartório ou judicial, consensual ou litigioso. Saiba quanto custa e como funciona com advogado de divórcio em SP. Fale pelo WhatsApp.",
 "h1":"Advogado de Divórcio em São Paulo",
 "hero_sub":"Divórcio no cartório ou na Justiça, consensual ou litigioso. Explico como funciona, quanto custa e cuido de tudo para que seja o mais tranquilo possível.",
 "hero_note":"Divórcio em cartório · Partilha e guarda · Atendimento reservado",
 "knows":["Divórcio","Divórcio extrajudicial","Divórcio consensual","Partilha de bens","Guarda de filhos","Pensão alimentícia"],
 "sit_eyebrow":"Tipos de divórcio",
 "sit_h2":"Qual é o seu caso",
 "sit_sub":"O caminho muda conforme há ou não acordo e filhos menores. Veja as situações mais comuns.",
 "cards":[
  {"t":"Divórcio no cartório","d":"Quando o casal está de acordo e não há filhos menores ou incapazes, o divórcio pode ser feito por escritura, de forma rápida."},
  {"t":"Divórcio consensual","d":"Há acordo sobre bens, guarda e pensão. É mais rápido e barato, mesmo quando precisa correr na Justiça."},
  {"t":"Divórcio litigioso","d":"Não há acordo. A Justiça decide partilha, guarda e pensão. Conduzo a defesa dos seus interesses."},
  {"t":"Partilha de bens","d":"Divisão do patrimônio conforme o regime de casamento. Imóveis, veículos, contas e dívidas."},
  {"t":"Guarda dos filhos","d":"Definição da guarda (em regra compartilhada), convivência e responsabilidades."},
  {"t":"Pensão alimentícia","d":"Fixação ou revisão de pensão para filhos e, em alguns casos, para o ex-cônjuge."},
 ],
 "prose":[
  {"h2":"Como funciona o divórcio no cartório",
   "p":["O divórcio em cartório (extrajudicial) é feito por <strong>escritura pública</strong> e costuma ser concluído em poucos dias. Para isso, o casal precisa estar <strong>de acordo</strong> sobre o fim do casamento e a partilha, e a presença de advogado é <strong>obrigatória</strong>, mesmo no cartório.",
        "Tradicionalmente, o caminho do cartório era reservado a casais <strong>sem filhos menores ou incapazes</strong>. Regras recentes vêm ampliando essas hipóteses em situações específicas, por isso o ideal é avaliar o seu caso antes de decidir o caminho."]},
  {"h2":"Qual a diferença entre divórcio judicial e extrajudicial",
   "p":["No <strong>extrajudicial</strong> (cartório), tudo é resolvido por escritura quando há consenso e não há questões pendentes envolvendo filhos menores. No <strong>judicial</strong>, o processo corre perante o juiz — necessário quando há litígio ou quando é preciso decidir guarda, convivência ou alimentos de filhos menores. O divórcio consensual judicial costuma ser bem mais rápido que o litigioso."]},
  {"h2":"Quanto custa um divórcio com advogado",
   "p":["O custo varia conforme o caminho. No cartório, há os <strong>emolumentos</strong> (taxas do tabelionato, que variam com o valor dos bens) somados aos <strong>honorários</strong> do advogado. No divórcio consensual, sem disputa de patrimônio, os valores tendem a ser menores. Na primeira conversa, explico a estimativa com transparência, sem compromisso."]},
  {"h2":"Posso me divorciar sem advogado?",
   "p":["Não. A lei exige a participação de advogado em qualquer divórcio, seja no cartório, seja na Justiça. O advogado pode ser comum ao casal no divórcio consensual, o que reduz custos e agiliza o processo."]},
 ],
 "steps_h2":"Como conduzo seu divórcio",
 "steps":[
  {"t":"Conversa reservada","d":"Você me conta a situação pelo WhatsApp, com total discrição. Avalio se cabe cartório ou Justiça."},
  {"t":"Organizo os documentos","d":"Reúno certidões, dados dos bens e os termos de partilha, guarda e pensão."},
  {"t":"Finalizo o divórcio","d":"Cuido da escritura ou da ação e acompanho até a averbação na certidão."},
 ],
 "faq_h2":"Perguntas frequentes sobre divórcio",
 "faqs":[
  {"q":"Como funciona o divórcio no cartório?","a":["É feito por escritura pública, com acordo do casal e presença obrigatória de advogado. Costuma ser concluído em poucos dias e, tradicionalmente, é indicado quando não há filhos menores ou incapazes — embora regras recentes venham ampliando as hipóteses em casos específicos."]},
  {"q":"Qual a diferença entre divórcio judicial e extrajudicial?","a":["O extrajudicial é feito em cartório quando há consenso e nenhuma pendência sobre filhos menores. O judicial corre na Justiça e é necessário quando há litígio ou questões de guarda, convivência e alimentos de filhos menores a decidir."]},
  {"q":"Quanto custa um divórcio com advogado?","a":["Soma os emolumentos do cartório (que variam com o valor dos bens) e os honorários do advogado. O divórcio consensual, sem disputa de patrimônio, tende a custar menos. Explico a estimativa na primeira conversa."]},
  {"q":"Posso me divorciar sem advogado?","a":["Não. A presença de advogado é obrigatória em qualquer divórcio. No divórcio consensual, o mesmo advogado pode atender o casal, reduzindo custos."]},
  {"q":"Como fica a guarda dos filhos no divórcio?","a":["A regra é a guarda compartilhada, em que ambos os pais participam das decisões, com definição da convivência e da pensão. Em situações específicas, pode ser fixada guarda unilateral, sempre considerando o melhor interesse da criança."]},
 ],
 "band_h2":"Divórcio com discrição e clareza",
 "band_sub":"Conte sua situação pelo WhatsApp, com total sigilo. Explico o caminho mais rápido e menos desgastante para o seu caso.",
 "contact_h2":"Fale com um advogado de divórcio",
 "about_line":"Atuação em Direito de Família, com atenção especial à discrição e ao bem-estar de quem está passando por um divórcio.",
}

PAGES["inventario"] = {
 "slug":"inventario",
 "title":"Advogado de Inventário em SP | Custo e Tabela OAB | Lemes",
 "meta":"Quanto custa um advogado de inventário? Veja a tabela OAB/SP, prazos e como funciona o inventário extrajudicial. Fale pelo WhatsApp com a Lemes.",
 "h1":"Advogado de Inventário em São Paulo",
 "hero_sub":"Precisa abrir o inventário e fazer a partilha dos bens? Explico custos, prazos e como funciona no cartório ou na Justiça, e cuido de todo o processo.",
 "hero_note":"Inventário no cartório · Partilha · Atendimento à família",
 "knows":["Inventário","Inventário extrajudicial","Partilha de bens","Sucessão","Testamento","ITCMD"],
 "sit_eyebrow":"Sobre o inventário",
 "sit_h2":"O que você precisa resolver",
 "sit_sub":"O inventário formaliza a transferência dos bens de quem faleceu aos herdeiros. Veja as situações mais comuns.",
 "cards":[
  {"t":"Inventário extrajudicial","d":"No cartório, por escritura, quando os herdeiros são maiores, capazes e estão de acordo. Mais rápido e econômico."},
  {"t":"Inventário judicial","d":"Necessário quando há herdeiro menor, incapaz, testamento ou desacordo entre os herdeiros."},
  {"t":"Partilha de bens","d":"Divisão de imóveis, contas, veículos e participações entre os herdeiros conforme a lei."},
  {"t":"Custo e tabela OAB","d":"Entenda os honorários, o ITCMD e as taxas de cartório antes de começar."},
  {"t":"Prazo para abrir","d":"A lei prevê prazo para iniciar o inventário, com multa do ITCMD em caso de atraso em SP."},
  {"t":"Alvará judicial","d":"Para liberar valores urgentes (contas, FGTS, saldo) antes do fim do inventário."},
 ],
 "prose":[
  {"h2":"Quanto custa um advogado para inventário?",
   "p":["O custo do inventário tem três componentes: os <strong>honorários do advogado</strong>, o imposto <strong>ITCMD</strong> (em São Paulo, em regra 4% sobre o valor dos bens) e as <strong>taxas de cartório</strong> (emolumentos). Os honorários costumam ser definidos como um percentual sobre o valor do espólio, com base em referências como a tabela da OAB/SP.",
        "Como cada inventário envolve patrimônios diferentes, o ideal é uma estimativa personalizada. Envie a relação dos bens pelo WhatsApp que faço um cálculo aproximado para você."]},
  {"h2":"Qual a tabela OAB para inventário em SP",
   "p":["A <strong>Tabela de Honorários da OAB/SP</strong> traz percentuais de referência para serviços advocatícios, inclusive inventário e partilha. Ela serve de parâmetro mínimo e orienta a contratação, mas o valor final é combinado entre as partes conforme a complexidade do caso. Explico esse ponto com transparência antes de iniciar."]},
  {"h2":"Como funciona o inventário extrajudicial",
   "p":["O inventário extrajudicial é feito por <strong>escritura pública em cartório</strong> e é possível quando <strong>todos os herdeiros são maiores e capazes</strong>, estão <strong>de acordo</strong> com a partilha e há advogado acompanhando. É o caminho mais rápido — pode ser concluído em semanas. Havendo herdeiro menor, incapaz, testamento ou conflito, o inventário deve correr na Justiça."]},
  {"h2":"Qual o prazo para abrir inventário?",
   "p":["Em São Paulo, o inventário deve ser <strong>aberto em até 60 dias</strong> contados do falecimento. O descumprimento gera <strong>multa sobre o ITCMD</strong>. Mesmo que a partilha demore, o importante é iniciar dentro do prazo para evitar o acréscimo."]},
 ],
 "steps_h2":"Como conduzo o inventário",
 "steps":[
  {"t":"Levantamento dos bens","d":"Você me envia a relação do patrimônio e dos herdeiros pelo WhatsApp e eu avalio o caminho."},
  {"t":"Cálculo e documentos","d":"Estimo custos e ITCMD, reúno certidões e preparo o plano de partilha."},
  {"t":"Escritura ou ação","d":"Conduzo o inventário no cartório ou na Justiça até a transferência dos bens."},
 ],
 "faq_h2":"Perguntas frequentes sobre inventário",
 "faqs":[
  {"q":"Quanto custa um advogado para inventário?","a":["O custo reúne honorários do advogado (em geral um percentual sobre o valor dos bens, com base na tabela da OAB/SP), o ITCMD (em SP, em regra 4%) e as taxas de cartório. Envie a relação dos bens pelo WhatsApp para uma estimativa personalizada."]},
  {"q":"Qual a tabela OAB para inventário em SP?","a":["A Tabela de Honorários da OAB/SP traz percentuais de referência para inventário e partilha. Ela serve de parâmetro, e o valor final é combinado conforme a complexidade do caso."]},
  {"q":"Como funciona o inventário extrajudicial?","a":["É feito por escritura em cartório quando todos os herdeiros são maiores, capazes e estão de acordo, com advogado acompanhando. É o caminho mais rápido. Havendo herdeiro menor, incapaz, testamento ou desacordo, o inventário corre na Justiça."]},
  {"q":"Qual o prazo para abrir inventário?","a":["Em São Paulo, o prazo é de 60 dias a contar do falecimento. O atraso gera multa sobre o ITCMD, por isso é importante iniciar dentro do prazo mesmo que a partilha leve mais tempo."]},
  {"q":"É possível fazer inventário sem ir ao cartório?","a":["No inventário extrajudicial é necessário lavrar a escritura em cartório, mas grande parte do trabalho (documentos, cálculos e negociação) é conduzida pelo advogado, com pouca exigência de deslocamento dos herdeiros."]},
 ],
 "band_h2":"Estime o custo do seu inventário",
 "band_sub":"Envie a relação dos bens e dos herdeiros pelo WhatsApp. Faço um cálculo aproximado de custos, ITCMD e prazos.",
 "contact_h2":"Fale com um advogado de inventário",
 "about_line":"Atuação em inventário, partilha e sucessões, com cuidado no atendimento à família em um momento delicado.",
}

PAGES["aereo"] = {
 "slug":"aereo",
 "title":"Advogado de Direito Aéreo | Overbooking e Voo | Lemes",
 "meta":"Overbooking, preterição de embarque, mala extraviada ou atraso de voo? Saiba seus direitos pela Resolução 400 da ANAC. Fale pelo WhatsApp.",
 "h1":"Direito do Passageiro Aéreo",
 "hero_sub":"Overbooking, preterição de embarque, voo atrasado ou cancelado, mala extraviada? Você pode ter direito a reacomodação, reembolso e indenização.",
 "hero_note":"Resolução 400 da ANAC · Indenização ao passageiro · Análise sem custo",
 "knows":["Direito Aéreo","Direito do passageiro","Overbooking","Preterição de embarque","Bagagem extraviada","Atraso de voo","Resolução 400 ANAC"],
 "sit_eyebrow":"Problemas no voo",
 "sit_h2":"O que aconteceu com você",
 "sit_sub":"Em todas estas situações a companhia aérea pode ter obrigações com o passageiro.",
 "cards":[
  {"t":"Overbooking","d":"A companhia vendeu mais assentos do que a capacidade e você ficou sem lugar? Há direito a compensação."},
  {"t":"Preterição de embarque","d":"Foi impedido de embarcar mesmo com passagem e check-in? A ANAC prevê reacomodação, reembolso e compensação financeira."},
  {"t":"Mala extraviada","d":"Bagagem perdida, violada ou danificada gera direito a indenização pelos prejuízos."},
  {"t":"Atraso e cancelamento","d":"Atrasos geram assistência (alimentação, hospedagem) e, conforme o caso, reembolso e danos morais."},
  {"t":"Voo remarcado","d":"Mudança de horário sem aviso adequado pode dar direito a reacomodação ou reembolso integral."},
  {"t":"Danos morais","d":"Perder compromisso, viagem ou conexão por falha da companhia pode render indenização."},
 ],
 "prose":[
  {"h2":"Quais são meus direitos em caso de overbooking?",
   "p":["No overbooking, quando há mais passageiros do que assentos, a companhia deve primeiro procurar <strong>voluntários</strong> para remarcar, mediante compensação acordada. Não havendo voluntários, ocorre a <strong>preterição</strong>, e o passageiro preterido tem direito a <strong>reacomodação em outro voo</strong>, <strong>reembolso</strong> ou execução do serviço por outra modalidade, além de <strong>compensação financeira</strong> prevista na Resolução 400 da ANAC e, conforme o prejuízo, indenização por danos morais."]},
  {"h2":"O que fazer quando a mala é extraviada",
   "p":["Registre imediatamente o <strong>RIB (Registro de Irregularidade de Bagagem)</strong> no balcão da companhia, ainda no aeroporto. A empresa tem prazo para localizar e devolver a bagagem; não devolvendo, deve <strong>indenizar</strong> os prejuízos. Guarde comprovantes do conteúdo e dos gastos com itens essenciais que você precisou comprar."]},
  {"h2":"Como funciona a Resolução 400 da ANAC",
   "p":["A <strong>Resolução ANAC nº 400/2016</strong> reúne as regras de proteção ao passageiro: assistência material em atrasos (a partir de 1h, comunicação; 2h, alimentação; 4h, hospedagem e transporte quando necessário), regras de reacomodação e reembolso, e a compensação em caso de preterição. Esses direitos se somam à proteção do Código de Defesa do Consumidor."]},
  {"h2":"Posso ser indenizado por atraso de voo?",
   "p":["Sim, dependendo do tempo de atraso e dos prejuízos. Além da assistência material, atrasos longos e cancelamentos que causem perda de compromissos, diárias ou conexões podem gerar <strong>reembolso</strong> e <strong>indenização por danos morais e materiais</strong>. Guarde cartão de embarque, comprovantes e prints das comunicações da companhia."]},
 ],
 "steps_h2":"Como buscamos sua indenização",
 "steps":[
  {"t":"Você relata o ocorrido","d":"Mande pelo WhatsApp o que aconteceu e os comprovantes (passagem, protocolos, gastos)."},
  {"t":"Avalio seus direitos","d":"Analiso o caso à luz da Resolução 400 da ANAC e do CDC e estimo a indenização cabível."},
  {"t":"Cobramos a companhia","d":"Buscamos acordo ou ação judicial contra a companhia aérea, e você acompanha tudo."},
 ],
 "faq_h2":"Perguntas frequentes sobre direito do passageiro",
 "faqs":[
  {"q":"Quais são meus direitos em caso de overbooking?","a":["Se não houver voluntários para remarcar, o passageiro preterido tem direito a reacomodação, reembolso ou execução por outra modalidade, mais a compensação financeira da Resolução 400 da ANAC e, conforme o prejuízo, indenização por danos morais."]},
  {"q":"O que fazer quando a mala é extraviada?","a":["Registre o RIB no balcão da companhia ainda no aeroporto e guarde comprovantes. A empresa deve localizar a bagagem no prazo previsto e, não o fazendo, indenizar os prejuízos e os gastos com itens essenciais."]},
  {"q":"Como funciona a resolução 400 da ANAC?","a":["A Resolução ANAC 400/2016 define a proteção ao passageiro: assistência material em atrasos, regras de reacomodação e reembolso e compensação por preterição. Esses direitos se somam aos do Código de Defesa do Consumidor."]},
  {"q":"Posso ser indenizado por atraso de voo?","a":["Sim. Além da assistência material, atrasos longos e cancelamentos com prejuízo (perda de compromissos, diárias, conexões) podem gerar reembolso e indenização por danos morais e materiais."]},
  {"q":"O que é preterição de embarque?","a":["É quando o passageiro com passagem e check-in é impedido de embarcar, geralmente por overbooking. Gera direito a reacomodação, reembolso e compensação financeira prevista na Resolução 400 da ANAC."]},
 ],
 "band_h2":"Teve problema no voo? Verifique seus direitos",
 "band_sub":"Envie passagem, protocolos e comprovantes pelo WhatsApp. Avalio sem custo a indenização cabível.",
 "contact_h2":"Fale com um advogado de direito aéreo",
 "about_line":"Atuação na defesa do passageiro aéreo — overbooking, bagagem, atrasos e cancelamentos — com base na Resolução 400 da ANAC e no CDC.",
}

PAGES["previdenciario"] = {
 "slug":"previdenciario",
 "title":"Advogado Previdenciário em SP | Aposentadoria | Lemes",
 "meta":"INSS negou seu benefício? Saiba com quantos anos a mulher se aposenta e como dar entrada na aposentadoria. Fale com advogado previdenciário em SP.",
 "h1":"Advogado Previdenciário em São Paulo",
 "hero_sub":"Vai se aposentar ou o INSS negou seu benefício? Analiso seu tempo de contribuição, verifico a melhor regra e oriento o caminho da sua aposentadoria.",
 "hero_note":"Aposentadoria · Revisão · INSS negado · Análise do seu caso",
 "knows":["Direito Previdenciário","Aposentadoria","Aposentadoria por idade","Tempo de contribuição","Benefício do INSS","Revisão de benefício"],
 "sit_eyebrow":"Benefícios e aposentadoria",
 "sit_h2":"Como posso ajudar",
 "sit_sub":"Da primeira simulação ao recurso contra o INSS, oriento cada etapa.",
 "cards":[
  {"t":"Aposentadoria da mulher","d":"Idade mínima, tempo de contribuição e regras de transição para a aposentadoria feminina."},
  {"t":"Tempo de contribuição","d":"Levantamento do seu histórico no CNIS e enquadramento na melhor regra."},
  {"t":"INSS negou meu benefício","d":"Recurso administrativo e ação judicial quando o pedido é indeferido indevidamente."},
  {"t":"Cálculo da aposentadoria","d":"Simulação do valor e da data mais vantajosa para se aposentar."},
  {"t":"Aposentadoria por idade","d":"Requisitos de idade e carência para quem completou o tempo mínimo."},
  {"t":"Revisão de benefício","d":"Conferência de benefícios já concedidos que podem estar com valor menor que o devido."},
 ],
 "prose":[
  {"h2":"Com quantos anos a mulher pode se aposentar?",
   "p":["Pela regra geral após a Reforma da Previdência (EC 103/2019), a mulher se aposenta por idade aos <strong>62 anos</strong>, com pelo menos <strong>15 anos de contribuição</strong>. Para quem já contribuía antes da reforma, existem <strong>regras de transição</strong> (como pontos e pedágio) que podem permitir a aposentadoria <strong>antes dos 62 anos</strong>. Por isso, vale simular qual regra é mais vantajosa no seu caso."]},
  {"h2":"Como funciona a aposentadoria por tempo de contribuição",
   "p":["A aposentadoria por tempo de contribuição “pura” foi extinta para quem entrou no sistema após a reforma. Quem já contribuía pode se aposentar pelas <strong>regras de transição</strong>, que combinam tempo de contribuição com idade mínima ou pontuação. O primeiro passo é levantar todo o seu histórico no <strong>CNIS</strong> e conferir se há períodos a incluir."]},
  {"h2":"Meu benefício do INSS foi negado, o que fazer?",
   "p":["Um indeferimento não é o fim. É possível apresentar <strong>recurso administrativo</strong> junto ao INSS e, se necessário, <strong>ação judicial</strong>. Muitos benefícios são negados por falta de documento ou erro na contagem do tempo, situações que costumam ser revertidas com a orientação correta. Guarde a carta de indeferimento e o número do processo."]},
  {"h2":"Como calcular minha aposentadoria",
   "p":["O valor depende da <strong>média das suas contribuições</strong> e da regra aplicável. Pequenas diferenças na data do pedido podem mudar bastante o valor final. Faço uma <strong>simulação</strong> com base no seu CNIS para indicar a data e a regra mais vantajosas antes de você dar entrada."]},
 ],
 "steps_h2":"Como oriento sua aposentadoria",
 "steps":[
  {"t":"Levanto seu histórico","d":"Analiso seu CNIS e tempo de contribuição a partir dos dados que você envia pelo WhatsApp."},
  {"t":"Simulo as regras","d":"Comparo as regras de transição e a regra geral para achar a mais vantajosa."},
  {"t":"Dou entrada ou recorro","d":"Oriento o requerimento ou ingresso com recurso/ação se o INSS negar."},
 ],
 "faq_h2":"Perguntas frequentes sobre aposentadoria e INSS",
 "faqs":[
  {"q":"Com quantos anos a mulher pode se aposentar?","a":["Pela regra geral pós-reforma, a mulher se aposenta por idade aos 62 anos, com no mínimo 15 anos de contribuição. Quem já contribuía antes de 2019 pode usar regras de transição e, em alguns casos, se aposentar antes dos 62 anos."]},
  {"q":"Como funciona a aposentadoria por tempo de contribuição?","a":["A modalidade pura foi extinta para novos segurados. Quem já contribuía pode se aposentar pelas regras de transição, que combinam tempo de contribuição com idade ou pontuação. O primeiro passo é conferir o histórico no CNIS."]},
  {"q":"Meu benefício do INSS foi negado, o que fazer?","a":["É possível apresentar recurso administrativo e, se necessário, ação judicial. Muitos indeferimentos decorrem de falta de documento ou erro na contagem do tempo e podem ser revertidos. Guarde a carta de indeferimento e o número do processo."]},
  {"q":"Como calcular minha aposentadoria?","a":["O valor depende da média das contribuições e da regra aplicável, e a data do pedido influencia bastante o resultado. Uma simulação com base no seu CNIS indica a data e a regra mais vantajosas."]},
 ],
 "band_h2":"Simule sua aposentadoria",
 "band_sub":"Envie seus dados de contribuição pelo WhatsApp. Indico a melhor regra e a data mais vantajosa para você se aposentar.",
 "contact_h2":"Fale com um advogado previdenciário",
 "about_line":"Atuação em aposentadorias, benefícios e revisões junto ao INSS, com simulação cuidadosa para encontrar a melhor regra.",
}

# ============================================================================ #
#  Render + escrita
# ============================================================================ #
def render(page):
    legal, faqpage = schema_for(page)
    schema_json = json.dumps({"@context":"https://schema.org","@graph":[legal, faqpage]}, ensure_ascii=False, indent=1)
    mapping = dict(NAP)
    mapping.update({
        "title": page["title"], "meta": page["meta"], "h1": page["h1"],
        "hero_sub": page["hero_sub"], "hero_note": page["hero_note"], "eyebrow": page["eyebrow_top"],
        "canonical": f"{LANDING}/{page['slug']}",
        "css": CSS, "js": JS, "zap": ZAP_SVG, "whats": WHATS, "ads_id": ADS_ID,
        "phone_display": NAP["phone_display"], "phone_tel": NAP["phone_tel"],
        "sit_eyebrow": page["sit_eyebrow"], "sit_h2": page["sit_h2"], "sit_sub": page["sit_sub"],
        "cards": cards_html(page["cards"], three=True),
        "prose": prose_html(page["prose"]),
        "steps_h2": page["steps_h2"], "steps": steps_html(page["steps"]),
        "faq_h2": page["faq_h2"], "faq": faq_html(page["faqs"]),
        "band_h2": page["band_h2"], "band_sub": page["band_sub"],
        "contact_h2": page["contact_h2"], "about_line": page["about_line"],
        "footer_links": footer_links(), "schema": schema_json,
    })
    return TPL.substitute(mapping)

def main():
    warnings = []
    all_schema = {}
    for slug, page in PAGES.items():
        page["eyebrow_top"] = f"Direito {dict(PRACTICES)[slug]} · São Paulo" if slug in dict(PRACTICES) else "São Paulo"
        # avisos de tamanho
        if len(page["title"]) > 60: warnings.append(f"[TITLE>60] {slug}: {len(page['title'])}")
        if len(page["meta"]) > 155: warnings.append(f"[META>155] {slug}: {len(page['meta'])}")
        (OUT / f"{slug}.html").write_text(render(page), encoding="utf-8")
        legal, faqpage = schema_for(page)
        all_schema[slug] = {"@context":"https://schema.org","@graph":[legal, faqpage]}

    (OUT / "schema-markup.json").write_text(json.dumps(all_schema, ensure_ascii=False, indent=2), encoding="utf-8")

    # home meta tags
    home_title = "Lemes Advogados | Trabalhista, Cível e Previdenciário SP"
    home_meta = "Escritório de advocacia em Perdizes, São Paulo. Trabalhista, Cível, Divórcio, Inventário, Previdenciário e Aéreo. Fale agora pelo WhatsApp."
    lines = ["# TITLES E META DESCRIPTIONS — colar em cada página no Wix (SEO > Editar título e descrição)\n"]
    lines.append(f"## HOME — {LANDING}/")
    lines.append(f"Title ({len(home_title)}): {home_title}")
    lines.append(f"Meta  ({len(home_meta)}): {home_meta}")
    lines.append(f"H1 sugerido: Lemes Sociedade Individual de Advogados\n")
    for slug, page in PAGES.items():
        lines.append(f"## /{slug} — {LANDING}/{slug}")
        lines.append(f"Title ({len(page['title'])}): {page['title']}")
        lines.append(f"Meta  ({len(page['meta'])}): {page['meta']}")
        lines.append(f"H1: {page['h1']}\n")
    (OUT / "home-meta-tags.txt").write_text("\n".join(lines), encoding="utf-8")

    print("Páginas geradas:", ", ".join(f"{s}.html" for s in PAGES))
    print("Extras: schema-markup.json, home-meta-tags.txt")
    if warnings:
        print("AVISOS:", *warnings, sep="\n  ")
    else:
        print("OK: todos os titles <=60 e metas <=155 caracteres.")

if __name__ == "__main__":
    main()

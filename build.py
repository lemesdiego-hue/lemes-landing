#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador das landing pages otimizadas da Lemes Advogados.
Fonte única de verdade: CSS, template e conteúdo de cada página ficam aqui.
Rode:  python3 build.py
Saída: pasta dist/ pronta para deploy (rotas limpas em diretório):
       dist/index.html (home), dist/<slug>/index.html (9 áreas),
       dist/404.html, dist/sitemap.xml, dist/robots.txt, dist/CNAME, dist/.nojekyll
Home gerada por render_home() (conteúdo em HOME); estático autoral: 404.html.
Artefatos de referência na raiz: schema-markup.json, home-meta-tags.txt.
"""
import json, pathlib, shutil, datetime
from string import Template

OUT = pathlib.Path(__file__).resolve().parent
WHATS = "https://wa.me/5511995155021?text=Ol%C3%A1%2C%20vim%20pelo%20site%20e%20gostaria%20de%20uma%20consulta"
# Domínio onde as páginas efetivamente ficam hospedadas (landing). O schema/marca
# continua apontando para o site institucional (NAP['url']).
LANDING = "https://lemesadvogados.com"
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
    ("familia",       "Família"),
    ("inventario",    "Inventário"),
    ("imobiliario",   "Imobiliário"),
    ("aereo",         "Direito Aéreo"),
    ("previdenciario","Previdenciário"),
    ("empresarial",   "Empresarial"),
]

GA4_ID = "G-3YLQXJDLJE"
CLARITY_ID = "xe34fpdzej"
FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Spectral:ital,wght@0,400;0,500;0,600;0,700;1,500&display=swap"
FOUNDED = "2016"
# Trajetória (texto aprovado pelo Diego em 21/10/2026 — sem citar a graduação)
BIO = ("Antes de fundar o escritório, em 2016, foi gestor de departamentos jurídicos de grandes empresas, "
       "onde coordenou casos em diversas áreas do direito. É especialista em Contratos Internacionais pela PUC-SP "
       "e tem MBA em Direito Tributário pela FGV.")
PHOTO = "/assets/diego-lemes-advogado-360.webp"
LOGO = "/assets/logo-claro.png"
SAME_AS = ["https://www.linkedin.com/in/diego-henrique-lemes-8882b0/", "https://www.instagram.com/lemesadvsp/"]
NAV_HOME = ('<a href="#areas">Áreas</a><a href="#como">Como funciona</a><a href="#sobre">O escritório</a>'
            '<a href="#duvidas">Dúvidas</a><a href="#contato">Contato</a>')
NAV_AREA = ('<a href="/">Início</a><a href="/#areas">Áreas</a><a href="#sobre">O advogado</a>'
            '<a href="#contato">Contato</a>')

# Ícones (traço) e linha curta de cada área — usados na lista de áreas da home
AREA_ICONS = {
    "trabalhista": "M3 8h18v12H3z M8 8V5h8v3 M3 13h18",
    "civel": "M6 3h9l4 4v14H6z M15 3v4h4 M9 12h7 M9 16h7",
    "divorcio": "M3 14a5 5 0 1 0 10 0a5 5 0 1 0-10 0 M11 14a5 5 0 1 0 10 0a5 5 0 1 0-10 0",
    "familia": "M8 8a3 3 0 1 0 0-.01 M16 9a2.5 2.5 0 1 0 0-.01 M3 20c0-3 2.2-5 5-5s5 2 5 5 M13 20c.3-2.4 1.6-4 3.5-4 2 0 3.5 1.6 3.5 4",
    "inventario": "M3 11l9-7 9 7 M5 10v10h14V10 M10 20v-6h4v6",
    "imobiliario": "M4 21V8l8-5 8 5v13 M9 21v-5h6v5 M9 11h.01 M15 11h.01",
    "aereo": "M22 2L11 13 M22 2l-7 20-4-9-9-4z",
    "previdenciario": "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z M9 12l2 2 4-4",
    "empresarial": "M3 21h18 M5 21V7l7-4 7 4v14 M9 10h2 M13 10h2 M9 14h2 M13 14h2",
}
AREA_LINES = {
    "trabalhista": "Demissão, verbas rescisórias, horas extras, FGTS e assédio.",
    "civel": "Contratos, consumidor, indenizações e cobranças.",
    "divorcio": "No cartório ou judicial, consensual ou litigioso, guarda e partilha.",
    "familia": "Guarda, pensão alimentícia, união estável e partilha.",
    "inventario": "Inventário judicial ou extrajudicial, herança e partilha.",
    "imobiliario": "Usucapião, regularização de imóvel, despejo e posse.",
    "aereo": "Voo cancelado ou atrasado, overbooking e bagagem extraviada.",
    "previdenciario": "Aposentadoria, benefício negado pelo INSS, BPC e revisão.",
    "empresarial": "Societário, acordo de sócios, marcas e contratos comerciais.",
}

HOME = {
    "title": "Advogado em São Paulo | Lemes Advogados",
    "meta": "Advogado em São Paulo, em Perdizes. Trabalhista, Cível, Família, Divórcio, Inventário, Previdenciário e Aéreo. Primeira conversa gratuita pelo WhatsApp.",
    "hero_areas": ["trabalhista", "divorcio", "inventario", "civel", "previdenciario", "aereo"],
    "pillars": [
        ("Você fala com o advogado", "Quem ouve o seu caso no primeiro contato é quem vai cuidar dele, do início ao fim."),
        ("Linguagem clara", "Explicação sem juridiquês: o que você pode buscar, quanto tempo costuma levar e quais documentos separar."),
        ("Tudo pelo celular", "Contrato e procuração assinados no celular. Se preferir, o escritório fica em Perdizes."),
    ],
    "prose": [
        {"h2": "Advogado em São Paulo com atendimento direto", "p": [
            "A <strong>Lemes Sociedade Individual de Advogados</strong> atua em São Paulo com foco em resolver o seu caso de forma clara e próxima. O atendimento é conduzido pelo próprio advogado, <strong>Diego Henrique Lemes (OAB/SP 255.888)</strong>, do primeiro contato ao desfecho, sem intermediários e sem juridiquês.",
            "O escritório fica em <strong>Perdizes, São Paulo</strong>, e atende clientes de toda a cidade e do estado. A primeira conversa é <strong>gratuita</strong> e começa pelo WhatsApp: você explica a situação do seu jeito e recebe uma orientação honesta sobre o que dá para fazer."]},
        {"h2": "Como saber qual é o seu caso", "p": [
            "Se você foi demitido ou tem horas extras não pagas, comece pelo <a href=\"/trabalhista/\">Direito Trabalhista</a>. Para separação, guarda e partilha, veja <a href=\"/divorcio/\">Divórcio</a> e <a href=\"/familia/\">Família</a>. Após o falecimento de um familiar, o <a href=\"/inventario/\">Inventário</a>. Contratos, consumidor e cobranças ficam no <a href=\"/civel/\">Cível</a>; imóveis, no <a href=\"/imobiliario/\">Imobiliário</a>. Aposentadoria e benefícios negados pelo INSS, no <a href=\"/previdenciario/\">Previdenciário</a>. Problemas em voos, no <a href=\"/aereo/\">Direito Aéreo</a>. Para empresas, o <a href=\"/empresarial/\">Empresarial</a>. Na dúvida, é só mandar uma mensagem que eu indico o caminho certo."]},
    ],
    "steps": [
        {"t": "Você conta o que houve", "d": "Uma mensagem no WhatsApp basta. Você explica do seu jeito e eu faço as perguntas certas."},
        {"t": "Analiso com cuidado", "d": "Leio os documentos e digo com honestidade o que dá para buscar e qual é o próximo passo."},
        {"t": "Seguimos juntos", "d": "Acordo ou ação: você acompanha cada etapa diretamente comigo."},
    ],
    "faqs": [
        {"q": "A primeira conversa é gratuita?", "a": ["Sim. Você explica a situação pelo WhatsApp e recebe uma orientação inicial, sem compromisso."]},
        {"q": "Quais áreas o escritório atende?", "a": ["Trabalhista, Cível, Divórcio, Família, Inventário, Imobiliário, Previdenciário, Direito Aéreo e Empresarial. Cada área tem uma página própria com direitos, prazos e documentos."]},
        {"q": "Preciso ir ao escritório?", "a": ["Não. Contrato e procuração são assinados pelo celular, e os processos tramitam de forma digital. Se preferir, o escritório fica na Rua Coronel Melo de Oliveira, 557, em Perdizes, São Paulo/SP."]},
        {"q": "Como falo com o advogado?", "a": ["Pelo WhatsApp (11) 99515-5021 ou pelo e-mail diego@lemesadvogados.com. Quem atende é o próprio Diego Henrique Lemes, OAB/SP 255.888."]},
    ],
}

HOME_BODY = r"""$header
<main id="conteudo">
<div class="top">
 <!-- HERO -->
 <section class="hero wrap g3" aria-labelledby="h1">
  <div class="c12">
   <h1 id="h1"><span class="eyebrow">Advogado em São Paulo<span class="hide-sm">&nbsp;· Perdizes</span></span> <span class="h1-main">Seu caso conduzido por quem atende você, <em>do começo ao fim.</em></span></h1>
   <p class="lead">Uma orientação clara, em linguagem simples, para você decidir com calma o próximo passo.</p>
   <div class="cta">
    <a class="btn" href="$whats" target="_blank" rel="noopener">$zap Primeira conversa gratuita</a>
    <a class="btn btn--ghost" href="#como">Como funciona</a>
   </div>
   <div class="sig"><img src="/assets/diego-lemes-advogado-120.webp" alt="" width="120" height="120"><span><b>$lawyer</b><span>Advogado · $oab</span></span></div>
  </div>
  <nav class="idx c3" aria-label="Principais áreas de atuação">
   <p class="eyebrow idx__t">Em que posso ajudar</p>
   $idx
  </nav>
 </section>
</div>

 <!-- COMO TRABALHAMOS -->
 <section class="section wrap" aria-labelledby="h-como-trab">
  <h2 class="sr-only" id="h-como-trab">Como trabalhamos</h2>
  <div class="g3">$pillars</div>
 </section>

 <!-- ÁREAS DE ATUAÇÃO (HUB) -->
 <section class="section tint" id="areas">
  <div class="wrap g3">
   <div class="c1 sec-head"><h2>Áreas de atuação</h2><p>Cada área tem uma página com direitos, prazos e documentos. Na dúvida, mande uma mensagem e eu indico o caminho.</p></div>
   <div class="rows c23">$rows</div>
  </div>
 </section>

 <!-- CONTEÚDO RASTREÁVEL -->
 <section class="section wrap">
  <div class="prose prose--split">
  $prose
  </div>
 </section>

 <!-- PASSOS -->
 <section class="section tint" id="como">
  <div class="wrap">
   <div class="g3"><div class="c12 sec-head"><h2>Como funciona</h2><p>Do primeiro contato à solução, em três passos.</p></div></div>
   $steps
  </div>
 </section>

 <!-- O ESCRITÓRIO / E-E-A-T -->
$about

 <!-- FAQ -->
 <section class="section wrap g3" id="duvidas">
  <div class="c1 sec-head"><h2>Perguntas frequentes</h2></div>
  <div class="c23">$faq</div>
 </section>

 <!-- FAIXA CTA -->
 <section class="section band">
  <div class="wrap g3 band__in">
   <div class="c12"><h2>Conte o que aconteceu.</h2><p>A primeira conversa é gratuita e sem compromisso.</p></div>
   <div class="c3 band__cta"><a class="btn btn--lite" href="$whats" target="_blank" rel="noopener">$zap Falar no WhatsApp</a></div>
  </div>
 </section>

 <!-- CONTATO + FORMULÁRIO -->
$contact
</main>

"""

def _person():
    return {"@type": "Person", "@id": f"{LANDING}/#diego", "name": NAP["lawyer"], "jobTitle": "Advogado",
            "identifier": NAP["oab"], "image": LANDING + PHOTO, "description": BIO, "sameAs": SAME_AS[:1],
            "worksFor": {"@id": f"{LANDING}/#escritorio"}}

def schema_home():
    org = {
        "@type": "LegalService", "@id": f"{LANDING}/#escritorio", "name": NAP["name"], "alternateName": NAP["short"],
        "url": f"{LANDING}/", "logo": LANDING + LOGO, "image": LANDING + "/assets/og-lemes-advogados.jpg",
        "description": HOME["meta"], "telephone": "+55-11-99515-5021", "email": NAP["email"], "priceRange": "$$",
        "foundingDate": FOUNDED, "openingHours": "Mo-Fr 09:00-18:00",
        "address": {"@type": "PostalAddress", "streetAddress": NAP["street"], "addressLocality": f"{NAP['district']}, {NAP['city']}",
                    "addressRegion": NAP["region"], "postalCode": NAP["cep"], "addressCountry": "BR"},
        "areaServed": "São Paulo, SP", "founder": {"@id": f"{LANDING}/#diego"}, "sameAs": SAME_AS,
        "knowsAbout": [f"Direito {l}" if not l.startswith("Direito") else l for _, l in PRACTICES],
    }
    site = {"@type": "WebSite", "@id": f"{LANDING}/#site", "url": f"{LANDING}/", "name": NAP["short"], "inLanguage": "pt-BR",
            "publisher": {"@id": f"{LANDING}/#escritorio"}}
    faq = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": " ".join(_strip(p) for p in q["a"])}}
        for q in HOME["faqs"]]}
    return {"@context": "https://schema.org", "@graph": [org, _person(), site, faq]}

# ============================================================================ #
#  CSS — sistema de design "Escritório" (topo tinta, papel, dourado, verde do WhatsApp)
#  Inline em cada página para portabilidade e velocidade (1 requisição a menos).
# ============================================================================ #
CSS = r"""
:root{
 --paper:#F4F1EA;--paper2:#EAE5D9;--white:#FFFFFF;--ink:#1B2420;--ink2:#3C453F;--text2:#4A4A3E;
 --gold:#C9A15B;--gold-ink:#7A5C24;--carimbo:#BE3A2B;--ledger:#2E6B52;--muted:#5C5848;
 --on-dark:#F4F1EA;--on-dark2:#CFC9BA;--on-dark3:#B9B2A2;
 --line:rgba(27,36,32,.18);--line2:rgba(27,36,32,.1);--line-dark:rgba(244,241,234,.14);
 --display:"Spectral",Georgia,serif;--ui:"Archivo",system-ui,sans-serif;--mono:var(--ui);--body:"Spectral",Georgia,serif;
 --s-1:clamp(.82rem,.8rem + .1vw,.88rem);--s0:clamp(1.02rem,.99rem + .15vw,1.12rem);
 --s1:clamp(1.2rem,1.12rem + .35vw,1.4rem);--s2:clamp(1.5rem,1.33rem + .75vw,1.95rem);
 --s3:clamp(2rem,1.6rem + 1.7vw,3.2rem);--s4:clamp(2.5rem,1.75rem + 3.2vw,4.25rem);
 --gutter:clamp(1rem,5vw,3rem);--maxw:1200px;--radius:6px;--gap:clamp(1.5rem,3vw,2.75rem);
}
*,*::before,*::after{box-sizing:border-box;margin:0}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation-duration:.001ms!important;transition-duration:.001ms!important}}
body{background:var(--paper);color:var(--ink);font-family:var(--body);font-size:var(--s0);line-height:1.62;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:hidden}
img{display:block;max-width:100%;height:auto}a{color:inherit}
:focus-visible{outline:2.5px solid var(--gold);outline-offset:3px}
.wrap{width:100%;max-width:var(--maxw);margin-inline:auto;padding-inline:var(--gutter)}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
h1,h2,h3{font-family:var(--display);font-weight:600;line-height:1.1;letter-spacing:-.01em;text-wrap:balance}
.eyebrow{display:flex;align-items:center;gap:.8em;font-family:var(--ui);font-weight:600;font-size:var(--s-1);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-ink);overflow-wrap:anywhere}
.eyebrow::before{content:"";flex:none;width:2.2em;height:1px;background:currentColor}
.section{padding-block:clamp(3.2rem,8vw,6.5rem)}
/* grade única de 3 colunas: todas as seções alinham nas mesmas linhas verticais */
.g3{display:grid;grid-template-columns:minmax(0,1fr);gap:2rem var(--gap)}
@media(min-width:900px){.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.c1{grid-column:1}.c12{grid-column:1/3}.c23{grid-column:2/4}.c3{grid-column:3}}
.sec-head h2{font-size:var(--s3)}
.sec-head p{margin-top:1rem;color:var(--text2)}
.sec-head .eyebrow+h2{margin-top:.8rem}
/* texto justificado (só em colunas largas o bastante), com hifenização em português */
.prose p,.prose li,.faq__a p,.about p.txt{hyphenate-limit-chars:6 3 3}
@media(min-width:640px){.prose p,.prose li,.faq__a p,.about p.txt{text-align:justify;-webkit-hyphens:auto;hyphens:auto}}
p,li{text-wrap:pretty}
@media(max-width:479px){.hide-sm{display:none}}
@media(min-width:900px){.prose--split p,.prose--split li,.about p.txt,.c23 .faq__a p{font-size:1.2rem;line-height:1.65}}
.lead{font-size:var(--s1);color:var(--text2);max-width:58ch}
/* topo escuro: barra + hero */
.top{background:var(--ink);color:var(--on-dark)}
.top .eyebrow{color:var(--on-dark3)}.top .eyebrow::before{background:var(--gold)}
.top .lead{color:var(--on-dark2)}
.bar{position:sticky;top:0;z-index:50;background:var(--ink);color:var(--on-dark);border-bottom:1px solid var(--line-dark)}
.bar__in{display:flex;align-items:center;justify-content:space-between;gap:1rem 2rem;padding-block:.75rem}
.brand{display:flex;align-items:center;flex:none;text-decoration:none}
.brand img{height:clamp(40px,4vw,54px);width:auto}
.nav{display:none;gap:1.8rem;margin-left:auto;font-family:var(--ui);font-weight:500;font-size:.95rem}
.nav a{text-decoration:none;color:var(--on-dark2)}.nav a:hover{color:#fff}
@media(min-width:980px){.nav{display:flex}}
.bar__phone{display:none;font-family:var(--ui);font-weight:600;font-size:.95rem;color:var(--on-dark2);text-decoration:none}
@media(min-width:760px){.bar__phone{display:block}}
/* botões */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.6em;min-height:3.25rem;font-family:var(--ui);font-weight:700;font-size:var(--s0);text-decoration:none;color:#fff;background:var(--ledger);border:1.5px solid var(--ledger);padding:.7em 1.6em;border-radius:999px;cursor:pointer;transition:transform .16s,background .16s,box-shadow .16s}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(27,36,32,.22)}
.btn svg{width:1.15em;height:1.15em;flex:none}
.btn--sm{min-height:2.75rem;padding:.5em 1.2em;font-size:.95rem}
.btn--line{background:transparent;color:var(--on-dark);border-color:rgba(244,241,234,.5)}
.btn--line:hover{background:rgba(244,241,234,.08);box-shadow:none}
.btn--ghost{background:transparent;color:var(--ink);border-color:var(--line)}
.btn--ghost:hover{border-color:var(--ink);box-shadow:none}
.top .btn--ghost{color:var(--on-dark);border-color:rgba(244,241,234,.4)}
.btn--lite{background:#fff;color:var(--ink);border-color:#fff}
.btn--lite svg{color:var(--ledger)}
/* hero */
.hero{padding-top:clamp(2.8rem,7vw,6.5rem);padding-bottom:clamp(3rem,7vw,6rem)}
.hero h1{font-size:var(--s4);margin-top:1.1rem;max-width:20ch;text-wrap:pretty}
.hero h1:first-child{margin-top:0}
.hero .c12,.hero .c3{align-self:start}
.hero h1 .eyebrow{font-size:var(--s-1);line-height:1.4;margin-bottom:1.2rem}.h1-main{display:block}
.hero h1 em{font-style:italic;font-weight:500;color:var(--gold)}
.hero .lead{margin-top:1.4rem}
.cta{display:flex;flex-wrap:wrap;gap:.9rem;align-items:center;margin-top:2rem}
.hero__note{font-family:var(--ui);font-size:var(--s-1);color:var(--on-dark3);margin-top:1rem}
.sig{display:flex;align-items:center;gap:.9rem;margin-top:2rem;font-family:var(--ui);line-height:1.35}
.sig img{width:60px;height:60px;border-radius:50%;box-shadow:0 0 0 2px var(--gold)}
.sig b{display:block;font-size:1rem;color:var(--on-dark)}.sig span span{font-size:.9rem;color:var(--on-dark3)}
.trust{display:flex;flex-wrap:wrap;gap:.5rem 1.6rem;margin-top:1.6rem;padding-top:1.2rem;border-top:1px solid var(--line-dark);font-family:var(--ui);font-size:var(--s-1);color:var(--on-dark2)}
/* home: hero em duas colunas + índice de áreas */
@media(max-width:899px){.idx{display:none}}
.idx__t{padding-bottom:1rem;border-bottom:1px solid rgba(244,241,234,.22)}
.top .hero__side{align-self:end;padding-top:1.3rem;border-top:1px solid var(--line-dark)}
.hero__side .sig{margin-top:0}
.hero__side-txt{margin-top:1rem;font-size:var(--s0);color:var(--on-dark2)}
.idx a{display:flex;align-items:baseline;gap:1.1rem;padding:.95rem 0;border-bottom:1px solid var(--line-dark);text-decoration:none;color:var(--on-dark)}
.idx a i{font-style:normal;font-family:var(--ui);font-weight:600;font-size:.8rem;color:var(--gold)}
.idx a b{flex:1;font-family:var(--display);font-weight:500;font-size:var(--s1)}
.idx a::after{content:"\2192";font-family:var(--ui);color:var(--on-dark3);transition:transform .2s}
.idx a:hover::after{transform:translateX(4px);color:#fff}
/* pilares */
.pillar{padding-top:1.3rem;border-top:2px solid var(--ink)}
.pillar h3{font-size:var(--s1)}.pillar p{margin-top:.6rem;color:var(--text2)}
/* títulos de seção */
.h2wrap{max-width:60ch}
.h2wrap h2{font-size:var(--s3)}
.h2wrap .eyebrow+h2{margin-top:.8rem}
.h2wrap p{margin-top:1rem;color:var(--text2)}
.tint{background:var(--paper2)}
.white{background:var(--white);border-block:1px solid var(--line2)}
/* cards (áreas e situações) */
.cards{display:grid;gap:1.25rem var(--gap);margin-top:clamp(1.8rem,4vw,2.8rem)}
@media(min-width:640px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(min-width:900px){.cards--3{grid-template-columns:repeat(3,minmax(0,1fr))}}
.card{display:flex;flex-direction:column;gap:.5rem;background:var(--white);border:1px solid var(--line2);border-radius:var(--radius);padding:clamp(1.3rem,2.5vw,1.8rem);text-decoration:none;transition:border-color .16s,transform .16s}
a.card:hover{border-color:var(--ink);transform:translateY(-2px)}
.card h3{font-size:var(--s1)}
.card p{color:var(--text2);font-size:var(--s0)}
.card__ico{color:var(--ledger)}.card__ico svg{width:28px;height:28px}
.card__more{margin-top:auto;padding-top:.5rem;font-family:var(--ui);font-weight:600;font-size:var(--s-1);color:var(--gold-ink)}
/* lista de áreas (home) */
.rows{display:grid;column-gap:var(--gap);align-content:start}
@media(min-width:640px){.rows{grid-template-columns:repeat(2,minmax(0,1fr))}}
.row:nth-child(-n+2){border-top:1px solid var(--line)}
@media(max-width:639px){.row:nth-child(2){border-top:0}}
.row{display:flex;gap:1.1rem;align-items:flex-start;padding:1.35rem .2rem;border-bottom:1px solid var(--line);text-decoration:none;transition:background .16s}
.row:hover{background:var(--white)}
.row svg{flex:none;width:28px;height:28px;margin-top:.25rem;color:var(--ledger)}
.row div{flex:1}.row h3{font-size:var(--s1)}.row p{margin-top:.2rem;color:var(--text2);font-size:var(--s0)}
.row::after{content:"\2192";font-family:var(--ui);font-size:1.2rem;color:var(--gold-ink);margin-top:.2rem}
/* blocos de conteúdo (texto rastreável) */
.prose h2{font-size:var(--s2);margin-top:clamp(2.2rem,4vw,3rem)}
.prose h2:first-child{margin-top:0}
.prose p{margin-top:1rem;max-width:68ch}
.prose ul{margin-top:1rem;max-width:68ch;padding-left:1.1rem}
.prose li{margin-top:.45rem}
.prose strong{color:var(--ink)}
.prose a{color:var(--ledger);text-underline-offset:3px}
.prose h3{font-size:var(--s1);margin-top:2rem;scroll-margin-top:6rem}.prose h2[id],#perguntas{scroll-margin-top:6rem}
.prose .sec-cta{margin-top:1.4rem}.prose a.btn{color:#fff;text-decoration:none;overflow-wrap:normal}
.prose{overflow-wrap:break-word}
@media(min-width:900px){
 .prose--split{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:var(--gap)}
 .prose--split>h2{grid-column:1;margin-top:3rem;font-size:var(--s2)}
 .prose--split>:not(h2){grid-column:2/4;max-width:none}
 .prose--split>h2+*{margin-top:3rem}
 .prose--split>h2:first-child,.prose--split>h2:first-child+*{margin-top:0}
}.prose a,.prose strong{overflow-wrap:anywhere}
/* passos */
.steps{display:grid;gap:2rem var(--gap);grid-template-columns:minmax(0,1fr);margin-top:clamp(1.8rem,4vw,2.8rem)}
@media(min-width:900px){.steps{grid-template-columns:repeat(3,minmax(0,1fr))}}
.step .n{font-family:var(--display);font-style:italic;font-weight:500;font-size:clamp(2.6rem,2rem + 2vw,4rem);line-height:1;color:var(--gold-ink)}
.step h3{font-size:var(--s1);margin:1rem 0 .5rem;padding-top:1rem;border-top:1px solid var(--line)}
.step p{color:var(--text2)}
/* faixa CTA */
.band{background:var(--ledger);color:#fff}
.band__in{align-items:center}
@media(min-width:900px){.band__cta{display:flex;justify-content:flex-end}}
.band h2{font-size:var(--s3)}
.band p{margin-top:.7rem;font-size:var(--s1);color:#E3EEE8;max-width:50ch}
/* FAQ — nativo, rastreável, sem JS */
.faq{border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;cursor:pointer;padding:1.25rem 2.6rem 1.25rem 0;position:relative;font-family:var(--display);font-weight:600;font-size:var(--s1);line-height:1.35}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:.3rem;top:1.05rem;font-family:var(--ui);font-size:1.6rem;font-weight:400;color:var(--gold-ink);transition:transform .2s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq__a{padding:0 0 1.4rem;max-width:72ch;color:var(--text2)}
.faq__a p+p{margin-top:.8rem}
/* sobre / E-E-A-T */
.about{align-items:center}
.about__photo{width:100%;max-width:300px;border-radius:50%;box-shadow:0 0 0 10px var(--paper),0 0 0 11px var(--line)}
.about__quote{font-family:var(--display);font-style:italic;font-weight:500;font-size:var(--s2);line-height:1.3;margin-top:1rem}
.about__name{margin-top:1.1rem;font-family:var(--ui);font-weight:700}
.about__name span{font-weight:500;color:var(--text2)}
.about p.txt{margin-top:1rem;color:var(--text2)}
.about .links{display:flex;flex-wrap:wrap;gap:1.4rem;margin-top:1.2rem;font-family:var(--ui);font-weight:600;font-size:.95rem}
.about .links a{text-underline-offset:5px}
/* contato + formulário */
.contact h2{font-size:var(--s2)}
.contact .lead{margin-top:1rem;font-size:var(--s0)}
.form__row{display:grid;gap:0 1rem}
@media(min-width:640px){.form__row{grid-template-columns:1fr 1fr}}
.napcard{margin-top:1.4rem;font-size:var(--s0);line-height:1.85;color:var(--text2)}
.napcard b{font-family:var(--ui);color:var(--ink)}
.napcard a{color:var(--ink);text-underline-offset:3px}
.form{background:var(--white);border:1px solid var(--line2);border-radius:var(--radius);padding:clamp(1.4rem,3vw,2.2rem)}
.form h3{font-size:var(--s1);margin-bottom:1.1rem}
.field{margin-bottom:1rem}
.field label{display:block;font-family:var(--ui);font-weight:600;font-size:.92rem;color:var(--ink);margin-bottom:.4rem}
.field input,.field textarea{width:100%;min-height:3rem;font-family:var(--body);font-size:var(--s0);color:var(--ink);background:var(--white);border:1px solid rgba(27,36,32,.32);border-radius:4px;padding:.65em .85em}
.field input:focus,.field textarea:focus{border-color:var(--ink);outline:none;box-shadow:0 0 0 3px rgba(201,161,91,.35)}
.field textarea{min-height:110px;resize:vertical}
.form .btn{width:100%;margin-top:.4rem}
.form small{display:block;margin-top:.9rem;color:var(--muted);font-size:var(--s-1)}
/* rodapé */
.foot{background:var(--ink);color:var(--on-dark);padding-block:clamp(3rem,6vw,4.5rem) 0}
.foot__grid{display:grid;gap:2.4rem;grid-template-columns:1fr}
@media(min-width:760px){.foot__grid{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:var(--gap)}}
.foot__logo{width:170px}
.foot__t{font-family:var(--ui);font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem;font-weight:700}
.foot a,.foot p{color:var(--on-dark2);text-decoration:none;display:block;margin-bottom:.5rem;font-size:var(--s0)}
.foot a:hover{color:#fff;text-decoration:underline;text-underline-offset:3px}
.foot__legal{max-width:78ch;margin-top:2.6rem;padding-block:1.4rem 2.2rem;border-top:1px solid var(--line-dark);font-size:var(--s-1)!important;color:var(--on-dark3)!important;line-height:1.6}
/* botão flutuante do WhatsApp */
.fab{position:fixed;right:clamp(.9rem,3vw,1.8rem);bottom:clamp(.9rem,3vw,1.8rem);z-index:60;display:inline-flex;align-items:center;gap:.55em;min-height:3.5rem;background:var(--ledger);color:#fff;padding:0 1.15em;border-radius:999px;text-decoration:none;font-family:var(--ui);font-weight:700;box-shadow:0 8px 24px rgba(27,36,32,.3);transition:transform .16s}
.fab svg{width:1.45em;height:1.45em}
.fab:hover{transform:translateY(-3px)}
.fab{transition:transform .16s,opacity .2s}.fab--oculto{opacity:0;transform:translateY(1rem);pointer-events:none}.fab span{display:none}
@media(min-width:520px){.fab span{display:inline}}
@media(max-width:560px){.hero .cta .btn{width:100%}.band .btn{width:100%}}
"""

JS = r"""
(function(){"use strict";
 var Z="https://wa.me/5511995155021";
 // local do clique no WhatsApp (rótulo para o GA4)
 function whatsLoc(a){
  if(a.dataset&&a.dataset.loc) return a.dataset.loc;
  if(a.classList.contains("fab")) return "fab";
  if(a.closest(".bar")) return "header";
  if(a.closest(".hero")) return "hero";
  if(a.closest(".band")) return "cta_band";
  if(a.closest("#contato")) return "contato";
  if(a.closest(".foot")) return "footer";
  return "other";
 }
 function whatsEvent(loc,url){
  if(typeof gtag==="function"){gtag("event","whatsapp_click",{link_location:loc,link_url:url||"",transport_type:"beacon"});}
 }
 // dispara o evento em qualquer clique num link de WhatsApp
 document.addEventListener("click",function(e){
  var a=e.target.closest?e.target.closest('a[href*="wa.me"],a[href*="whatsapp"]'):null;
  if(a){whatsEvent(whatsLoc(a),a.href);}
 },true);
 // formulário -> WhatsApp (CTA secundário funciona sem backend)
 var f=document.getElementById("leadform");
 if(f){f.addEventListener("submit",function(e){e.preventDefault();
  var n=(f.nome.value||"").trim(),c=(f.contato.value||"").trim(),m=(f.msg.value||"").trim();
  var t="Olá! Meu nome é "+n+". "+(m||"Gostaria de uma consulta.")+(c?" Meu contato: "+c+".":"");
  whatsEvent("form","");
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
        anchor = f' id="{b["id"]}"' if b.get("id") else ""  # âncora usada pelos sitelinks do Google Ads
        if b.get("h3"):  # subtítulo dentro da seção (fica na coluna do texto)
            out.append(f'<h3{anchor}>{esc(b["h3"])}</h3>')
        else:
            out.append(f'<h2{anchor}>{esc(b["h2"])}</h2>')
        for p in b.get("p", []):
            out.append(f"<p>{p}</p>")  # p pode conter <strong>/<a> intencionais
        if b.get("ul"):
            out.append("<ul>" + "".join(f"<li>{li}</li>" for li in b["ul"]) + "</ul>")
        if b.get("cta"):  # botão de WhatsApp da seção (rótulo, link, local p/ o evento whatsapp_click)
            label, url, loc = b["cta"]
            out.append(f'<p class="sec-cta"><a class="btn" href="{url}" target="_blank" rel="noopener" data-loc="{loc}">{ZAP_SVG} {esc(label)}</a></p>')
    return "\n".join(out)

def steps_html(steps):
    out = []
    for i, s in enumerate(steps, 1):
        out.append(f'<div class="step"><p class="n">{i}</p><h3>{esc(s["t"])}</h3><p>{esc(s["d"])}</p></div>')
    return '<div class="steps">' + "".join(out) + "</div>"

def faq_html(faqs):
    out = ['<div class="faq">']
    for q in faqs:
        ans = "".join(f"<p>{p}</p>" for p in q["a"])
        out.append(f'<details><summary>{esc(q["q"])}</summary><div class="faq__a">{ans}</div></details>')
    out.append("</div>")
    return "".join(out)

def footer_links():
    links = "".join(f'<a href="/{slug}/">{label}</a>' for slug, label in PRACTICES)
    return links + '<a href="/noticias/" style="font-weight: bold;">Notícias & Decisões</a>'

def schema_for(page):
    legal = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "@id": f"{LANDING}/{page['slug']}/#legalservice",
        "name": NAP["name"],
        "description": page["meta"],
        "url": f"{LANDING}/{page['slug']}/",
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
        "logo": LANDING + LOGO,
        "image": LANDING + "/assets/og-lemes-advogados.jpg",
        "foundingDate": FOUNDED,
        "founder": {"@type": "Person", "name": NAP["lawyer"], "jobTitle": "Advogado", "identifier": NAP["oab"], "image": LANDING + PHOTO},
        "sameAs": SAME_AS,
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
HEAD = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<meta name="description" content="$meta">
<link rel="canonical" href="$canonical">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="#1B2420">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lemes Advogados">
<meta property="og:title" content="$title">
<meta property="og:description" content="$meta">
<meta property="og:url" content="$canonical">
<meta property="og:locale" content="pt_BR">
<meta property="og:image" content="$landing/assets/og-lemes-advogados.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Lemes Advogados — Diego Henrique Lemes, advogado em São Paulo">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="BR-SP">
<meta name="geo.placename" content="São Paulo">
<link rel="icon" href="/assets/diego-lemes-advogado-120.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Fonte sem bloquear render (media=print -> all no onload); texto aparece na hora. -->
<link rel="stylesheet" href="$fonts" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="$fonts"></noscript>
<!-- Google tag (gtag.js) — Google Ads + GA4 numa carga só (um clique rápido no -->
<!-- WhatsApp não se perde esperando dois scripts). Uma biblioteca, dois destinos. -->
<script async src="https://www.googletagmanager.com/gtag/js?id=$ads_id"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', '$ads_id');
 gtag('config', '$ga4_id');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "$clarity_id");
</script>
<style>$css</style>
<script type="application/ld+json">$schema</script>
</head>
<body>
"""

HEADER = r"""<header class="bar">
 <div class="wrap bar__in">
  <a class="brand" href="/" aria-label="Lemes Advogados — início"><img src="/assets/logo-claro.webp" alt="Lemes Advogados" width="373" height="157"></a>
  <nav class="nav" aria-label="Principal">$nav</nav>
  <a class="bar__phone" href="tel:$phone_tel">$phone_display</a>
  <a class="btn btn--line btn--sm" href="$whats" target="_blank" rel="noopener">$zap WhatsApp</a>
 </div>
</header>
"""

ABOUT = r"""<section class="section white" id="sobre">
 <div class="wrap g3 about">
  <div class="c1"><img class="about__photo" src="/assets/diego-lemes-advogado-360.webp" alt="Diego Henrique Lemes, advogado em São Paulo" width="360" height="360" decoding="async"></div>
  <div class="c23">
   <p class="eyebrow">$about_eyebrow</p>
   <p class="about__quote">“Quem conversa com você no primeiro dia é quem assina as peças e acompanha o processo até o fim.”</p>
   <p class="about__name">$lawyer <span>· $oab</span></p>
   <p class="txt">$bio</p>
   $about_extra
   <div class="links"><a href="https://www.instagram.com/lemesadvsp/" target="_blank" rel="noopener">Instagram @lemesadvsp</a><a href="https://www.linkedin.com/in/diego-henrique-lemes-8882b0/" target="_blank" rel="noopener">LinkedIn</a></div>
  </div>
 </div>
</section>
"""

CONTACT = r"""<section class="section wrap" id="contato">
 <div class="g3 contact">
  <div class="c1">
   <h2>$contact_h2</h2>
   <p class="lead">Prefere escrever? Preencha o formulário e a mensagem abre pronta no WhatsApp. A primeira conversa é sem compromisso.</p>
   <div class="napcard">
    <b>$name</b><br>
    $street — $district<br>
    $city/$region · CEP $cep<br>
    WhatsApp / Tel: <a href="$whats" target="_blank" rel="noopener">$phone_display</a><br>
    E-mail: <a href="mailto:$email">$email</a><br>
    $hours
   </div>
  </div>
  <form class="form c23" id="leadform">
   <h3>Conte seu caso</h3>
   <div class="form__row">
    <div class="field"><label for="nome">Seu nome</label><input id="nome" name="nome" type="text" required autocomplete="name"></div>
    <div class="field"><label for="contato">Telefone ou e-mail</label><input id="contato" name="contato" type="text" autocomplete="tel"></div>
   </div>
   <div class="field"><label for="msg">Resumo do seu caso</label><textarea id="msg" name="msg"></textarea></div>
   <button class="btn" type="submit">$zap Enviar pelo WhatsApp</button>
   <small>Ao enviar, você abre uma conversa no WhatsApp com os dados preenchidos. Suas informações não são compartilhadas com terceiros.</small>
  </form>
 </div>
</section>
"""

FOOTER = r"""<footer class="foot">
 <div class="wrap foot__grid">
  <div>
   <img class="foot__logo" src="/assets/logo-claro.webp" alt="Lemes Advogados" width="373" height="157" loading="lazy">
   <p style="margin-top:1rem">$name. Advocacia em $district, $city. Atendimento pessoal e linguagem clara.</p>
  </div>
  <div>
   <h2 class="foot__t">Áreas de atuação</h2>
   $footer_links
  </div>
  <div>
   <h2 class="foot__t">Contato</h2>
   <a href="$whats" target="_blank" rel="noopener">WhatsApp $phone_display</a>
   <a href="mailto:$email">$email</a>
   <p>$street</p>
   <p>$district, $city/$region · $cep</p>
   <a href="https://www.instagram.com/lemesadvsp/" target="_blank" rel="noopener">Instagram</a>
   <a href="https://www.linkedin.com/in/diego-henrique-lemes-8882b0/" target="_blank" rel="noopener">LinkedIn</a>
  </div>
 </div>
 <div class="wrap">
  <p class="foot__legal">$name · CNPJ $cnpj · Advogado responsável: $lawyer ($oab).<br>
  Conteúdo de caráter exclusivamente informativo, em conformidade com o Código de Ética e Disciplina da OAB e o Provimento nº 205/2021. Não constitui oferta de serviços, captação de clientela nem promessa de resultado. Cada caso é analisado individualmente.</p>
 </div>
</footer>

<a class="fab" href="$whats" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">$zap<span>Fale conosco</span></a>
<script>(function(){var f=document.querySelector('.fab'),h=document.querySelector('.hero .cta');if(!f||!h||!('IntersectionObserver' in window))return;var m=matchMedia('(max-width:899px)');new IntersectionObserver(function(e){f.classList.toggle('fab--oculto',m.matches&&e[0].isIntersecting)}).observe(h)})()</script>
<script>$js</script>
</body>
</html>
"""

AREA_BODY = r"""$header
<main id="conteudo">
<div class="top">
 <!-- HERO -->
 <section class="hero wrap g3" aria-labelledby="h1">
  <div class="c12">
   <p class="eyebrow">$eyebrow</p>
   <h1 id="h1">$h1</h1>
   <p class="lead">$hero_sub</p>
   <div class="cta">
    <a class="btn" href="$whats" target="_blank" rel="noopener">$zap Falar agora no WhatsApp</a>
    <a class="btn btn--ghost" href="#contato">Enviar mensagem</a>
   </div>
   <p class="hero__note">$hero_note</p>
  </div>
  <div class="c3 hero__side">
   <div class="sig"><img src="/assets/diego-lemes-advogado-120.webp" alt="" width="120" height="120"><span><b>$lawyer</b><span>Advogado · $oab</span></span></div>
   <p class="hero__side-txt">Atendimento direto com o advogado, do primeiro contato ao fim. Escritório em $district, $city.</p>
  </div>
 </section>
</div>

 <!-- SITUAÇÕES / SERVIÇOS -->
 <section class="section wrap">
  <div class="g3"><div class="c12 sec-head"><p class="eyebrow">$sit_eyebrow</p><h2>$sit_h2</h2><p>$sit_sub</p></div></div>
  $cards
 </section>

 <!-- CONTEÚDO RASTREÁVEL -->
 <section class="section tint">
  <div class="wrap prose prose--split">
  $prose
  </div>
 </section>

 <!-- PASSOS -->
 <section class="section wrap">
  <div class="g3"><div class="c12 sec-head"><h2>$steps_h2</h2></div></div>
  $steps
 </section>

 <!-- FAQ -->
 <section class="section tint">
  <div class="wrap g3">
   <div class="c1 sec-head"><h2 id="perguntas">$faq_h2</h2></div>
   <div class="c23">$faq</div>
  </div>
 </section>

 <!-- FAIXA CTA -->
 <section class="section band">
  <div class="wrap g3 band__in">
   <div class="c12"><h2>$band_h2</h2><p>$band_sub</p></div>
   <div class="c3 band__cta"><a class="btn btn--lite" href="$whats" target="_blank" rel="noopener">$zap Falar no WhatsApp</a></div>
  </div>
 </section>

 <!-- SOBRE / E-E-A-T -->
$about

 <!-- CONTATO + FORMULÁRIO -->
$contact
</main>

"""



# ============================================================================ #
#  CONTEÚDO DE CADA PÁGINA
# ============================================================================ #
PAGES = {}

# Link de WhatsApp com mensagem própria (o clique segue no evento whatsapp_click do GA4)
def _wa(msg):
    from urllib.parse import quote
    return "https://wa.me/5511995155021?text=" + quote(msg, safe="")
WHATS_IMOB_CERT = _wa("Olá, vim pelo site e preciso das certidões para compra e venda de um imóvel")

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
 "hero_sub":"Divórcio, inventário, partilha, contratos e pequenas causas. Atendimento próximo e personalizado por um advogado cível especialista para orientar e defender seus direitos com total transparência.",
 "hero_note":"Advogado cível perto de você · Atendimento em todo São Paulo",
 "knows":["Direito Civil","Divórcio","Inventário","Partilha de bens","Pequenas causas","Contratos","Indenizações"],
 "sit_eyebrow":"Áreas do direito cível",
 "sit_h2":"Como podemos ajudar",
 "sit_sub":"Atuo nas principais demandas cíveis das famílias e do dia a dia. Clique para ver a página específica.",
 "cards":[
  {"t":"Divórcio","d":"Consensual ou litigioso, no cartório ou na Justiça. Veja como funciona e quanto custa.","href":"/divorcio/"},
  {"t":"Inventário e partilha","d":"Partilha de bens após o falecimento, no cartório ou judicial. Prazos, custos e tabela OAB.","href":"/inventario/"},
  {"t":"Pequenas causas","d":"Cobranças, problemas de consumo e conflitos de menor valor no Juizado Especial."},
  {"t":"Contratos e indenizações","d":"Revisão de contratos, descumprimento, danos morais e materiais."},
  {"t":"Cobranças e dívidas","d":"Negociação, defesa em cobranças indevidas e inscrição irregular em cadastros."},
  {"t":"Família e união estável","d":"Reconhecimento e dissolução de união estável, alimentos e guarda."},
 ],
 "prose":[
  {"h2":"Advogado cível perto de você em São Paulo",
   "p":["Se você precisa de um <strong>advogado cível em São Paulo</strong> para assessorar em questões familiares, contratuais ou patrimoniais, o escritório está localizado em <strong>Perdizes, São Paulo</strong> e atende tanto de forma digital quanto física. O atendimento inicial do seu caso é feito de forma prática via WhatsApp diretamente pelo advogado cível responsável, garantindo acompanhamento especializado do início ao fim do processo."]},
  {"h2":"Pequenas causas: quando vale a pena", "id":"pequenas-causas",
   "p":["O Juizado Especial Cível julga conflitos de até 40 salários mínimos, tais como cobranças indevidas, problemas em relações de consumo e descumprimento de pequenos contratos. Para causas de até 20 salários mínimos, a lei permite ingressar sem assistência jurídica, porém o acompanhamento de um <strong>advogado cível</strong> experiente aumenta significativamente as chances de êxito e evita falhas técnicas processuais que costumam atrasar ou anular seu direito."]},
  {"h2":"Divórcio e inventário: as demandas mais comuns",
   "p":["A atuação de um <strong>advogado cível</strong> qualificado também é de suma importância em momentos cruciais de transição e partilha patrimonial, tais como o <strong>divórcio</strong> e o <strong>inventário</strong>. Quando há consenso e concordância mútua, ambos os procedimentos podem ser realizados extrajudicialmente de maneira rápida e com custos reduzidos diretamente em cartório. Conte com a assessoria especializada do nosso advogado cível e confira os guias completos sobre como funciona o <a href=\"/divorcio/\">divórcio em cartório</a> e o <a href=\"/inventario/\">inventário extrajudicial</a>."]},
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
  {"h2":"Como funciona o divórcio no cartório", "id":"cartorio",
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
 "title":"Quanto Custa Advogado de Inventário em SP? Tabela OAB",
 "meta":"Quanto cobra um advogado para inventário em SP: honorários pela tabela OAB/SP, ITCMD de 4% e custos de cartório. Peça sua estimativa pelo WhatsApp.",
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
  {"h2":"Quanto custa um advogado para inventário?", "id":"custo",
   "p":["O custo do inventário tem três componentes: os <strong>honorários do advogado</strong>, o imposto <strong>ITCMD</strong> (em São Paulo, em regra 4% sobre o valor dos bens) e as <strong>taxas de cartório</strong> (emolumentos). Os honorários costumam ser definidos como um percentual sobre o valor do espólio, com base em referências como a tabela da OAB/SP.",
        "Como cada inventário envolve patrimônios diferentes, o ideal é uma estimativa personalizada. Envie a relação dos bens pelo WhatsApp que faço um cálculo aproximado para você."]},
  {"h2":"Qual a tabela OAB para inventário em SP",
   "p":["A <strong>Tabela de Honorários da OAB/SP</strong> traz percentuais de referência para serviços advocatícios, inclusive inventário e partilha. Ela serve de parâmetro mínimo e orienta a contratação, mas o valor final é combinado entre as partes conforme a complexidade do caso. Explico esse ponto com transparência antes de iniciar."]},
  {"h2":"Como funciona o inventário extrajudicial", "id":"extrajudicial",
   "p":["O inventário extrajudicial é feito por <strong>escritura pública em cartório</strong> e é possível quando <strong>todos os herdeiros são maiores e capazes</strong>, estão <strong>de acordo</strong> com a partilha e há advogado acompanhando. É o caminho mais rápido — pode ser concluído em semanas. Havendo herdeiro menor, incapaz, testamento ou conflito, o inventário deve correr na Justiça."]},
  {"h2":"Qual o prazo para abrir inventário?", "id":"prazo",
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

PAGES["familia"] = {
 "slug":"familia",
 "title":"Advogado de Família em SP | Guarda, Pensão e Divórcio",
 "meta":"Guarda, pensão alimentícia, união estável, partilha ou divórcio? Advogado de família em São Paulo. Fale agora pelo WhatsApp, com discrição.",
 "h1":"Advogado de Família em São Paulo",
 "hero_sub":"Guarda de filhos, pensão alimentícia, união estável, partilha de bens ou divórcio? Cuido de cada caso com atenção e discrição, e você fala direto comigo pelo WhatsApp.",
 "hero_note":"Guarda e pensão · União estável · Divórcio · Atendimento reservado",
 "knows":["Direito de Família","Guarda de filhos","Pensão alimentícia","União estável","Partilha de bens","Divórcio","Alienação parental"],
 "sit_eyebrow":"Áreas do direito de família",
 "sit_h2":"Como posso ajudar",
 "sit_sub":"Atuo nas principais demandas de família. Clique no divórcio para ver a página específica.",
 "cards":[
  {"t":"Divórcio","d":"Consensual ou litigioso, no cartório ou na Justiça. Veja como funciona, quanto custa e os prazos.","href":"/divorcio/"},
  {"t":"Guarda de filhos","d":"Definição da guarda (em regra compartilhada), convivência e responsabilidades, sempre no melhor interesse da criança."},
  {"t":"Pensão alimentícia","d":"Fixação, revisão (para mais ou para menos) e execução de pensão atrasada, para filhos e, em alguns casos, ex-cônjuge."},
  {"t":"União estável","d":"Reconhecimento e dissolução de união estável, inclusive homoafetiva, com partilha e definição de direitos."},
  {"t":"Partilha de bens","d":"Divisão do patrimônio conforme o regime de casamento ou união: imóveis, veículos, contas e dívidas."},
  {"t":"Alienação parental","d":"Quando um dos pais tenta afastar o filho do outro. A lei prevê medidas para proteger o convívio."},
 ],
 "prose":[
  {"h2":"O que faz um advogado de família",
   "p":["O advogado de família cuida dos conflitos mais pessoais: <strong>divórcio</strong>, <strong>guarda</strong>, <strong>pensão alimentícia</strong>, <strong>união estável</strong> e <strong>partilha de bens</strong>. São temas delicados, e o meu compromisso é conduzir cada caso com <strong>discrição</strong>, linguagem clara e o menor desgaste possível. O escritório fica em <strong>Perdizes, São Paulo</strong>, e o atendimento começa pelo WhatsApp, com a mesma pessoa do início ao fim."]},
  {"h2":"Como funciona a guarda dos filhos", "id":"guarda",
   "p":["A regra hoje é a <strong>guarda compartilhada</strong>, em que ambos os pais participam das decisões sobre a vida do filho, com definição da convivência (as antigas “visitas”). A guarda unilateral só é fixada em situações específicas, quando um dos pais não pode ou não deve exercê-la. Em qualquer caso, o critério que orienta a decisão é o <strong>melhor interesse da criança</strong>."]},
  {"h2":"Pensão alimentícia: como é definida, revisada e cobrada", "id":"pensao",
   "p":["A pensão é fixada conforme o <strong>binômio necessidade e possibilidade</strong> — o que o filho precisa e o que o alimentante pode pagar. Quando a situação de qualquer um muda, cabe <strong>revisão</strong> (para aumentar ou reduzir) ou até exoneração.",
        "Se a pensão não é paga, existe a <strong>execução de alimentos</strong>, que pode levar à <strong>penhora de bens</strong> e até à <strong>prisão do devedor</strong>. Se você precisa cobrar pensão atrasada ou revisar o valor, me envie os detalhes pelo WhatsApp."]},
  {"h2":"União estável: reconhecimento e dissolução", "id":"uniao-estavel",
   "p":["A união estável é a convivência pública, contínua e duradoura com objetivo de constituir família — e gera <strong>direitos patrimoniais e sucessórios</strong> semelhantes aos do casamento. Pode ser reconhecida ou dissolvida em cartório (quando há acordo) ou na Justiça, com <strong>partilha dos bens</strong> adquiridos na constância da união. Um <strong>contrato de convivência</strong> ajuda a definir o regime de bens e evitar disputas futuras."]},
 ],
 "steps_h2":"Como conduzo seu caso",
 "steps":[
  {"t":"Conversa reservada","d":"Você me conta a situação pelo WhatsApp, com total sigilo. Avalio o que cabe e qual o caminho."},
  {"t":"Organizo o caso","d":"Reúno documentos e defino a estratégia — acordo, cartório ou Justiça — com custos e prazos claros."},
  {"t":"Conduzo até o fim","d":"Cuido de toda a parte jurídica e mantenho você informado em cada etapa do processo."},
 ],
 "faq_h2":"Perguntas frequentes sobre direito de família",
 "faqs":[
  {"q":"O que faz um advogado de família?","a":["Atua nos conflitos de família: divórcio, guarda de filhos, pensão alimentícia, união estável, partilha de bens e alienação parental, entre outros. Orienta acordos, atua em cartório quando possível e representa o cliente na Justiça quando necessário."]},
  {"q":"Como funciona a guarda compartilhada?","a":["Na guarda compartilhada, ambos os pais participam das decisões sobre a vida do filho, com a convivência definida entre eles. É a regra atual e não depende de os pais morarem juntos. A guarda unilateral só é fixada em situações específicas, sempre no melhor interesse da criança."]},
  {"q":"Como é definido o valor da pensão alimentícia?","a":["Pelo binômio necessidade e possibilidade: o que o filho precisa e o quanto o alimentante pode pagar. Não há percentual fixo em lei. Quando a situação muda, o valor pode ser revisado para mais ou para menos, ou até cessar."]},
  {"q":"O que fazer quando a pensão não é paga?","a":["É possível ajuizar a execução de alimentos. Conforme o rito, o devedor pode ter bens penhorados e, no rito mais severo, ser preso pela dívida de pensão. Guarde os comprovantes do que não foi pago."]},
  {"q":"União estável precisa de partilha ao terminar?","a":["Sim. A dissolução da união estável, como o divórcio, exige a partilha dos bens adquiridos durante a convivência, conforme o regime aplicável. Havendo acordo, pode ser feita em cartório; havendo conflito, na Justiça."]},
 ],
 "band_h2":"Resolva sua questão de família com discrição",
 "band_sub":"Conte sua situação pelo WhatsApp, com total sigilo. Explico, sem compromisso, o caminho mais tranquilo para o seu caso.",
 "contact_h2":"Fale com um advogado de família",
 "about_line":"Atuação em Direito de Família — divórcio, guarda, pensão, união estável e partilha — com discrição e atenção a quem vive um momento delicado.",
}

PAGES["imobiliario"] = {
 "slug":"imobiliario",
 "title":"Advogado Imobiliário SP | Usucapião e Regularização",
 "meta":"Usucapião, regularização de imóvel, despejo ou reintegração de posse? Advogado imobiliário em São Paulo. Fale agora pelo WhatsApp, sem compromisso.",
 "h1":"Advogado Imobiliário em São Paulo",
 "hero_sub":"Usucapião, regularização de imóvel, despejo, reintegração de posse ou problema com construtora? Analiso seu caso com clareza e você fala direto comigo pelo WhatsApp.",
 "hero_note":"Usucapião e regularização · Despejo e posse · Atendimento direto com o advogado",
 "knows":["Direito Imobiliário","Usucapião","Usucapião extrajudicial","Reintegração de posse","Regularização de imóveis","Ação de despejo","Distrato de imóvel"],
 "sit_eyebrow":"Em que posso ajudar",
 "sit_h2":"Situações que mais atendo",
 "sit_sub":"Veja se o seu caso aparece abaixo — em todos há um caminho jurídico para regularizar, recuperar ou proteger o imóvel.",
 "cards":[
  {"t":"Usucapião","d":"Ocupa um imóvel há anos, sem escritura? A usucapião — judicial ou extrajudicial — pode reconhecer você como proprietário."},
  {"t":"Regularização de imóveis","d":"Imóvel sem escritura, sem registro ou preso a inventário? Regularizo a documentação para você poder vender, doar ou financiar."},
  {"t":"Reintegração de posse","d":"Imóvel invadido ou ocupado indevidamente? A ação de reintegração de posse busca devolver o bem a quem tem direito."},
  {"t":"Ação de despejo","d":"Inquilino em atraso ou contrato vencido? Conduzo o despejo por falta de pagamento ou por fim do contrato de locação."},
  {"t":"Atraso da construtora","d":"A obra atrasou ou você quer desistir da compra na planta? Busco a devolução dos valores pagos e a multa cabível."},
  {"t":"Compra e venda de imóvel","d":"Vício no imóvel, distrato ou desfazimento do negócio — analiso o contrato e defendo o seu interesse."},
 ],
 "prose":[
  {"h2":"Como funciona a usucapião de um imóvel", "id":"usucapiao",
   "p":["A usucapião é a forma de adquirir a propriedade de um imóvel pela <strong>posse prolongada</strong>, mansa e pacífica, ao longo do tempo previsto em lei. O prazo varia conforme a modalidade — de <strong>5 anos</strong> (usucapião especial urbana, para quem mora no imóvel e não tem outro) a <strong>15 anos</strong> (usucapião extraordinária), com regras intermediárias.",
        "Hoje, boa parte dos casos pode ser resolvida por <strong>usucapião extrajudicial</strong>, feita diretamente no cartório de registro de imóveis, sem processo judicial, quando não há conflito. É o caminho mais rápido — mas exige documentação e planta assinada por profissional habilitado. Avalio se o seu caso se enquadra."]},
  {"h2":"Como regularizar um imóvel sem escritura", "id":"regularizacao",
   "p":["Comprou um imóvel só com <strong>contrato de gaveta</strong>, recibo ou promessa de compra e venda, e nunca passou a escritura? Enquanto não há registro, você não é, formalmente, o dono — o que impede vender, financiar ou usar o imóvel em inventário. A regularização pode ser feita por <strong>adjudicação compulsória</strong>, escritura ou usucapião, conforme a situação. Analiso os documentos e indico o caminho mais rápido e barato."]},
  {"h2":"Reintegração de posse e ação de despejo: qual a diferença", "id":"despejo",
   "p":["A <strong>reintegração de posse</strong> serve para recuperar um imóvel que foi <strong>invadido ou ocupado indevidamente</strong>, quando não há contrato entre as partes. Já a <strong>ação de despejo</strong> é usada contra o <strong>inquilino</strong> — por falta de pagamento do aluguel ou pelo fim do contrato de locação. São ações diferentes, com ritos próprios; identifico qual se aplica e conduzo do início à desocupação."]},
  {"h2":"A construtora atrasou a entrega do imóvel, quais são meus direitos?", "id":"construtora",
   "p":["O contrato costuma prever um <strong>prazo de tolerância de até 180 dias</strong>. Passado esse prazo, o atraso é da construtora e você pode ter direito a <strong>multa contratual</strong>, <strong>indenização</strong> pelos prejuízos e até ao <strong>distrato com devolução dos valores pagos</strong>. Guarde o contrato, os comprovantes de pagamento e as comunicações com a construtora."]},
  {"h2":"Certidões para compra e venda de imóvel", "id":"certidoes",
   "p":["Antes do sinal e da escritura, a <strong>matrícula atualizada</strong> mostra quem é o proprietário e se há hipoteca, penhora, indisponibilidade ou ação averbada. Ela é o ponto de partida, mas não mostra dívidas e processos do vendedor que ainda não chegaram ao registro.",
        "Por isso levantamos também as certidões dos vendedores e do imóvel e analisamos os apontamentos antes da assinatura. Uma certidão com apontamento nem sempre impede o negócio: pode ser irrelevante, ser resolvida antes da escritura ou pedir uma cláusula específica no contrato."],
   "ul":["Matrícula atualizada, com ônus reais e ações",
         "Certidões de distribuição dos vendedores nos tribunais estaduais, federais e do trabalho pertinentes",
         "Certidões de protesto",
         "Certidão negativa de débitos trabalhistas (CNDT)",
         "Certidões de débitos federais, estaduais e municipais dos vendedores",
         "Situação do IPTU do imóvel e, em condomínio, declaração de quitação",
         "Taxas e emolumentos de cartórios e órgãos são pagos à parte"],
   "cta":("Falar sobre certidões do imóvel", WHATS_IMOB_CERT, "imobiliario_certidoes")},
  {"h2":"Due diligence completa", "id":"due-diligence",
   "p":["Para compra de imóvel de empresa, aquisição de participação societária, inventário, divórcio ou licitação, veja como funciona a <a href=\"/societario/#due-diligence\">due diligence e o levantamento de certidões</a>."]},
 ],
 "steps_h2":"Do primeiro contato à solução",
 "steps":[
  {"t":"Você me conta a situação","d":"Mande uma mensagem no WhatsApp explicando o que houve com o imóvel. Faço as perguntas certas, sem juridiquês."},
  {"t":"Analiso a documentação","d":"Confiro os documentos do imóvel e digo com honestidade qual o caminho e as reais chances."},
  {"t":"Regularizo ou entro com a ação","d":"Conduzo a usucapião, a regularização, o despejo ou a ação cabível, e você acompanha cada passo."},
 ],
 "faq_h2":"Perguntas frequentes sobre direito imobiliário",
 "faqs":[
  {"q":"O que é usucapião e quem tem direito?","a":["Usucapião é a aquisição da propriedade pela posse prolongada do imóvel, de forma mansa e pacífica, pelo prazo previsto em lei (de 5 a 15 anos, conforme a modalidade). Tem direito quem ocupa o imóvel como se fosse dono, sem oposição, e cumpre os requisitos legais da modalidade aplicável."]},
  {"q":"Qual a diferença entre usucapião judicial e extrajudicial?","a":["A extrajudicial é feita diretamente no cartório de registro de imóveis, sem processo, quando não há conflito e a documentação está completa — é mais rápida. A judicial corre na Justiça, necessária quando há discordância de confrontantes, herdeiros ou do antigo proprietário, ou quando falta documentação."]},
  {"q":"Como regularizar um imóvel sem escritura?","a":["Depende de como o imóvel foi adquirido. Havendo contrato de compra e venda, é possível a adjudicação compulsória ou a lavratura da escritura; em outros casos, a usucapião. O primeiro passo é analisar os documentos que você tem para indicar o caminho mais rápido e econômico."]},
  {"q":"Como funciona a ação de despejo por falta de pagamento?","a":["Quando o inquilino deixa de pagar o aluguel, o locador pode ingressar com ação de despejo. O inquilino pode, em regra, evitar o despejo quitando o débito no prazo legal (purgação da mora). Não havendo pagamento, a Justiça determina a desocupação do imóvel."]},
  {"q":"A construtora atrasou a entrega do imóvel, o que posso fazer?","a":["Após o prazo de tolerância (em geral 180 dias), o atraso é responsabilidade da construtora e pode gerar multa, indenização pelos prejuízos e até o distrato com devolução dos valores pagos. Guarde o contrato, os comprovantes e as comunicações para embasar o pedido."]},
 ],
 "band_h2":"Regularize ou recupere seu imóvel",
 "band_sub":"Conte sua situação pelo WhatsApp. Explico, sem compromisso, o caminho para regularizar a documentação ou recuperar a posse do imóvel.",
 "contact_h2":"Fale com um advogado imobiliário",
 "about_line":"Atuação em Direito Imobiliário — usucapião, regularização, posse e despejo — com análise clara da documentação e do melhor caminho para cada caso.",
}

PAGES["empresarial"] = {
 "slug":"empresarial",
 "title":"Advogado Empresarial SP | Assessoria e Defesa de Empresas",
 "meta":"Advogado empresarial em São Paulo. Assessoria preventiva, societário, acordos de sócios, marcas e contratos comerciais. Fale agora pelo WhatsApp.",
 "h1":"Advogado Empresarial em São Paulo",
 "hero_sub":"Assessoria societária, elaboração de contratos comerciais, proteção de patrimônio e defesa em litígios. Atendimento boutique sob medida para blindar e impulsionar a sua empresa.",
 "hero_note":"Assessoria societária e contratual · Blindagem de patrimônio · Atendimento boutique ágil",
 "knows":["Direito Empresarial","Sociedades","Acordo de sócios","Holding familiar","Registro de marcas","Contratos comerciais","Defesa tributária"],
 "sit_eyebrow":"Como apoiar seu negócio",
 "sit_h2":"Serviços e soluções empresariais",
 "sit_sub":"Veja se a sua demanda corporativa aparece abaixo — estruturamos defesas e arranjos preventivos sob medida para blindar, organizar e acelerar sua empresa.",
 "cards":[
  {"t":"Societário e Holding","d":"Constituição de sociedades, acordos de sócios, planos de vesting e holdings familiares para fins de blindagem patrimonial e eficiência de impostos."},
  {"t":"Contratos Empresariais","d":"Elaboração, análise e revisão de contratos de fornecedores, prestação de serviços, parcerias comerciais e locação não-residencial."},
  {"t":"Registro de Marcas","d":"Proteção jurídica da sua marca no INPI contra cópias, plágios e notificações extrajudiciais. Registre e blinde o seu maior ativo comercial."},
  {"t":"Compliance Trabalhista","d":"Auditoria trabalhista preventiva para eliminar brechas de processos de funcionários, acordos extrajudiciais e adequação jurídica de rotinas."},
  {"t":"Planejamento Tributário","d":"Redução legal da carga de impostos, recuperação de créditos fiscais e defesas contra autuações administrativas e execuções fiscais."},
  {"t":"Defesa em Litígios","d":"Atuação contenciosa especializada e estratégica em processos judiciais movidos por clientes, ex-sócios, fornecedores ou cobranças indevidas."},
 ],
 "prose":[
  {"h2":"A importância vital do Acordo de Sócios (Quotas/Ações)",
   "p":["Em qualquer sociedade (Limitada ou Anônima), o Contrato Social padrão de Junta Comercial é extremamente insuficiente para prever desentendimentos e conflitos futuros. O <strong>Acordo de Sócios</strong> é o contrato de gaveta ideal para estabelecer as regras privadas de tomada de decisão, dissolução de impasse, direito de preferência e critérios de saída de um sócio (valuation).",
        "Ele funciona como um 'seguro contra brigas', impedindo que problemas pessoais paralisem a operação, travem as contas bancárias do negócio ou levem a empresa à dissolução forçada."]},
  {"h2":"Blindagem Patrimonial e Sucessão com Holding Familiar",
   "p":["A constituição de uma <strong>holding familiar ou patrimonial</strong> é o mecanismo corporativo mais sólido para blindar os bens imóveis e o patrimônio pessoal dos sócios contra riscos operacionais e trabalhistas da empresa principal.",
        "Além disso, ela organiza a sucessão dos bens em vida (planejamento sucessório), eliminando por completo a necessidade, os custos astronômicos e a lentidão de um inventário judicial tradicional para os herdeiros, garantindo que o negócio continue operando normalmente."]},
  {"h2":"Por que registrar sua Marca no INPI é um ato urgente",
   "p":["Utilizar uma marca sem ter o seu registro oficial no INPI (Instituto Nacional da Propriedade Industrial) expõe a empresa a um risco existencial gravíssimo. Qualquer concorrente pode registrar o mesmo nome antes de você e te enviar uma notificação judicial exigindo a <strong>mudança imediata de nome fantasia, logomarcas, fachadas, redes sociais e domínios de site da noite para o dia</strong>, sob pena de pesadas multas diárias.",
        "O registro da marca é a única ferramenta jurídica que garante a propriedade e o uso exclusivo do seu nome comercial em todo o território nacional."]},
 ],
 "steps_h2":"Como funciona o atendimento corporativo",
 "steps":[
  {"t":"Diagnóstico inicial","d":"Entendemos a operação, o setor e as principais dores ou riscos da sua empresa pelo WhatsApp, de forma direta e sem burocracia."},
  {"t":"Análise documental","d":"Revisamos o contrato social atual, os principais contratos vigentes e processos ativos para identificar gargalos e propor blindagem."},
  {"t":"Execução e Implementação","d":"Redigimos as minutas sob medida, reestruturamos as defesas ou registramos a sua marca para que você possa focar no crescimento do negócio."},
 ],
 "faq_h2":"Perguntas frequentes sobre direito empresarial",
 "faqs":[
  {"q":"O que é e para que serve uma Holding Familiar?","a":["É uma empresa constituída com o objetivo de administrar e centralizar o patrimônio de uma família (imóveis, participações societárias, ativos). Ela serve para proteger legalmente os bens familiares contra riscos operacionais das empresas de mercado, planejar a herança em vida sem necessidade de inventário futuro e economizar impostos na locação e venda de bens."]},
  {"q":"Por que o Contrato Social padrão de internet é perigoso?","a":["Porque ele é genérico e não prevê conflitos reais. Ele não diz o que acontece se um sócio falecer (se os herdeiros assumem ou são pagos), como calcular o valor da empresa para pagar quem sai, ou quem tem a palavra final em impasses. Qualquer briga em um contrato genérico pode parar a operação da empresa na Justiça."]},
  {"q":"O que acontece se eu não registrar minha marca no INPI?","a":["Você corre o risco de ser notificado a qualquer momento por outra empresa que registrou a marca primeiro, sendo obrigado a remover seu site do ar, mudar de redes sociais, descartar embalagens e mudar de nome fantasia da noite para o dia, além de poder sofrer ação de perdas e danos pelo uso indevido da marca alheia."]},
  {"q":"Como o escritório pode ajudar na redução de processos trabalhistas?","a":["Através de um compliance e auditoria trabalhista preventiva. Analisamos os contratos de trabalho, prestadores de serviços (PJ), horas extras e formas de remuneração para identificar e estancar brechas legais que geram processos judiciais, reduzindo drasticamente o passivo trabalhista da empresa."]},
 ],
 "band_h2":"Blinde e estruture o seu negócio hoje",
 "band_sub":"Agende um diagnóstico inicial preventivo e sem compromisso pelo WhatsApp. Analiso a estrutura e contratos da sua empresa para mitigar riscos comerciais.",
 "contact_h2":"Fale com o advogado especialista",
 "about_line":"Atuação em Direito Empresarial — acordo de sócios, holdings patrimoniais, blindagem de bens, contratos comerciais, marcas (INPI) e assessoria preventiva boutique.",
}


# ---------------------------------------------------------------------------- #
#  SOCIETÁRIO — página única (rascunho 31/10/2026, ainda NÃO publicada)
#  Reúne alteração contratual, abertura, atos societários e due diligence.
#  Fora de PRACTICES de propósito: não entra na home, no rodapé nem no sitemap
#  até o OK do Diego. Sem preço, sem "grátis", sem promessa (Provimento 205/2021).
#  Não citamos sociedade simples, associação nem fundação (atos de cartório de
#  RCPJ, fora do escopo — Diego, 31/10/2026).
#  Âncoras estáveis (usadas pelos anúncios): #alteracao-contratual #abertura-de-empresa
#  #atos-societarios #due-diligence #como-funciona #documentos #perguntas
#  e subâncoras #endereco #cnae #nome-empresarial #socios #consolidacao #tipos #holding
#  #atas #contas #reorganizacao #baixa #imovel #empresa #inventario #licitacao #certidoes
# ---------------------------------------------------------------------------- #

WHATS_SOC = _wa("Olá, vim pelo site e preciso de um serviço societário para a minha empresa")
WHATS_ALT = _wa("Olá, vim pelo site e preciso fazer uma alteração contratual da minha empresa")
WHATS_ABR = _wa("Olá, vim pelo site e quero abrir uma empresa")
WHATS_ATOS = _wa("Olá, vim pelo site e preciso registrar um ato societário (ata, aprovação de contas, cisão, incorporação, distrato ou baixa)")
WHATS_DD = _wa("Olá, vim pelo site e preciso de uma due diligence / levantamento de certidões")

PAGES["societario"] = {
 "slug":"societario",
 "eyebrow":"Direito Societário · São Paulo",
 "whats": WHATS_SOC,
 "title":"Alteração Contratual e Serviços Societários em SP | Advogado",
 "meta":"Alteração contratual, abertura de empresa, atas, cisão, incorporação, distrato e due diligence com advogado. Registro na JUCESP e assinatura pelo gov.br.",
 "h1":"Alteração Contratual e Serviços Societários em São Paulo",
 "hero_sub":"Alteração do contrato social, abertura de empresa, atas e reorganizações, encerramento e due diligence, conduzidos por advogado, com registro na JUCESP e assinatura dos sócios pelo gov.br.",
 "hero_note":"Processo 100% online · Assinatura pelo gov.br · Registro na JUCESP · Atendimento direto com o advogado",
 "knows":["Alteração contratual","Contrato social","JUCESP","Direito societário","Abertura de empresa","Sociedade limitada","Sociedade anônima","Holding","Ata de reunião de sócios","Cisão","Incorporação","Distrato social","Due diligence","Certidões negativas"],
 "sit_eyebrow":"O que fazemos",
 "sit_h2":"Serviços societários",
 "sit_sub":"Escolha o assunto para ir direto à explicação. Cada ato tem forma, quórum e documentos próprios.",
 "cards":[
  {"t":"Alteração contratual","d":"Endereço, atividades (CNAE), nome empresarial, sócios, capital, administração e consolidação do contrato social.","href":"#alteracao-contratual"},
  {"t":"Abertura de empresa","d":"Constituição de LTDA, SLU, S.A., empresário individual e holding, com contrato social pensado para a operação.","href":"#abertura-de-empresa"},
  {"t":"Atos societários","d":"Atas, aprovação de contas, distribuição de lucros, cisão, incorporação, fusão, transformação, distrato e baixa.","href":"#atos-societarios"},
  {"t":"Due diligence e certidões","d":"Matrícula e certidões levantadas e analisadas para compra de imóvel ou empresa, inventário, divórcio e licitação.","href":"#due-diligence"},
  {"t":"Como funciona","d":"Atendimento pelo WhatsApp, minutas revisadas por advogado, assinatura pelo gov.br e protocolo online.","href":"#como-funciona"},
  {"t":"Documentos","d":"O que costuma ser pedido em cada caso. Antes de pedir, consultamos sozinhos o que é público.","href":"#documentos"},
 ],
 "prose":[
  # ---------------- ALTERAÇÃO CONTRATUAL ----------------
  {"h2":"Alteração contratual", "id":"alteracao-contratual",
   "p":["A alteração do contrato social da LTDA ou SLU é feita pela internet: consulta de viabilidade na Prefeitura (quando muda endereço ou atividade), Documento Básico de Entrada (DBE) na Receita Federal, instrumento assinado digitalmente pelos sócios e registro na <strong>JUCESP</strong>. Depois do registro, conferimos o CNPJ, a inscrição estadual e o cadastro municipal (CCM).",
        "Uma alteração pode reunir vários atos no mesmo instrumento, o que costuma economizar tempo e taxas públicas."],
   "cta":("Falar sobre alteração contratual", WHATS_ALT, "alteracao-contratual")},
  {"h3":"Mudança de endereço da empresa", "id":"endereco",
   "p":["Antes de assinar o contrato de locação, vale consultar a viabilidade: a Prefeitura verifica se a atividade é permitida no endereço (zoneamento) e se é preciso licença de funcionamento. Em São Paulo, o pedido exige o número do IPTU (SQL). Também é preciso definir se a empresa vai atender público e ter estoque no local ou usá-lo apenas como endereço fiscal (escritório virtual, coworking ou residência)."]},
  {"h3":"Inclusão ou troca de atividades (CNAE)", "id":"cnae",
   "p":["A atividade nova entra na cláusula do objeto social e nos códigos CNAE do CNPJ. Antes de pedir, conferimos se ela é permitida no Simples Nacional, se exige inscrição estadual ou licença específica e se cabe no endereço atual."]},
  {"h3":"Troca do nome empresarial", "id":"nome-empresarial",
   "p":["Com duas ou três opções de nome, fazemos a pesquisa de colidência na JUCESP e uma checagem de marcas no INPI: um nome igual a marca registrada de outra empresa pode gerar exigência no registro ou disputa depois."]},
  {"h3":"Entrada e saída de sócios, quotas, capital e administração", "id":"socios",
   "p":["Mudanças no quadro de sócios pedem mais cuidado do que uma alteração cadastral. Conferimos o contrato vigente, o quórum, o direito de preferência dos demais sócios, o valor da cessão das quotas e a responsabilidade de quem sai, que continua respondendo por obrigações da sociedade por até dois anos após a averbação da saída (art. 1.003 do Código Civil).",
        "Desde a Lei 14.451/2022, a modificação do contrato social da limitada exige, em regra, votos que representem mais da metade do capital social (art. 1.076 do Código Civil). O próprio contrato pode exigir mais; por isso a leitura do contrato atual vem antes da minuta."]},
  {"h3":"Alteração simples ou contrato consolidado?", "id":"consolidacao",
   "p":["A alteração simples traz só as cláusulas que mudaram. A consolidação reúne tudo num texto único e atualizado, o que facilita a vida com bancos, fornecedores e órgãos públicos quando a empresa já acumula várias alterações. Se o instrumento for levado a registro em até 30 dias da assinatura, os efeitos contam da data em que foi assinado (art. 36 da Lei 8.934/1994)."]},
  # ---------------- ABERTURA ----------------
  {"h2":"Abertura de empresa", "id":"abertura-de-empresa",
   "p":["A escolha do tipo societário define quem decide, como os sócios respondem e como alguém pode sair. Fazemos a pesquisa do nome, a viabilidade do endereço, o DBE, o contrato social ou estatuto, o registro na JUCESP e acompanhamos as inscrições (CNPJ, inscrição estadual, quando a atividade exige, e CCM). O regime tributário é definido junto com o contador."],
   "cta":("Falar sobre abertura de empresa", WHATS_ABR, "abertura-de-empresa")},
  {"h3":"LTDA, SLU, S.A. ou empresário individual?", "id":"tipos",
   "p":["Na <strong>limitada</strong>, cada sócio responde pelo valor das suas quotas, e todos respondem pela integralização do capital. A <strong>limitada unipessoal</strong> tem um único titular, com a mesma proteção. A <strong>sociedade anônima</strong> tem estatuto, ações e regras próprias de assembleia e administração. O <strong>empresário individual</strong> atua em nome próprio, e o patrimônio pessoal responde pelas dívidas do negócio.",
        "O contrato social padrão costuma ser genérico; administração, lucros, saída ou falecimento de sócio e solução de impasses ficam mais simples quando já estão escritos. O Estatuto da Advocacia exige o visto de advogado nos atos constitutivos de pessoas jurídicas, com dispensa para microempresas e empresas de pequeno porte (art. 1º, § 2º, da Lei 8.906/1994 e art. 9º, § 2º, da LC 123/2006)."]},
  {"h3":"Holding familiar e patrimonial", "id":"holding",
   "p":["A holding concentra participações societárias ou bens da família numa sociedade, com regras sobre quem administra, como os lucros são distribuídos e como as quotas passam aos herdeiros. A estrutura depende do patrimônio, dos custos de ITBI e ITCMD e dos objetivos da família, e por isso é analisada caso a caso, junto com o planejamento sucessório."]},
  # ---------------- ATOS ----------------
  {"h2":"Atos societários", "id":"atos-societarios",
   "p":["Decisões importantes da sociedade são tomadas em reunião ou assembleia e registradas em ata. Conferimos a forma de convocação, o quórum do contrato e da lei, redigimos os documentos e fazemos o arquivamento na JUCESP. Também cuidamos de outros arquivamentos, como abertura e encerramento de filial e nomeação ou destituição de administradores."],
   "cta":("Falar sobre um ato societário", WHATS_ATOS, "atos-societarios")},
  {"h3":"Atas de reunião e assembleia de sócios", "id":"atas",
   "p":["Na limitada, a reunião ou assembleia pode ser dispensada quando todos os sócios decidem por escrito (art. 1.072, § 3º, do Código Civil). Na S.A., as assembleias gerais ordinária (AGO) e extraordinária (AGE) seguem a Lei 6.404/1976."]},
  {"h3":"Aprovação de contas e distribuição de lucros", "id":"contas",
   "p":["Na limitada, os sócios devem se reunir ao menos uma vez por ano, nos quatro meses seguintes ao fim do exercício, para aprovar as contas e, se for o caso, eleger administradores (art. 1.078 do Código Civil). Na S.A., a assembleia geral ordinária segue o mesmo prazo (art. 132 da Lei 6.404/1976). A distribuição de lucros, inclusive desproporcional à participação, deve estar prevista no contrato e documentada em ata, com as demonstrações preparadas pelo contador."]},
  {"h3":"Cisão, incorporação, fusão e transformação", "id":"reorganizacao",
   "p":["Na <strong>incorporação</strong>, uma sociedade absorve outra; na <strong>fusão</strong>, duas ou mais se unem numa nova; na <strong>cisão</strong>, o patrimônio é dividido, total ou parcialmente. Essas operações exigem protocolo e justificação, avaliação do patrimônio, aprovação pelos sócios de cada sociedade e registro, e afetam contratos, empregados e credores.",
        "A <strong>transformação</strong> muda o tipo societário sem dissolver a empresa, por exemplo de empresário individual para LTDA ou SLU, ou de LTDA para S.A. Trabalhamos junto com o contador nos balanços e laudos."]},
  {"h3":"Distrato social e baixa da empresa", "id":"baixa",
   "p":["O encerramento regular passa pelo distrato (ou pela dissolução e liquidação), pelo registro na JUCESP e pela baixa do CNPJ, da inscrição estadual e do CCM. A lei permite a baixa mesmo com débitos, mas os sócios e administradores continuam respondendo por eles (art. 9º da LC 123/2006). Antes do distrato, levantamos pendências fiscais, trabalhistas e contratuais para planejar a saída."]},
  # ---------------- DUE DILIGENCE ----------------
  {"h2":"Due diligence e certidões", "id":"due-diligence",
   "p":["Antes de comprar, vender, partilhar ou contratar, levantamos a matrícula do imóvel e as certidões do vendedor ou da empresa nos órgãos e tribunais pertinentes, e entregamos um relatório com o que cada uma mostra e os pontos de atenção. A lista é ajustada ao negócio e aos lugares onde as partes viveram ou tiveram sede nos últimos anos."],
   "cta":("Falar sobre due diligence", WHATS_DD, "due-diligence")},
  {"h3":"Compra e venda de imóvel", "id":"imovel",
   "p":["A matrícula atualizada mostra o proprietário, as hipotecas, penhoras, indisponibilidades e ações averbadas. Desde a Lei 13.097/2015, esses registros devem estar concentrados na matrícula, e a Lei 14.382/2022 deixou de exigir certidões forenses para a validade do negócio. Ainda assim, as certidões do vendedor mostram riscos que não aparecem na matrícula: dívidas trabalhistas e fiscais, execuções e protestos que podem indicar insolvência e levar a discussões sobre fraude contra credores ou à execução. Por isso o levantamento costuma ser feito antes do sinal e da escritura."]},
  {"h3":"Aquisição de empresa", "id":"empresa",
   "p":["Na compra de uma empresa ou de participação societária, levantamos as certidões da sociedade e dos sócios, a situação na JUCESP e na Receita Federal, débitos fiscais e trabalhistas, protestos e processos, junto com a revisão do contrato social e das alterações, para identificar responsabilidades que passam ao comprador."]},
  {"h3":"Inventário, divórcio e licitação", "id":"inventario",
   "p":["No inventário e no divórcio, as certidões dos bens e das pessoas são exigidas pelo cartório ou pelo juiz para a partilha; organizamos o levantamento conforme o caso, inclusive as matrículas dos imóveis. Para habilitação em licitações, conferimos a regularidade fiscal, previdenciária e trabalhista da empresa e a validade de cada certidão na data da sessão."]},
  {"h3":"Quais certidões levantamos", "id":"certidoes",
   "p":[],
   "ul":["Matrícula atualizada do imóvel, com ônus reais e ações",
         "Certidão conjunta federal (Receita Federal e PGFN)",
         "Certidões estaduais (Secretaria da Fazenda e dívida ativa da PGE)",
         "Certidões municipais (tributos imobiliários e mobiliários)",
         "Certificado de regularidade do FGTS (CRF), para empresas",
         "Certidão negativa de débitos trabalhistas (CNDT)",
         "Certidões de protesto",
         "Certidões de distribuição dos tribunais estaduais, federais e do trabalho pertinentes",
         "Certidão de falência e recuperação judicial, quando aplicável",
         "Taxas, emolumentos e custas de cartórios e órgãos são pagos à parte"]},
  # ---------------- COMO FUNCIONA / DOCUMENTOS ----------------
  {"h2":"Como funciona", "id":"como-funciona",
   "p":["O atendimento é 100% online. Você informa o CNPJ (ou o imóvel) e o que precisa; consultamos os dados públicos e pedimos só o que falta. Os sócios assinam com a conta <strong>gov.br</strong> nível prata ou ouro, ou com certificado digital, sem precisar ir à Junta Comercial. O tempo total depende da Prefeitura, da Junta Comercial, dos cartórios e de eventuais exigências; informamos a previsão depois de ver o caso."]},
  {"h2":"Documentos", "id":"documentos",
   "p":["Antes de pedir, buscamos sozinhos o que é público (cartão CNPJ, ficha da JUCESP, inscrição estadual e CCM). Em regra, pedimos:"],
   "ul":["Último contrato social consolidado e alterações posteriores (para empresas já abertas)",
         "Dados de cada sócio: documento de identidade com data de emissão, CPF, estado civil e regime de bens, endereço",
         "Conta gov.br prata ou ouro (ou certificado digital) de quem vai assinar",
         "Dados do contador responsável, exigidos no DBE",
         "Para mudança de endereço ou abertura: endereço completo e número do IPTU (SQL)",
         "Para due diligence: matrícula ou endereço do imóvel e dados das partes",
         "As taxas públicas da Junta Comercial são pagas diretamente pela empresa"]},
 ],
 "steps_h2":"Etapas do atendimento",
 "steps":[
  {"t":"Você conta o que precisa","d":"Pelo WhatsApp, você informa o CNPJ ou o imóvel e o que vai mudar, abrir, registrar ou verificar."},
  {"t":"Documentos revisados por advogado","d":"Conferimos contrato, quórum e prazos, redigimos minutas e atas e levantamos as certidões necessárias."},
  {"t":"Assinatura, registro e relatório","d":"Colhemos as assinaturas pelo gov.br, protocolamos na JUCESP e acompanhamos as atualizações, ou entregamos o relatório da due diligence."},
 ],
 "faq_h2":"Perguntas frequentes",
 "faqs":[
  {"q":"Preciso ir à Junta Comercial ou a cartório?","a":["Para alterações, abertura e atos registrados na JUCESP, não: o pedido e o registro são feitos pela internet, e os sócios assinam com a conta gov.br (prata ou ouro) ou certificado digital."]},
  {"q":"A alteração atualiza o CNPJ automaticamente?","a":["Pelo sistema integrado (Redesim), o registro na JUCESP atualiza o CNPJ. A inscrição estadual e o cadastro municipal podem exigir passos próprios, e conferimos cada um ao final."]},
  {"q":"Minha empresa precisa ter contador?","a":["Sim. O DBE exige a indicação do contador responsável, e o regime tributário, a escrita fiscal e as demonstrações ficam com ele. Trabalhamos em conjunto."]},
  {"q":"Precisa de capital mínimo para abrir uma LTDA ou SLU?","a":["Não há capital mínimo na lei para LTDA e SLU. O valor deve ser compatível com a atividade, porque os sócios respondem pela integralização."]},
  {"q":"Toda ata precisa ser registrada na JUCESP?","a":["Não. Precisam de arquivamento as atas que alteram o contrato, elegem ou destituem administradores e outros atos que devam produzir efeitos perante terceiros. Indicamos caso a caso."]},
  {"q":"Dá para fechar uma empresa com dívidas?","a":["A lei permite a baixa mesmo com débitos, mas a responsabilidade dos sócios e administradores continua. Por isso levantamos as pendências antes do distrato."]},
  {"q":"Se a matrícula do imóvel está limpa, preciso das certidões do vendedor?","a":["A matrícula é o ponto de partida, mas não mostra dívidas e processos que ainda não foram averbados. As certidões do vendedor ajudam a avaliar o risco antes de pagar. Uma certidão com apontamento nem sempre impede o negócio: o relatório explica cada caso."]},
  {"q":"Atendem fora da capital?","a":["Sim, em todo o estado de São Paulo, já que o registro na JUCESP é online. A viabilidade segue as regras da Prefeitura de cada cidade, e a maioria das certidões é solicitada pela internet."]},
 ],
 "band_h2":"Precisa alterar, abrir, registrar ou verificar?",
 "band_sub":"Envie o CNPJ ou os dados do imóvel e conte o que precisa. Respondemos com os documentos necessários e as etapas do seu caso.",
 "contact_h2":"Fale com o advogado",
 "about_line":"Atuação em direito societário: alterações contratuais, abertura de empresas, atas, reorganizações, encerramento e due diligence, com registro na JUCESP.",
}

# ============================================================================ #
#  Render + escrita
# ============================================================================ #
def _base_mapping(page_title, page_meta, canonical, schema_json):
    m = dict(NAP)
    m.update({
        "title": page_title, "meta": page_meta, "canonical": canonical,
        "css": CSS, "js": JS, "zap": ZAP_SVG, "whats": WHATS, "landing": LANDING, "fonts": FONTS,
        "ads_id": ADS_ID, "ga4_id": GA4_ID, "clarity_id": CLARITY_ID,
        "footer_links": footer_links(), "schema": schema_json, "bio": BIO,
    })
    return m

def _fill(tpl, m):
    return Template(tpl).substitute(m)

def render(page):
    legal, faqpage = schema_for(page)
    schema_json = json.dumps({"@context":"https://schema.org","@graph":[legal, faqpage]}, ensure_ascii=False, indent=1)
    m = _base_mapping(page["title"], page["meta"], f"{LANDING}/{page['slug']}/", schema_json)
    if page.get("whats"): m["whats"] = page["whats"]  # mensagem própria do WhatsApp (ex.: societário)
    m.update({
        "h1": page["h1"], "hero_sub": page["hero_sub"], "hero_note": page["hero_note"], "eyebrow": page["eyebrow_top"],
        "sit_eyebrow": page["sit_eyebrow"], "sit_h2": page["sit_h2"], "sit_sub": page["sit_sub"],
        "cards": cards_html(page["cards"], three=True),
        "prose": prose_html(page["prose"]),
        "steps_h2": page["steps_h2"], "steps": steps_html(page["steps"]),
        "faq_h2": page["faq_h2"], "faq": faq_html(page["faqs"]),
        "band_h2": page["band_h2"], "band_sub": page["band_sub"],
        "contact_h2": page["contact_h2"],
        "nav": NAV_AREA, "about_eyebrow": "O advogado",
        "about_extra": f'<p class="txt">{page["about_line"]}</p>',
    })
    m["header"] = _fill(HEADER, m)
    m["about"] = _fill(ABOUT, m)
    m["contact"] = _fill(CONTACT, m)
    return _fill(HEAD, m) + _fill(AREA_BODY, m) + _fill(FOOTER, m)

def render_home():
    m = _base_mapping(HOME["title"], HOME["meta"], f"{LANDING}/", json.dumps(schema_home(), ensure_ascii=False, indent=1))
    idx = "".join(f'<a href="/{s}/"><i>{n:02d}</i><b>{dict(PRACTICES)[s]}</b></a>' for n, s in enumerate(HOME["hero_areas"], 1))
    rows = "".join(
        f'<a class="row" href="/{s}/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{AREA_ICONS[s]}"/></svg>'
        f'<div><h3>{dict(PRACTICES)[s]}</h3><p>{esc(AREA_LINES[s])}</p></div></a>'
        for s, _ in PRACTICES)
    pillars = "".join(f'<div class="pillar"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in HOME["pillars"])
    m.update({
        "nav": NAV_HOME, "idx": idx, "rows": rows, "pillars": pillars,
        "prose": prose_html(HOME["prose"]), "steps": steps_html(HOME["steps"]), "faq": faq_html(HOME["faqs"]),
        "about_eyebrow": "O escritório", "about_extra": "",
        "contact_h2": "Fale com um advogado em São Paulo",
    })
    m["header"] = _fill(HEADER, m)
    m["about"] = _fill(ABOUT, m)
    m["contact"] = _fill(CONTACT, m)
    return _fill(HEAD, m) + _fill(HOME_BODY, m) + _fill(FOOTER, m)

def sitemap_xml():
    """Gera o sitemap.xml a partir de LANDING + PRACTICES (forma com barra /slug/)."""
    today = datetime.date.today().isoformat()
    entries = [(f"{LANDING}/", "1.0")] + [(f"{LANDING}/{slug}/", "0.8") for slug, _ in PRACTICES]
    entries.append((f"{LANDING}/privacidade/", "0.2"))
    urls = "\n".join(
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        f"    <priority>{prio}</priority>\n"
        "  </url>"
        for loc, prio in entries
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n")

def robots_txt():
    return f"User-agent: *\nAllow: /\n\nSitemap: {LANDING}/sitemap.xml\n"

def main():
    warnings = []
    all_schema = {}

    # ---- diretório de saída pronto para deploy (rotas limpas /slug/) ----
    dist = OUT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()

    for slug, page in PAGES.items():
        page["eyebrow_top"] = page.get("eyebrow") or (f"Direito {dict(PRACTICES)[slug]} · São Paulo" if slug in dict(PRACTICES) else "São Paulo")
        # avisos de tamanho
        if len(page["title"]) > 60: warnings.append(f"[TITLE>60] {slug}: {len(page['title'])}")
        if len(page["meta"]) > 155: warnings.append(f"[META>155] {slug}: {len(page['meta'])}")
        page_dir = dist / slug
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(render(page), encoding="utf-8")
        legal, faqpage = schema_for(page)
        all_schema[slug] = {"@context":"https://schema.org","@graph":[legal, faqpage]}

    # ---- estáticos autorais (entradas, NÃO geradas aqui) copiados para o dist ----
    #   404.html = fallback de rotas (a home agora é gerada por render_home)
    (dist / "index.html").write_text(render_home(), encoding="utf-8")
    if len(HOME["title"]) > 60: warnings.append(f"[TITLE>60] home: {len(HOME['title'])}")
    if len(HOME["meta"]) > 155: warnings.append(f"[META>155] home: {len(HOME['meta'])}")
    for static_name in ("404.html",):
        src = OUT / static_name
        if src.exists():
            shutil.copy2(src, dist / static_name)
        else:
            warnings.append(f"[FALTANDO] estático '{static_name}' não encontrado em {OUT}")

    # ---- configuração/SEO gerada (sempre em sincronia com as páginas) ----
    (dist / "sitemap.xml").write_text(sitemap_xml(), encoding="utf-8")
    (dist / "robots.txt").write_text(robots_txt(), encoding="utf-8")
    (dist / "CNAME").write_text(LANDING.split("//")[-1] + "\n", encoding="utf-8")
    (dist / ".nojekyll").write_text("", encoding="utf-8")

    # ---- artefatos de referência (não servidos) ficam na raiz do projeto ----
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
        lines.append(f"## /{slug} — {LANDING}/{slug}/")
        lines.append(f"Title ({len(page['title'])}): {page['title']}")
        lines.append(f"Meta  ({len(page['meta'])}): {page['meta']}")
        lines.append(f"H1: {page['h1']}\n")
    (OUT / "home-meta-tags.txt").write_text("\n".join(lines), encoding="utf-8")

    print("Site gerado em:", dist)
    print("Rotas:", "/  " + "  ".join(f"/{s}/" for s in PAGES))
    print(f"Deploy: cp -R {dist}/. ~/Projects/lemes-landing/ && (cd ~/Projects/lemes-landing && git add -A && git commit && git push)")
    if warnings:
        print("AVISOS:", *warnings, sep="\n  ")
    else:
        print("OK: todos os titles <=60 e metas <=155 caracteres.")

if __name__ == "__main__":
    main()

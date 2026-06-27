# Checklist priorizado — Quality Score, conversão e SEO

O **Quality Score (QS)** do Google Ads tem 3 componentes:
1. **Experiência na página de destino** ← onde está o maior problema (conteúdo em JS) e o maior ganho destas entregas.
2. **Relevância do anúncio** ← alinhar palavra-chave → página → H1/texto.
3. **CTR esperado** ← anúncios e correspondência de termos.

Subir o QS aumenta o **Ad Rank**, o que recupera **Impression Share perdido por
ranking** (71,7% no Trabalhista, 50,1% no Cível) **sem aumentar o lance**.

---

## 🔴 PRIORIDADE 1 — Esta semana (QS crítico 1–3)

- [ ] **Publicar `/divorcio`** (QS 1 🔴). H1 "Advogado de Divórcio em São Paulo",
      texto respondendo "como funciona o divórcio no cartório", "judicial x
      extrajudicial", "quanto custa". Conteúdo já pronto em `divorcio.html`.
- [ ] **Publicar `/inventario`** (QS 2 🔴). H1 "Advogado de Inventário…", texto sobre
      "quanto custa", "tabela OAB SP", "inventário extrajudicial", "prazo".
- [ ] **Apontar os grupos de anúncios para a página certa** (relevância):
      - `divórcio extrajudicial`, `advogado divórcio`, `advogada divorcio` → **/divorcio**
      - `advogado inventário`, `quanto custa advogado inventário` → **/inventario**
      - (Hoje provavelmente apontam para /civel ou home — esse descasamento derruba o QS.)
- [ ] Colar **Title + Meta** dessas páginas (de `home-meta-tags.txt`).
- [ ] Colar **schema LegalService + FAQPage** dessas páginas (de `schema-markup.json`).
- [ ] Confirmar **botão WhatsApp acima do fold** nas duas.

**Por quê primeiro:** QS 1–3 = páginas que o Google considera quase irrelevantes
para o termo. Criar página dedicada, com o termo no H1/URL/texto, é o que mais
sobe o QS rápido. "advogada divorcio" converte a **40%** de CTR — a página dedicada
transforma esse interesse em lead.

---

## 🟠 PRIORIDADE 2 — Próximos dias (volume e conversão)

- [ ] **Otimizar `/trabalhista`** com o conteúdo de `trabalhista.html` (texto nativo).
      Foco nos termos que convertem: **"calculo rescisão"** (44 conv!),
      "calcular rescisão", "rescisão indireta", "fui demitido o que fazer".
- [ ] Destacar o bloco **"Calcule sua rescisão gratuitamente"** (faixa CTA) — é o
      maior conversor do Trabalhista; transforme em chamada clara para o WhatsApp.
- [ ] **Otimizar `/civel`** com `civel.html`; usar como hub que linka /divorcio e /inventario.
- [ ] Garantir que cada anúncio de Trabalhista leve para **/trabalhista** (não a home).
- [ ] Conferir **velocidade mobile** (PageSpeed) das páginas de maior gasto.

**Trabalhista hoje:** CTR 4,48%, CPC R$1,36, mas **Impression Share só 10%**
(perde 71,7% por ranking). Página rastreável + QS maior = mais impressões pelo
mesmo orçamento.

---

## 🟡 PRIORIDADE 3 — Completar cobertura

- [ ] **Publicar `/aereo`** (`aereo.html`). Termos: "preterição de embarque" (CTR 33%),
      "resolução 400 anac", "overbooking o que fazer", "mala extraviada",
      "direito do passageiro aéreo".
- [ ] **Publicar `/previdenciario`** (`previdenciario.html`). Termos:
      "com quantos anos a mulher se aposenta/pode se aposentar" (12 conv somadas).
- [ ] Criar grupos de anúncios específicos para esses termos apontando às novas páginas.
- [ ] **Home:** Title/Meta novos + schema LegalService; links para as 6 áreas.

---

## 🔵 PRIORIDADE 4 — SEO orgânico e reforço (contínuo)

- [ ] **Google Business Profile** com NAP idêntico (categoria Advogado) → "perto de mim".
      Termos como "advogado civil perto de mim" (CTR 12,86%), "advocacia civil perto
      de mim" (CTR 25%), "advogado pequenas causas sp" pedem sinal local forte.
- [ ] Validar todas as páginas em **Rich Results Test** (FAQPage aparecendo).
- [ ] Enviar **sitemap** atualizado no Google Search Console e pedir indexação das
      novas URLs.
- [ ] Acompanhar QS por palavra-chave em 2–4 semanas (o QS recalcula com histórico).
- [ ] Considerar conteúdo de blog para os termos informativos de alto CTR
      ("o que é rescisão indireta" 15%, "como se divorciar no cartório" 27%).

---

## ✔️ Como cada requisito do briefing foi atendido (por página)

| Requisito                          | Status |
|------------------------------------|--------|
| Title ≤ 60 caracteres              | ✅ conferido no build |
| Meta description ≤ 155             | ✅ conferido no build |
| H1 alinhado à palavra-chave        | ✅ |
| H2/H3 com termos que convertem     | ✅ (cards + blocos + FAQ) |
| Texto rastreável (dúvidas reais)   | ✅ seções `prose` + FAQ |
| WhatsApp acima do fold             | ✅ hero + header + FAB |
| CTA secundário (formulário)        | ✅ |
| Schema LegalService                | ✅ + FAQPage |
| FAQ com perguntas reais            | ✅ (as do briefing) |
| Velocidade                         | ✅ CSS inline, 1 fonte dupla, sem imagens pesadas, JS mínimo |

---

## ⚠️ Não esquecer (restrições do briefing)

- **NÃO** alterar as **tags de conversão / Google Ads** já instaladas.
- **NÃO** alterar o **número/integração de WhatsApp** já configurado.
- Conteúdo em **conformidade com a OAB** (Provimento 205/2021): tom informativo,
  sem promessa de resultado — já refletido no texto e no disclaimer do rodapé.
- Ao migrar para texto nativo no Wix, **não** deixar o conteúdo só dentro de um
  HTML embed (iframe) — não é indexado.

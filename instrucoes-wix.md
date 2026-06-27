# Implementação no Wix — passo a passo

Objetivo: levar o **conteúdo em texto rastreável** das páginas geradas para o
Wix, de forma que o Google leia tudo (resolvendo o problema de Quality Score
baixo por conteúdo em JavaScript).

> **Regra de ouro:** o Google indexa o **texto nativo** das páginas Wix (elementos
> de Texto), não o conteúdo dentro de um **HTML embed (iframe)**. Por isso, **NÃO**
> cole as páginas inteiras dentro de um bloco "Incorporar HTML". Use os arquivos
> `.html` como **roteiro de conteúdo** e recrie cada bloco com **elementos nativos
> do Wix** (Texto, Botão, Caixa, Formulário). Só o schema (JSON-LD) entra como código.

---

## 0. Mapa de arquivos → páginas Wix

| Arquivo gerado        | Página Wix (URL)              | Ação        |
|-----------------------|-------------------------------|-------------|
| `trabalhista.html`    | `/trabalhista`                | Otimizar    |
| `civel.html`          | `/civel`                      | Otimizar    |
| `divorcio.html`       | `/divorcio`                   | **Criar** 🔴 |
| `inventario.html`     | `/inventario`                 | **Criar** 🔴 |
| `aereo.html`          | `/aereo`                      | **Criar**   |
| `previdenciario.html` | `/previdenciario`             | **Criar**   |
| `home-meta-tags.txt`  | Home + todas                  | Title/Meta  |
| `schema-markup.json`  | Todas                         | JSON-LD     |

Abra cada `.html` no navegador (duplo clique) para ver o layout-alvo enquanto monta no Wix.

---

## 1. Title e Meta Description (todas as páginas)

Use o arquivo **`home-meta-tags.txt`** (já com a contagem de caracteres conferida).

No Editor Wix:
1. Menu lateral **Páginas** → selecione a página → ícone **⋯** → **SEO básico**
   (ou painel **Marketing & SEO → Ferramentas de SEO → Páginas do site**).
2. Cole o **Título SEO** (campo "What's the page title…").
3. Cole a **Descrição** (campo "Description").
4. Confirme o **slug da URL** (ex.: `divorcio`).
5. Deixe "Permitir que mecanismos de busca indexem" **ligado**.

---

## 2. Conteúdo da página (o mais importante para o QS)

Para cada página, recrie estes blocos com **elementos nativos** de Texto, na ordem:

1. **H1** — título da página. No elemento de Texto, escolha o tema/tag **Heading 1 (H1)**.
   Use **apenas um H1 por página** (veja o H1 no `home-meta-tags.txt`).
2. **Parágrafo de introdução** (o texto "lead" do hero) — tag Parágrafo.
3. **Botão WhatsApp acima do fold** (ver passo 3).
4. **Cards de situações** — cada título como **H3**, descrição como Parágrafo.
   No Wix, use uma **Caixa/Repeater** ou colunas; o importante é o texto ser nativo.
5. **Blocos de conteúdo** ("Quanto custa…", "Como funciona…") — cada pergunta-título
   como **H2** e os parágrafos como texto nativo. **Copie o texto na íntegra** dos
   arquivos `.html` (seção `<section class="prose">`). É esse texto que o Google lê.
6. **Passos 01/02/03** — texto nativo.
7. **FAQ** — cada **pergunta como H3** e a **resposta como Parágrafo**, em texto nativo
   (pode usar o elemento "Acordeão/FAQ" do Wix, desde que o conteúdo seja texto, não imagem).
   As perguntas/respostas devem ser **idênticas** às do schema FAQPage (passo 5).
8. **Bloco "Sobre" (E-E-A-T)** — nome do advogado, **OAB/SP 255.888**, CNPJ e endereço.
   Sinais de autoridade ajudam muito em sites jurídicos (tema YMYL).
9. **Formulário de contato** (passo 4).
10. **Rodapé com NAP** — Nome, endereço completo, telefone, e-mail, horário
    (idêntico em todas as páginas — ver abaixo).

> **Não use imagem com texto dentro.** Texto em imagem não é lido pelo Google.

---

## 3. Botão WhatsApp acima do fold

1. **Adicionar → Botão**. Texto: "Falar agora no WhatsApp".
2. Selecione o botão → **Link (🔗) → Endereço da web** e cole:
   ```
   https://wa.me/5511995155021?text=Olá,%20vim%20pelo%20site%20e%20gostaria%20de%20uma%20consulta
   ```
   Marque **"Abrir em nova aba"**.
3. Posicione o botão **dentro da primeira tela** (acima da dobra), no hero.
4. **Botão flutuante:** instale o app **"WhatsApp Chat"** (Wix App Market) ou fixe
   um botão (Configurações do botão → **Fixar na tela**) no canto inferior direito,
   com o mesmo link. Não altere o número/integração de WhatsApp já configurado.

---

## 4. Formulário de contato (CTA secundário)

Use **Wix Forms** (Adicionar → Contato → Formulário):
- Campos: **Nome**, **Telefone/E-mail**, **Resumo do caso**.
- Em **Configurações do formulário → Notificações**, envie para **diego@lemesadvogados.com**.
- Botão de envio: "Enviar".
- (O formulário dos arquivos `.html` abre o WhatsApp via JavaScript — no Wix prefira
  o Wix Forms nativo, que registra o lead e é mais confiável.)

---

## 5. Schema markup (JSON-LD) — todas as páginas

O arquivo **`schema-markup.json`** tem, para cada página, um bloco com
**LegalService + FAQPage**. Para colar no Wix:

**Opção A (recomendada) — por página:**
1. **Páginas → ⋯ → SEO básico → Avançado → Marcação de dados estruturados**
   (Advanced SEO → Structured data markup).
2. **Adicionar marcação** → cole o objeto JSON daquela página (o valor dentro de
   `"divorcio": { ... }`, por exemplo — só o objeto, sem a chave externa).

**Opção B — Custom Code:**
1. **Configurações → Código personalizado (Custom Code) → Adicionar código**.
2. Cole envolvendo em `<script type="application/ld+json"> … </script>`.
3. Em "Adicionar código a", escolha **a página específica** (não "todas").

> Valide depois em **search.google.com/test/rich-results**. O FAQPage pode render
> as perguntas direto no Google (rich result), aumentando CTR.

---

## 6. NAP idêntico (SEO local)

Mantenha **exatamente igual** em todas as páginas e no Google Business Profile:

```
Lemes Sociedade Individual de Advogados
Rua Coronel Melo de Oliveira, 557 — Perdizes
São Paulo/SP — CEP 05011-040
(11) 99515-5021  ·  diego@lemesadvogados.com
Seg–Sex, 9h às 18h  ·  CNPJ 25.385.186/0001-75  ·  OAB/SP 255.888
```

Crie/atualize o **Perfil da Empresa no Google** (Google Business Profile) com
esse mesmo NAP e categoria "Advogado" — isso reforça o "advogado perto de mim".

---

## 7. Velocidade (afeta a "experiência na página de destino" do QS)

- Comprima e use **imagens WebP**; ative **lazy load** (padrão Wix).
- Evite excesso de apps/animações pesadas no topo da página.
- Use **fontes do sistema ou poucas fontes** (as páginas usam Archivo + Spectral).
- Teste em **PageSpeed Insights** (mobile) e mire em LCP < 2,5s.
- Publique e teste no celular real.

---

## 8. Ligações internas

No rodapé de cada página, adicione links para as outras áreas
(Trabalhista, Cível, Divórcio, Inventário, Aéreo, Previdenciário). Isso ajuda o
Google a rastrear e entender o site (já existe no rodapé dos `.html`).

---

## 9. Ordem sugerida de execução

1. 🔴 Criar `/divorcio` e `/inventario` (QS 1 e 2 — maior urgência).
2. 🔴 Otimizar `/trabalhista` e `/civel` (mais tráfego e conversão).
3. Criar `/aereo` e `/previdenciario`.
4. Title/Meta da Home + schema da Home.
5. Validar rich results e PageSpeed.
6. Apontar cada grupo de anúncios para a página correspondente (ver `checklist-qs.md`).

> Os arquivos `.html` ficam como **referência viva** de conteúdo e layout. O
> gerador `build.py` permite regenerar tudo se você editar algum texto.

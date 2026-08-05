# Reestruturação da campanha "Cível" no Google Ads

**Diagnóstico (relatório de 21/07):** todas as ~36 palavras-chave num único grupo
"Cível", dividindo o mesmo anúncio genérico → `advogado divórcio`, `advogado para
separação`, `advogado para inventário` com **Relevância "Abaixo da média"**.

**Princípio:** 1 intenção → 1 anúncio (keyword no título) → 1 URL dedicada. Mas só
cria grupo para área que tem **volume real + página**. Área com ~10 buscas/mês não
ganha grupo.

**Base de dados:** volume real de SP do Planejador de Palavras-chave (jul/25–jun/26).

---

## DECISÃO DE ARQUITETURA — 5 grupos, 1 campanha (por enquanto)

**Não são 6 grupos fixos.** O volume real reduziu para **5** (Cobrança e Contratos
saem — volume baixo/desconhecido). Divórcio é o único incerto (export não trouxe o
volume); se preferir, ele entra junto de Família e viram **4 grupos**.

⚠️ **Orçamento no Ads é por CAMPANHA, não por grupo.** Numa campanha só, Imobiliário
e Família (1.300 cada) vão consumir a verba e sufocar Inventário e Pequenas causas.
**Decisão:** manter **uma campanha só** agora (conta de baixo volume — fragmentar em
5 campanhas impede o Google de aprender). Separar uma área em campanha própria só
**quando ela começar a puxar toda a verba** (provável: Imobiliário).

---

## OS 5 GRUPOS (por volume real, SP/mês)

### GRUPO 1 — Imobiliário / Usucapião → `/imobiliario` ⭐ (1.300 — maior volume)
Keywords: advogado imobiliário [sp] · advogado usucapião · usucapião extrajudicial ·
reintegração de posse · regularização de imóveis · advogado despejo · ação de despejo ·
distrato / atraso na entrega de imóvel · advogado contra construtora · [advogado para
regularização de imóveis] · [advogado especialista em usucapião] · [advogado para
reintegração de posse].
**Títulos:** `Advogado Imobiliário SP` · `Usucapião e Regularização` · `Reintegração e Despejo`
> Página `/imobiliario` já construída (aguardando deploy). Enquanto não publica,
> apontar para `/civel`. Reativar `usucapião` (hoje pausada) quando a página for ao ar.

### GRUPO 2 — Família → `/familia` ⭐ (1.300)
Keywords: advogado de família / familiar [sp] · advogado guarda de filhos · advogado
pensão alimentícia · advogado união estável · dissolução de união estável · partilha de
bens · alienação parental · advogado vara de família · `"Advogado União Estável"` ·
`advogado de direito de família em perdizes`.
**Títulos:** `Advogado de Família em SP` · `Guarda, Pensão e Partilha` · `União Estável e Divórcio`
> Página `/familia` já construída (aguardando deploy). Card de divórcio linka p/ `/divorcio`.

### GRUPO 3 — Divórcio → `/divorcio` (volume incerto — validar; senão, fundir no Grupo 2)
Keywords: advogado divórcio [sp] · `[divorcio advogado]` · [advogado para divórcio
consensual] · [advogado divórcio extrajudicial] · [advogado para separação] · [advogado
para separação são paulo] · `"Advogado Separação Consensual"` · [advogado para divócio]
(typo) · [advogado para divócio são paulo] (typo).
**Títulos:** `Advogado de Divórcio em SP` · `Cartório ou Justiça` · `Consensual e Litigioso`
> ⚠️ Export não trouxe o volume de "advogado divórcio" (só `advogada de divorcio` = 50).
> Validar na 2ª extração. Se baixo, mover estas keywords para o Grupo 2 (Família).

### GRUPO 4 — Cível + Pequenas causas → `/civel` ⭐ (1.000 + 320)
Keywords cível: advogada/advogado cível [sp] · advogado civil · advocacia cível ·
`escritório de advocacia cível sp` · `advogado cível on-line` · indenização · dano moral ·
cobrança indevida.
Keywords pequenas causas (**CPC mais barato: R$2,89–8,29**): advogado para pequenas
causas [sp] · juizado especial cível · problema de consumo · advogado consumidor.
**Títulos:** `Advogado Cível em São Paulo` · `Pequenas Causas e Juizado` · `Perdizes · Zona Oeste`
> ⚠️ Keyword que fatura hoje (`advogado cível`, QS 5). QS segurado por "Exp. na página
> Abaixo da média" → **confirmar Final URL = landing `/civel`** (não home Wix) +
> **PageSpeed mobile**. É o único QS com dado real; resolver primeiro.
> Nota: pequenas causas pode virar bloco de texto próprio dentro da `/civel`.

### GRUPO 5 — Inventário / Sucessões → `/inventario` (390 — lance caro, até R$45)
Keywords: advogado inventário / para inventário [sp] · advogado especialista em inventário
[judicial] · inventário extrajudicial · partilha de herança · advogado de sucessões ·
`"advogado especialista em sucessões"` · `advogado para inventário e partilha` ·
`advogado consulta inventário` · `Advogado partilha`.
**Títulos:** `Advogado de Inventário SP` · `Judicial e Extrajudicial` · `Partilha e Testamento`
> Lance alto (R$45) → priorizar cauda longa mais barata ("inventário fora do prazo multa
> ITCMD") e conversão via FAQ/orgânico. Não subir lance geral.

---

## PAUSAR (sem volume / sem página — não ganham grupo)

| Keyword | Motivo |
|---|---|
| `advogado cobrança` e variantes | ~10 buscas/mês — volume baixíssimo |
| `[advogado para ação de cobrança empresarial]` | "não qualificado, raramente exibido" |
| `[advogado analisar contrato]` / `advogado analise contratos` | sem volume confiável |
| `[advogado para Contrato locação]` / `[advogado para ação revisional]` | revalidar na 2ª extração |
| `[advogado para ação renovatória]` | "não qualificado, raramente exibido" |
| `[advogado para holding familiar]` | nicho societário sem página |

> Não apagar — pausar. Contratos/Revisional: revalidar volume antes de decidir grupo/página.
> Cobrança: fica citada dentro da `/civel`, sem verba dedicada.

---

## ORDEM DE EXECUÇÃO

1. **Antes de tudo:** confirmar Final URL do anúncio do grupo Cível atual = landing
   `/civel` + PageSpeed mobile (resolve o único QS real, o do `advogado cível`).
2. **Deploy das páginas novas** `/imobiliario` e `/familia` (aguardando revisão do Diego).
3. Criar os Grupos 1–2 e 4–5 (têm página) e mover as keywords; Grupo 3 conforme a decisão de volume.
4. 1 RSA por grupo com os títulos acima (keyword no Título 1).
5. Pausar as keywords da lista de pausa.
6. Reativar `usucapião` (Grupo 1) quando `/imobiliario` estiver no ar.
7. **Manter tudo numa campanha só.** Monitorar; separar Imobiliário (ou Família) em
   campanha própria quando começar a consumir a verba das demais.

**Não medir resultado antes de ~2–4 semanas** — o QS recalcula com histórico novo.

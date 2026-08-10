#!/usr/bin/env node

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import { marked } from 'marked';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Carregar constantes estruturais do build.py via Python para garantir sincronia absoluta
function getSiteConstants() {
  const pythonCmd = `import sys; sys.path.append('${__dirname}'); import build, json; print(json.dumps({'NAP': build.NAP, 'WHATS': build.WHATS, 'LANDING': build.LANDING, 'PRACTICES': build.PRACTICES, 'CSS': build.CSS, 'JS': build.JS, 'ZAP_SVG': build.ZAP_SVG}))`;
  try {
    const stdout = execSync(`python3 -c "${pythonCmd}"`, { encoding: 'utf8' });
    return JSON.parse(stdout);
  } catch (err) {
    console.error("❌ Erro ao ler constantes do build.py via Python:", err.message);
    process.exit(1);
  }
}

// Parsear Frontmatter manualmente
function parseMarkdownWithFrontmatter(content) {
  const frontmatterRegex = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);
  
  if (!match) {
    return {
      metadata: {},
      body: content
    };
  }

  const yamlBlock = match[1];
  const body = match[2];
  const metadata = {};

  yamlBlock.split('\n').forEach(line => {
    const colonIndex = line.indexOf(':');
    if (colonIndex > -1) {
      const key = line.slice(0, colonIndex).trim();
      let value = line.slice(colonIndex + 1).trim();
      // Remover aspas em volta do valor se houver
      if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      metadata[key] = value;
    }
  });

  return { metadata, body };
}

// Formatação amigável de data brasileira (Ex: 09 de agosto de 2026)
function formatBrazilianDate(dateStr) {
  if (!dateStr) return '';
  const parts = dateStr.split('-');
  if (parts.length !== 3) return dateStr;
  
  const months = [
    'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
    'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
  ];
  
  const day = parseInt(parts[2], 10);
  const month = months[parseInt(parts[1], 10) - 1];
  const year = parts[0];
  
  return `${day} de ${month} de ${year}`;
}

// Template Base da Página (Cabeçalho, Rodapé, CSS do escritório)
function getHtmlTemplate(title, meta, canonical, bodyContent, constants) {
  const { CSS, JS, ZAP_SVG, WHATS, NAP } = constants;
  
  // Links do rodapé
  const footerLinksHtml = constants.PRACTICES.map(([slug, label]) => 
    `<a href="/${slug}/">${label}</a>`
  ).join('\n');

  // Ajustes de estilo específicos para o blog
  const extraCss = `
    .prose h1, .prose h2, .prose h3 { margin-top: 2rem; margin-bottom: 1rem; text-transform: none; }
    .prose p { margin-bottom: 1.2rem; font-size: var(--s0); }
    .prose strong { font-weight: 700; color: var(--ink); }
    .prose ul, .prose ol { margin-bottom: 1.5rem; padding-left: 1.5rem; }
    .prose li { margin-bottom: 0.5rem; }
  `;

  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="${meta}">
<link rel="canonical" href="${canonical}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lemes Advogados">
<meta property="og:title" content="${title}">
<meta property="og:description" content="${meta}">
<meta property="og:url" content="${canonical}">
<meta property="og:locale" content="pt_BR">
<meta name="geo.region" content="BR-SP">
<meta name="geo.placename" content="São Paulo">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=Spectral:wght@400;500;600&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=Spectral:wght@400;500;600&display=swap"></noscript>
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-993352616"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', 'AW-993352616');
 gtag('config', 'G-3YLQXJDLJE');
</script>
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "xe34fpdzej");
</script>
<style>
${CSS}
${extraCss}
</style>
</head>
<body>
<header class="bar">
 <div class="wrap bar__in">
  <a class="brand" href="/" aria-label="Lemes Advogados — início" style="display: flex; align-items: center; text-decoration: none;"><img src="/assets/logo_lemes.png" alt="Lemes Advogados" style="height: 42px; width: auto; display: block;"></a>
  <a class="bar__phone" href="tel:${NAP.phone_tel}">${NAP.phone_display}</a>
  <a class="btn" href="${WHATS}" target="_blank" rel="noopener">${ZAP_SVG} WhatsApp</a>
 </div>
</header>

<main>
  ${bodyContent}
</main>

<footer class="foot">
 <div class="wrap foot__grid">
  <div>
   <h2>${NAP.name}</h2>
   <p style="margin-top:.8rem">Advocacia em ${NAP.district}, ${NAP.city}. Atendimento humano, linguagem clara e foco em resolver o seu caso.</p>
  </div>
  <div>
   <h4>Áreas de atuação</h4>
   ${footerLinksHtml}
  </div>
  <div>
   <h4>Contato</h4>
   <a href="${WHATS}" target="_blank" rel="noopener">WhatsApp ${NAP.phone_display}</a>
   <a href="mailto:${NAP.email}">${NAP.email}</a>
   <p>${NAP.street}</p>
   <p>${NAP.district}, ${NAP.city}/${NAP.region} · ${NAP.cep}</p>
   <a href="https://www.linkedin.com/in/diego-henrique-lemes-8882b0/" target="_blank" rel="noopener">LinkedIn</a>
   <a href="https://www.instagram.com/lemesadvsp/" target="_blank" rel="noopener">Instagram</a>
  </div>
 </div>
 <div class="wrap">
  <p class="foot__legal">${NAP.name} · ${NAP.cnpj} · Advogado responsável: ${NAP.lawyer} (${NAP.oab}).<br>
  Conteúdo de caráter exclusivamente informativo, em conformidade com o Código de Ética e Disciplina da OAB e o Provimento nº 205/2021. Não constitui oferta de serviços, captação de clientela nem promessa de resultado. Cada caso é analisado individualmente.</p>
 </div>
</footer>

<a class="fab" href="${WHATS}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">${ZAP_SVG}<span>Fale conosco</span></a>

<script>
${JS}
</script>
</body>
</html>`;
}

async function main() {
  console.log("=== COMPILADOR DE NOTÍCIAS DO BLOG (site-lemes) ===");
  
  const constants = getSiteConstants();
  const noticiasDir = path.join(__dirname, 'noticias');
  const distDir = path.join(__dirname, 'dist');
  const distNoticiasDir = path.join(distDir, 'noticias');

  // Garantir existência de dist/noticias/
  await fs.mkdir(distNoticiasDir, { recursive: true });

  // Listar arquivos markdown da pasta noticias/
  let files;
  try {
    files = await fs.readdir(noticiasDir);
  } catch (e) {
    console.log("⚠️ Nenhuma notícia encontrada na pasta noticias/.");
    return;
  }

  const posts = [];

  for (const file of files) {
    if (!file.endsWith('.md')) continue;
    
    const filePath = path.join(noticiasDir, file);
    const slug = path.basename(file, '.md');
    const content = await fs.readFile(filePath, 'utf8');
    
    const { metadata, body } = parseMarkdownWithFrontmatter(content);
    
    const title = metadata.title || metadata.titulo || "Notícia · Lemes Advogados";
    const date = metadata.date || metadata.data || "";
    const category = metadata.category || metadata.categoria || "Geral";
    const summary = metadata.description || metadata.resumo || "";

    posts.push({
      slug,
      title,
      date,
      category,
      summary,
      bodyMarkdown: body
    });
  }

  // Ordenar posts pela data (mais recentes primeiro)
  posts.sort((a, b) => b.date.localeCompare(a.date));

  // 1. GERAR PÁGINAS INDIVIDUAIS DE NOTÍCIA
  for (const post of posts) {
    const postDistDir = path.join(distNoticiasDir, post.slug);
    await fs.mkdir(postDistDir, { recursive: true });

    // Converter fechamento especial [[fecho]] se houver
    let bodyWithCta = post.bodyMarkdown;
    if (bodyWithCta.includes('[[fecho]]')) {
      bodyWithCta = bodyWithCta.replace('[[fecho]]', `<p class="eyebrow" style="margin-top: 3rem; color: var(--carimbo);">Lemes Advogados</p>`);
    }

    const htmlBody = marked(bodyWithCta);
    const formattedDate = formatBrazilianDate(post.date);

    const pageContentHtml = `
      <section class="section wrap" style="max-width: 800px; margin-inline: auto; padding-top: 2rem;">
        <p class="eyebrow" style="margin-bottom: 0.5rem;">Decisões & Notícias · ${post.category}</p>
        <h1 style="font-size: var(--s3); margin-bottom: 1.5rem; text-transform: none; line-height: 1.1;">${post.title}</h1>
        <div style="font-family: var(--mono); font-size: var(--s-1); color: var(--muted); margin-bottom: 2.5rem; border-bottom: 1px solid var(--line); padding-bottom: 1rem;">
          Publicado em ${formattedDate}
        </div>
        <article class="prose" style="font-size: var(--s0); line-height: 1.7; font-family: var(--body);">
          ${htmlBody}
        </article>
        
        <!-- Bloco CTA de rodapé da notícia -->
        <div style="background: var(--paper2); border: 1px solid var(--line); border-radius: var(--radius); padding: clamp(1.5rem, 4vw, 2.5rem); margin-block: 4rem; display: flex; flex-direction: column; gap: 1rem; align-items: flex-start; clear: both;">
          <h2 style="font-family: var(--display); text-transform: uppercase; font-size: var(--s1); font-weight: 800; margin-top: 0;">Ficou com alguma dúvida?</h2>
          <p style="color: var(--ink2); font-size: var(--s0); margin-bottom: 0.5rem; max-width: 60ch;">Se você se identificou com este caso e deseja entender melhor os seus direitos, entre em contato direto com a nossa equipe.</p>
          <a class="btn" href="${constants.WHATS}" target="_blank" rel="noopener">${constants.ZAP_SVG} Falar com o Advogado</a>
        </div>
      </section>
    `;

    const canonical = `${constants.LANDING}/noticias/${post.slug}/`;
    const fullPageHtml = getHtmlTemplate(
      `${post.title} | Lemes Advogados`,
      post.summary,
      canonical,
      pageContentHtml,
      constants
    );

    await fs.writeFile(path.join(postDistDir, 'index.html'), fullPageHtml, 'utf8');
    console.log(`✅ Post compilado em: dist/noticias/${post.slug}/index.html`);
  }

  // 2. GERAR PÁGINA DE ÍNDICE (/noticias/index.html)
  const listHtml = posts.map(post => {
    const formattedDate = formatBrazilianDate(post.date);
    return `
      <div style="border-bottom: 1px solid var(--line2); padding-bottom: 2.5rem; margin-bottom: 2.5rem;">
        <span class="eyebrow" style="font-size: var(--s-1); color: var(--muted); display: block; margin-bottom: 0.6rem;">${post.category} · ${formattedDate}</span>
        <h2 style="font-size: var(--s2); margin-bottom: 0.8rem; text-transform: none; line-height: 1.2;">
          <a href="/noticias/${post.slug}/" style="text-decoration: none; color: inherit;">${post.title}</a>
        </h2>
        <p style="color: var(--ink2); font-size: var(--s0); line-height: 1.6; margin-bottom: 1.2rem; max-width: 75ch;">${post.summary}</p>
        <a href="/noticias/${post.slug}/" style="font-family: var(--mono); font-size: var(--s-1); font-weight: 700; text-decoration: none; color: var(--carimbo);">Ler decisão completa &rarr;</a>
      </div>
    `;
  }).join('\n');

  const indexContentHtml = `
    <section class="section wrap" style="max-width: 850px; margin-inline: auto; padding-top: 2rem;">
      <p class="eyebrow" style="margin-bottom: 0.5rem;">Informativo</p>
      <h1 style="font-size: var(--s4); margin-bottom: 1rem; line-height: 1.05;">NOTÍCIAS & DECISÕES</h1>
      <p class="lead" style="margin-bottom: 4rem;">Acompanhe vitórias judiciais reais obtidas pelo nosso escritório, novidades legislativas e esclarecimentos importantes sobre os seus direitos.</p>
      
      <div>
        ${listHtml || '<p style="color: var(--muted);">Nenhuma publicação cadastrada até o momento.</p>'}
      </div>
    </section>
  `;

  const indexCanonical = `${constants.LANDING}/noticias/`;
  const indexPageHtml = getHtmlTemplate(
    `Blog e Notícias | Lemes Advogados`,
    `Acompanhe as principais notícias do escritório Lemes Advogados, decisões do escritório e artigos de utilidade jurídica.`,
    indexCanonical,
    indexContentHtml,
    constants
  );

  await fs.writeFile(path.join(distNoticiasDir, 'index.html'), indexPageHtml, 'utf8');
  console.log(`✅ Índice do Blog compilado em: dist/noticias/index.html`);

  // 3. ATUALIZAR O SITEMAP.XML PARA INCLUIR AS NOTÍCIAS
  try {
    const sitemapPath = path.join(distDir, 'sitemap.xml');
    let sitemapContent = await fs.readFile(sitemapPath, 'utf8');
    
    // Ler o sitemap original e inserir antes de </urlset>
    const today = new Date().toISOString().split('T')[0];
    
    let newsUrls = '';
    // Índice
    newsUrls += `  <url>\n    <loc>${constants.LANDING}/noticias/</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>\n`;
    
    // Posts
    for (const post of posts) {
      newsUrls += `  <url>\n    <loc>${constants.LANDING}/noticias/${post.slug}/</loc>\n    <lastmod>${post.date}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n`;
    }

    if (sitemapContent.includes('</urlset>')) {
      sitemapContent = sitemapContent.replace('</urlset>', `${newsUrls}</urlset>`);
      await fs.writeFile(sitemapPath, sitemapContent, 'utf8');
      console.log(`✅ Sitemap.xml atualizado com os links das notícias.`);
    }
  } catch (e) {
    console.warn(`[Aviso] Falha ao injetar links de notícias no sitemap: ${e.message}`);
  }

  console.log(`🎉 COMPILAÇÃO DO BLOG FINALIZADA COM SUCESSO!\n`);
}

main().catch(err => {
  console.error("❌ Erro fatal na compilação do blog:", err.message);
  process.exit(1);
});

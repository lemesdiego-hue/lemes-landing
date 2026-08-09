#!/usr/bin/env node

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import { GoogleGenerativeAI, SchemaType } from '@google/generative-ai';
import { GoogleAIFileManager } from '@google/generative-ai/server';
import mammoth from 'mammoth';
import pdfParse from 'pdf-parse/lib/pdf-parse.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const MAX_DOCX_CHARS = 120_000;
const MAX_PDF_TEXT_CHARS = 120_000;
const FILE_PROCESSING_POLL_MS = 2000;

// Buscar a GOOGLE_API_KEY automaticamente dos arquivos .env conhecidos
async function getApiKey() {
  if (process.env.GOOGLE_API_KEY) return process.env.GOOGLE_API_KEY;
  const envPaths = [
    '/Users/diegolemes/Projects/pdf-organizer/.env',
    '/Users/diegolemes/Projects/judicial-monitor/.env',
    path.join(__dirname, '.env')
  ];
  for (const p of envPaths) {
    try {
      const content = await fs.readFile(p, 'utf8');
      const match = content.match(/GOOGLE_API_KEY=(.*)/);
      if (match && match[1]) {
        return match[1].trim().replace(/['"]/g, '');
      }
    } catch (e) {
      // continua buscando
    }
  }
  throw new Error('Chave GOOGLE_API_KEY não encontrada nas variáveis de ambiente nem nos arquivos .env do projeto.');
}

// Extração local de PDF
async function extractPdfTextLocally(filePath) {
  try {
    const buffer = await fs.readFile(filePath);
    const data = await pdfParse(buffer);
    return data.text && data.text.trim() ? data.text.trim() : null;
  } catch (err) {
    console.warn(`[Aviso] Falha ao extrair texto local do PDF (${err.message}). Tentando via OCR.`);
    return null;
  }
}

// Upload + OCR com Gemini File API
async function extractPdfTextViaOcr(filePath, apiKey) {
  const fileManager = new GoogleAIFileManager(apiKey);
  console.log(`[OCR] Fazendo upload do PDF para processamento visual...`);
  const { file: uploaded } = await fileManager.uploadFile(filePath, {
    mimeType: 'application/pdf',
    displayName: path.basename(filePath)
  });

  let file = uploaded;
  while (file.state === 'PROCESSING') {
    await new Promise((resolve) => setTimeout(resolve, FILE_PROCESSING_POLL_MS));
    file = await fileManager.getFile(file.name);
  }

  if (file.state === 'FAILED') {
    throw new Error(`O processamento visual do PDF falhou: ${file.error?.message || 'erro desconhecido'}`);
  }

  console.log(`[OCR] PDF pronto e processado pelo Gemini File API.`);
  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });
    const result = await model.generateContent([
      { fileData: { mimeType: file.mimeType, fileUri: file.uri } },
      { text: "Por favor, extraia todo o texto em português contido neste documento, mantendo a fidelidade à ordem das páginas." }
    ]);
    return result.response.text();
  } finally {
    await fileManager.deleteFile(file.name).catch(() => {});
  }
}

// Extração de texto de DOCX
async function extractDocxText(filePath) {
  const { value } = await mammoth.extractRawText({ path: filePath });
  return value && value.trim() ? value.trim() : null;
}

const SYSTEM_PROMPT = `Você é o assessor de imprensa e redator jurídico sênior do escritório "Lemes Advogados" (São Paulo/SP).
Sua tarefa é ler um documento jurídico (sentença, decisão, petição, acórdão) e transformá-lo em uma notícia fantástica, clara e ética para o blog do site institucional e para publicação de engajamento nas redes sociais.

--- REGRAS CRÍTICAS DE CONTEÚDO ---
1. ANONIMIZAÇÃO (LGPD/Ética): Nunca revele nomes completos de clientes, CPFs, CNPJs, RGs ou detalhes pessoais que permitam identificar a parte envolvida. Refira-se a eles de forma genérica (ex: "um eletricista de São Paulo", "uma enfermeira de Perdizes", "um passageiro que teve seu voo atrasado", "uma consumidora lesada") ou por iniciais (ex: "A.C.S."). É permitido mencionar "o advogado Diego Henrique Lemes" ou "o escritório Lemes Advogados" como patrono da ação.
2. ÉTICA DA OAB: Nunca garanta ou prometa resultados para futuros casos. O tom deve ser de caso de sucesso informativo ("Em caso recente, a Justiça decidiu...", "Este entendimento resguarda o direito de..."). Nunca utilize expressões mercantilistas ou captação agressiva.
3. ESTILO DO BLOG:
   - Escreva em português brasileiro moderno, com vocabulário simples e de fácil compreensão por pessoas leigas (sem juridiquês exagerado).
   - O título do post deve ser chamativo, positivo e conter no máximo 60 caracteres.
   - Use intertítulos (##) bem definidos para estruturar a matéria (ex: ## O Conflito, ## A Decisão Judicial, ## O Direito Garantido).
   - Termine o texto com o fechamento canônico do escritório:
     [[fecho]]
     Se você está passando por uma situação semelhante ou deseja esclarecer dúvidas sobre os seus direitos, entre em contato com a equipe especializada da Lemes Advogados.
4. ESTILO DE REDE SOCIAL (Instagram/Facebook):
   - Gere um texto enxuto e dinâmico adaptado para redes sociais.
   - Use um título inicial com emojis chamativos.
   - Apresente um resumo estruturado em bullet points (•) de leitura rápida.
   - Termine com uma chamada para ação (CTA) para o link na bio ou WhatsApp.
   - Inclua hashtags relevantes (ex: #direito #advocacia #direitodotrabalho #lemesadvogados).

--- FORMATO DE SAÍDA ---
Você deve responder estritamente com um objeto JSON válido (sem cercas de código adicionais como \`\`\`json no início ou fim, apenas o JSON bruto ou tratado) com as seguintes chaves:
{
  "slug": "slug-da-url-em-minusculas-com-hifens",
  "categoria": "Trabalhista, Cível, Divórcio, Inventário, Direito Aéreo, ou Previdenciário",
  "markdown": "O post completo do blog contendo o frontmatter completo no topo, o título e as seções",
  "socialMedia": "O texto formatado pronto para copiar e colar nas redes sociais (Instagram/Facebook)"
}`;

const RESPONSE_SCHEMA = {
  type: SchemaType.OBJECT,
  properties: {
    slug: { type: SchemaType.STRING, description: 'Slug amigável para URL do post, ex: reversao-justa-causa-eletricista' },
    categoria: { type: SchemaType.STRING, description: 'Trabalhista, Cível, Divórcio, Inventário, Direito Aéreo, ou Previdenciário' },
    markdown: { type: SchemaType.STRING, description: 'O post completo do blog com o frontmatter de metadados no topo' },
    socialMedia: { type: SchemaType.STRING, description: 'Texto otimizado com emojis e hashtags para Instagram e Facebook' }
  },
  required: ['slug', 'categoria', 'markdown', 'socialMedia']
};

async function generateNewsFromDocument(documentText, apiKey) {
  const genAI = new GoogleGenerativeAI(apiKey);
  const model = genAI.getGenerativeModel({
    model: 'gemini-2.5-flash',
    systemInstruction: SYSTEM_PROMPT,
    generationConfig: {
      maxOutputTokens: 8192,
      responseMimeType: 'application/json',
      responseSchema: RESPONSE_SCHEMA
    }
  });

  const prompt = `Analise o documento jurídico a seguir e gere a notícia para o blog e redes sociais conforme as diretrizes:\n\n${documentText.slice(0, MAX_PDF_TEXT_CHARS)}`;
  
  console.log(`[IA] Enviando conteúdo para o Gemini formatar a notícia...`);
  const result = await model.generateContent(prompt);
  const responseText = result.response.text();
  
  try {
    return JSON.parse(responseText);
  } catch (e) {
    // Caso ocorra falha de parse por causa de cercas markdown geradas pela IA
    const cleanText = responseText.replace(/^```json\n?/, '').replace(/\n?```$/, '').trim();
    return JSON.parse(cleanText);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const filePathArg = args.find(arg => !arg.startsWith('--'));

  if (!filePathArg) {
    console.log(`\n❌ Erro: Por favor, forneça o caminho de um arquivo PDF, Word (.docx) ou Texto.`);
    console.log(`Uso: node gerar-noticia-ia.js <caminho_do_arquivo>\n`);
    process.exit(1);
  }

  const resolvedPath = path.resolve(filePathArg);
  try {
    await fs.access(resolvedPath);
  } catch {
    console.error(`\n❌ Erro: Arquivo não encontrado em: ${resolvedPath}\n`);
    process.exit(1);
  }

  const ext = path.extname(resolvedPath).toLowerCase();
  console.log(`\n📄 Processando arquivo: ${path.basename(resolvedPath)} (${ext})`);

  let textContent = '';
  const apiKey = await getApiKey();

  if (ext === '.pdf') {
    console.log(`[Leitura] Tentando extrair texto embutido do PDF...`);
    textContent = await extractPdfTextLocally(resolvedPath);
    if (!textContent) {
      console.log(`[Leitura] PDF escaneado ou sem camada de texto. Acionando OCR...`);
      textContent = await extractPdfTextViaOcr(resolvedPath, apiKey);
    }
  } else if (ext === '.docx') {
    console.log(`[Leitura] Extraindo conteúdo do arquivo Word...`);
    textContent = await extractDocxText(resolvedPath);
  } else if (ext === '.txt' || ext === '.md') {
    console.log(`[Leitura] Lendo arquivo de texto simples...`);
    textContent = await fs.readFile(resolvedPath, 'utf8');
  } else {
    console.error(`❌ Erro: Extensão de arquivo não suportada (${ext}). Use .pdf, .docx, .txt ou .md.`);
    process.exit(1);
  }

  if (!textContent || !textContent.trim()) {
    console.error(`❌ Erro: Não foi possível extrair nenhum conteúdo textual deste arquivo.`);
    process.exit(1);
  }

  console.log(`✅ Conteúdo extraído com sucesso (${textContent.length} caracteres).`);

  // Gerar notícia usando IA
  const noticia = await generateNewsFromDocument(textContent, apiKey);

  // Criar pasta de notícias se não existir
  const noticiasDir = path.join(__dirname, 'noticias');
  await fs.mkdir(noticiasDir, { recursive: true });

  // Salvar arquivos resultantes
  const mdFileName = `${noticia.slug}.md`;
  const mdFilePath = path.join(noticiasDir, mdFileName);
  const socialFileName = `${noticia.slug}_social.txt`;
  const socialFilePath = path.join(noticiasDir, socialFileName);

  // Garantir data corrente no Markdown se não estiver correto
  const today = new Date().toISOString().split('T')[0];
  let markdownContent = noticia.markdown;
  markdownContent = markdownContent.replace(/data:\s*YYYY-MM-DD/g, `data: ${today}`);
  markdownContent = markdownContent.replace(/data:\s*""/g, `data: ${today}`);

  await fs.writeFile(mdFilePath, markdownContent, 'utf8');
  await fs.writeFile(socialFilePath, noticia.socialMedia, 'utf8');

  console.log(`\n🎉 SUCESSO! Notícia e cópia para redes sociais geradas com sucesso!`);
  console.log(`----------------------------------------------------------------------`);
  console.log(`📰 Categoria: ${noticia.categoria}`);
  console.log(`📁 Post do Blog salvo em: site-lemes/noticias/${mdFileName}`);
  console.log(`📱 Cópia Social salva em: site-lemes/noticias/${socialFileName}`);
  console.log(`----------------------------------------------------------------------`);
  
  console.log(`⚙️  Compilando site completo (landing pages + blog)...`);
  try {
    execSync('python3 build.py && node build-blog.js', { cwd: __dirname, stdio: 'inherit' });
    console.log(`----------------------------------------------------------------------`);
    console.log(`🚀 COMPILAÇÃO AUTOMÁTICA CONCLUÍDA! O site está pronto para deploy.`);
    console.log(`Comando para deploy:`);
    console.log(`cp -R dist/. ~/Projects/lemes-landing/ && (cd ~/Projects/lemes-landing && git add -A && git commit -m "Nova noticia" && git push)`);
    console.log(`----------------------------------------------------------------------\n`);
  } catch (e) {
    console.error(`⚠️  Falha ao executar a compilação automática:`, e.message);
  }
}

main().catch(err => {
  console.error(`\n❌ Ocorreu um erro crítico durante a execução:`, err.message);
  process.exit(1);
});

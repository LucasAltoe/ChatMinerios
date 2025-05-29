from pathlib import Path
import re
from unidecode import unidecode

# Caminhos base
base_dir = Path(__file__).resolve().parents[2]
markdown_dir = base_dir / 'data' / 'processed' / 'markdown'
chunks_dir = base_dir / 'data' / 'chunks'

SECTIONS = [
    'estrutura', 'hábito', 'propriedades físicas',
    'propriedades óticas', 'propriedades diagnósticas',
    'gênese', 'usos'
]

def carregar_md(path: Path) -> str:
    return path.read_text(encoding='utf-8')

def extrair_nome_minerio(texto: str) -> str:
    for linha in texto.split('\n'):
        linha = linha.strip()
        if not linha or linha.startswith('##') or linha.startswith('<!--'):
            continue
        match = re.match(r'^([A-ZÇÃÉÍÓÚ][A-ZÇÃÉÍÓÚ\s\-]+)\s*\(', linha)
        if match:
            nome = match.group(1).strip().lower()
            return unidecode(nome.replace(' ', '_'))
    return 'desconhecido'

def limpar_conteudo(texto: str) -> str:
    texto = re.sub(r'<!--.*?-->', '', texto)  # Remove comentários HTML
    texto = re.sub(r'^##.*$', '', texto, flags=re.MULTILINE)  # Remove cabeçalhos markdown
    texto = re.sub(r'^Figura\s+\d+.*$', '', texto, flags=re.MULTILINE)  # Remove legendas de figuras
    texto = re.sub(r'^Tabela\s+\d+.*$', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'(?i)^GUILLERMO RAFAEL.*$', '', texto, flags=re.MULTILINE)  # Remove autor
    texto = re.sub(r'(?i)^Livro de referência.*$', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'\n{2,}', '\n\n', texto)  # Remove quebras excessivas
    return texto.strip()

def chunk_por_secoes(texto: str) -> dict:
    texto = limpar_conteudo(texto)

    padrao = '|'.join([re.escape(secao) + ':' for secao in SECTIONS])
    blocos = re.split(f'(?i)({padrao})', texto)

    chunks = {}
    chave_atual = "nome"
    chunks[chave_atual] = blocos[0].strip()

    for i in range(1, len(blocos), 2):
        titulo = blocos[i].strip(':').lower()
        conteudo = blocos[i + 1].strip()
        chunks[titulo] = conteudo

    return chunks

def salvar_chunks(minerio: str, chunks: dict):
    destino = chunks_dir / minerio
    destino.mkdir(parents=True, exist_ok=True)

    for secao, conteudo in chunks.items():
        nome_arquivo = destino / f'{secao.replace(" ", "_")}.md'
        nome_arquivo.write_text(conteudo, encoding='utf-8')

def processar_arquivos():
    arquivos_md = markdown_dir.glob('*.md')

    for arquivo in arquivos_md:
        texto = carregar_md(arquivo)
        nome_minerio = extrair_nome_minerio(texto)
        chunks = chunk_por_secoes(texto)
        salvar_chunks(nome_minerio, chunks)
        print(f'Chunks salvos para: {nome_minerio}')

if __name__ == "__main__":
    processar_arquivos()

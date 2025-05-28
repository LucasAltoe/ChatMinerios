from docling.document_converter import DocumentConverter
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
converter = DocumentConverter()

source_raw_dir = Path('../../data/raw').resolve()
processed_dir = Path('../../data/processed/markdown').resolve()

def is_dir_empty(dir_path):
    try:
        return not any(Path(dir_path).iterdir())
    except FileNotFoundError:
        print(f"Erro: Pasta '{dir_path}' não encontrada")
        return True
    except PermissionError:
        print(f"Erro: Sem permissão para acessar '{dir_path}'")
        return False

if is_dir_empty(source_raw_dir):
    logging.info(f"A pasta {source_raw_dir} está vazia!")
else:
    logging.info(f"A pasta {source_raw_dir} contém arquivos")

for document in source_raw_dir.iterdir():
    if document.suffix.lower() == ".pdf":
        try:
            result = converter.convert(document)
            logging.info(f"Convertido: {document.name} -> {result}")

            markdown_content = result.document.export_to_markdown()
            output_markdown_path = processed_dir / f"{document.stem}.md"

            with output_markdown_path.open('w') as f:
                f.write(markdown_content)

            logging.info(f"Arquivo salvo: {output_markdown_path}")

        except Exception as e:
            logging.error(f"Erro ao converter {document.name} -> {str(e)})")

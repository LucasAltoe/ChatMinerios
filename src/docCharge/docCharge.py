from docling.document_converter import DocumentConverter
import os
import logging

logging.basicConfig(level=logging.INFO)
converter  = DocumentConverter()

source = os.path.abspath('../../data/raw')
processed_dir = os.path.abspath('../../data/processed/markdown')


def is_dir_empty(dir_path):
    try:
        return len(os.listdir(dir_path)) == 0
    except FileNotFoundError:
        print(f"Erro: Pasta '{dir_path}' não encontrada")
        return True
    except PermissionError:
        print(f"Erro: Sem permissão para acessar '{dir_path}'")
        return False

if is_dir_empty(source):
    logging.info(f"A pasta {source} está vazia!")
else:
    logging.info(f"A pasta {source} contém arquivos")

for document in os.listdir(source):
    if document.endswith(".pdf"):
        full_path_document = os.path.join(source, document)
        try:
            result = converter.convert(full_path_document)
            logging.info(f"Convertido: {document} -> {result}")

            markdown_content = result.document.export_to_markdown()
            output_markdown_path = os.path.join(processed_dir, f"{os.path.splitext(document)[0]}.md")

            with open(output_markdown_path, 'w') as f:
                f.write(markdown_content)
            
            logging.info(f"Arquivo salvo: {output_markdown_path}")

        except Exception as e:
            logging.error(f"Erro ao converter {document} -> {str(e)}")
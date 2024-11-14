import os
import logging
import re

class InstructionGluer:
    def __init__(self, md_file_path, code_folder):
        self.md_file_path = md_file_path
        self.code_folder = code_folder

    def insert_code_into_md(self):
        logging.info(f"Starting to insert code into {self.md_file_path} from {self.code_folder}")

        # Odczytaj plik markdown
        try:
            with open(self.md_file_path, 'r') as md_file:
                md_content = md_file.read()
            logging.debug(f"Read markdown file: {self.md_file_path}")
        except Exception as e:
            logging.error(f"Failed to read markdown file: {self.md_file_path} - {e}")
            return

        # Usuń wszystkie istniejące bloki kodu
        md_content = re.sub(r'```.*?```', '', md_content, flags=re.DOTALL)

        # Przeszukaj folder doc_examples w poszukiwaniu plików
        code_files = {}
        for root, dirs, files in os.walk(self.code_folder):
            for file in files:
                # Stwórz mapę plików {nazwa_pliku: ścieżka_pliku}
                code_files[file] = os.path.join(root, file)
        logging.debug(f"Code files found: {code_files}")

        new_md_content = []
        for line in md_content.splitlines(keepends=True):
            # Check for custom notation [[filename]]
            match = re.search(r'\[\[(.*?)\]\]', line)
            if match:
                filename = match.group(1).strip()
                logging.debug(f"Found custom notation for file: {filename}")

                # Jeśli nazwa pliku jest w słowniku code_files
                if filename in code_files:
                    try:
                        # Odczytaj zawartość pliku z kodem
                        with open(code_files[filename], 'r') as code_file:
                            code_content = code_file.read()
                        logging.debug(f"Read code from file: {filename}")
                    except Exception as e:
                        logging.error(f"Failed to read code file: {filename} - {e}")
                        continue

                    # Determine the language for the code block
                    language = 'bash' if filename.endswith('.sh') else 'python'

                    # Reinsert the placeholder and add the code content
                    new_md_content.append(f"[[{filename}]]\n")
                    new_md_content.append(f"```{language}\n")
                    new_md_content.append(code_content + "\n")
                    new_md_content.append("```\n")
                else:
                    # Jeśli plik nie został znaleziony, pozostaw oryginalną linię
                    new_md_content.append(line)
            else:
                # Jeśli nie ma dopasowania, po prostu dodaj oryginalną linię
                new_md_content.append(line)

        # Write the new content back to the markdown file
        try:
            with open(self.md_file_path, 'w') as md_file:
                md_file.writelines(new_md_content)
            logging.info(f"Successfully updated markdown file: {self.md_file_path}")
        except Exception as e:
            logging.error(f"Failed to write updated content to markdown file: {self.md_file_path} - {e}")

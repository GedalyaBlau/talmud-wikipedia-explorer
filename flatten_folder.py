import os
import re

def read_file_contents(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def remove_comments_and_blank_lines(content):
    content = re.sub(re.compile("#.*?\n"), "", content)  # Remove comments
    content = re.sub(re.compile("\n\s*\n"), "\n", content)  # Remove blank lines
    content = re.sub(re.compile("\s\s+"), " ", content)  # Remove extra whitespace
    return content.strip()

def is_ignored_folder(folder, ignore_folders):
    normalized_folder = folder.replace(os.sep, '/')
    return any(ignore in normalized_folder for ignore in ignore_folders)

def flatten_django_folder(folder_path, output_file, ignore_folders=None):
    relevant_extensions = ['.py', '.html', '.css', '.js', '.json']
    ignore_folders = ignore_folders or []

    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(folder_path):
            if not is_ignored_folder(root, ignore_folders):
                for file in files:
                    if any(file.endswith(ext) for ext in relevant_extensions):
                        file_path = os.path.join(root, file)
                        content = read_file_contents(file_path)
                        cleaned_content = remove_comments_and_blank_lines(content)
                        outfile.write(f"===== {file_path} =====\n")
                        outfile.write(cleaned_content)
                        outfile.write("\n\n")

if __name__ == "__main__":
    folder_path = "talmud_wikipedia_explorer"
    output_file = "flattened_django_app222.txt"
    ignore_folders = ["explorer/migrations"]
    flatten_django_folder(folder_path, output_file, ignore_folders)

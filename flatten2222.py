import os
import re
import htmlmin
import csscompressor
import jsmin

# Other functions (read_file_contents, is_ignored_folder) remain the same
def read_file_contents(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
def remove_comments(content, file_type):
    if file_type == 'py':
        return re.sub(re.compile("#.*?\n"), "", content)
    elif file_type in ['html', 'css', 'js']:
        return re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", content)
    return content

def minify_content(file_path, content):
    _, ext = os.path.splitext(file_path)
    file_type = ext[1:]
    content = remove_comments(content, file_type)

    if ext == ".html":
        return htmlmin.minify(content, remove_comments=True, remove_empty_space=True)
    elif ext == ".css":
        return csscompressor.compress(content)
    elif ext == ".js":
        return jsmin.jsmin(content)
    elif ext == ".py":
        content = re.sub(re.compile("\n\s*\n"), ";", content)  # Replace newlines with semicolons
        content = re.sub(re.compile("\s\s+"), " ", content)  # Remove extra whitespace
        return content.strip()
    else:
        return content

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
                        minified_content = minify_content(file_path, content)
                        outfile.write(f"===== {file_path} =====\n")
                        outfile.write(minified_content)
                        outfile.write("\n\n")

if __name__ == "__main__":
    folder_path = "talmud_wikipedia_explorer"
    output_file = "flattened_django33.txt"
    ignore_folders = ["explorer/migrations"]
    flatten_django_folder(folder_path, output_file, ignore_folders)

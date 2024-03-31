import os

ENCODINGS = ["utf-8", "utf-16", "iso-8859-15", "cp437"]
DEFAULT_PATH = "D:\\Programmation"


def main():
    path = input("Chemin d'accès du projet : ")
    while not os.path.exists(path):
        if path == "":
            path = DEFAULT_PATH
            print("Chemin par défaut utilisé :", path)
        else:
            print("Le chemin spécifié est incorrect")
            path = input("Chemin d'accès du projet : ")

    allowed_extensions = ["java", "py", "c", "h", "cpp", "hpp", "cs", "ino",
                          "sql",
                          "js", "php", "sql", "html", "css",
                          # "resx", "sln", "cvxproj", "filters"
                          ]
    # "java", "py", "c", "cs", "js", "php", "sql", "html", "css", "json", "txt"

    exclude_dirs = ["venv", "Lib", "lib", "Library", ".idea", ".settings", "bin", "LWJGL 3", "LWJGL 3 + Assets",
                    "New-Beginner-Java-Game-Programming-Src-master", "Build Tools Spigot Minecraft",
                    "node_modules", "Lux-Viewer-2021-master", ".vscode", ".metadata", "x64", ".vs", ".git", "html_temp"]

    extension_lines = {}
    for extension in allowed_extensions:
        extension_lines[extension] = 0
    explore_dir(path, extension_lines, allowed_extensions, exclude_dirs)

    # Count total lines
    total_nb_line = 0
    for nb_lines in extension_lines.values():
        total_nb_line += nb_lines

    # Sort extensions
    sorted_extension_lines = sorted(extension_lines.items(), key=lambda item: item[1], reverse=True)

    # Print lines per extension
    print("Nombre de ligne par type de fichier:")
    for extension, nb_lines in sorted_extension_lines:
        if nb_lines > 0:
            percentage = round(nb_lines / total_nb_line * 100, 2)
            print(f"{extension}: {nb_lines} lignes ({percentage}%)")
    print(f"Pour un total de {total_nb_line} lignes dans le dossier sélectionné")


def explore_dir(path, extension_lines, allowed_extensions, exclude_dirs):
    nb_lines = 0
    if os.path.exists(path):
        if os.path.isdir(path):
            for file_name in os.scandir(path):
                if file_name.is_file():
                    count_lines(file_name.path, extension_lines, allowed_extensions)
                elif file_name.is_dir() and file_name.name not in exclude_dirs:
                    explore_dir(file_name.path, extension_lines, allowed_extensions, exclude_dirs)
        elif os.path.isfile(path):
            count_lines(path, extension_lines, allowed_extensions)
    return


def count_lines(file_path: str, extension_lines: dict[str, int], allowed_extensions: list[str]):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        p, extension = os.path.splitext(file_path)
        if extension != "" and len(extension) > 1 and extension[1:] in allowed_extensions:
            print("Lecture du fichier:", file_path)
            read_lines_file(file_path, extension, extension_lines)
    else:
        print("Le chemin spécifié du fichier est incorrect")
    return


def read_lines_file(file_path: str, extension: str, extension_lines: dict[str, int]):
    nb_lines = 0
    if os.path.exists(file_path) and os.path.isfile(file_path):
        i = 0
        file_read = False

        while i < len(ENCODINGS) and not file_read:
            try:
                file = open(file_path, "r", encoding=ENCODINGS[i])
                n = len(file.readlines())
                extension_lines[extension[1:]] += n
                # print(n, file_path)
                file.close()
                file_read = True
            except (UnicodeDecodeError, UnicodeError) as e:
                i += 1

    return


if __name__ == "__main__":
    main()

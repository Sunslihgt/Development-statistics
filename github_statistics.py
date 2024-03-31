# Use command: git log --reflog --stat

def count_lines_per_user() -> None:
    print("Use command: git log --reflog --stat")
    print("Paste the output here and enter 2-3 empty lines to end the input")
    contents: list[str] = []
    last_line_empty = False
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
        if line == "" and last_line_empty:
            break
        last_line_empty = line == ""
        # print("Last line empty: ", last_line_empty)

    print(contents)
    print(len(contents))

    commits_string = []
    commit_start = 0
    for i in range(len(contents)):
        if contents[i].startswith("commit"):
            if commit_start != i:
                commit_string = [contents[j] for j in range(commit_start, i)]
                commits_string.append(commit_string)
                commit_start = i
    # Last commit
    if commit_start < len(contents) - 1:
        commit_string = [contents[j] for j in range(commit_start, len(contents))]
        commits_string.append(commit_string)
    print(len(commits_string))
    print(commits_string)

    authors_lines: dict[str, int] = {}
    for commit_string in commits_string:
        author, email = get_commit_author(commit_string)
        if author is None or email is None:
            continue

        modified_lines = count_lines_commit_string(commit_string)
        if email not in authors_lines:
            authors_lines[email] = 0
        authors_lines[email] += modified_lines

    total_lines = sum([author_line for author_line in authors_lines.values()])
    print_authors_lines(authors_lines, total_lines)


def count_lines_commit_string(commit_string: list[str]) -> int:
    modified_lines = 0
    for line in commit_string:
        if "|" in line:
            splitted_string: list[str] = line.split("|")
            if len(splitted_string) == 2:
                line_infos: str = splitted_string[1]
                number_start: int = -1
                for i in range(len(line_infos)):
                    if line_infos[i].isnumeric() and number_start < 0:
                        number_start = i
                    elif line_infos[i] == " " and number_start >= 0:
                        try:
                            if i == len(line_infos) - 1:
                                modified_lines += int(line_infos[number_start:])
                            else:
                                modified_lines += int(line_infos[number_start:i])
                            break
                        except:
                            break
                    elif not line_infos[i].isnumeric() and line_infos[i] != " ":
                        break
    # if modified_lines > 1000:
    #     print(f"Strange commit, {modified_lines} lines: ", commit_string[0].split("commit ")[1])
    return modified_lines


def get_commit_author(commit_string: list[str]) -> list:
    for line in commit_string:
        if line.startswith("Author"):
            author = line.replace("Author", "")
            email = line.split("<")[1].split(">")[0]
            return [author, email]
    return [None, None]


def print_authors_lines(authors_lines: dict[str, int], total_lines: int) -> None:
    print(f"Total lines --- {total_lines} (100 %)")
    for email, lines in authors_lines.items():
        percent = round(lines / total_lines * 100, 0)
        print(f"{email} --- {lines} ({percent} %)")


if __name__ == "__main__":
    count_lines_per_user()

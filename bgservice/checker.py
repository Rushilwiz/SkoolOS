import os


def shell_check():
    bash_history = [line.strip() for line in open(os.path.expanduser("~/.bash_history"), 'r')]
    zsh_history = [line.strip() for line in open(os.path.expanduser("~/.histfile"), 'r')]
    report = "Suspicios commands found:\n"
    for i in bash_history + zsh_history:
        if "git" in i:
            report += i + "\n"
    if report != "Suspicios commands found:\n":
        return report
    return "Nothing suspicious found in bash or zsh history."


def file_check(dir_):


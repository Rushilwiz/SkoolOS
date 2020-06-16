import os
from glob import glob

file_whitelist = [
    # text and document files
    ".doc",
    ".docx",
    ".odt",
    ".pdf",
    ".rtf",
    ".tex",
    ".txt",
    ".wpd",
    # video files
    ".3g2",
    ".3gp",
    ".avi",
    ".flv",
    ".h264",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpg",
    ".mpeg",
    ".rm",
    ".swf",
    ".vob",
    ".wmv",
    # spreadsheet files
    ".ods",
    ".xls",
    ".xlsm",
    ".xlsx",
    ".csv",
    # programming files
    ".c",
    ".class",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".java",
    ".pl",
    ".sh",
    ".swift",
    ".vb",
    # presentation files
    ".key",
    ".odp",
    ".pps",
    ".ppt",
    ".pptx",
    # image files
    ".ai",
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".png",
    ".ps",
    ".psd",
    ".svg",
    ".tif",
    ".tiff",
]


def shell_check():
    bash_history = [
        line.strip()
        for line in open(os.path.expanduser("~/.bash_history"), 'r')
    ]
    zsh_history = [
        line.strip() for line in open(os.path.expanduser("~/.histfile"), 'r')
    ]
    report = "Suspicios commands found:\n"
    for i in bash_history + zsh_history:
        if "git" in i:
            report += i + "\n"
    if report != "Suspicios commands found:\n":
        return report
    return "Nothing suspicious found in bash or zsh history."


def verify_file(file_):
    for ext in file_whitelist:
        if file_[len(file_) - len(ext):] == ext:
            return True
    return False


def file_check(dir_):
    files = glob(dir_ + "/**/*", recursive=True)
    suspicious_files = []
    for file_ in files:
        if not verify_file(file_):
            suspicious_files.append(file_)
    return suspicious_files

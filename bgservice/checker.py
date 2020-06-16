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
    """
    Check .bash_history and .histfile for git commands that could interfere with SkoolOS
    :return: results of the check
    """
    bash_history = [
        line.strip()
        for line in open(os.path.expanduser("~/.bash_history"), 'r')
    ]
    zsh_history = [
        line.strip() for line in open(os.path.expanduser("~/.histfile"), 'r')
    ]
    suspicious_commands = []
    for i in bash_history + zsh_history:
        if "git" in i:
            suspicious_commands.append(i)
    if suspicious_commands:
        return str(
            len(suspicious_commands)
        ) + " suspicious commands found:\n" + "\n".join(suspicious_commands)
    return "Nothing suspicious found in bash or zsh history."


def verify_file(file_):
    """
    Check if the file name has an extension in the list of whitelisted file exentsions
    :param file_: path to file
    :return: whether or not the file's extension is whitelisted
    """
    for ext in file_whitelist:
        if len(file_) > len(ext):
            if file_[len(file_) - len(ext):] == ext:
                return True
    return False


def file_check(dir_):
    """
    Checks specified dir_ for non-whitelisted files using verify_file()
    :param dir_: directory to check
    :return: list of suspicious files
    """
    files = glob(dir_ + "/**/*", recursive=True)
    suspicious_files = []
    for file_ in files:
        if not verify_file(file_):
            suspicious_files.append(file_)
    return suspicious_files

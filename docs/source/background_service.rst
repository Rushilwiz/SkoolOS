Background Service
=================

This requires no user input. The proper events are
called by the main application to log events in the
student's work directory. The service records file
accesses, editions, deletions, files moved from an
outside directory, and file to an outside directory.
Additionally, it records any git commands discovered
in the student's .bash_history or .histfile (zsh
equivalent), as git commands can interfere with the
service. It also checks for files that do not have
extensions that are whitelisted. The whitelist
includes common file extensions such as text files,
presentations, and programming file extensions (e.g.
.py for python and .class for java).

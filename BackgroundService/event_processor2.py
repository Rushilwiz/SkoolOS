import pyinotify

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE | \
    pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_OPEN

class EventHandler(pyinotify.ProcessEvent):
    _methods = ["IN_CREATE",
                "IN_CLOSE_WRITE",
                "IN_DELETE",
                "IN_MOVED_TO",
                "IN_MOVED_FROM",
                "IN_OPEN",
                ]
   def __process_generator(self, event):
       description = \
           "Event: {}\n" \
           "Event Path: {}\n" \
           "Timestamp: {}\n".format(
               method,
               event.pathname,
               time.strftime("%A, %B %d, %Y %H:%M:%S", time.localtime())
           )
       if "IN_DELETE" in description:
           description += "WARNING: Unexpected file deletion\n"
       if "IN_MOVED_TO" in description:
           description += "WARNING: Unexpected file add to work\n"
       if "IN_MOVED_FROM" in description:                                     
           description += "WARNING: Unexpected file moved out of directory\n"
       return description

    def process_IN_CREATE(self, event):
        self.__process_generator(event)
    def process_IN_CLOSE_WRITE(self, event):
        self.__process_generator(event)
    def process_IN_DELETE(self, event):
        self.__process_generator(event)
    def process_IN_MOVED_TO(self, event):
        self.__process_generator(event)
    def process_IN_MOVED_FROM(self, event):
        self.__process_generator(event)
    def process_IN_OPEN(self, event):
        self.__process_generator(event)


notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
notifier.start()

wdd = wm.add_watch('/tmp', mask, rec=True)
input("Press any key to continue...")

notifier.stop()

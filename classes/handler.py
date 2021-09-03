from watchdog.events import FileSystemEventHandler

from classes.processor import Processor


class LogModifiedHandler(FileSystemEventHandler):

    def __init__(self, logfile, processor: Processor) -> None:
        self.logfile = logfile
        self.processor = processor
        log = open(logfile, "r")
        log.read(-1)
        self.last_row = log.tell()
        log.close()
        super().__init__()

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.logfile:
            log = open(event.src_path, "r")
            log.seek(self.last_row)
            self.processor.process(log.read(-1).strip())
            self.last_row = log.tell()
            log.close()
        return super().on_modified(event)

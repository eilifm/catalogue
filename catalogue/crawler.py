from hashlib import sha1
import hashlib
import os
import shutil
import os
import sys
from path import Path
import time
import json
import platform
from joblib import Parallel, delayed
from itertools import islice
import logging
logger = logging.getLogger('pycat')

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

IGNORE_NAMES = [
    ".DS_Store"
]


def find_files(rootdir):
    for root, subdirs, files in os.walk(rootdir):
        # for subdir in subdirs:
            # print('\t- subdirectory ' + subdir)

        for filename in files:
            file_path = os.path.join(root, filename)
            if filename in IGNORE_NAMES:
                continue
            yield filename, file_path
            # print('\t- file %s (full path: %s)' % (filename, file_path))


def sha1sum(filename):
    h = hashlib.sha1()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def file_times(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file), os.path.getctime(path_to_file), os.path.getsize(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_mtime, stat.st_birthtime, stat.st_size
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime, stat.st_mtime, stat.st_size


def process(files):
    for file in files:
        logger.debug(file)
        filename, path = file[0], file[1]
        # print(file)
        try:
            with open(path, 'r') as f:
                pass
        except IOError or FileNotFoundError:
            print("File not accessible")
            continue

        modified, created, size = file_times(path)
        extension = filename.split(".")[-1]
        file_metadata = {
            "filename": filename,
            "path": path,
            "hash": None,
            "extension": extension,
            "modified_ts": int(modified),
            "created_ts": int(created),
            "version": int(time.time()),
            "file_size": size
        }

        file_metadata['hash'] = sha1sum(Path(path).abspath())
        yield json.dumps(file_metadata)


def process_file_worker(file_list):
    return list(process(file_list))


def crawl_files(file_list):
    with Parallel(n_jobs=4, verbose=50, batch_size=30) as parallel:
        results = parallel(delayed(process_file_worker)([files]) for files in file_list)



if __name__ == "__main__":
    files = find_files()
    # crawl_files(files)
    with open("./raw_metadata.ldjson", 'a') as metadata_file:
        for file in process(files):
            metadata_file.write(file+"\n")


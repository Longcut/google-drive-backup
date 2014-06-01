"""Simple command-line sample incremental backup for Google Drive.

Command-line application that lists backed up copies of a given file.

Currently this file only lists the location of backups.  The backed up copies
are not restored automatically by this script.  They must be manually taken
from the file location(s) provided by this script.

Examples:

    $ python recover.py --file_id=11QYOerwAn_0F2fIx2R3kz73sccVmTHe8iqo7_1KxOYE
        (to find backups by drive file id)

    $ python recover.py --folder=testfolder/
        (to find backups by folder, exact match only, not recommended)

    $ python recover.py --file_name=testdoc.txt
        (to find backups by file name, exact match only)

You can also get help on all the command-line flags the program understands
by running:

    $ python drive.py --help

"""

__author__ = 'jeremy.lakey@gmail.com (Jeremy Dean Lakey)'

import gflags, httplib2, logging, os, pprint, sys, re, time
import pprint

import fmanager

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError, flow_from_clientsecrets
from oauth2client.tools import run


FLAGS = gflags.FLAGS

# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_string('file_id', '', 'Exact key of backed up file')
gflags.DEFINE_string('file_name', '', 'Exact name of file' )
gflags.DEFINE_string('folder', '', 'Exact location of file(s) relative to the backed up folder' )
gflags.DEFINE_string('destination', 'downloaded/', 'Folder where backups were made', short_name='d')


def main(argv):
    # Let the gflags module process the command-line arguments
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
        sys.exit(1)
    try:
        fmanager.set_destination(FLAGS.destination)
    except:
        print ( "Could not write to directory %s. Please check permissions." % FLAGS.destination )
        exit(1)
    file_id = FLAGS.file_id
    file_name = FLAGS.file_name
    folder = FLAGS.folder
    backup_copies = fmanager.get_copies_list(file_id, file_name, folder )
    if not backup_copies:
         "No files found that matched your query."
    for copy in backup_copies:
         print "key:      ", copy[0]
         print "file name:", copy[1], copy[2]
         print "modified: ", copy[3]
         print "location: ", copy[4]
         print ''

if __name__ == '__main__':
    main(sys.argv)


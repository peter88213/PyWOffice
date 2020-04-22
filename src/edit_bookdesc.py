"""Import and export ywriter7 book descriptions for editing. 

Convert yw7 book descriptions to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yw7.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWOffice
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.converter.cnv_runner import CnvRunner

from pywoffice.fileop.odt_bookdesc_writer import OdtBookDescWriter
from pywoffice.fileop.html_bookdesc_reader import HtmlBookDescReader


def run(sourcePath, silentMode=True):

    if sourcePath.endswith('.yw7'):
        document = OdtBookDescWriter('')
        extension = 'odt'

    elif sourcePath.endswith('.html'):
        document = HtmlBookDescReader('')
        extension = 'html'

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = CnvRunner(sourcePath, document,
                          extension, silentMode, '_books')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)

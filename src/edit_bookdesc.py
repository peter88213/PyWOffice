"""Import and export ywriter7 book descriptions for editing. 

Convert yw7 book descriptions to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yw7.

Copyright (c) 2019, peter88213
For further information see https://github.com/peter88213/PyWOffice
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.converter.yw_cnv_gui import YwCnvGui

from pywoffice.odt.odt_bookdesc import OdtBookDesc
from pywoffice.html.html_bookdesc import HtmlBookDesc


def run(sourcePath, silentMode=True):

    if sourcePath.endswith('.yw7'):
        document = OdtBookDesc('')
        extension = 'odt'

    elif sourcePath.endswith('.html'):
        document = HtmlBookDesc('')
        extension = 'html'

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document,
                          extension, silentMode, '_books')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)

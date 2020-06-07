HEADER = 'MIME-Version: 1.0\n' \
         'Content-Type:multipart/mixed;boundary="KkK170891tpbkKk__FV_KKKkkkjjwq"\n'
MIME_BOUNDRY = 'KkK170891tpbkKk__FV_KKKkkkjjwq'
FILE_TEMPLATE = 'Content-Type:application/octet-stream;name="{0}"\n' \
                'Content-Transfer-Encoding:base64\n' \
                'Content-Disposition:attachment;filename="{0}"\n' \
                '\n\r' \
                '{1}'
PLAIN_TEXT_TEMPLATE = 'Content-Type: text/plain; charset=utf-8\n' \
                      '\n\r' \
                      '{0}'
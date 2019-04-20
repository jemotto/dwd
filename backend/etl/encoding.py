import magic

def determine_encoding(filepath):
    mime = magic.Magic(mime_encoding=True)
    return mime.from_file(filepath)
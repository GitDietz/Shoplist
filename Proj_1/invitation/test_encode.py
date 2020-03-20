from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

if __name__ == '__main__':
    pk = 23
    byted = force_bytes(pk)
    # force_text(urlsafe_base64_decode(force_bytes(pk)))
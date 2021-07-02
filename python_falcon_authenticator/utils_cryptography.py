import base64
import struct

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers


def intarr2long(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)


def base64_to_long(data):
    if isinstance(data, str):
        data = data.encode("ascii")

    # urlsafe_b64decode will happily convert b64encoded data
    _d = base64.urlsafe_b64decode(bytes(data) + b'==')
    return intarr2long(struct.unpack('%sB' % len(_d), _d))


def jwk_to_public_key(jwk):
    exponent = base64_to_long(jwk['e'])
    modulus = base64_to_long(jwk['n'])
    numbers = RSAPublicNumbers(exponent, modulus)

    return numbers.public_key(backend=default_backend())

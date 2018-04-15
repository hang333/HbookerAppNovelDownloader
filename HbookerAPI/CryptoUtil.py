from Crypto.Cipher import AES
import base64
import hashlib

iv = b'\0' * 16


def encrypt(text, key):
    aeskey = hashlib.sha256(key.encode('utf-8')).digest()
    aes = AES.new(aeskey, AES.MODE_CFB, iv)
    return base64.b64encode(aes.encrypt(text))


def decrypt(encrypted, key='zG2nSeEfSHfvTCHy5LCcqtBbQehKNLXn'):
    aeskey = hashlib.sha256(key.encode('utf-8')).digest()
    aes = AES.new(aeskey, AES.MODE_CBC, iv)
    return pkcs7unpadding(aes.decrypt(base64.b64decode(encrypted)))


def pkcs7unpadding(data):
    length = len(data)
    unpadding = ord(chr(data[length - 1]))
    return data[0:length - unpadding]


if __name__ == '__main__':
    print('decrypt,key=', decrypt(
        'c1SR02T7X+xmq37zfs0U8NAj73eedAs3tnXMQKDNUPlI2vcaNRXpKA3JktMoffp3EYPCsvCjzeCJUynjDISbNP4D5HjaCp6tMrOsBBfQzVI='))
    test = b'{"code":200001,"tip":"\\u7f3a\\u5c11\\u767b\\u5f55\\u5fc5\\u9700\\u53c2\\u6570"}\x08\x08\x08\x08\x08\x08\x08\x08'
    print('pkcs7unpadding', pkcs7unpadding(test))


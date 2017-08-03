'''
    给出一种AES加密和解密方法
'''
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import base64


def crypt(key_str, data):
    # 生成秘钥的字符串,可以用验证码
    key_md5 = MD5.new()
    key_md5.update(bytes(key_str, 'utf-8'))
    # 可以用于AES的key
    key_str = key_md5.hexdigest()
    # 可以用于AES的iv
    iv_str = key_str[2:18]
    # python需要使用'\0'来填充,否则加密得到的结果会和js加密结果不同
    PADDING = '\0'
    pad_it = lambda s: s + (16 - len(s) % 16) * PADDING
    generator = AES.new(key_str, AES.MODE_CBC, iv_str)
    crypted_bytes = generator.encrypt(pad_it(data))
    crypted_str = base64.b64encode(crypted_bytes).decode()
    return crypted_str

def decrypt(key_str, data):
    key_md5 = MD5.new()
    key_md5.update(bytes(key_str, 'utf-8'))
    key_str = key_md5.hexdigest()
    iv_str = key_str[2:18]
    PADDING = '\0'
    pad_it = lambda s: s + (16 - len(s) % 16) * PADDING
    generator = AES.new(key_str, AES.MODE_CBC, iv_str)
    data = base64.b64decode(data)
    recovery = generator.decrypt(data)
    recovery_str = recovery.decode().rstrip(PADDING)
    return recovery_str
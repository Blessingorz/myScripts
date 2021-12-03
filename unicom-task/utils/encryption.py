import os,sys
import base64,rsa,time,requests,logging,traceback
# 手机号密码加密算法
#获取公钥的key
def str2key(s):
    # 对字符串解码
    b_str = base64.b64decode(s)

    if len(b_str) < 162:
        return False

    hex_str = ''

    # 按位转换成16进制
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h

    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2

    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]

    return modulus,exponent

#对手机号和登录密码进行加密
def encryption(message):
    message=str.encode(message)
    key = str2key("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB")
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    rsa_pubkey = rsa.PublicKey(modulus, exponent)
    crypto = rsa.encrypt(message, rsa_pubkey)
    b64str = base64.b64encode(crypto)
    return b64str
    

#对手机号和登录密码进行加密
def encryption_2(message):
    with open('./utils/unicom.js', 'r', encoding='utf8') as fp:
        js = fp.read()
    ctx = execjs.compile(js)
    b64str = ctx.call('RSAEncrypt', message)
    return b64str

#这里对手机号和密码加密，传入参数需是 byte 类型
# username = encryption(username)
# password = encryption(password)

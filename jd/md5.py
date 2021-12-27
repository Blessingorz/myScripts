
import hashlib,os

with open(os.path.abspath('e:\桌面\自动任务\myScripts\jd\jd_wabao_help.py'), 'rb') as f:
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    md5_file = md5obj.hexdigest()
    print(md5_file)


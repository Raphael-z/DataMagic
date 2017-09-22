#coding:utf8
"""
    config.py
"""


DEBUG = True

SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % ('root', '901225shl', 'localhost', 'raphael')
SQLALCHEMY_POOL_TIMEOUT = 100
SQLALCHEMY_POOL_RECYCLE = 5
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# USERNAME = 'admin'
# PASSWORD = 'admin'
#
# UPLOAD_FOLDER = './static/upload/'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# RECAPTCHA_PUBLIC_KEY = '6Ld4rwITAAAAAKUD5AntlHi7HL36W2vHJQOIjQmA'
# RECAPTCHA_PRIVATE_KEY = '6Ld4rwITAAAAAFE8nTS852QbsqCBx1mN8D4BqenE'
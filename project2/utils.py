import hashlib

def generate_short_code(url):
    return hashlib.md5(url.encode()).hexdigest()[:6]
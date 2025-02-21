import requests
from bs4 import BeautifulSoup
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

url = 'https://www.w3.org/History.html'
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
text = soup.get_text()

words = re.findall(r'\b[\w]+\b', text) 

unique_words = set(words)
repeated_words = []

for word in unique_words:
    repeated_word = (word * (32 // len(word))) + word[:32 % len(word)] 
    repeated_words.append(repeated_word)

for word in repeated_words:
    print(word)

def is_ascii(data):
    try:
        data.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

ciphertext_b64 = "ZUbG9utX0sQNDzbwyZLV528SMvBN5MTnKbAlIzcfx0g8UOWdwsMfRulCZDQ3/jTb0xPUmK56wOS4k+SIeey33+3/F09+juy2jZnSWw0bL3dni2v7N8TYn1U1HVkqwv84S/sOig89tkdrzHwXsTocGHUoR+3Zbbi7jJFK8aw/oRtJjrQGUpY3sw/Vj9R1VLlQ/c7sgUxCLafHWU9sakoQ5Rv2ICHqoBadrwSUXSNihCI="
ciphertext = base64.b64decode(ciphertext_b64)

def decrypt_aes(key, ciphertext, mode):
    cipher = AES.new(key.encode('utf-8'), mode)
    try:
        if mode == AES.MODE_ECB:
            decrypted = cipher.decrypt(ciphertext)
        elif mode == AES.MODE_CBC:
            iv = b'0000000000000000'  
            cipher = AES.new(key.encode('utf-8'), mode, iv=iv)
            decrypted = cipher.decrypt(ciphertext)
        else:
            return None
        return decrypted
    except Exception as e:
        print(f"Decryption failed with error: {e}")
        return None

def attempt_decryption(key, ciphertext):
    decrypted_ecb = decrypt_aes(key, ciphertext, AES.MODE_ECB)
    if decrypted_ecb and is_ascii(decrypted_ecb):
        print(f"Decrypted with ECB: {decrypted_ecb.decode('ascii')}")
    
    decrypted_cbc = decrypt_aes(key, ciphertext, AES.MODE_CBC)
    if decrypted_cbc and is_ascii(decrypted_cbc):
        print(f"Decrypted with CBC ({key}): {decrypted_cbc.decode('ascii')}")
        
for word in repeated_words:
    attempt_decryption(word, ciphertext)

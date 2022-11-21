import random
import hashlib
import base64
import time
import math
import sys
import hmac
import pyqrcode
import os
import struct


LENGTH = 6 # codes will be 6 digits long
INTERVAL = 30 # 30 second intervals
#INTERVAL = 10 # 10 second intervals

def generate_secret():
    # generate a random base32 secret key
    secret = ""
    for i in range(0, 20):
        secret += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
        # ignoring 1 and 0 because they look too similar to I and O
        encoded = base64.b32encode(secret.encode("utf-8"))
    return encoded

def generate_qr():
    uri_start = "otpauth://totp/Example:user@company.com?secret="
    # prefix for a google authenticator uri
    # based on the example shown at https://github.com/google/google-authenticator/wiki/Key-Uri-Format 
    uri_end = "&issuer=Example&period="
    uri_end += str(INTERVAL)
    # issuer and period for the uri are included after the secret.
    secret = generate_secret()
    #print("Secret: %s" % secret)
    # save the secret to a file secret.txt
    with open("secret.txt", "w") as f:
        f.write(secret.decode())
    # generate the QR code
    qr = pyqrcode.create(uri_start + secret.decode() + uri_end)
    #save as svg
    qr.svg("qr.svg", scale=8)

def get_otp():
    # if the secret file doesn't exist, throw an error and exit
    if not os.path.isfile("secret.txt"):
        print("No secret file found. Please run %s --generate-qr first." % sys.argv[0])
        sys.exit(1)
    
    # read the secret from the file secret.txt
    with open("secret.txt", "r") as f:
        secret = f.read()
    
    #secret = base64.base32decode(secret, True)

    i = INTERVAL - (int(time.time()) % INTERVAL) # get the current interval
    print("sleeping for %d seconds" % i)
    time.sleep((math.floor(i))) # sleep for the current interval in order to syncronize with google authenticator

    while True:
        # generate the OTP
        totp = get_totp(secret)
        print("OTP:", totp, "valid for", str(INTERVAL), "seconds")
        # wait for 30 seconds before generating the next OTP
        time.sleep(INTERVAL)

    
def get_hotp(secret, i):
    key = base64.b32decode(secret, True) # decode the secret from base32 to bytes
    msg = struct.pack(">Q", i) # pack the current interval into a 8 byte unsigned long, big endian
    h = hmac.new(key, msg, hashlib.sha1).digest() # generate the hmac
    offset = h[-1] & 0x0f # get the offset from the last byte of the hmac
    truncatedHash = h[offset:offset + 4] # get the truncated hash of the hmac
    truncatedHash = struct.unpack(">L", truncatedHash)[0] # unpack the truncated hash into a long
    truncatedHash &= 0x7fffffff # make the truncated hash positive
    code = truncatedHash % (10 ** LENGTH) # get the OTP from the truncated hash
    return code # return the OTP

def get_totp(secret):
    res = str(get_hotp(secret, math.floor(int(time.time())/INTERVAL)))
    # use zfill to pad the OTP with zeros until it's 6 digits long
    return res.zfill(LENGTH)

def main():
    if len(sys.argv) != 2:
        print("Usage: %s --[generate-qr || get-otp]" % sys.argv[0])
        sys.exit(1)
    
    if sys.argv[1] == "--generate-qr":
        generate_qr()
    
    elif sys.argv[1] == "--get-otp":
        get_otp()

    else:
        print("Unknown option. Usage: %s --[generate-qr || get-otp]" % sys.argv[0])
        sys.exit(1)
    
main()
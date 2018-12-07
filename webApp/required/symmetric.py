
def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True
#----------------------------------------------------------------------------------------------------------#
#------------------------------------------caesar Cipher---------------------------------------------------#

def caesar_cipher(text,key,flag):
    if(key==""):
        key=2
    key=int(key)
    cipher_text=""
    for char in text:
        if(char.isdigit()):
            cipher_text+=chr(( ord(char) + key*flag - ord('0')) % 10 + ord('0') )
        elif(char.isupper()):
            cipher_text+=chr(( ord(char) + key*flag - ord('A')) % 26 + ord('A') )
        elif(char.islower()):
            cipher_text+=chr(( ord(char) + key*flag - ord('a')) % 26 + ord('a') )
        else:
            cipher_text+=char
    return [cipher_text,key]
def caesar_decipher(text,key):
    return caesar_cipher(text, key,-1)
def caesar(text,text2,key,flag):
    print "caesar"
    if(flag==1):
        ls=caesar_cipher(text,key,1)
        ls.append(-1)
        return ls   
    else:
        ls=caesar_decipher(text2,key)
        print "decipher called"
        ls.append(1)
        return ls
#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------Vigenere Cipher-------------------------------------------------------#
def vigenere_cipher(text,key):
    return vigenere_encrypts(text,key,1)
def vigenere_encrypts(text,key,flag):
    if(key==""):
        key="vigenere"
    key_len=len(key)
    keys=key
    key=key.upper()
    cipher_text=""
    key_tmp=0
    for char in text:
        if(char.isdigit()):
            cipher_text += chr( ( ord(char) + (ord(key[key_tmp])-ord('A')+1)*flag - ord('0') )%10 + ord('0') )
        elif(char.islower()):
            cipher_text += chr(( ord(char) + (ord(key[key_tmp])-ord('A')+1)*flag - ord('a'))%26 + ord('a') )
        elif(char.isupper()):
            cipher_text+= chr(( ord(char) + (ord(key[key_tmp])-ord('A')+1)*flag -ord('A'))%26 + ord('A') )
        else:
            cipher_text+=char
        key_tmp+=1
        key_tmp%=key_len    
    return [cipher_text,keys]

def vigenere_decipher(text,key):
    return vigenere_encrypts(text,key,-1)
def vigenere(text,text2,key,flag):
    if(flag==1):
        ls=vigenere_cipher(text,key)
        ls.append(-1)
        return ls
    else:
        ls= vigenere_decipher(text2,key)
        ls.append(1)
        return ls
#------------------------------------------------------------------------------------------------------------#
#-----------------------------------------Playfair-----------------------------------------------------------#
def key_playfair(key):
    key=key.upper()
    ls=[]
    for i in range(ord('A'),ord('Z')+1):
        ls.append(chr(i))
    for i in xrange(10):
        ls.append(str(i))
    keys=[]
    for i in xrange(6):
        keys.append([])
    count=0
    row=0
    for char in key:
        if(char in ls):
            keys[row].append(char)
            ls.remove(char)
            count+=1
            if(count%6==0):
                count=0
                row+=1
    for i in ls:
        keys[row].append(i)
        count+=1
        if(count%6==0):
            count=0
            row+=1
    dic={}
    for i in range(6):
        for j in range(6):
            dic[keys[i][j]]=[i,j]
    
    return keys,dic
def wrapMessage(text):
    ls=[]
    text=text.upper()
    text = text.replace(" ","")
    l=len(text)
    text+='X'
    ls=[]
    i=0
    while(i<l):
        if(text[i]!=text[i+1]):
            ls.append(text[i]+text[i+1])
            i+=2
        else:
            ls.append(text[i]+'X')
            i+=1
    return ls
def playfair_cipher(text,key):
    if(key==""):
        key="playfair"
    keys,dic=key_playfair(key)
    message=wrapMessage(text)
    ans=[]
    for i in message:
        row1,col1=dic[i[0]]
        row2,col2=dic[i[1]]
        if(col1==col2):
            row1= (row1+1)%6
            row2= (row2+1)%6
        elif(row1==row2):
            col1 = (col1+1)%6
            col2 = (col2+1)%6
        else:
            col1,col2=col2,col1
        ans.append(keys[row1][col1]+keys[row2][col2])
    value="".join(ans)
    return [value,key]
def playfair_decipher(text,key):
    if(key==""):
        key="playfair"
    keys,dic=key_playfair(key)
    message=wrapMessage(text)
    ans=[]
    for i in message:
        row1,col1=dic[i[0]]
        row2,col2=dic[i[1]]
        if(col1==col2):
            row1= (row1-1)%6
            row2= (row2-1)%6
        elif(row1==row2):
            col1 = (col1-1)%6
            col2 = (col2-1)%6
        else:
            col1,col2=col2,col1
        ans.append(keys[row1][col1]+keys[row2][col2])
    value="".join(ans)
    return [value,key]
def playfair(text,text2,key,flag):
    if(flag==1):
        ls=playfair_cipher(text,key)
        ls.append(-1)
        return ls
    else:
        ls=playfair_decipher(text2,key)
        ls.append(1)
        return ls
#--------------------------------------------------------------------------------------------------------#
#--------------------------------------------DES---------------------------------------------------------#
def DES_cipher(text,key):
    pass
def DES_decipher(text,key):
    pass
#--------------------------------------------------------------------------------------------------------#
#--------------------------------------------3DES--------------------------------------------------------#
def DES3_cipher(text,key):
    pass
def DES3_decipher(text,key):
    pass
#--------------------------------------------------------------------------------------------------------#
#--------------------------------------------BlowFish----------------------------------------------------#
def Blowfish_encrypt(text,key):
    pass
def Blowfish_decrypt(text,key):
    pass
#--------------------------------------------------------------------------------------------------------#
#---------------------------------------------RC5--------------------------------------------------------#
def RC5_cipher(text,key):
    pass
def RC5_decipher(text,key):
    pass
#--------------------------------------------------------------------------------------------------------#
#---------------------------------------------RC4--------------------------------------------------------#
def RC4_cipher(data,key):
    if(key==""):
        key="rc4"
    S, j, out = list(range(256)), 0, []
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for ch in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        out.append("&#"+str(ord(ch) ^ S[(S[i] + S[j]) % 256])+";")
    print "key is {}".format(key)
    return ["".join(out),key]
def RC4_decipher(text,key):
    ls=text.split(";")
    ans=""
    for i in ls:
        ans+=str(i[2:])
    return RC4_cipher(text, ans)
def RC4(text,text2,key,flag):
    print "type of text is {} and type of text2 is {}".format(type(text),type(text2))
    ls=[]
    if(flag==1):
        if(";" in text):
            print "flase called at flag1"
            ls=RC4_decipher(text,key)
        else:
            ls=RC4_cipher(text,key)
        ls.append(-1)
    else:
        if(";" in text2):
            print "false called at flag-1"
            ls=RC4_decipher(text2,key)
        else:
            ls=RC4_cipher(text2,key)
        ls.append(1)
    return ls
#--------------------------------------------------------------------------------------------------------#
#---------------------------------------------AES--------------------------------------------------------#
def AES_cipher(text,key):
    pass
def AES_decipher(text,key):
    pass
#--------------------------------------------------------------------------------------------------------#
#--------------------------------------------ROT13-------------------------------------------------------#
def ROT13_cipher(text,key):
    return caesar_cipher(text,13,1)
def ROT13_decipher(text,key):
    return caesar_decipher(text, 13)
def RoT13(text,text2,key,flag):
    if(flag==1):
        ls=ROT13_cipher(text,key)
        ls.append(-1)
        return ls
    else:
        ls = ROT13_decipher(text2,key)
        ls.append(1)
        return ls
#---------------------------------------------------------------------------------------------------------#
#-------------------------------------------Sosemanuk-----------------------------------------------------#
def sosemanuk_cipher(text,key):
    pass
def sosemanuk_decipher(text,key):
    pass
#--------------------------------------------------------------------------------------------------------#

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM")
    return private_key, public_key
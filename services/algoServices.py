from md5hash import md5
from PIL import Image
import speech_recognition as speech
import subprocess

def algo(mail,key):
   
        l = ''                                  # empty string
        for i in mail:                          # iterate characters of mail
            l+=str(ord(i)%100)                  # generate ascii and % 100
                                                # restricts each character to max of 2 places
                                               
        key = str(int(l)-int(key))              # subtracts key from hash string making new hash
        key += str(9872-len(key))               # length of hash made 4 digits by subtracting from a large 4 digit no.
                                                # length stored at end of key
                                               
        return key
   
def key_wise(key):
    
    try :        
        temp = int(key)    
    except Exception:        
        temp = ''
        for i in [i for i in md5(key.encode()).hexdigest() if i < 'a'][:8]:
            temp += i
        
    return int(temp)%253 + 1

def encrypt(mail,key,path):

    try:
        # Read image data as byte array
        with open(path,'rb') as f:
            image = bytearray(f.read())

        # Encryption : XOR
        for index, values in enumerate(image):
            image[index] = values ^ key

        # Encrypt file
        with open(path, 'wb') as f:
            f.write(image)
            f.write(eval('b"'+algo(mail,key)+'"'))
            
    except Exception:
        return 0

    return 1

def decrypt(mail,key,path):

    try:
        # Check if key correct
        with open(path,'rb') as f:
            re = f.read()
            if int(algo(mail,key)) == int(re[-1*(9872-int(re[-4:]))-4:]):
                flag = True
            else:
                flag = False
                
        if (flag):
            # read file
            with open(path, 'rb') as f:
                image = bytearray(f.read()[:-1*len(algo(mail,key))])
            
            # Decryption : XOR
            for index, values in enumerate(image):
                image[index] = values ^ key
            
            # Decrypt file
            with open(path, 'wb') as f:
                f.write(image)
                
            # successful
            
            if (path[-3:]).lower() in ("jpg","png"):
                
                # open file if image
                im = Image.open()
                im.show()
                                
            else:
                
                # open file location
                subprocess.Popen('explorer /select,'+path)
    except Exception:
        return 0
    return 1
             
    
def voice(self):
    
    self.shint = ''
    
    # voice recognizer object
    voice = speech.Recognizer()
    
    # use microphone
    with speech.Microphone() as source:
        voice_command = voice.listen(source)
        
# check input
    try:
        
        self.ids.key.text = voice.recognize_google(voice_command)

# handle the exceptions
    except speech.UnknownValueError:
        
        self.shint = "System could not understand. Please try again."

    except Exception:
        self.shint = "No Internet Connection."
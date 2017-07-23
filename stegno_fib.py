import sys
import os 
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def decodeStegno(sec_bytes,path):
    #fileSize = os.path.getsize(path)/1000 # get file size as kilobytes.
    try:
        in_reader = open(path,'r')  # read image input file.
    except IOError:
        print " [*] Reading from file failed!"
        print " [*] Exiting..."
        in_reader.close()
        sys.exit(1)
    bytes_arr=[]
    seeker=0
    fibArray=[0,1]  # initiate a fibbonachi array with 0 and 1.
    while(len(sec_bytes)):
        val = fibArray[-1]+fibArray[-2] # the next fibonnachi value
        if(val == seeker):    # if it is equal to our byte number...
            fibArray.append(val) # append new value to fibArray
            try:
                in_reader.seek(seeker) # read the byte in the seeker location.
                byte=in_reader.read(1)  # read 1 byte at a time.
            except (EOFError,IOError) as e:
                print " [*] Error seeking in input file."
                print " [*] Exiting..."
                sys.exit(1)
            bits = '{0:08b}'.format(ord(byte)) # get 8 bits from image.
            ''' create new byte (8 bits) including the bit value from our secret. '''
            new_bits=str(bits[:-1])+str(sec_bytes.pop(0))
            i+=1
            bytesArr.append(new_bits)
        else:
            ''' if the  val!=seeker - append the original byte to our array. '''
            try:
                in_reader.seek(seeker)
            except (EOFError,IOError) as e:
                print " [*] Error seeking in input file."
                print " [*] Exiting..."
                sys.exit(1)
            bytesArr.append('{0:08b}'.format(ord(in_reader.read(1)))) 
        seeker+=1
    in_reader.close()
    return bytesArr

def writeNewfile(data,path):
    try:    
        out_writer = open(path,'wb')
        out_writer.write(data)
    except IOError:
        print " [*] Writing to file failed!"
    out_writer.close()

def printBanner():
    print '''
   _____  __                                         ______ _  __                                       __     _ 
  / ___/ / /_ ___   ____ _ ____   ____              / ____/(_)/ /_   ____   ____   ____   ____ _ _____ / /_   (_)
  \__ \ / __// _ \ / __ `// __ \ / __ \   ______   / /_   / // __ \ / __ \ / __ \ / __ \ / __ `// ___// __ \ / / 
 ___/ // /_ /  __// /_/ // / / // /_/ /  /_____/  / __/  / // /_/ // /_/ // / / // / / // /_/ // /__ / / / // /  
/____/ \__/ \___/ \__, //_/ /_/ \____/           /_/    /_//_.___/ \____//_/ /_//_/ /_/ \__,_/ \___//_/ /_//_/   
                 /____/                                                                                          '''

def printUsage():
    print " [#] Usage: stegno_fib.py <file in path> <image out path> <secret>"
    print "                 [*] Please Take Notice ! :"
    print " [*] the required size of the input file is linked to the lenght of the secret message."

def printArgsError():
    print " [*] stegno_fib needs exactly 3 arguments!"
    print " [*] Exiting..."

def printInvalidPathsError():
    print " [*] you must enter valid paths !"
    print " [*] Exiting..."

def checkPath(path):
    try:
        open(path, 'w')
    except IOError:
        return False
    
    return True
    
def main():
    if(len(sys.argv)!=4):
        printUsage()
        printArgsError()
        sys.exit(1)
    ## TODO: add 'encode' / 'decode' options
    printBanner()
    printUsage()
    in_path = str(sys.argv[1])
    out_path = str(sys.argv[2])
    secret = str(sys.argv[3])

    pathIsOk = (checkPath(in_path) and checkPath(out_path))
    if(pathIsOk):
        secret_bits = tobits(secret)
        new_data = decodeStegno(secret_bits,in_path)
        writeNewfile(new_data,out_path)
    else:
        printInvalidPathsError()
        sys.exit(1)
        

if(__name__ == "__main__"):
    main()

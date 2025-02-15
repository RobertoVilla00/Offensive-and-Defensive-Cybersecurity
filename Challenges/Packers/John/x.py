import sys
from pwn import u32,p32

if len(sys.argv) <4:
    print("Usage: %s <inputfile> <address> <size>" % sys.argv[0])
    exit(0)

#inputfile=./john

filepath=sys.argv[1]
address=int(sys.argv[2], 16)
size=int(sys.argv[3], 16)

BEG_BIN=0x08048000
KEY=[0x04030201, 0x40302010, 0x42303042, 0x44414544, 0xffffffff]
ff=open(filepath, "rb")
f=ff.read()
ff.close()

off=address - BEG_BIN
to_decode=f[off: off+(size*4)]
k=KEY[address % 5]

decode=b""
for i in range(size):
    decode+= p32(u32(to_decode[i*4: (i+1)*4]) ^ k)


f= f[:off]+ decode + f[off+(size*4):]

ff=open(filepath, "wb")
ff.write(f)
ff.close()




# run 'flag{packer-4o3-1337&-annoying__}'

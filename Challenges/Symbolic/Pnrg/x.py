import z3

class State:
   def __init__(self):
      self.state=[0]* 0x270
      self.index= 0

def mag(i):
   return z3.If(i==0, z3.BitVecVal(0x0,32), z3.BitVecVal(0x9908b0df,32))

def seedRand(s,i):
  s.state[0] = i & 0xffffffff
  s.index = 1
  while s.index < 0x270:
    s.state[s.index] =  (s.state[s.index -1]* 0x17b5) & 0xffffffff
    s.index = s.index + 1
  return s  




def genRandLong(s):
  if ((0x26f < s.index) or s.index < 0): 
    if ((0x270 < s.index) or s.index < 0):
         seedRand(s.state,0x1105)
    
    for local_14 in range(0xe3):
      p1=s.state[local_14 + 0x18d] 
      p2=((s.state[local_14 + 1] & 0x7fffffff | s.state[local_14] & 0x80000000)) 
      p2= z3.LShR(p2,1)
      p3=mag(s.state[local_14 + 1] & 1)
      s.state[local_14]=( p1 ^ p2 ^ p3) & 0xffffffff
    
    for local_14 in range(0xe3, 0x26f):
      p1= s.state[local_14 + -0xe3] 
      p2= ((s.state[local_14 + 1] & 0x7fffffff | s.state[local_14] & 0x80000000))
      p2=z3.LShR(p2,1)
      p3= mag(s.state[local_14 + 1] & 1)
      s.state[local_14]=( p1 ^ p2 ^ p3) & 0xffffffff
    

    p1=s.state[0x18c]
    p2=((s.state[0] & 0x7fffffff | s.state[0x26f] & 0x80000000))
    p2=z3.LShR(p2,1)
    p3= mag(s.state[0] & 1) 
    s.state[0x26f] =( p1 ^ p2 ^ p3) & 0xffffffff
    s.index = 0
  
  iVar2 = s.index
  s.index = iVar2 + 1
  uVar1 = (s.state[iVar2] ^ z3.LShR(s.state[iVar2], 0xb)) & 0xffffffff
  uVar1 = (uVar1 ^ (uVar1 << 7) & 0x9d2c5680) & 0xffffffff
  uVar1 = (uVar1 ^ (uVar1 << 0xf) & 0xefc60000) & 0xffffffff
  rand_num= (uVar1 ^ z3.LShR(uVar1, 0x12)) & 0xffffffff
  
  return s, rand_num


seed =z3.BitVec('seed',32)
s=State()
s=seedRand(s,seed)
for _ in range(0,1000):
   s,n=genRandLong(s)

s,n = genRandLong(s)

solver= z3.Solver()
solver.add(n== 0xdd29a315)

import IPython
IPython.embed()


# model.check()

# a= model.solver()

# a
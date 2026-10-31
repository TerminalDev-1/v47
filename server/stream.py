"""Bounded binary stream primitives for v47 service messages."""
import struct
class Reader:
 def __init__(self,data):self.data=memoryview(data);self.offset=0
 def take(self,n):
  if n<0 or self.offset+n>len(self.data):raise ValueError('Truncated message')
  b=self.data[self.offset:self.offset+n].tobytes();self.offset+=n;return b
 def integer(self):return struct.unpack('>i',self.take(4))[0]
 def long(self):return int.from_bytes(self.take(8),'big',signed=False)
 def string(self):
  n=self.integer()
  if n==-1:return None
  if n<0 or n>65536:raise ValueError('Invalid string length')
  return self.take(n).decode('utf8')
 def vint(self):
  first=self.take(1)[0];negative=bool(first&64);value=first&63;shift=6;byte=first
  for i in range(5):
   if not byte&128:return value-(1<<shift) if negative else value
   byte=self.take(1)[0];value|=(byte&127)<<shift;shift+=7
  raise ValueError('Invalid variable integer')
class Writer:
 def __init__(self):self.data=bytearray();self.bit=None
 def integer(self,value):self.bit=None;self.data.extend(struct.pack('>I',value&0xffffffff))
 def long(self,value):self.bit=None;self.data.extend(value.to_bytes(8,'big'))
 def string(self,value=None):
  if value is None:self.integer(-1)
  else:
   b=value.encode('utf8');self.integer(len(b));self.data.extend(b)
 def vint(self,value):
  self.bit=None;negative=value<0;b=(value&63)|(64 if negative else 0);value>>=6
  while True:
   done=value==(-1 if negative else 0);self.data.append(b|(0 if done else 128))
   if done:return
   b=value&127;value>>=7
 def boolean(self,value):
  if self.bit is None:self.data.append(0);self.bit=0
  if value:self.data[-1]|=1<<self.bit
  self.bit=(self.bit+1)%8
  if self.bit==0:self.bit=None
 def reference(self,table,row=0):
  self.vint(table)
  if table:self.vint(row)
 def bytes(self):return bytes(self.data)

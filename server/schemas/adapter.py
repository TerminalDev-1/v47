import zlib
from stream import Writer
class SchemaWriter(Writer):
 writeVInt=Writer.vint
 writeInt=Writer.integer
 writeString=Writer.string
 writeBoolean=Writer.boolean
 writeDataReference=Writer.reference
 def writeByte(self,value):self.bit=None;self.data.append(value&255)
 def writeLong(self,high,low):self.integer(high);self.integer(low)
 def writeVLong(self,high,low):self.vint(high);self.vint(low)
 def writeCompressedString(self,value):
  compressed=zlib.compress(value);self.integer(len(compressed)+4);self.bit=None;self.data.extend(len(value).to_bytes(4,'little'));self.data.extend(compressed)
class ByteStreamHelper:
 @staticmethod
 def encodeIntList(writer,values):
  writer.writeVInt(len(values))
  for value in values:writer.writeVInt(value)

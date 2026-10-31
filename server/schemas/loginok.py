# Adapted from itswester/Brawl-Stars-v47, commit 09acf78802b7faf60bc6850ed976e682741652e9.
# Original BSDS contributors; Apache License 2.0, see LICENSE-APACHE-2.0.txt.
# Modified for persistent account identity and a minimal inventory.
from .adapter import SchemaWriter, ByteStreamHelper

class LoginOk(SchemaWriter):
    def encode(self, fields, player):
            self.writeLong(player.ID[0], player.ID[1])
            self.writeLong(player.ID[0], player.ID[1])
            self.writeString(player.Token)
            self.writeString()
            self.writeString()
            self.writeInt(47)
            self.writeInt(227)
            self.writeInt(1)
            self.writeString("dev")
            self.writeInt(0)
            self.writeInt(0)
            self.writeInt(0)
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeInt(0)
            self.writeString()
            self.writeString("CA")
            self.writeString()
            self.writeInt(0)
            self.writeString()
            self.writeInt(0)
            self.writeInt(0)
            self.writeVInt(0)
            self.writeCompressedString(b'')
            self.writeBoolean(True)
            self.writeBoolean(False)
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeBoolean(False)

            self.writeBoolean(False)
            if False:
                self.writeString()

            self.writeBoolean(False)
            if False:
                self.writeString()

            self.writeBoolean(False)
            if False:
                self.writeString()

            self.writeBoolean(False)
            if False:
                self.writeString()

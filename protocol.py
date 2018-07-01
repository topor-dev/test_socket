from enum import Enum, auto

class Opcode(Enum):
    error = 0
    add = auto()
    sub = auto()
    div = auto()
    mul = auto()
    result = auto()


class Protocol:
    opcode_len = 2
    data_length_len = 2
    byteorder = 'big'

    @staticmethod
    def encode(opcode, bdata=b''):
        try:
            opcode = opcode.value.to_bytes(
                Protocol.opcode_len,
                Protocol.byteorder)
            data_length = len(bdata).to_bytes(
                Protocol.data_length_len,
                Protocol.byteorder)
        except Exception as e:
            return (False, None)
        return (True, b''.join([opcode, data_length, bdata]))

    @staticmethod
    def decode(packet):
        try:
            opcode = Opcode(
                int.from_bytes(
                    packet[0:Protocol.opcode_len], Protocol.byteorder
                    )
                )
            data_length = int.from_bytes(
                packet[Protocol.opcode_len:
                    Protocol.opcode_len + Protocol.data_length_len],
                Protocol.byteorder
                )
        except Exception:
            return (False, None)

        data = packet[Protocol.opcode_len + Protocol.data_length_len:]
        if data_length != len(data):
            return (False, None)
        return (True, (opcode, data))

    def error_packet():
        return Protocol.encode(Opcode.error)[1]
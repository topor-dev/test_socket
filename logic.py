import json
import sys

from protocol import *

signs = {
    '+': Opcode.add,
    '-': Opcode.sub,
    '*': Opcode.mul,
    '/': Opcode.div
    }


def client_logic_data_to_send():
    sign, a, b = sys.argv[2:]
    
    success, res = Protocol.encode(
        signs.get(sign, Opcode.error.value),
        json.dumps({'a': int(a), 'b': int(b)}).encode('utf-8')
        )
    
    if not success:
        print('fail while encode user data')
        raise SystemExit(1)
    return res
    
    
def server_logic(bdata):
    success, res = Protocol.decode(bdata)
    if not success:
        print('err decode')
        return Protocol.error_packet()

    opcode, data = res
    try:
        data = json.loads(data.decode('utf-8'))
    except ValueError:
        print('err json')
        return Protocol.error_packet()
    
    a, b = data.get('a', 0), data.get('b', 0)
    res = -1
    
    if opcode == Opcode.add:
        res = a + b
    if opcode == Opcode.sub:
        res = a - b
    if opcode == Opcode.mul:
        res = a * b
    if opcode == Opcode.div:
        res = a / b  # TODO: add zero division check
    
    success, res = Protocol.encode(
        Opcode.result,
        json.dumps(res).encode('utf-8')
    )
    
    if not success:
        print('err encode')
        return Protocol.error_packet()
    return res
    
    

def client_logic_retrive_data(bdata):
    success, res = Protocol.decode(bdata)
    if not success:
        print('error while parse response')
    
    opcode, data = res
    if opcode == Opcode.error:
        print('server return error')
        return
    
    print('result:', data.decode('utf-8'))
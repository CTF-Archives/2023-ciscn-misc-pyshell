import socket
import threading
import asyncio


class Service(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        

    def run(self):
        self.sock = socket.create_server(("0.0.0.0", self.port),reuse_port=True)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2)
        print("listener started")
        self.client.connect(("127.0.0.1", 12345))
        rabbish = self.client.recv(1024)
        while not rabbish.decode().strip().endswith('>>>'):
            rabbish = self.client.recv(1024)

        while True:
            ss, addr = self.sock.accept()
            print("accept a connect")
            try:
                ss.send(b'Welcome to this python shell,try to find the flag!\r\n')
                while True:
                    ss.send(b'>>')
                    msg = ss.recv(1024)

                    if not msg:
                        continue
                    elif is_validate(msg.decode().strip()):

                        self.client.send(msg)
                        total_result = bytes()
                        while True:
                            try:
                                result = self.client.recv(1024)
                                total_result += result
                                if result.decode().strip().endswith('>>>'):
                                    break
                            except:
                                break
                        
                        print(total_result)
                        if total_result.decode().strip().endswith('>>>'):
                            total_result = total_result[:-4]
                        elif total_result.decode().strip().endswith('...'):
                            self.client.send(b'\r\n')
                            while True:                            
                                result = self.client.recv(1024)
                                total_result += result
                                if result.decode().strip().endswith('>>>'):
                                    break
                            total_result = total_result[:-4]
                        else:

                            total_result = b'error\r\n'
                        
                        ss.send(total_result)
                    else:
                        ss.send(b'nop\r\n')
                        continue

            except:
                continue


def is_validate(s):
    if 'exit' in s or 'help' in s:
        return False
    if len(s) > 7:
        return False
    if '=' in s:
        return False
    return True


service = Service(9999)
service.run()
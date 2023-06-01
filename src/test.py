import socketserver
import signal
import pwn

flag = b'flag{test}'

banner = br'''
 __        ___             ____          ____            _                 
 \ \      / / |__  _   _  / ___|  ___   / ___|  ___ _ __(_) ___  _   _ ___ 
  \ \ /\ / /| '_ \| | | | \___ \ / _ \  \___ \ / _ \ '__| |/ _ \| | | / __|
   \ V  V / | | | | |_| |  ___) | (_) |  ___) |  __/ |  | | (_) | |_| \__ \
    \_/\_/  |_| |_|\__, | |____/ \___/  |____/ \___|_|  |_|\___/ \__,_|___/
                   |___/                                                                  

        CISCN 2023 Misc-Pyshell Rewriten by Randark_JMT           
'''
def is_validate(s):
    if 'exit' in s or 'help' in s:
        return False
    if len(s) > 7:
        return False
    if '=' in s:
        return False
    return True

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'>>') -> bytes:
        self.send(prompt, newline=False)
        return self._recvall()
    
    def client_init(self):
        self.client = pwn.remote("127.0.0.1",12345)
        self.client.settimeout(99999)
        rabbish = self.client.recv(1024)
        while not rabbish.decode().strip().endswith('>>>'):
            rabbish = self.client.recv(1024)
        del rabbish

    def handle(self):
        signal.alarm(30)
        self.send(banner)
        # self.send(b"\nPlease input the \"ctf\":")
        self.client_init()
        self.nulltime=0
        self.send(b'Welcome to this python shell,try to find the flag!\r\n')
        while True:
            msg = self.recv()
            print("recv:"+str(msg))
            if not msg :
                self.nulltime+=1
                if self.nulltime==30:
                    print("Nulltime == 30")
                    break
                continue
            elif is_validate(msg.decode().strip()):
                self.nulltime=0
                try:
                    self.client.sendline(msg)
                    res=self.client.recvuntil(">>>")
                except:
                    self.send(b"Session timeout!")
                print("res:"+str(res))
                self.send(res[:-4])
            else:
                self.nulltime=0
                self.send(b'nop')


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 9999
    print("HOST:POST " + HOST+":" + str(PORT))
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

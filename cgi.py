import subprocess
import shutil
import os
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
command="/usr/bin/tcc -run ./cgi-bin/table.c"
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        command=str(self.path)
     
        try:
            scn=command.split("/cgi-bin/")
            lscn=len(scn)
            if lscn>1:
                command="./cgi-bin/"+scn[1]
                cnd="./cgi-bin/"+scn[1]
                print(cnd)
                f1=open(command)
                command=f1.read()
                f1.close()
                command=command.replace("\r","\n")
                scn1=command.split("\n")
                cnd2=scn1[0]
                cnd2=cnd2.split("#")
                cndl=len(cnd2)
                print(cnd2)
                if cndl>1:
                    cnd2=cnd2[1]
                    lcnd2=cnd2.find("/")
                    if lcnd2>-1:
                        cnd2=cnd2[lcnd2:]
                    command=cnd2+" "+cnd
                    print(command)
                    result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
                else:
                    result="error\n"
                self.send_response(200)
                self.send_header("Content-type",'text/html' )
                self.end_headers()
                bs=(result).encode("utf-8")
                self.wfile.write(bs)
            
        except subprocess.CalledProcessError as e:
            if 0==0:
                
                bs=("Error executing command:\n"+e.output)
                bs=(bs).encode("utf-8")
                self.wfile.write(bs)
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()


print("\x1bc\x1b[44;37m")
if __name__ == "__main__":
    run()

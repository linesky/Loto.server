import subprocess
import shutil
import os
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
command="/usr/bin/tcc -run ./cgi-bin/table.c"
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        command=str(self.path)
        result=""
        try:
            
            scn=command.split("/cgi-bin/")
            lscn=len(scn)
            sscn=command.find(".elf")
            if sscn<0:
                sscn=command.find(".exe")
            if sscn>-1:
                result = subprocess.check_output("."+command, stderr=subprocess.STDOUT, shell=True, text=True)
            elif lscn>1:
                cnd3=scn[1].split("?")
                lcnd3=len(cnd3)
                command="./cgi-bin/"+cnd3[0]
                cnd="./cgi-bin/"+cnd3[0]
                scn4=""
                if lcnd3>1:
                    scn4=cnd3[1]
                    scn4=scn4.replace("_"," ")
                    scn4=scn4.replace("%20"," ")
                print(cnd)
                try:
                    f1=open(command)
                    command=f1.read()
                    f1.close()
                except:
                    command="error"
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
                    command=cnd2+" "+cnd+" "+scn4


                        
                    print(command)
                    result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
                else:
                    result="error\n"
            else:
                if command=="/":
                    command="."+command+"index.html"
                else:
                    command="."+command
                try:
                    f1=open(command)
                    result=f1.read()
                    f1.close()    
                except:
                    result="error"
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

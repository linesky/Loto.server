import subprocess
import shutil
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
command="/usr/bin/tcc -run ./cgi-bin/table.c"
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.send_response(200)
            self.send_header("Content-type",'text/html' )
            self.end_headers()
            bs=(result).encode("utf-8")
            self.wfile.write(bs)
        except subprocess.CalledProcessError as e:
            if 0==0:
                #self.send_header(
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

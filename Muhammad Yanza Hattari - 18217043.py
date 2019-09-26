
# coding: utf-8

# In[16]:


from http.server import HTTPServer, SimpleHTTPRequestHandler

port= 8100
with HTTPServer(("",port), SimpleHTTPRequestHandler) as httpd:
    print("working in ",port)
    httpd.serve_forever()


# In[ ]:


from http.server import HTTPServer, SimpleHTTPRequestHandler
import base64
import http.server
import ssl

userName="admin"
password="12345"
authkey = userName+":"+password
authkey_b64 = "Basic " + str(base64.b64encode(authkey.encode("utf-8")),"utf-8")


class HTTPNewHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate','Basic realm=\"Test\"')
        self.send_header('Content-type','text/html')
        self.end_headers()
        
    def do_GET(self):
        if self.headers.get("authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(b"ga ada authorization")
            pass
            
        elif self.headers.get("authorization") == authkey_b64:
            return SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(b"salah password")
            pass

port= 1234
with http.server.HTTPServer(("",port), HTTPNewHandler) as httpd:
    print("jalan woe",port)
    httpd.socket = ssl.wrap_socket(httpd.socket,keyfile="key.pem",certfile="certificate.pem",server_side=True)
    httpd.serve_forever()


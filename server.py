#  coding: utf-8 
import SocketServer
import os

# Copyright 2013 Raman Dhatt, Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        requests = self.data.splitlines() # ex: ['GET / HTTP/1.1', 'User-Agent: curl/7.35.0', 'Host: 127.0.0.1:8080', 'Accept: */*']
        request = requests[0].split() # ex: 'GET / HTTP/1.1'
        requestType = request[0]
        requestedFile = request[1]
        print ("Got the following request: %s\n" % self.data)
        
        # Make sure only the GET request is allowed.
        if (requestType != "GET"):
            response_headers = self.generate_headers(501)
            self.request.sendall(response_headers)
            
        else:
            try:

                if requestedFile.endswith("deep"):
                    requestedFile += "/"
                elif requestedFile == "/deep.css":
                    requestedFile = "/deep/" + requestedFile

                # if no file is given, re-direct to index.html
                if requestedFile.endswith("/"):
                    requestedFile += "index.html"
                    print(self.generate_headers(301) + "\nLocation: " + requestedFile + "\r\n")
                    
                # Read the requested file
                read_file = open("www/" + requestedFile, 'r')
                msg = ""
                for line in read_file:
                    msg += line
                
                mimeType = ""
		
                if requestedFile.endswith(".html"):
                    mimeType = 'text/html'
                elif requestedFile.endswith(".css"):
                    mimeType = 'text/css'
                else:
                    raise Exception
               
                # send information, including content type so that css works in browser.
                self.request.sendall(self.generate_headers(200))
                self.request.sendall("Content-Type: " + mimeType + "\r\n")
                self.request.sendall("Content-Length: " + str(len(msg)) + "\r\n\r\n")
                self.request.sendall(msg  + "\r\n\r\n")
            
            except:
                # If requested file doesn't exist or unsupported file type, throw 404 exception code
                self.request.sendall(self.generate_headers(404))
                
        self.request.close()
        
    def generate_headers(self, code):
        # generate header depending on the response code 
        h = ''
        if (code == 200):
            h = "HTTP/1.1 200 OK\r\n"
    	elif (code == 301):
            h = "HTTP/1.1 301 MOVED PERMANENTLY"
        elif (code == 404):
            h = "HTTP/1.1 404 NOT FOUND\r\n\r\n<html><body><h1>Error 404: NOT FOUND</h1> \
                <p>File not found.</p></body></html>\r\n\r\n"
        elif (code == 415):
            h = ("HTTP/1.1 415 UNSUPPORTED MEDIA TYPE\r\n" +
                 "Only .html and .css files are supported.\r\n\r\n")
        elif (code == 501):
            h = ("HTTP/1.1 501 METHOD NOT IMPLEMENTED\r\n" +
                 "Content-type: text/html\r\n" +
                 "Only the GET request is supported.\r\n\r\n")
        return h
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)
    print ("Starting server on port 8080. To stop the program, do Ctrl-C.")

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import random
import subprocess
import json

class BtcBtn:
    def __init__(self):
        class RequestHandler (BaseHTTPRequestHandler):
            def do_GET(req):
                for route, method in self.routes:
                    m = re.match(route, req.path)
                    if m and method(req, *m.groups()) == None:
                        break

        self.bitcoin_path = 'bitcoin'
        self.style = open("style.css").read()
        self.HTTPServer = HTTPServer
        self.RequestHandler = RequestHandler
        self.routes = [
            ("/donate/(\d+(.\d+)?)BTC/([0-9a-zA-Z]+)", self.http_donate),
            ("/confirm/(.+)", self.http_confirm),
            (".*", self.not_found)
        ]
        self.views = {
            'donate': 'donate.html',
            'confirm': 'confirm.html'
        }
        self.views = dict((k, open(v).read()) for k, v in self.views.items())
        self.to_confirm = {}
        self.model = { 'style': self.style }

    def http_confirm(self, req, code):
        if code not in self.to_confirm:
            return self.not_found(req)
        model = self.to_confirm[code]
        model['answer'] = self.btc_donate(**model)
        self.ok(req, self.render('confirm', model))

    def http_donate(self, req, amount, _, address):
        if req.client_address[0] != '127.0.0.1':
            return self.access_denied(req)
        token = self.new_token()
        model = {
            'amount': str(float(amount)),
            'address': address,
            'referer': req.headers.get('referer', 'unknown'),
            'token': token,
            'balance': self.btc_balance()
        }
        self.to_confirm[token] = model
        self.ok(req, self.render('donate', model))

    def btc_donate(self, **model):
        cmd = '{0} sendtoaddress {address} {amount} "btcbtn {referer}"'
        cmd = cmd.format(self.bitcoin_path, **model)
        output = subprocess.getoutput(cmd)
        try:
            x = output[output.index('{'):]
            return json.loads(x)['message']
        except:
            return output

    def btc_balance(self):
        cmd = '{0} getbalance'
        cmd = cmd.format(self.bitcoin_path)
        return str(float(subprocess.getoutput(cmd)))

    def new_token(self):
        while 1:
            token = str(random())
            if token not in self.to_confirm:
                return token

    def render(self, view, model):
        model = model.copy()
        model.update(self.model)
        return bytes(self.views[view].format(**model), 'utf-8')

    def ok(self, req, content):
        req.send_response(200)
        req.send_header('Content-Type', 'text/html')
        req.send_header('charset', 'utf-8')
        req.end_headers()
        req.wfile.write(content)

    def access_denied(self, req):
        req.send_error(403)

    def not_found(self, req):
        req.send_error(404)

    def run(self):
        server_address = ('127.0.0.1', 8170)
        httpd = HTTPServer(server_address, self.RequestHandler)
        httpd.serve_forever()

def main():
    try:
        btcbtn = BtcBtn()
        btcbtn.run()
    except KeyboardInterrupt:
        print('\nthanks for useing bitcoins and bitcoin button')

if __name__ == '__main__': main()


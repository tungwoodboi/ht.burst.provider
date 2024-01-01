from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
from lib.torrentio import torrentio

# HOST = "localhost"
PORT = 8989
class HTHTTP(BaseHTTPRequestHandler):
  
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        path = self.path
        parse_path = urlparse(path)
        queries = parse_qs(parse_path.query)

        if not 'proxyUrl' in queries:
            self.wfile.write(bytes('No proxy url specified', "utf-8"))
        else:
            proxyUrl = queries['proxyUrl'][0]
            try:
                response = requests.get(proxyUrl)
                body = response.text
                response.raise_for_status()

                if 'https://torrentio.strem.fun/' in proxyUrl:
                    body = torrentio(body)

                self.wfile.write(bytes(body, "utf-8"))
            except requests.exceptions.HTTPError as errh:
                self.wfile.write(bytes(f"Http Error: {errh}", "utf-8"))
            except requests.exceptions.ConnectionError as errc:
                self.wfile.write(bytes(f"Error Connecting: {errc}", "utf-8"))
            except requests.exceptions.Timeout as errt:
                self.wfile.write(bytes(f"Timeout Error: {errt}", "utf-8"))
            except requests.exceptions.RequestException as err:
               self.wfile.write(bytes(f"Error: {err}", "utf-8"))

        # self.wfile.write(bytes("<html><body><h1>Hello, World!</h1></body></html>", "utf-8"))

server = HTTPServer(("", PORT), HTHTTP)
server.serve_forever()
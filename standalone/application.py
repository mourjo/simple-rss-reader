# coding: utf-8
# __author__ = 'Mourjo'
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import xml.dom.minidom, urllib, re, string

class RequestHandler(BaseHTTPRequestHandler):
    is_url = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def _writeheaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._writeheaders()

    def do_GET(self):
        self._writeheaders()
        try:
            if self.path.find('?') != -1:
                 self.path, self.query_string = self.path.split('?', 1)
            else:
                 self.query_string = ''

            self.wfile.write('<!DOCTYPE html><html lang="en"><head>\n<link rel="stylesheet" '
                             'href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">\n'
                             '<link href="http://fonts.googleapis.com/css?family=Roboto" '
                             'rel="stylesheet" type="text/css"><title>Simple RSS Reader</title></head><body>'
                             '<div class="container" style="font-family:'
                             ' \'Roboto\', sans-serif;">')

            self.wfile.write('''<header style="background-color:#002E5C;" class="jumbotron subhead" id="overview">
                <div class="container" style="color:white;"><h1 style="text-align:center;">Simple RSS Reader</h1>
                <h4 style="text-align:center;">By <a target='blank' href='https://github.com/mourjo'>Mourjo Sen</a>
                </h4></div></header>''')

            resp = urllib.unquote(self.query_string).decode('utf8')[2:]

            if RequestHandler.is_url.match(resp):
                self.wfile.write('<form><div class="row"><div class="col-lg-12"><div class="input-group">'
                                 '<input type="text" class="form-control" name="q" value="'+resp
                                 + '""><span class="input-group-btn"><button type="submit" '
                                  'class="btn btn-default">Go!</button></span></div></div>'
                                  '</div><!-- /.row --></form><br>')

                document_dom = xml.dom.minidom.parse(urllib.urlopen(resp))
                items = document_dom.documentElement.getElementsByTagName("item")

                for item in items:

                    links = item.getElementsByTagName("link")
                    titles = item.getElementsByTagName("title")
                    descriptions = item.getElementsByTagName("description")

                    if len(links) > 0 and len(titles) > 0 and len(descriptions) > 0:
                        s = "<div class='well'><a style='font-size:18pt' target='blank' href="\
                            +links[0].childNodes[0].data+">"+titles[0].childNodes[0].data+\
                            "</a><br>"+descriptions[0].childNodes[0].data+"</div>"

                        self.wfile.write(filter(lambda x: x in string.printable, s))
            else:

                self.wfile.write('''<form><div class="row"><div class="col-lg-12"><div class="input-group">
                    <input type="text" class="form-control" name="q" placeholder="Enter a valid RSS URL">
                    <span class="input-group-btn"><button type="submit" class="btn btn-default">Go!
                    </button></span></div></div></div><br>''')

            self.wfile.write("</div></body></html>")

        except:
            self.wfile.write("""<div class='well'>RSS feed unavailable. Please try again later.</div></div></body>
            </html>""")

serveraddr = ('',8012)
srvr = HTTPServer(serveraddr, RequestHandler)
srvr.serve_forever()
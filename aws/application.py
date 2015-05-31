import logging
import logging.handlers
import xml.dom.minidom, re, urllib.parse, urllib.request
# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/var/log/uwsgi/sample-app.log' # /var/log/uwsgi is the default log path for Docker preconfigured python containers
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)


def generate_html(path):
    html_out = ''
    is_url = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    try:
        html_out += '<!DOCTYPE html><html lang="en"><head>\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">\n<link href="http://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css"><title>Simple RSS Reader</title></head><body "style=\'overflow-y:scroll;\'"> <div class="container" style="font-family:\'Roboto\', sans-serif;">'
        html_out += '<header style="background-color:#002E5C;" class="jumbotron subhead" id="overview"><div class="container" style="color:white;"><h1 style="text-align:center;">Simple RSS Reader</h1><h4 style="text-align:center;">By <a target="blank" href="https://github.com/mourjo">Mourjo Sen</a></h4></div></header>'
        
        resp = ''
        if path is not None:
            if len(path) != 0:
                resp = urllib.parse.unquote(path)[2:]

        if resp != '' and is_url.match(resp):
            html_out += '<form><div class="row"><div class="col-lg-12"><div class="input-group"><input type="text" class="form-control" name="q" value="'+resp+ '""><span class="input-group-btn"><button type="submit" class="btn btn-default">Go!</button></span></div></div></div><!-- /.row --></form><br>'
            document_dom = xml.dom.minidom.parse(urllib.request.urlopen(resp))
            items = document_dom.documentElement.getElementsByTagName("item")
            
            for item in items:
                links = item.getElementsByTagName("link")
                titles = item.getElementsByTagName("title")
                descriptions = item.getElementsByTagName("description")
                
                if len(links) > 0 and len(titles) > 0 and len(descriptions) > 0:
                    html_out += '<div class="well"><a style="font-size:18pt" target="blank" href='+links[0].childNodes[0].data+'>'+titles[0].childNodes[0].data+'</a><br>'+descriptions[0].childNodes[0].data+'</div>'
                elif len(links) > 0 and len(titles) > 0:
                    html_out += '<div class="well"><a style="font-size:18pt" target="blank" href='+links[0].childNodes[0].data+'>'+titles[0].childNodes[0].data+'</a></div>'
        
        else:

            html_out += '<form><div class="row"><div class="col-lg-12"><div class="input-group"><input type="text" class="form-control" name="q" placeholder="Enter a valid RSS URL"><span class="input-group-btn"><button type="submit" class="btn btn-default">Go!</button></span></div></div></div><br>'

        html_out += '</div></body></html>'
        return html_out

    except Exception as e:
        html_out += '<div class="well">RSS feed unavailable. Please try again later.</div></div></body></html>'
        return html_out

def application(environ, start_response):
    response = generate_html(environ['QUERY_STRING'])
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [response.encode('utf-8')]

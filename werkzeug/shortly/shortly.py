import os
import redis
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

def is_valid_url(url):
    parts = urlparse.urlparse(url)
    return parts.scheme in ('http', 'https')

def base36_encode(number):
    assert number >= 0, 'positive integer required'
    if number == 0:
        return '0'
    base36 = []
    while number != 0:
        number, i = divmod(number, 36)
        base36.append('0123456789abcdefghijklmnopqrstuvwxyz'[i])
    return ''.join(reversed(base36))

class Shortly(object):

    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])

        #import pdb; pdb.set_trace()

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                 autoescape=True)
        self.url_map = Map([
                            Rule('/', endpoint='new_url'),
                            Rule('/<short_id>', endpoint='follow_short_link'),
                            Rule('/<short_id>+', endpoint='short_link_details')
                          ])

    def render_template(self, template_name, **context):
        #import pdb; pdb.set_trace()
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def on_new_url(self, request):
        # Archana: 
        #i)GET Control comes here when we type the ip:port on brwsr
        #ii)POST Control comes here when we type a url in the box
        error = None
        url = ''
        if request.method == 'POST':
            # ii) POST
            url = request.form['url']
        if not is_valid_url(url):
            # i) GET
            error = 'Please enter a valid URL'
        else:
            # ii) POST
            #import pdb; pdb.set_trace()
            short_id = self.insert_url(url)
            return redirect('/%s+' % short_id)
        return self.render_template('new_url.html', error=error, url=url)

    def on_follow_short_link(self, request, short_id):

        #Archana: changed code temporarily to test get
        #Archana: when I explicitly put xyz as arg and set this key 
        #in redis-cli to point to http://www.google.com it works
        #redis-cli>> set xyz http://www.google.com 
        #link_target = self.redis.get('xyz')

        #for browser input 192.168.33.10:5003/foo ...
        #if you populate at redis-cli> set url-target:foo http://www.cnn.com
        # it finds the link for cnn and redirects

        #import pdb; pdb.set_trace()
        link_target = self.redis.get('url-target:' + short_id)
        if link_target is None:
            raise NotFound()
        self.redis.incr('click-count:' + short_id)
        return redirect(link_target)

    def on_short_link_details(self, request, short_id):
        #Archana:
        # Once we post a url to shorten in the box, control comes
        # to ii) and then it sends a 200OK back with redirect details
        # and short id like 192.168.33.10:5003/g+ so 'g' is the new
        # short id that it calculated/mapped and then now, the client
        # HTTP sends another GET (after POST) with the new short id 
        # link ... details for that are populated here where it gives
        # back all information in another 200 OK with stuff like 

        #import pdb; pdb.set_trace()
        link_target = self.redis.get('url-target:'+short_id)
        if link_target is None:
            raise Notfound()
        click_count = int(self.redis.get('click-count'+short_id) or 0)
        return self.render_template('short_link_details.html',
                link_target=link_target,
                short_id=short_id,
                click_count=click_count
                )

    def insert_url(self, url):
        short_id = self.redis.get('reverse-url:' + url)
        if short_id is not None:
            return short_id
        url_num = self.redis.incr('last-url-id')
        short_id = base36_encode(url_num)
        self.redis.set('url-target:' + short_id, url)
        self.redis.set('reverse-url:' + url, short_id)
        return short_id


    def dispatch_request(self, request):
        #import pdb; pdb.set_trace()
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        import pdb; pdb.set_trace()
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = Shortly({
        'redis_host':       redis_host,
        'redis_port':       redis_port
    })#Shortly class init fn called here 

    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })# This is where it gets in wsgi.py module in werkzeug
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    #import pdb; pdb.set_trace()
    run_simple('192.168.33.10', 5003, app, use_debugger=True, use_reloader=True)

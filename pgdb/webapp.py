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

class GroceryApp(object):

    def __init__(self):
#        self.db_hndl = dbcur
        self.order = False
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                 autoescape=True)
        self.url_map = Map([
                            Rule('/', endpoint='new_cust'),
                            Rule('/<short_id>', endpoint='follow_short_link'),
                            Rule('/<short_id>+', endpoint='short_link_details')
                          ])

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        #import pdb; pdb.set_trace()
        return Response(t.render(context), mimetype='text/html')

    def on_new_cust(self, request):
        error = None
        #import pdb; pdb.set_trace()
        url = request.url
        print request.headers
        if request.method == 'GET':
            # i) GET
            gl = ["Mangoes", "Onions", "Potatoes"]
            print "From GET method"
            template_filename='list_db.html'
        if request.method == 'POST':
            # ii) POST
            #item_list is specified as input_name for checbox control in 
            #the rendering template file. It is the name of the input received

            if self.order == False:
                #Customer has filled an order cart
                #Werkzeug allows you to get the multidict values from this fn
                gl=request.form.getlist('item_list') 

                #get session id from cookie in req header
                Cust_info = request.headers.get('Cookie')
                key,eqls,session_id=Cust_info.rpartition('=')

                #get price order from database
                qty = 1
                price = 3
                total = price*(len(gl))

                print "From POST method the items received:\n"
                for item in gl:
                    print item
                print "\n"
                template_filename='list_order.html'
                self.order = True
                return self.render_template(template_filename, 
                                  grocery_list=gl, qty=qty, price=price, total=total)
            else:
                #Customer has confirmed order or canceled
                gl=request.form.getlist('item_list') 
                if "Place Order" in gl:
                    template_filename='order_complete.html'
                else:
                    template_filename='order_cancel.html'
        return self.render_template(template_filename, grocery_list=gl)
# Expecting keyword args to form dict

    def on_follow_short_link(self, request, short_id):

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

        #generate session id for each customer
        session_id='123456'
        response.set_cookie('session_id',session_id, expires='Tue')
        response.set_cookie('newid','abche78',expires='Thu')
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    #import pdb; pdb.set_trace()
    app = GroceryApp()

    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    #import pdb; pdb.set_trace()
    run_simple('192.168.33.10', 5004, app, use_debugger=True, use_reloader=True)

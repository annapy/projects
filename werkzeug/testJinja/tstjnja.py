import os
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

var = 100
list = [1, 2, 3]

def print_html_doc():
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print j2_env.get_template('chldJnj2.html').render(
                              title='Hellow Gist from GutHub',
                              var = var,
                              list = list
                                           )
if __name__ == '__main__':
    print_html_doc()

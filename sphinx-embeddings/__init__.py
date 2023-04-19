from docutils import nodes
from hashlib import md5
from json import dumps
import tiktoken

encoding = tiktoken.encoding_for_model('gpt-4')
data = {}

def estimate_token_count(text):
    return len(encoding.encode(text))

def generate_embeddings(app, doctree, docname):
    data[docname] = {}
    for section in doctree.traverse(nodes.section):
        text = section.astext()
        checksum = md5(text.encode('utf-8')).hexdigest()
        data[docname][checksum] = {
            'text': text,
            'tokens': estimate_token_count(text)
        }
    print(data)

def setup(app):
    app.connect('doctree-resolved', generate_embeddings)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

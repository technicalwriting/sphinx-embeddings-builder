from sphinx.builders import Builder
from sphinx.locale import __
from hashlib import md5
from tiktoken import get_encoding
from sphinx.util.osutil import ensuredir
from os import path

class EmbeddingsBuilder(Builder):
    name = 'embeddings'
    format = 'json'
    epilog = __('TODO')

    def init(self):
        self['data'] = {}
        # TODO: This should be a configurable value.
        # def count(text):
        #     return len(get_encoding('cl100k_base').encode(text))
        # self['count_tokens'] = lambda text: count(text)

    def get_outdated_docs(self):
        return self.env.all_docs

    def get_target_uri(self, docname, typ=None):
        return docname

    def write_doc(self, docname, doctree):
        text = section.astext()
        self['data'][docname] = {
            # 'tokens': self['count_tokens'](text),
            'checksum': md5(text.encode('utf-8')).hexdigest()
        }

    def finish(self):
        outdir = path.join(self.outdir, 'embeddings')
        ensuredir(outdir)
        with open(path.join(outdir, 'embeddings.json'), 'w') as f:
            json.dump(self['data'], f, indent=2)
        


# from docutils import nodes
# from hashlib import md5
# from json import dumps
# import tiktoken
# 
# encoding = tiktoken.encoding_for_model('gpt-4')
# data = {}
# 
# def estimate_token_count(text):
#     return len(encoding.encode(text))
# 
# def generate_embeddings(app, doctree, docname):
#     data[docname] = {}
#     for section in doctree.traverse(nodes.section):
#         text = section.astext()
#         checksum = md5(text.encode('utf-8')).hexdigest()
#         data[docname][checksum] = {
#             'text': text,
#             'tokens': estimate_token_count(text)
#         }
#     print(data)
# 
# def setup(app):
#     app.connect('doctree-resolved', generate_embeddings)
#     return {
#         'version': '0.1',
#         'parallel_read_safe': True,
#         'parallel_write_safe': True,
#     }

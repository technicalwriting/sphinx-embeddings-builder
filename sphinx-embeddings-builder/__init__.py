from sphinx.builders import Builder
from sphinx.locale import __
from hashlib import md5
from tiktoken import get_encoding
from sphinx.util.osutil import ensuredir
from os import path
from json import dump
from docutils.nodes import section as section_node

__version__ = '0.0.1'

class EmbeddingsBuilder(Builder):
    name = 'embeddings'
    format = 'json'
    epilog = __('TODO')

    def init(self):
        self.data = {}
        self.dir = path.join(self.outdir, 'embeddings')
        # TODO: This should be a configurable value.
        self.count_tokens = lambda text: len(get_encoding('cl100k_base').encode(text))

    def get_outdated_docs(self):
        return self.env.all_docs

    def get_target_uri(self, docname, typ=None):
        return docname

    def prepare_writing(self, docnames):
        ensuredir(self.dir)

    def write_doc(self, docname, doctree):
        self.data[docname] = {}
        for section in doctree.traverse(section_node):
            text = section.astext()
            # Checksum should be generated before any modifications are made to the section.
            checksum = md5(text.encode('utf-8')).hexdigest()
            tokens = self.count_tokens(text)
            # TODO: Add a config value for maximum token threshold and skip any sections that
            # are larger than the threshold.
            self.data[docname][checksum] = {
                'tokens': self.count_tokens(text)
            }
        # self.data[docname] = {
        #     # 'tokens': self.count_tokens(text),
        #     'checksum': md5(text.encode('utf-8')).hexdigest()
        # }

    def finish(self):
        data_path = path.join(self.dir, 'embeddings.json')
        with open(data_path, 'w') as f:
            dump(self.data, f, indent=2)

def setup(app):
    app.add_builder(EmbeddingsBuilder)
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


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

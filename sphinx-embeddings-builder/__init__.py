from sphinx.builders import Builder
from sphinx.locale import __
from hashlib import md5
from tiktoken import get_encoding
from sphinx.util.osutil import ensuredir
from os import path
from json import dump
from docutils.nodes import section as section_node
from logging import info
import openai

__version__ = '0.0.1'

class EmbeddingsBuilder(Builder):
    name = 'embeddings'
    format = 'json'
    epilog = __('TODO')

    def init(self):
        self.data = {}
        # TODO: This should be a configurable value.
        self.count_tokens = lambda text: len(get_encoding('cl100k_base').encode(text))
        openai.api_key = 'TODO'
        # TODO: This should be a configurable value.
        def gen(text):
            model = 'text-embedding-ada-002'
            data = openai.Embedding.create(input=text, model=model)
            return data['data'][0]['embedding']
        self.generate_embedding = gen

    def get_outdated_docs(self):
        return self.env.all_docs

    def get_target_uri(self, docname, typ=None):
        return docname

    def prepare_writing(self, docnames):
        pass

    def write_doc(self, docname, doctree):
        self.data[docname] = {}
        for section in doctree.traverse(section_node):
            text = section.astext()
            # Checksum should be generated before any modifications are made to the section.
            checksum = md5(text.encode('utf-8')).hexdigest()
            tokens = self.count_tokens(text)
            if tokens > self.config.sphinx_embeddings_builder_max_tokens:
                continue
            self.data[docname][checksum] = {
                'tokens': self.count_tokens(text),
                'text': text,
                'embedding': self.generate_embedding(text)
            }

    def finish(self):
        data_path = path.join(self.outdir, 'embeddings.json')
        with open(data_path, 'w') as f:
            dump(self.data, f, indent=2)
        info(data_path)

def setup(app):
    app.add_builder(EmbeddingsBuilder)
    # https://platform.openai.com/docs/guides/embeddings/embedding-models
    text_embedding_ada_002_max_tokens = 8191
    app.add_config_value('sphinx_embeddings_builder_max_tokens', text_embedding_ada_002_max_tokens, 'env')
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

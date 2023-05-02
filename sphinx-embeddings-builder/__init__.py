from sphinx.builders import Builder
from sphinx.locale import __
from hashlib import md5
from tiktoken import get_encoding
from sphinx.util.osutil import ensuredir
from os import path
from json import dump
from docutils.nodes import section as section_node
import openai

__version__ = '0.0.1'

class EmbeddingsBuilder(Builder):
    name = 'embeddings'
    format = 'json'

    def init(self):
        self.data = {}
        # self.count = self.config.sphinx_embeddings_builder_count_tokens
        self.count = lambda text: 5
        self.generate = lambda text: [1, 2, 3, 4, 5]
        self.max_tokens = 100
        # openai.api_key = 'TODO'
        # def gen(text):
        #     model = 'text-embedding-ada-002'
        #     data = openai.Embedding.create(input=text, model=model)
        #     return data['data'][0]['embedding']
        # self.generate = self.config.sphinx_embeddings_builder_generate_embedding

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
            tokens = self.count(text)
            if tokens > self.max_tokens:
                continue
            self.data[docname][checksum] = {
                'tokens': tokens,
                'text': text,
                'embedding': self.generate(text)
            }

    def finish(self):
        data_path = path.join(self.outdir, 'embeddings.json')
        with open(data_path, 'w') as f:
            dump(self.data, f, indent=2)

def setup(app):
    app.add_builder(EmbeddingsBuilder)
    # Defaults to max token size for text-embedding-ada-002
    # https://platform.openai.com/docs/guides/embeddings/embedding-models
    # max_tokens = 8191
    # app.add_config_value('sphinx_embeddings_builder_max_tokens', max_tokens, 'env')
    # count_tokens = lambda text: len(get_encoding('cl100k_base').encode(text))
    # app.add_config_value('sphinx_embeddings_builder_count_tokens', count_tokens, 'env')
    # generate_embedding = lambda text: [1, 2, 3, 4, 5]
    # app.add_config_value('sphinx_embeddings_builder_generate_embedding', generate_embedding, 'env')
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

from sphinx.builders import Builder
from hashlib import md5
from os import path
from json import dump
from docutils.nodes import section as section_node

__version__ = '0.0.6'

class EmbeddingsBuilder(Builder):
    name = 'embeddings'
    format = 'json'

    def init(self):
        self.data = {}
        self.count = self.config.sphinx_embeddings_builder_count_tokens
        self.generate = self.config.sphinx_embeddings_builder_generate_embedding
        self.max_tokens = self.config.sphinx_embeddings_builder_max_tokens

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
            if tokens is None:
                continue
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
    app.add_config_value('sphinx_embeddings_builder_count_tokens', None, 'env')
    app.add_config_value('sphinx_embeddings_builder_max_tokens', None, 'env')
    app.add_config_value('sphinx_embeddings_builder_generate_embedding', None, 'env')
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

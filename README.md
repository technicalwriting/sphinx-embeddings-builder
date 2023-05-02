# sphinx-embeddings-builder

A [Sphinx Builder] for generating [embeddings].

## Get started

Install the package:

```
pip install sphinx-embeddings-builder
```

Update `conf.py` in your Sphinx project:

```py
extensions = [
    # ...
    'sphinx-embeddings-builder
]

sphinx_embeddings_builder_max_tokens = my_max_token_size
sphinx_embeddings_builder_count_tokens = my_token_counting_function
sphinx_embeddings_builder_generate_embedding = my_embedding_generation_function
```

**All of the configuration variables are required.** See [Examples] to learn how
to set them up with different generative AI services.

<h2 id="examples">Examples</h2>

### Google

```py
import google.generativeai as palm

# ...

extensions = [
    # ...
    'sphinx-embeddings-builder'
]

# ...

palm_api_endpoint = '...'
palm_model = 'models/embedding-gecko-001'
palm_api_key = '...' # Load from a secure environment variable. 
                     # Don't leak your key!
palm_client_options = {
    'api_endpoint': palm_api_endpoint
}

palm.configure(api_key=palm_api_key, client_options=palm_client_options)

sphinx_embeddings_builder_max_tokens = 1024 # embedding-gecko-001's limit

def count(text):
    try:
        response = palm.count_message_tokens(prompt=text)
        return response['token_count']
    except Exception as e:
        return None
sphinx_embeddings_builder_count_tokens = count

def gen(text):
    try:
        response = palm.generate_embeddings(model=palm_model, text=text)
        return response['embedding']
    except Exception as e:
        return None
sphinx_embeddings_builder_generate_embedding = gen

# ...
```

### OpenAI

```py
from tiktoken import get_encoding
from openai import key as openai_key, Embedding

# ...

extensions = [
    # ...
    'sphinx-embeddings-builder'
]

# ...

openai_key = '...' # Load from a secure environment variable.
                   # Don't leak your key!

sphinx_embeddings_builder_max_tokens = 8191

sphinx_embeddings_builder_count_tokens = lambda text: len(get_encoding('cl100k_base').encode(text))

def gen(text):
    response = Embedding.create(input=text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']
sphinx_embeddings_builder_generate_embedding = gen

# ...
```

## Architecture

### Data schema

```
{
    "<docname>": {
        "<checksum>": {
            "tokens": "<int>",
            "text": "<string>",
            "embeddings": "<array of floats>"
        }
    }
}
```

### How pages are processed

Pages are processed on a per-section basis. Sections are processed recursively.
For example, given the following pseudo-XML document:

```
<document>
    <section id="section1">
        <title>Title 1</title>
        <paragraph>Paragraph 1</paragraph>
        <section id="section2">
            <title>Title 2</title>
            <paragraph>Paragraph 2</paragraph>
        </section>
    </section>
    <section id="section3">
        <title>Title 3</title>
        <paragraph>Paragraph 3</paragraph>
        <section id="section4">
            <title>Title 4</title>
            <paragraph>Paragraph 4</paragraph>
        </section>
    </section>
</document>
```

You'll get embeddings for:

1. The entire document.
2. Everything within `section1`.
3. Everything within `section2`.
4. Everything within `section3`.
5. Everything within `section4`.

Note that the content of lower-level sections will "show up" in
multiple embeddings. In the example above, embeddings #1-3 would
have the `section2` content "in them".

[Sphinx Builder]: https://www.sphinx-doc.org/en/master/usage/builders/index.html
[embeddings]: https://en.wikipedia.org/wiki/Word_embedding
[Examples]: #examples

# sphinx-embeddings-builder

A [Sphinx Builder] for generating [embeddings].

## Get started

Install the package:

```
pip install sphinx-embeddings-builder
```

Update `conf.py` in your Sphinx project:

```
extensions = [
    # ...
    'sphinx-embeddings-builder
]

# All config values are required.
sphinx_embeddings_builder_max_tokens = my_max_token_size
sphinx_embeddings_builder_count_tokens = my_token_counting_function
sphinx_embeddings_builder_generate_embedding = my_embedding_generation_function
```

## Examples

### OpenAI

```
from tiktoken import get_encoding
from openai import key as openai_key, Embedding

# ...

extensions = [
    # ...
    'sphinx-embeddings-builder'
]

# ...

sphinx_embeddings_builder_max_tokens = 8191
sphinx_embeddings_builder_count_tokens = lambda text: len(get_encoding('cl100k_base').encode(text))
def gen(text):
    openai_key = '...'
    response = Embedding.create(input=text, model='text-embedding-ada-002')
    return data['data'][0]['embedding']
sphinx_embeddings_builder_generate_embedding = gen
```


## Notes

* Embedding stats for https://sphinx-doc.org
  * Complete generation took 3m17s
  * Ignored sections with token size greater than 8191 (since text-embedding-ada-002 can't handle more than that)
  * `embeddings.json` file is ~43MB

## Features

* Configurable token limits

## Architecture

### Data "schema"

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

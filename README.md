# sphinx-embeddings-builder

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

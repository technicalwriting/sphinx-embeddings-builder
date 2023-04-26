from json import load

data_file_path = '/tmp/sphinx/build/sphinx/embeddings/embeddings.json'

with open(data_file_path, 'r') as f:
    data = load(f)

count = 0
for docname in data:
    for checksum in data[docname]:
        count += data[docname][checksum]['tokens']

print('Token count: {}'.format(count))

cost = (count / 1000) * 0.0004

print('Cost: {}'.format(cost))

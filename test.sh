name=seb
dir=/tmp/$name
conf=$dir/conf.py
wd=$(pwd)

if [ ! -d "venv" ]; then
  python3 -m venv venv
  python3 -m pip install -r requirements.txt
fi

source venv/bin/activate

if [ -d "$dir" ]; then
  rm -rf $dir
fi

echo "setting up $dir"
sphinx-quickstart --project=$name --author=$name --quiet $dir
hacks='import os
import sys
from tiktoken import get_encoding
sys.path.append(os.path.abspath("./ext"))
extensions = ["sphinx-embeddings-builder"]
exclude_patterns = ["ext/venv"]
sphinx_embeddings_builder_count_tokens = lambda text: len(get_encoding("cl100k_base").encode(text))
sphinx_embeddings_builder_generate_embedding = lambda text: [3, 0, 9]
sphinx_embeddings_builder_max_tokens = 100'
echo "$hacks" >> $conf

mkdir $dir/ext
cd ..
cp -r sphinx-embeddings-builder/* $dir/ext/

cd $dir
make embeddings

cd $wd
deactivate

cat $dir/_build/embeddings/embeddings.json

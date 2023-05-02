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
echo "import os" >> $conf
echo "import sys" >> $conf
echo "sys.path.append(os.path.abspath('./ext'))" >> $conf
echo "extensions = ['sphinx-embeddings-builder']" >> $conf
echo "exclude_patterns = ['ext/venv']" >> $conf

mkdir $dir/ext
cd ..
cp -r sphinx-embeddings-builder/* $dir/ext/

cd $dir
make embeddings

cd $wd
deactivate

cat $dir/_build/embeddings/embeddings.json

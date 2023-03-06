source ~/.bashrc
conda create -n env2 python=3.9
conda activate env2
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
pip install dgl-cu113 dglgo -f https://data.dgl.ai/wheels/repo.html
pip install setuptools-git-versioning && pip install -e .
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.3.0/en_core_web_lg-3.3.0.tar.gz
pip install datasets pdfplumber fasttext dask
python src/main.py --src-data DocLayNet --add-geom  --add-hist --add-embs --add-eweights --data-type pdf --edge-type knn --node-granularity ocr --gpu 0 --model e2e
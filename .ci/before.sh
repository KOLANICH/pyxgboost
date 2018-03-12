apt-get update

git clone --depth=1 https://gitlab.com/kaitaiStructCompile.py/kaitaiStructCompile.py.git
export KSCP=./kaitaiStructCompile.py
pip install --upgrade $KSCP

pip3 install --upgrade coveralls git+https://github.com/berkerpeksag/astor.git xgboost git+https://gitlab.com/KOLANICH/alternativez.py.git git+https://github.com/kaitai-io/kaitai_struct_python_runtime.git

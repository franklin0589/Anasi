python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade build setuptools[core]
python -m build
pip install -e .
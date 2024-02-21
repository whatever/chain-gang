# :cake:

* scrape chain texts
* finetune llama 2


## Install

```bash
#  install the package locally
pip3 intall -e .

# install the dev tools
pip3 install -e ".[dev]"

# install llama-cpp for cuda gpu
pip3 uninstall llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir

# install llama-cpp for apple metal
pip uninstall llama-cpp-python -y
CMAKE_ARGS="-DLLAMA_METAL=on" pip install -U llama-cpp-python --no-cache-dir
```

## CLI


```bash
chain_gang scrape
```

### TODO

* [ ] scrape multiple paragraphs from reddit

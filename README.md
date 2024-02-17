# :cake:

* scrape chain texts
* finetune llama 2


## Install

```bash
pip3 intall -e .
pip3 install -e ".[dev]"
pip3 uninstall llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```

## CLI


```bash
chain_gang
```

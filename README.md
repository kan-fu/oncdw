# Getting Started

## Create a virtual environment

Create a virtual environment in the root directory.
Make sure the Python version meets the minimum version requirement defined in pyproject.toml.


```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the venv
$ source .venv/bin/activate
# For Windows, use .venv\Scripts\activate, and use Powershell instead of Windows Powershell

# Install onc library in editable mode
$ pip install -e .
```
Or you can use [VS Code](https://code.visualstudio.com/docs/python/environments)
or [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env) to create the env. The IDE will activate the env automatically.

## Create ./.streamlit/secrets.toml

Create a file called `secrets.toml` under `./.streamlit` folder, and put `ONC_TOKEN="<YOUR_TOKEN>"` inside (double quotes are required).


## Start the server

```shell
$ streamlit run Home.py
```

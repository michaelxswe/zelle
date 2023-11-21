This setting is only specific to:
  MacOS

Make sure you have python3 and pip3 installed:
  python3 --version
  pip3 --version

Extensions:
  python
  black Formatter
  isort

VSCode settings:
  hide pycahce files: search files.exclude and add pattern <**/__pycache__> <**/.pytest_cache>
  subfolder: explorer.compactFolder => uncheck
  
settings.json:
  "python.analysis.typeCheckingMode": "strict",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.formatOnPaste": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }


pip: 
  python3 -m venv .venv
  pip install -r requirements/dev.txt
  pip freeze > requirements/dev.txt

poetry:
  
Run app:
  uvicorn src.main:app
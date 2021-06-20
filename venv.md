# Virtualenv best practices

## Before pushing to github

we need to create a propper .gitignore file
```bash
pip freeze >> requirements.txt
```

## After pulling from github

```bash
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

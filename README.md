# WebiA — MLP vs RBF

A server-rendered Flask website comparing multilayer perceptron and radial basis function networks in Portuguese, English, and Spanish.

## Run locally

```text
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

On the MLP and RBF training pages, use **Visualizar configuração** to preview
the current settings and save them as `mlp.json` or `rbf.json` in the project
directory. A later preview replaces the corresponding file.

## Test

```text
python -m pytest
```

# eng-zap-challenge-python

### Clone the repository into your PC
```sh
$ git clone https://github.com/BZ3R0/eng-zap-challenge-python.git
```

## Instalation

- Get inside the repository directory

```sh
$ cd eng-zap-challenge-python
```

- Install virutalenv (python virtual environment)

```sh
$ virtualenv -p python3 venv
```

- Activate virtualenv

```sh
$ . venv/bin/activate
```

- Install dependences

```sh
$ cd src/
$ pip3 install -r requirements.txt
```

## Initialization

- Get into your project directory

```sh
$ cd <path-to-directory>/eng-zap-chanllenge-python
```

- Start the virtual environment
```sh
$ . venv/bin/activate
```

- Get into src folder

```sh
$ cd src/
```

- Run the application

```sh
$ python3 run.py
```

- Access endpoints for test

```
localhost:5000/api/lista_imoveis
localhost:5000/api/lista_imoveis_elegiveis
localhost:5000/api/lista_imoveis_nao_elegiveis
localhost:5000/api/zap/vendas
localhost:5000/api/zap/boundingbox
localhost:5000/api/vr/aluguel
localhost:5000/api/vr/boundingbox
```
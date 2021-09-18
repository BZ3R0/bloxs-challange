# bloxs-challenge-python

This getting started guide is avaiable for linux OS (Ubuntu/Debian).

### Clone the repository into your PC
```sh
$ git clone https://github.com/BZ3R0/bloxs-challenge.git
```

## Instalation

- Get inside the repository directory

```sh
$ cd <path-to-project>/bloxs-challenge
```

- Install virutalenv (python virtual environment)

```sh
$ sudo apt-get install virtualenv
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
$ cd <path-to-project>/bloxs-challenge
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
# localhost:5000/api/cadastro_pessoa
    Cadastra uma pessoa ou mais

    ```sh
    {
        "persons": [
            { "name": string, "cpf": string, "dataNascimento": string }
        ]
    }
    ```

# localhost:5000/api/cadastro_conta - Cadastra uma conta por usuário ou mais
    ```sh
        {
            "contas": [
                { "idPessoa": int, "saldo": float, "limiteSaqueDiario": float, "tipoConta": int}
            ]
        }
    ```

# localhost:5000/api/deposito_conta - Realiza um crédito em uma conta específica
    ```sh
        {
            "deposito":
                { "idConta": int, "valorDeposito": float}
        }
    ```

# localhost:5000/api/consulta_conta - Realiza a consulta de uma conta específica
    ```sh
        {
            "conta":
                { "idConta": int}
        }
    ```

# localhost:5000/api/debito_conta - Realiza o débito em uma conta específica
    ```sh
        {
            "debito":
                { "idConta": int, "valorDebito": float}
        }
    ```

# localhost:5000/api/bloqueio_conta - Bloqueia uma conta
    ```sh
        {
            "conta":
                { "idConta": int}
        }
    ```
    
# localhost:5000/api/extrato_conta - Exibe o extrato de transações de uma conta específica
    ```sh
            {
                "conta":
                    { "idConta": int}
            }
    ```
```
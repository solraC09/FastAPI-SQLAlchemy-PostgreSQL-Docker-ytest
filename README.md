# API de Gerenciamento de Produtos

Projeto desenvolvido com FastAPI, SQLAlchemy, PostgreSQL, Docker e Pytest.

## Tecnologias Utilizadas

* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Docker Compose
* Pytest
* Pydantic


# Estrutura do Projeto

```text
.
├── main.py
├── conftest.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
└── tests/
    ├── __init__.py
    └── test_produtos.py
```


# Subindo os Bancos PostgreSQL

Executar:

```bash
docker compose up -d
```

Verificar se os containers estão ativos:

```bash
docker ps
```

Saída esperada:

```text
postgres_dev
postgres_test
```

Banco de desenvolvimento:

```text
localhost:5432
```

Banco de testes:

```text
localhost:5433
```


# Executando a API

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar:

```bash
uvicorn main:app --reload
```

Acessar:

```text
http://localhost:8000/docs
```


# Executando os Testes

Com os containers PostgreSQL ativos:

```bash
pytest
```

Ou:

```bash
pytest -v
```


# Saída Esperada do Pytest

```text
============================= test session starts =============================
collected 14 items

tests/test_produtos.py::test_listar_produtos_vazio PASSED
tests/test_produtos.py::test_criar_produto PASSED
tests/test_produtos.py::test_produto_persistido_no_banco PASSED
tests/test_produtos.py::test_produto_aparece_na_listagem PASSED
tests/test_produtos.py::test_buscar_produto_por_id PASSED
tests/test_produtos.py::test_buscar_produto_inexistente PASSED
tests/test_produtos.py::test_deletar_produto PASSED
tests/test_produtos.py::test_deletar_produto_e_confirmar_remocao PASSED
tests/test_produtos.py::test_deletar_produto_inexistente PASSED
tests/test_produtos.py::test_payloads_invalidos[payload0] PASSED
tests/test_produtos.py::test_payloads_invalidos[payload1] PASSED
tests/test_produtos.py::test_payloads_invalidos[payload2] PASSED
tests/test_produtos.py::test_payloads_invalidos[payload3] PASSED
tests/test_produtos.py::test_banco_comeca_limpo PASSED

============================= 14 passed =============================
```


# Endpoints Disponíveis

## Listar Produtos

```http
GET /produtos
```

Resposta:

```json
[
  {
    "id": 1,
    "nome": "Notebook",
    "preco": 4500,
    "estoque": 10,
    "ativo": true
  }
]
```


## Criar Produto

```http
POST /produtos
```

Exemplo:

```json
{
  "nome": "Mouse Gamer",
  "preco": 199.90,
  "estoque": 15,
  "ativo": true
}
```


## Buscar Produto por ID

```http
GET /produtos/{id}
```


## Remover Produto

```http
DELETE /produtos/{id}
```


# Como Funciona o Isolamento dos Testes

O isolamento é garantido através da fixture `client` definida em `conftest.py`.

Antes de cada teste:

* As tabelas são criadas utilizando `Base.metadata.create_all()`.

Durante o teste:

* O FastAPI utiliza `dependency_overrides` para substituir a conexão padrão pelo banco PostgreSQL de testes.

Após o término do teste:

* Todas as tabelas são removidas utilizando `Base.metadata.drop_all()`.

Dessa forma, cada teste executa em um ambiente limpo, sem depender dos dados criados por outros testes, garantindo previsibilidade e repetibilidade dos resultados.


# Autor

Projeto desenvolvido utilizando FastAPI, PostgreSQL, Docker e Pytest para demonstração de API REST com testes automatizados e isolamento de banco de dados.

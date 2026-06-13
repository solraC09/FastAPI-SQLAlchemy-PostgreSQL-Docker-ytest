import pytest


def test_isolamento_entre_testes(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert len(response.json()) == 0

def test_criar_produto(client):
    payload = {
        "nome": "Mouse Gamer",
        "preco": 199.90,
        "estoque": 15,
        "ativo": True
    }

    response = client.post("/produtos", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["nome"] == payload["nome"]
    assert data["preco"] == payload["preco"]
    assert data["estoque"] == payload["estoque"]
    assert data["ativo"] == payload["ativo"]


def test_produto_persistido_no_banco(client):
    response = client.post(
        "/produtos",
        json={
            "nome": "Teclado Mecânico",
            "preco": 350.00,
            "estoque": 8,
            "ativo": True
        }
    )

    produto = response.json()

    busca = client.get(f"/produtos/{produto['id']}")

    assert busca.status_code == 200
    assert busca.json()["nome"] == "Teclado Mecânico"


def test_produto_aparece_na_listagem(client):
    client.post(
        "/produtos",
        json={
            "nome": "Monitor",
            "preco": 1200.00,
            "estoque": 5,
            "ativo": True
        }
    )

    response = client.get("/produtos")

    produtos = response.json()

    assert response.status_code == 200
    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Monitor"


def test_buscar_produto_por_id(client, produto_existente):
    response = client.get(
        f"/produtos/{produto_existente['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == produto_existente["id"]


def test_buscar_produto_inexistente(client):
    response = client.get("/produtos/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_deletar_produto(client, produto_existente):
    response = client.delete(
        f"/produtos/{produto_existente['id']}"
    )

    assert response.status_code == 204


def test_deletar_produto_e_confirmar_remocao(
    client,
    produto_existente
):
    client.delete(
        f"/produtos/{produto_existente['id']}"
    )

    response = client.get(
        f"/produtos/{produto_existente['id']}"
    )

    assert response.status_code == 404


def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


@pytest.mark.parametrize(
    "payload",
    [
        {
            "nome": "",
            "preco": 100,
            "estoque": 1,
            "ativo": True
        },
        {
            "nome": "Produto",
            "preco": 0,
            "estoque": 1,
            "ativo": True
        },
        {
            "nome": "Produto",
            "preco": -10,
            "estoque": 1,
            "ativo": True
        },
        {
            "nome": "Produto",
            "preco": 100,
            "estoque": -1,
            "ativo": True
        }
    ]
)
def test_payloads_invalidos(client, payload):
    response = client.post(
        "/produtos",
        json=payload
    )

    assert response.status_code == 422


def test_banco_comeca_limpo(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []
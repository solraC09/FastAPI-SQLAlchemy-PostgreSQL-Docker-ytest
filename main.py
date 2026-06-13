import os

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, field_validator
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/produtos_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)


class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: float = Field(..., gt=0)
    estoque: int = Field(default=0, ge=0)
    ativo: bool = True

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value):
        if not value.strip():
            raise ValueError("Nome não pode ser vazio")
        return value.strip()


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)


app = FastAPI(
    title="API de Produtos",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@app.get(
    "/produtos",
    response_model=list[ProdutoResponse],
    status_code=status.HTTP_200_OK
)
def listar_produtos(
    db: Session = Depends(get_db)
):
    return db.query(Produto).all()


@app.post(
    "/produtos",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db)
):
    nome = produto.nome.strip()

    if not nome:
        raise HTTPException(
            status_code=422,
            detail="Nome do produto não pode ser vazio"
        )

    novo_produto = Produto(
        nome=nome,
        preco=produto.preco,
        estoque=produto.estoque,
        ativo=produto.ativo
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@app.get(
    "/produtos/{produto_id}",
    response_model=ProdutoResponse,
    status_code=status.HTTP_200_OK
)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = (
        db.query(Produto)
        .filter(Produto.id == produto_id)
        .first()
    )

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    return produto


@app.delete(
    "/produtos/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remover_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = (
        db.query(Produto)
        .filter(Produto.id == produto_id)
        .first()
    )

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()

    return None
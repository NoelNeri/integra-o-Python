import sqlalchemy

from sqlalchemy import Integer, select
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import inspect

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey


Base = declarative_base()


class Cliente(Base):
    __tablename__ = "tb_cliente"
    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)

    conta = relationship(
        "Conta", back_populates="cliente"
    )

    def __repr__(self):
        return f"Client(id={self.id}, name = {self.name}, cpf={self.cpf})"


class Conta(Base):
    __tablename__ = "tb_conta"
    # Attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(30), nullable=False)
    agencia = Column(String(30), nullable=False)
    num_conta = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("tb_cliente.id"), nullable=False)
    saldo = Column(String())

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, agencia={self.agencia}, num_conta={self.num_conta}, saldo={self.saldo})"


print(Cliente.__tablename__)
print(Conta.__tablename__)


# Conexão com banco de dados
engine = create_engine("sqlite://")

# Criando classes como tabelas no banco de dados
Base.metadata.create_all(engine)

inspector = inspect(engine)

print(inspector.has_table("tb_cliente"))

print(inspector.get_table_names())

print(inspector.default_schema_name)


# Estabelecendo uma sessão
with Session(engine) as session:

    maria = Cliente(
        id = 1,
        name = 'Maria da Silva',
        cpf = '123123111',
        conta = [Conta(
                    tipo='poupança',
                    agencia='0543',
                    num_conta=123,
                    id_cliente=1,
                    saldo='1000,33'),
                Conta(
                    tipo='conta corrente',
                    agencia='0543',
                    num_conta=923,
                    id_cliente=1,
                    saldo='3000,33')
                ]
            )

    bernardo = Cliente(
        id=2,
        name = 'Bernardo Maria da Silva',
        cpf='123123112',
        conta = [Conta(
                    tipo='poupança',
                    agencia='0543',
                    num_conta=124,
                    id_cliente=2,
                    saldo='5000,33'),
                Conta(
                    tipo='conta corrente',
                    agencia='0543',
                    num_conta=924,
                    id_cliente=2,
                    saldo='2000,33')
                ]
            )


# Gravando no banco de dados

    session.add_all([maria, bernardo])

    session.commit()


print("\nListando tabela de clientes")
stmt = select(Cliente).where(Cliente.name.is_not(""))
for cliente in session.scalars(stmt):
    print(cliente)

print("\nListando tabela de conta")
stmt = select(Conta).where(Conta.num_conta.is_not(0))
for conta in session.scalars(stmt):
    print(conta)


stmt_join = select(Cliente.id, Cliente.name, Cliente.cpf, Conta.tipo, Conta.agencia, Conta.num_conta, Conta.saldo).join_from(Cliente, Conta)


connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)


session.close()


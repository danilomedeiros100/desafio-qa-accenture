"""Geração de massa de dados aleatória (Faker) para os cenários."""
from __future__ import annotations

import random
import string
import time
from dataclasses import dataclass
from datetime import date

from faker import Faker

fake = Faker("pt_BR")

MESES_EM_INGLES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# Valores aceitos pelos componentes do Practice Form (autocomplete / react-select)
MATERIAS = [
    "Maths", "Accounting", "Arts", "Social Studies", "Physics", "Chemistry",
    "Computer Science", "Commerce", "Economics", "Civics", "English", "History", "Biology",
]
ESTADOS_E_CIDADES = {
    "NCR": ["Delhi", "Gurgaon", "Noida"],
    "Uttar Pradesh": ["Agra", "Lucknow", "Merrut"],
    "Haryana": ["Karnal", "Panipat"],
    "Rajasthan": ["Jaipur", "Jaiselmer"],
}
GENEROS = ["Male", "Female", "Other"]
HOBBIES = ["Sports", "Reading", "Music"]
DEPARTAMENTOS = ["QA", "Engineering", "Legal", "Compliance", "Insurance", "Finance", "Marketing"]


# ---------------------------------------------------------------- API
@dataclass
class UsuarioApi:
    nome_usuario: str
    senha: str


def novo_usuario_api() -> UsuarioApi:
    """Usuário único por execução; a senha cumpre a política da API
    (maiúscula, minúscula, número, caractere especial, 8+)."""
    sufixo = f"{int(time.time() * 1000)}{random.randint(100, 999)}"
    senha = (
        fake.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
        + random.choice("!@#$%&*")
        + "Aa1"
    )
    return UsuarioApi(nome_usuario=f"qa_{sufixo}", senha=senha)


# ---------------------------------------------------------------- Practice Form
@dataclass
class Estudante:
    nome: str
    sobrenome: str
    email: str
    genero: str
    celular: str
    data_nascimento: date
    materias: list[str]
    hobbies: list[str]
    endereco: str
    estado: str
    cidade: str
    imagem: str = ""

    @property
    def nome_completo(self) -> str:
        return f"{self.nome} {self.sobrenome}"

    @property
    def data_nascimento_formatada(self) -> str:
        """Formato exibido no popup do demoqa: '05 March,1995'."""
        d = self.data_nascimento
        return f"{d.day:02d} {MESES_EM_INGLES[d.month - 1]},{d.year}"


def novo_estudante(imagem: str = "") -> Estudante:
    estado = random.choice(list(ESTADOS_E_CIDADES))
    return Estudante(
        nome=fake.first_name(),
        sobrenome=fake.last_name(),
        email=fake.unique.ascii_free_email(),
        genero=random.choice(GENEROS),
        celular="".join(random.choices(string.digits, k=10)),
        data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=60),
        materias=random.sample(MATERIAS, k=random.randint(1, 3)),
        hobbies=random.sample(HOBBIES, k=random.randint(1, 3)),
        endereco=fake.street_address().replace("\n", ", "),
        estado=estado,
        cidade=random.choice(ESTADOS_E_CIDADES[estado]),
        imagem=imagem,
    )


# ---------------------------------------------------------------- Web Tables
@dataclass
class Funcionario:
    nome: str
    sobrenome: str
    email: str
    idade: str
    salario: str
    departamento: str

    def como_linha(self) -> dict:
        """Dados na ordem das colunas da tabela."""
        return {
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "idade": self.idade,
            "email": self.email,
            "salario": self.salario,
            "departamento": self.departamento,
        }

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} <{self.email}>"


def novo_funcionario() -> Funcionario:
    return Funcionario(
        nome=fake.first_name(),
        sobrenome=fake.last_name(),
        email=fake.unique.ascii_company_email(),
        idade=str(random.randint(18, 65)),
        salario=str(random.randint(1500, 30000)),
        departamento=random.choice(DEPARTAMENTOS),
    )

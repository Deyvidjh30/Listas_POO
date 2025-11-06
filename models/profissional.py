import json

class Profissional:
    def __init__(self, id, nome, especialidade, conselho, email, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_especialidade(especialidade)
        self.set_conselho(conselho)
        self.set_email(email)
        self.set_senha(senha)

    # Gets
    def get_id(self): return self.id
    def get_nome(self): return self.nome
    def get_especialidade(self): return self.especialidade
    def get_conselho(self): return self.conselho
    def get_email(self): return self.email
    def get_senha(self): return self.senha

    # Sets
    def set_id(self, id): self.id = id
    def set_nome(self, nome): self.nome = nome
    def set_especialidade(self, especialidade): self.especialidade = especialidade
    def set_conselho(self, conselho): self.conselho = conselho
    def set_email(self, email): self.email = email
    def set_senha(self, senha): self.senha = senha

    def to_json(self):
        dic = {
            "id": self.id,
            "nome": self.nome,
            "especialidade": self.especialidade,
            "conselho": self.conselho,
            "email": self.email,
            "senha": self.senha
        }
        return dic

    @staticmethod
    def from_json(dic):
        return Profissional(dic["id"], dic["nome"], dic["especialidade"],
                            dic["conselho"], dic["email"], dic["senha"])

    def __str__(self):
        return f"{self.id} - {self.nome} - {self.especialidade} - {self.conselho} - {self.email}"


class ProfissionalDAO:
    objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        id = 0
        for aux in cls.objetos:
            if aux.get_id() > id:
                id = aux.get_id()
        obj.set_id(id + 1)
        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.objetos

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("profissional.json", mode="r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Profissional.from_json(dic)
                    cls.objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("profissional.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=Profissional.to_json)

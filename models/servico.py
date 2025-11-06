import json

class Servico:
    def __init__(self, id, descricao, valor):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_valor(valor)

    # Gets
    def get_id(self): return self.id
    def get_descricao(self): return self.descricao
    def get_valor(self): return self.valor

    # Sets
    def set_id(self, id): self.id = id
    def set_descricao(self, descricao): self.descricao = descricao
    def set_valor(self, valor): self.valor = valor

    def to_json(self):
        dic = {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor
        }
        return dic

    @staticmethod
    def from_json(dic):
        return Servico(dic["id"], dic["descricao"], dic["valor"])

    def __str__(self):
        return f"{self.id} - {self.descricao} - R$ {self.valor:.2f}"


class ServicoDAO:
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
            with open("servicos.json", mode="r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Servico.from_json(dic)
                    cls.objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("servicos.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=Servico.to_json)

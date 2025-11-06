# models/servico.py
import json

class Servico:
    def __init__(self, id, descricao, valor):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_valor(valor)

    # Gets/sets
    def get_id(self): return self.id
    def get_descricao(self): return self.descricao
    def get_valor(self): return self.valor
    def set_id(self, id): self.id = id
    def set_descricao(self, descricao): self.descricao = descricao
    def set_valor(self, valor): self.valor = valor

    # Preço padrão (serviço fixo)
    def calcular_preco(self, horas=1):
        return self.valor

    def to_json(self):
        return {
            "tipo": "fixo",
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor
        }

    @staticmethod
    def from_json(dic):
        tipo = dic.get("tipo", "fixo")
        if tipo == "hora":
            return ServicoPorHora(dic["id"], dic["descricao"], dic["valor_hora"])
        else:
            return Servico(dic["id"], dic["descricao"], dic["valor"])

    def __str__(self):
        return f"{self.id} - {self.descricao} - R$ {self.valor:.2f}"


class ServicoPorHora(Servico):
    def __init__(self, id, descricao, valor_hora):
        # Reuse valor para representar valor por hora
        super().__init__(id, descricao, valor_hora)

    # horas é número de horas contratadas
    def calcular_preco(self, horas=1):
        return self.valor * max(1, int(horas))

    def to_json(self):
        return {
            "tipo": "hora",
            "id": self.id,
            "descricao": self.descricao,
            "valor_hora": self.valor
        }

    def __str__(self):
        return f"{self.id} - {self.descricao} - R$ {self.valor:.2f}/hora"


class ServicoDAO:
    objetos = []
    arquivo = "servicos.json"

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        id_max = 0
        for aux in cls.objetos:
            if aux.get_id() > id_max:
                id_max = aux.get_id()
        obj.set_id(id_max + 1)
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
            with open(cls.arquivo, mode="r", encoding="utf-8") as f:
                list_dic = json.load(f)
                for dic in list_dic:
                    cls.objetos.append(Servico.from_json(dic))
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open(cls.arquivo, mode="w", encoding="utf-8") as f:
            json.dump([o.to_json() for o in cls.objetos], f, ensure_ascii=False, indent=2)

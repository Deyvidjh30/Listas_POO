from datetime import datetime
import json

class Horario:
    def __init__(self, id, data):
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(False)
        self.set_id_cliente(0)
        self.set_id_servico(0)
        self.set_id_profissional(0)

    # Representação textual
    def __str__(self):
        return f"{self.id} - {self.data.strftime('%d/%m/%Y %H:%M')} - {self.confirmado}"

    # Gets
    def get_id(self): return self.id
    def get_data(self): return self.data
    def get_confirmado(self): return self.confirmado
    def get_id_cliente(self): return self.id_cliente
    def get_id_servico(self): return self.id_servico
    def get_id_profissional(self): return self.id_profissional

    # Sets
    def set_id(self, id): self.id = id
    def set_data(self, data): self.data = data
    def set_confirmado(self, confirmado): self.confirmado = confirmado
    def set_id_cliente(self, id_cliente): self.id_cliente = id_cliente
    def set_id_servico(self, id_servico): self.id_servico = id_servico
    def set_id_profissional(self, id_profissional): self.id_profissional = id_profissional

    # Conversão para JSON
    def to_json(self):
        dic = {
            "id": self.id,
            "data": self.data.strftime("%d/%m/%Y %H:%M"),
            "confirmado": self.confirmado,
            "id_cliente": self.id_cliente,
            "id_servico": self.id_servico,
            "id_profissional": self.id_profissional
        }
        return dic

    @staticmethod
    def from_json(dic):
        horario = Horario(dic["id"], datetime.strptime(dic["data"], "%d/%m/%Y %H:%M"))
        horario.set_confirmado(dic["confirmado"])
        horario.set_id_cliente(dic["id_cliente"])
        horario.set_id_servico(dic["id_servico"])
        horario.set_id_profissional(dic["id_profissional"])
        return horario


class HorarioDAO:
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
            with open("horarios.json", mode="r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    obj = Horario.from_json(dic)
                    cls.objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("horarios.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=Horario.to_json)

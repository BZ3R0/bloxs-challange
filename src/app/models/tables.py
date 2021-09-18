from app import db

class Conta(db.Model):
    __tablename__ = 'Blxs_Conta'

    idConta = db.Column(db.Integer, primary_key=True)
    idPessoa = db.Column(db.Integer, db.ForeignKey('Blxs_Pessoa.idPessoa'))
    saldo = db.Column(db.Float)
    limiteSaqueDiario = db.Column(db.Float)
    flagAtivo = db.Column(db.Boolean, default=True)
    tipoConta = db.Column(db.SmallInteger)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())

    pessoa = db.relationship('Pessoa', foreign_keys=idPessoa)

    def __init__(self, idPessoa, saldo, limiteSaqueDiario, tipoConta):
        self.idPessoa = idPessoa
        self.saldo = saldo
        self.limiteSaqueDiario = limiteSaqueDiario
        self.tipoConta = tipoConta

    def __repr__(self):
        return "<idConta='%i', idPessoa='%s', saldo='%s', limiteSaqueDiario='%s', flagAtivo='%s', tipoConta='%i'>" % (self.idConta, self.idPessoa, self.saldo, self.limiteSaqueDiario, self.flagAtivo, self.tipoConta)


class Transacao(db.Model):
    __tablename__ = 'Blxs_Transacao'

    idTransacao = db.Column(db.Integer, primary_key=True)
    idConta = db.Column(db.Integer, db.ForeignKey('Blxs_Conta.idConta'))
    valor = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())

    def __init__(self, idConta, valor):
        self.idConta = idConta
        self.valor = valor

    def __repr__(self):
        return "<idTransacao='%i', idConta='%s', valor='%s'>" % (self.idTransacao, self.idConta, self.valor)


class Pessoa(db.Model):
    __tablename__ = "Blxs_Pessoa"

    idPessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256))
    cpf = db.Column(db.String(14), unique=True)
    dataNascimento = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())

    def __init__(self, nome, cpf, dataNascimento):
        self.nome = nome
        self.cpf = cpf
        self.dataNascimento = dataNascimento

    def __repr__(self):
        return "<idPessoa='%i', nome='%s', cpf='%s', dataNascimento='%s'>" % (self.idPessoa, self.nome, self.cpf, self.dataNascimento)
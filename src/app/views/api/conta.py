from app import app, db
from flask import jsonify
from flask_restful import reqparse, Resource
from datetime import datetime
from app.models.tables import Pessoa, Conta, Transacao


parser = reqparse.RequestParser()


class InsufficientFunds(Exception):
    def __init__(self, m):
        self.m = m
        super().__init__(self, m)


class BlockedAccount(Exception):
    def __init__(self, m):
        self.m = m
        super().__init__(self, m)


class CadastroPessoa(Resource):
    def post(self):
        parser.add_argument('persons', type=dict, required=True, action='append')
        args = parser.parse_args()

        try:
            for person in args['persons']:
                name = person['name']
                cpf = '{}.{}.{}-{}'.format(person['cpf'][:3], person['cpf'][3:6], person['cpf'][6:9], person['cpf'][9:])
                dataNascimento = person['dataNascimento']
                dataNascimento = datetime.strptime(dataNascimento, '%d/%m/%Y') # Convert date from string to datetime

                ins = Pessoa(nome=name, cpf=cpf, dataNascimento=dataNascimento)
                db.session.add(ins)

            db.session.commit() # register bulk of users or cancel the whole process
            return jsonify({'status_code' : 200, 'message' : 'User(s) regitered successfully'})
        except:
            db.session.rollback()
            return jsonify({'status_code' : 500, 'message' : 'Error: Can not register user'})


class CadastroConta(Resource):
    def post(self):
        parser.add_argument('contas', type=dict, required=True, action='append')
        args = parser.parse_args()

        try:
            for conta in args['contas']:
                idPessoa = int(conta['idPessoa'])
                saldo = float(conta['saldo'])
                limiteSaqueDiario = float(conta['limiteSaqueDiario'])
                tipoConta = int(conta['tipoConta'])

                ins = Conta(idPessoa=idPessoa, saldo=saldo, limiteSaqueDiario=limiteSaqueDiario, tipoConta=tipoConta)
                db.session.add(ins)

            db.session.commit() # register bulk of accounts or cancel the whole process
            return jsonify({'status_code' : 200, 'message' : 'Accounts regitered successfully'})
        except:
            db.session.rollback()
            return jsonify({'status_code' : 500, 'message' : 'Error: Can not register account'})


class DepositoConta(Resource):
    def post(self):
        parser.add_argument('deposito', type=dict, required=True)
        args = parser.parse_args()

        try:
            # Get values from post
            idConta = int(args['deposito']['idConta'])
            valorDeposito = float(args['deposito']['valorDeposito'])

            # calculate new funds and update
            saldo_antigo = db.session.query(Conta.saldo, Conta.flagAtivo).filter(Conta.idConta==idConta).first()

            if not saldo_antigo.flagAtivo:
                raise BlockedAccount('Can not deposit funds into this account because is blocked')

            novo_saldo = saldo_antigo.saldo + valorDeposito
            db.session.query(Conta).filter(Conta.idConta==idConta).update({Conta.saldo: novo_saldo})

            # register the transaction
            ins = Transacao(idConta=idConta, valor=valorDeposito)
            db.session.add(ins)
            db.session.commit()

            return jsonify({'status_code' : 200, 'message' : 'Deposit realized successfully'})
        except BlockedAccount as e:
            db.session.rollback()
            return jsonify({"status_code" : 200, 'message' : str(e)})
        except:
            db.session.rollback()
            return jsonify({'status_code' : 500, 'message' : 'Error: Can not register the transaction and update de account funds'})


class ConsultaConta(Resource):
    def post(self):
        parser.add_argument('conta', type=dict, required=True)
        args = parser.parse_args()

        try:
            # Get values from post
            idConta = int(args['conta']['idConta'])

            # calculate new funds and update
            dados_conta = db.session.query(Pessoa.nome, Conta.idConta, Conta.saldo, Conta.flagAtivo, Conta.limiteSaqueDiario).join(Conta, Conta.idPessoa==Pessoa.idPessoa).filter(Conta.idConta==idConta).first()
            result = {'idConta' : dados_conta.idConta, 'nome' : dados_conta.nome, 'saldo' : dados_conta.saldo, 'flagAtivo' : dados_conta.flagAtivo, 'limiteSaqueDiario' : dados_conta.limiteSaqueDiario}

            return jsonify({'status_code' : 200, 'message' : 'Deposit realized successfully', 'result' : result})
        except:
            db.session.rollback()
            return jsonify({'status_code' : 500, 'message' : 'Error: Can not query the account'})


class DebitoConta(Resource):
    def post(self):
        parser.add_argument('debito', type=dict, required=True)
        args = parser.parse_args()

        try:
            # Get values from post
            idConta = int(args['debito']['idConta'])
            valorDebito = float(args['debito']['valorDebito'])

            # calculate new funds and update
            saldo_antigo = db.session.query(Conta.saldo, Conta.flagAtivo).filter(Conta.idConta==idConta).first()

            if not saldo_antigo.flagAtivo:
                raise BlockedAccount('Can not debit funds from this account because is blocked')

            novo_saldo = saldo_antigo.saldo - valorDebito
            # if user try to debit more than he has
            if novo_saldo < 0:
                raise InsufficientFunds('Can not debit this value from this account')

            db.session.query(Conta).filter(Conta.idConta==idConta).update({Conta.saldo: novo_saldo})

            # register the transaction
            ins = Transacao(idConta=idConta, valor=valorDebito)
            db.session.add(ins)
            db.session.commit()

            app.logger.info('User debited: %s from account with id: %s', str(valorDebito), str(idConta))
            return jsonify({'status_code' : 200, 'message' : 'Debit realized successfully'})
        except BlockedAccount as e:
            db.session.rollback()
            return jsonify({"status_code" : 200, 'message' : str(e)})
        except InsufficientFunds as e:
            db.session.rollback()
            return jsonify({"status_code" : 200, 'message' : str(e)})
        except:
            db.session.rollback()
            return jsonify({'status_code' : 500, 'message' : 'Error: Can not register the transaction and update de account funds'})


class BloqueioConta(Resource):
    def post(self):
        parser.add_argument('conta', type=dict, required=True)
        args = parser.parse_args()

        try:
            idConta = int(args['conta']['idConta'])
            db.session.query(Conta).filter(Conta.idConta==idConta).update({Conta.flagAtivo : False})
            db.session.commit()
            return jsonify({'status_code' : 200, 'message' : 'Account blocked successfully'})
        except:
            db.session.rollback()
            return jsonify({'status_code' : 500, 'message' : 'Error: Can not register the transaction and update de account funds'})


class ExtratoConta(Resource):
    def post(self):
        parser.add_argument('conta', type=dict, required=True)
        args = parser.parse_args()

        try:
            idConta = int(args['conta']['idConta'])
            extrato_completo = []
            extrato_conta = db.session.query(Transacao).filter(Transacao.idConta==idConta).order_by(Transacao.idTransacao).all()
            for extrato in extrato_conta:
                extrato_completo.append({'idTransacao' : extrato.idTransacao, 'idConta' : extrato.idConta, 'valor' : extrato.valor, 'data' : extrato.created_at})

            return jsonify({'status_code' : 200, 'message' : 'Account extract', 'result' : extrato_completo})
        except:
            return jsonify({'status_code' : 500, 'message' : 'Error: Can not register the transaction and update de account funds'})
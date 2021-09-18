from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('instance.config')

api = Api(app)
db = SQLAlchemy(app)

# Routes
from .views.api.conta import CadastroPessoa, CadastroConta, DepositoConta, ConsultaConta, DebitoConta, BloqueioConta, ExtratoConta
api.add_resource(CadastroPessoa, '/api/cadastro_pessoa')
api.add_resource(CadastroConta, '/api/cadastro_conta')
api.add_resource(DepositoConta, '/api/deposito_conta')
api.add_resource(ConsultaConta, '/api/consulta_conta')
api.add_resource(DebitoConta, '/api/debito_conta')
api.add_resource(BloqueioConta, '/api/bloqueio_conta')
api.add_resource(ExtratoConta, '/api/extrato_conta')

from app.models import tables

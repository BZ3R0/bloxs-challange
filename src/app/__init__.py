from flask import Flask
from flask_restful import Api


app = Flask(__name__)
app.config.from_object('instance.config')

api = Api(app)

# Routes
from .views.api.zap.imoveis import ListaImoveis, ListaImoveisElegiveis, ListaImoveisNaoElegiveis
api.add_resource(ListaImoveis, '/api/lista_imoveis')
api.add_resource(ListaImoveisElegiveis, '/api/lista_imoveis_elegiveis')
api.add_resource(ListaImoveisNaoElegiveis, '/api/lista_imoveis_nao_elegiveis')

from .views.api.zap.vendas import ListaImoveisVendasZap, ImovelDescontoValoMinimo
api.add_resource(ListaImoveisVendasZap, '/api/zap/vendas')
api.add_resource(ImovelDescontoValoMinimo, '/api/zap/desconto')

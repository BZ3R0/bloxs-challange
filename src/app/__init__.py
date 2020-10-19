from flask import Flask
from flask_restful import Api


app = Flask(__name__)
app.config.from_object('instance.config')

api = Api(app)

# Routes
from .views.api.building import ListBuldings, ListBuldingsElegible, ListBuldingsNotElegible
api.add_resource(ListBuldings, '/api/lista_imoveis')
api.add_resource(ListBuldingsElegible, '/api/lista_imoveis_elegiveis')
api.add_resource(ListBuldingsNotElegible, '/api/lista_imoveis_nao_elegiveis')

from .views.api.sales import ListBuildingsSaleZap, BuildingOffMinimalValue
api.add_resource(ListBuildingsSaleZap, '/api/zap/vendas')
api.add_resource(BuildingOffMinimalValue, '/api/zap/boundingbox')

from .views.api.rental import ListBuildingRentalVR, BuildingBBMaximunValue
api.add_resource(ListBuildingRentalVR, '/api/vr/aluguel')
api.add_resource(BuildingBBMaximunValue, '/api/vr/boundingbox')

from app import app
from flask import jsonify, request
from flask_restful import Resource
from .building import get_data_per_page_from_json, get_elegible_building
import requests


minlon = -46.693419
minlat = -23.568704
maxlon = -46.641146
maxlat = -23.546686


class ListBuildingsSaleZap(Resource):
    def get(self):
        # Display only eligible sale buildings
        response = get_data_per_page_from_json()
        data = get_elegible_building(response['data'])
        data = get_building_elegible_sale(data)

        metadata = {'pageNumber' : response['page'], 'pageSize' : response['per_page'], 'totalCount' : len(data), 'listings' : [data]}

        return metadata


class BuildingOffMinimalValue(Resource):
    def get(self):
        # Giving 10% off for elegible buildings on boundingbox
        response = get_data_per_page_from_json()
        data = get_elegible_building(response['data'])
        data = get_building_elegible_sale(data)

        for building in enumerate(data):
            lon = building[1]['address']['geoLocation']['location']['lon']
            lat = building[1]['address']['geoLocation']['location']['lat']
            if lon >= minlon and lon <= maxlon and lat >= minlat and lat <= maxlat:
                price = float(building[1]['pricingInfos']['price'])
                building[1]['pricingInfos']['price'] = price - (price * 0.10)

        metadata = {'pageNumber' : response['page'], 'pageSize' : response['per_page'], 'totalCount' : len(data), 'listings' : [data]}

        return metadata


def get_building_elegible_sale(data):
    # Getting all elegible sale buildings
    list_index_to_remove = []

    for building in enumerate(data):
        businessType = building[1]['pricingInfos']['businessType']
        price = float(building[1]['pricingInfos']['price'])
        usableAreas = int(building[1]['usableAreas'])
        if businessType == 'RENTAL' or usableAreas == 0 or price/usableAreas <= 3500:
                list_index_to_remove.append(building[0])

    # Removes items from data by their index, reverse is true because otherwise we can get range out of index
    for index in sorted(list_index_to_remove, reverse=True):
        data.pop(index)

    return data
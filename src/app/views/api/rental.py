from app import app
from flask import jsonify, request
from flask_restful import Resource
from .building import get_data_per_page_from_json, get_elegible_building
import requests


minlon = -46.693419
minlat = -23.568704
maxlon = -46.641146
maxlat = -23.546686


class ListBuildingRentalVR(Resource):
    def get(self):
        # Display only rental buildings with monthlyCondoFee < 30% of the rental price
        response = get_data_per_page_from_json()
        data = get_elegible_building(response['data'])
        data = get_building_elegible_rental(data)

        metadata = {'pageNumber' : response['page'], 'pageSize' : response['per_page'], 'totalCount' : len(data), 'listings' : [data]}

        return metadata


class BuildingBBMaximunValue(Resource):
    def get(self):
        # adding 50% for rental buildings on boundingbox
        response = get_data_per_page_from_json()
        data = get_elegible_building(response['data'])
        data = get_building_elegible_rental(data)

        for building in enumerate(data):
            lon = building[1]['address']['geoLocation']['location']['lon']
            lat = building[1]['address']['geoLocation']['location']['lat']
            if lon >= minlon and lon <= maxlon and lat >= minlat and lat <= maxlat:
                price = float(building[1]['pricingInfos']['price'])
                building[1]['pricingInfos']['price'] = price + (price * 0.50)

        metadata = {'pageNumber' : response['page'], 'pageSize' : response['per_page'], 'totalCount' : len(data), 'listings' : [data]}

        return metadata


def get_building_elegible_rental(data):
    # Getting all elegible rental buildings
    list_index_to_remove = []

    for building in enumerate(data):
        businessType = building[1]['pricingInfos']['businessType']
        price = float(building[1]['pricingInfos']['price'])
        monthlyCondoFee = building[1]['pricingInfos']['monthlyCondoFee']
        if businessType == 'SALE' or not monthlyCondoFee.isdigit() or float(monthlyCondoFee) >= price * 0.3:
                list_index_to_remove.append(building[0])

    # Removes items from data by their index, reverse is true because otherwise we can get range out of index
    for index in sorted(list_index_to_remove, reverse=True):
        data.pop(index)

    return data
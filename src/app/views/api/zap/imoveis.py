from app import app
from flask import jsonify, request
from flask_restful import Resource
import requests


class ListaImoveis(Resource):
    def get(self):
        response = get_data_per_page_from_json()
        data = response['data']
        metadata = {'pageNumber' : response['page'], 'pageSize' : response['per_page'], 'totalCount' : len(data), 'listings' : [data]}

        return metadata


class ListaImoveisElegiveis(Resource):
    def get(self):
        response = get_data_per_page_from_json()
        data = get_elegible_building(response['data'])
        metadata = {'pageNumber' : response['page'], 'pageSize' : response['per_page'], 'totalCount' : len(data), 'listings' : [data]}

        return metadata


class ListaImoveisNaoElegiveis(Resource):
    def get(self):
        response = get_data_per_page_from_json()
        data = response['data']

        list_index_to_remove = []

        # Identify the building with lon and lat != 0 then add their index to a list
        for building in enumerate(data):
            lon = building[1]['address']['geoLocation']['location']['lon']
            lat = building[1]['address']['geoLocation']['location']['lat']
            if lon != 0 and lat != 0:
                list_index_to_remove.append(building[0])

        # Removes items from data by their index, reverse is true because otherwise we can get range out of index
        for index in sorted(list_index_to_remove, reverse=True):
            data.pop(index)

        metadata = {'pageNumber' : response['page'], 'pageSize' : response['per_page'], 'totalCount' : len(data), 'listings' : [data]}

        return metadata


def get_data_per_page_from_json():
    try:
        rq = requests.get('http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-2.json', timeout=30)

        # Pagination of the request
        page = int(request.args.get('page')) if 'page' in request.args and request.args.get('page') and request.args.get('page').isdigit() and int(request.args.get('page')) >= 1 else 1
        per_page = int(request.args.get('per_page')) if 'per_page' in request.args and request.args.get('per_page') else 10
        begin_offset = ((page - 1) * per_page)
        end_offeset = begin_offset + per_page

        # Get data from an offset
        data = rq.json()[begin_offset:end_offeset]
        return {'data' : data, 'page' : page, 'per_page' : per_page}

    except requests.exceptions.ConnectionError:
        return jsonify({'data' : 'connection error'})

    except requests.exceptions.Timeout:
        return jsonify({'data' : 'timeout'})

    except requests.exceptions.TooManyRedirects:
        return jsonify({'data' : 'too many redirect'})


def get_elegible_building(data):
    list_index_to_remove = []

    # Identify the building with lon and lat = 0 and removes from data
    for building in enumerate(data):
        lon = building[1]['address']['geoLocation']['location']['lon']
        lat = building[1]['address']['geoLocation']['location']['lat']
        if lon == 0 and lat == 0:
            list_index_to_remove.append(building[0])

    # Removes items from data by their index, reverse is true because otherwise we can get range out of index
    for index in sorted(list_index_to_remove, reverse=True):
        data.pop(index)

    return data
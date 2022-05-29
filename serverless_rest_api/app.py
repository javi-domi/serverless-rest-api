import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('empresa')


@app.route('/', methods='GET')
def index():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello, world!"
        })}


@app.route('/empresa', methods=['GET', 'POST'])
def put_list_empresa():
    if request.method == 'GET':
        empresa = table.scan()['Items']
        return json_response(empresa)
    else:
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "empresa registrada com sucesso"})


@app.route('/empresa/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_empresa(id):
    key = {'id': id}
    if request.method == 'GET':
        empresa = table.get_item(Key=key).get('Item')
        if empresa:
            return json_response(empresa)
        else:
            return json_response({"message": "registro de empresa não encontrado"}, 404)
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({"message": "registro de empresa atualizado"})
    else:
        table.delete_item(Key=key)
        return json_response({"message": "empresa excluida com sucesso"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
from bson.objectid import ObjectId

from src.server.database import db

FAILURE = 0
SUCCESS = 1


async def create_address(address_collection, address, user):
    try:
        # Pesquisa endereco para determinar usuario
        address_exists = await get_address_by_user(address_collection, user["_id"])
        
        # Se nao existem enderecos, registra o primeiro endereco como array
        if not address_exists:
            add_address = await address_collection.insert_one({"user": user, "address": address["address"]})
            if add_address.inserted_id:
                return add_address
        
        # Caso contrario, adiciona um novo element ao array address existente
        query = {"_id": ObjectId(address_exists["_id"])}
        
        new_address = {
            "$addToSet": {
                "address": address['address'][0]
            }
        }
        
        # Atualiza o array de enderecos existentes, adicionando o novo endereco
        updated = await address_collection.update_one(query, new_address)
        
        # Verifica se foram incluidos e retorna
        if updated.modified_count:
            return {'status': 'Address updated'}

        # Neste ponto, o processo falhou
        return FAILURE
    except Exception as e:
        print(f'create_address.error: {e}')

async def get_address_by_user(address_collection, user_id):
    try:
        address = await address_collection.find_one({'user._id': ObjectId(user_id)})
        return address
    except Exception as e:
        print(f'get_address_by_user.error: {e}')
        
async def get_delivery_address_by_user(address_collection, user_id):
    try:
        address = await get_address_by_user(address_collection, user_id)
        
        if address:
            for addr in address["address"]:
                if(addr["is_delivery"]):
                    return addr
        return None
    except Exception as e:
        print(f'get_address_by_user.error: {e}')

async def delete_address_by_id(address_collection, address_id):
    try:
        delete = await address_collection.delete_one({'_id': ObjectId(address_id)})
        
        if delete.deleted_count:
            return {'status': 'Address deleted'}
    except Exception as e:
        print(f'delete_address.error: {e}')
        
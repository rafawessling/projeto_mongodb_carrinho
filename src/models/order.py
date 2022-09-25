from src.models.address import get_delivery_address_by_user
from src.models.product import get_product
from src.server.database import db

from bson.objectid import ObjectId

async def create_order_items(order_items_collection, user, product_id):
    try:
        produto = await get_product(db.product_collection, product_id)
        
        delivery_address = await get_delivery_address_by_user(db.address_collection, user['_id'])
        
        if not delivery_address:
            return "Endereco de entrega não registrado."
        
        order_insert = {
            "user": user,
            "price": produto["price"],
            "paid": "false",
            "address": delivery_address
        }
        insert_ordem = await db.order_collection.insert_one(order_insert)
        
        if not insert_ordem.inserted_id:
            return "Nao foi possível criar a order para o carrinho."
        
        order = await get_order(db.order_collection, insert_ordem.inserted_id)
        
        query_carrinho = {
            "order": order,
            "product": [produto]
        }
        carrinho = await order_items_collection.insert_one(query_carrinho)
        
        if not carrinho.inserted_id:
            return "Nao foi possível criar a order para o carrinho."
        
        return {'status': 'carrinho criado'}
    except Exception as e:
        print(f'create_order_items.error: {e}')

async def add_product_order_items(order_items_collection, product_id, carrinho_id):
    try:
        produto = await get_product(db.product_collection, product_id)
        
        query = {"_id": ObjectId(carrinho_id)}
        
        order_update = {
            "$inc": {"order.price": produto["price"]}
        }
        
        update_ordem = await order_items_collection.update_one(query, order_update)
        
        if not update_ordem.modified_count:
            return "Nao foi possível criar a order para o carrinho."
        
        query = {"_id": ObjectId(carrinho_id)}
        
        new_product = {
            "$addToSet": {
                "product": produto
            }
        }
        
        updated_produtos = await order_items_collection.update_one(query, new_product)
                
        if updated_produtos.modified_count:
            return {'status': 'order e produtos atualizados'}
        return "Failure"
    except Exception as e:
        print(f'add_product_order_items.error: {e}')

async def remove_product_order_items(order_items_collection, product_id, carrinho_id):
    try:
        produto = await get_product(db.product_collection, product_id)
        
        query = {"_id": ObjectId(carrinho_id)}
        
        remover_produto = {
            "$pull": {
                "product": {"_id": product_id}
            }
        }
        
        remover_produto = await order_items_collection.update_many(query, remover_produto)
                
        if remover_produto.modified_count:
            query = {"_id": ObjectId(carrinho_id)}
        
            order_update = {
                "$inc": {"order.price": -produto["price"]}
            }
            
            update_ordem = await order_items_collection.update_one(query, order_update)
            
            if update_ordem.modified_count:
                return {'status': 'produto removido e ordem atualizada.'}
        return "Failure"
    except Exception as e:
        print(f'remove_product_order_items.error: {e}')

async def remove_order_items(order_items_collection, carrinho_id):
    try:
        query = {"_id": ObjectId(carrinho_id)}
        remover_carrinho = await order_items_collection.delete_one(query)
                
        if remover_carrinho.deleted_count:
            return {'status': 'carrinho removido.'}
        return "Failure"
    except Exception as e:
        print(f'remove_order_items.error: {e}')


async def get_order(order_collection, order_id):
    try:
        data = await order_collection.find_one({'_id': order_id})
        if data:
            return data
    except Exception as e:
        print(f'get_order.error: {e}')

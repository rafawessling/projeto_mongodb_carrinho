from src.models.order import (
    add_product_order_items,
    create_order_items,
    remove_order_items,
    remove_product_order_items
)
from src.models.user import get_user_by_email
from src.server.database import connect_db, db, disconnect_db
from bson.objectid import ObjectId


async def order_crud():
    option = input("Entre com a opção de CRUD (order): ")
    
    await connect_db()
    order_collection = db.order_collection

    product_id = ObjectId("6325d2760b2b7841417c501f")
    product_id2 = ObjectId("63307521df2fbdcac09a1cdd")
    carrinho_id = "6330d45cfed6a20ce04e625b"
    user_email = "lu2_domagalu@gmail.com"

    if option == '1':
        user = await get_user_by_email(
            db.users_collection,
            user_email
        )
        order = await create_order_items(
            db.order_items_collection,
            user,
            product_id
        )
        print(order)
    elif option == '2':
        produto_adicionado = await add_product_order_items(
            db.order_items_collection,
            product_id2,
            carrinho_id
        )
        print(produto_adicionado)
    elif option == '3':
        produto_removido = await remove_product_order_items(
            db.order_items_collection,
            product_id2,
            carrinho_id
        )
        print(produto_removido)
    elif option == '4':
        carrinho_removido = await remove_order_items(
            db.order_items_collection,
            carrinho_id
        )
        print(carrinho_removido)

    await disconnect_db()

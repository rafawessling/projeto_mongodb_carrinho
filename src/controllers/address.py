from src.models.address import (create_address, delete_address_by_id, get_address_by_user)

from src.models.user import (
    get_user_by_email
)
from src.server.database import connect_db, db, disconnect_db

async def address_crud():
    option = input("Entre com a opção de CRUD (address): ")
    
    await connect_db()
    address_collection = db.address_collection
    users_collection = db.users_collection
    
    address = [{
            "street": "Rua sete de setembro 32",
            "cep": "12345678",
            "district": "Centro",
            "city": "Curitiba",
            "state": "Parana",
            "is_delivery": False
    }]

    user_id = "633077732235625abe00edf3"
    user_email = "lu2_domagalu@gmail.com"
    id_address_remove = "6330a0d77c60ae4095315a10"

    address_schema = {
        "user": user_id,
        "address": address
    }
    
    if option == '1':
        # create address
        user = await get_user_by_email(
            users_collection,
            user_email
        )
        
        if user:
            address = await create_address(
                address_collection,
                address_schema,
                user
            )
        
        print(address)
    elif option == '2':
        address = await get_address_by_user(
            address_collection,
            user_id
        )
        print(address)
        
    elif option == '3':
        delete = await delete_address_by_id(
            address_collection,
            id_address_remove
        )
        print(delete)
    await disconnect_db()
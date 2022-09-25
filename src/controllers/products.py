from src.models.product import (
    create_product,
    delete_product,
    get_product_by_code,
    get_products,
    update_product,
)
from src.server.database import connect_db, db, disconnect_db


async def product_crud():
    option = input("Entre com a opção de CRUD (product): ")
    
    await connect_db()
    product_collection = db.product_collection

    product =  {
        "name": "Álbum Copa Do Mundo 2022 + figurinhas",
        "description": "Este ano temos Copa do Mundo e o tão aguardado ÁLBUM DA COPA DO MUNDO 2022 da Panini está chegando para alegrar ainda mais a sua torcida. Fique sabendo tudo sobre as 32 seleções que vão participar desta edição no Qatar, conheça os estádios e fique de olho para não perder as figurinhas extras. A coleção contém 670 cromos, sendo 50 especiais e mais 80 raros. Este Kit Contém: 1 Álbum Capa Mole Panini Copa do Mundo Qatar 2022. 2 Pacotes de Figurinhas, cada envelope contém 5 figurinhas, totalizando 10 figurinhas.",
        "price": 47.00,
        "image": "https://a-static.mlcdn.com.br/800x560/album-da-copa-do-mundo-qatar-2022-panini-10-figurinhas/mazzeiinformatica/colalbcop10f/207ae3e681448c5425da55e68247ce77.jpeg",
        "code": 123456789
    }

    if option == '1':
        # create product
        product = await create_product(
            product_collection,
            product
        )
        print(product)
    
    elif option == '2':
        # get product
        product = await get_product_by_code(
            product_collection,
            product["code"]
        )
        print(product)

    elif option == '3':
        # update
        product = await get_product_by_code(
            product_collection,
            product["code"]
        )

        product_data = {
            "name": "Álbum Copa Do Mundo Qatar 2022 Panini + 10 figurinhas",
            "price": 44.98
        }

        is_updated, numbers_updated = await update_product(
            product_collection,
            product["_id"],
            product_data
        )
        if is_updated:
            print(f"Atualização realizada com sucesso, número de documentos alterados {numbers_updated}")
        else:
            print("Atualização falhou!")

    elif option == '4':
        # delete
        product = await get_product_by_code(
            product_collection,
            product["code"]
        )

        result = await delete_product(
            product_collection,
            product["_id"]
        )

        print(result)

    elif option == '5':
        # pagination
        product = await get_products(
            product_collection,
            skip=0,
            limit=3
        )
        print(product)

    await disconnect_db()

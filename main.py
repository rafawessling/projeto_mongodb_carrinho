import asyncio

from src.controllers.users import users_crud
from src.controllers.products import product_crud
from src.controllers.address import address_crud
from src.controllers.orders import order_crud

loop = asyncio.get_event_loop()

## Descomentar somente um para testar individualmente
#loop.run_until_complete(users_crud())
#loop.run_until_complete(product_crud())
#loop.run_until_complete(address_crud())
#loop.run_until_complete(order_crud())


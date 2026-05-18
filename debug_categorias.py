import traceback
from app.core.uow import UnitOfWork, get_uow
from app.modules.categorias.service import CategoriaService

try:
    uow = UnitOfWork()
    with uow:
        service = CategoriaService(uow)
        cats = service.list_all()
        print('OK', len(cats))
        for c in cats:
            print(c)
except Exception as e:
    traceback.print_exc()

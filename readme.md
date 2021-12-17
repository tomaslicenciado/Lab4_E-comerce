# E-Commerce Api

Trabajo práctico para materia de Laboratorio, Universidad Blas Pascal.

Grupo 2: Tomas Ferreyra, Matias Cermak

Api para e-commerce en Django con Python

## Instalación

Usar el instalador de Python [pip](https://pip.pypa.io/en/stable/) para instalar los requerimientos en [requeriments.txt](https://github.com/tomaslicenciado/Lab4_E-comerce/blob/master/requeriments.txt)

```bash
pip install -r requeriments.txt
```

## Distribución

Apps instaladas en el proyecto Django:

### Api_users:
  - App de Usuarios. Heredado del sistema de autenticación nativo de Django.
  - Modificado para que el sistema de "logueo" se realice con el e-mail
  - Registro de nuevos usuarios, cambio de atributos y contraseñas
  - Obtención de token de autorización. Heredado de [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

### Products
  - Creación y administración de productos para la venta
  - Manejo de proveedores y categorías para organizar los productos

### Shop_cart
  - Un carro de compra por usuario creado de manera automática al registrarse el usuario
  - Detalles de carro creados al agregar productos al carro de compra del usuario
  - Estados de detalles de carro: En carro, Vendido, Cancelado

### Sales
  - Confirmación de compra de los productos cargados en el carro de compra del usuario
  - Compra directa de productos sin uso visible del carro de compras. Transparencia para el usuario

### Stock
  - Manejo de stock de productos: agregar producto o registrar stock real de productos mediante la api

## Documentación
Para acceder a la documentación de las app del proyecto, inicie el servidor Django con el siguiente comando:
```
python manage.py runserver
```
Luego abra el navegador y diríjase a [http://127.0.0.1:8000/redocs/](http://127.0.0.1:8000/redocs/)

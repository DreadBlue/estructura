from fastapi import FastAPI
from pydantic import BaseModel
from BST import BST
from LinkedList import LinkedList

app = FastAPI()
 
bst = BST()
ll = LinkedList()

class Producto(BaseModel):
        key: int
        nombre: str
        precio: int
        stock: int

class Pedido (BaseModel):
        id: int
        productos: object
        total: int

@app.post("/api/productos")
def crear_producto(producto: Producto):
    new_producto = {
        "key": producto.key,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock
    }
    bst.insert(producto.key, new_producto)
    return {"mensaje": "Producto agregado correctamente"}

@app.get("/api/productos/{key}")
def obtener_producto(key: int):
    producto = bst.search(key)
    if producto:
        return producto

@app.post("/api/pedidos/")
def crear_pedido(id: int, pedido: Pedido):
    productos_encontrados = []
    total = 0
    for producto in pedido.productos:
        productoList = bst.find(producto.id)
        if productoList:
            productos_encontrados.append(producto)
            total += producto.precio
    
    new_pedido = {
         "id": id,
         "productos": productos_encontrados,
         "total": total
    } 

    ll.add(new_pedido)
    return {"mensaje": "Pedido creado correctamente"}

@app.get("/api/pedidos/{id}")
def obtener_pedido(id: int):
    pedido = ll.find(id)
    if pedido:
        return pedido

@app.get("/api/pedidos/")
def listar_pedidos():
    pedidos = []
    actual = ll.head
    while actual:
        pedidos.append(actual)
        actual = actual.next
    return pedidos

@app.delete("/api/pedidos/{id}")
def eliminar_pedido(id: int):
    ll.delete(id)
    return {"mensaje": "Pedido eliminado correctamente"}

@app.put("/api/pedidos/")
def editar_pedido(id: int, pedido: Pedido):
     pedido = ll.find(id)
     if pedido:
          ll.reemplazar(id, pedido)
          return {'mensaje': "Pedido modificado"}
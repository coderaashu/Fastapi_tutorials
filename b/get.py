@app.get("/users")
def get_users(name: str = None):
    return {"name": name}
@app.get("/products/{product_id}")
def get_product(product_id: str):
    return {"product_id": product_id}
@app.get("/orders")
def get_orders(order_id: str = None, status: str = None):
    return {"order_id": order_id, "status": status}
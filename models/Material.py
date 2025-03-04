class Material:
    def __init__(self, name, type, supplier, import_price, import_qty, sell_price, sold_qty, use_day):
        self.name = name
        self.type = type
        self.supplier = supplier
        self.import_price = import_price
        self.import_qty = import_qty
        self.sell_price = sell_price
        self.sold_qty = sold_qty
        self.use_day = use_day
    def __str__(self):
        return f"{self.name}"

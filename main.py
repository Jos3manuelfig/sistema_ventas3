from abc import ABC, abstractmethod
from typing import List


class Product:
    def __init__(self, code: str, name: str, price: float):
        self.code = code
        self.name = name
        self.price = price  # Corregido a self.price


class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class IProductRepository(ABC):
    @abstractmethod
    def get_product_by_code(self, code: str) -> Product:
        pass


class ICustomerRepository(ABC):
    @abstractmethod
    def get_customer_by_email(self, email: str) -> Customer:
        pass


class InvoiceService:
    def __init__(self,
                 product_repository: IProductRepository,
                 customer_repository: ICustomerRepository):
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def create_invoice(self, customer_email: str, product_codes: List[str], quantities: List[int]) -> float:
        customer = self.customer_repository.get_customer_by_email(customer_email)
        if not customer:
            raise Exception("Customer not found")

        total = 0.0
        for code, quantity in zip(product_codes, quantities):
            product = self.product_repository.get_product_by_code(code)
            if not product:
                raise Exception(f"Product with code {code} not found")

            total += product.price * quantity

        return total


class InMemoryProductsRepository(IProductRepository):
    def __init__(self):
        self.products = {
            "P001": Product("P001", "Laptop", 1000),
            "P002": Product("P002", "Phone", 500),
            "P003": Product("P003", "Laptop", 1000),
            "P004": Product("P004", "Phone", 2000)
            # Corregido
        }

    def get_product_by_code(self, code: str) -> Product:
        return self.products.get(code)


class InMemoryCustomerRepository(ICustomerRepository):
    def __init__(self):
        self.customers = {
            "jose@example.com": Customer("Jose", "jose@example.com")
        }

    def get_customer_by_email(self, email: str) -> Customer:
        return self.customers.get(email)


# Repositorios en memoria
product_repository = InMemoryProductsRepository()
customer_repository = InMemoryCustomerRepository()

# Servicio de facturación
invoice_service = InvoiceService(product_repository, customer_repository)

# Crear factura
try:
    total = invoice_service.create_invoice(
        "jose@example.com", ["P001", "P002", "P003", "P004"], [1, 2,3,4]  # Corregido "p002" a "P002"
    )
    print(f"Total a pagar: {total}")
except Exception as e:
    print(f"Error: {e}")

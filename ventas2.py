from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class Product:
    def __init__(self, code: str, name: str, price: float):
        self.code = code
        self.name = name
        self.price = price


class Customer:
    def __init__(self, name: str, dni: str, phone: str, email: str):
        self.name = name
        self.dni = dni
        self.phone = phone
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
    def __init__(self, product_repository: IProductRepository, customer_repository: ICustomerRepository):
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def create_invoice(self, invoice_number: str, customer_email: str, product_codes: List[str], quantities: List[int]) -> None:
        customer = self.customer_repository.get_customer_by_email(customer_email)
        if not customer:
            raise Exception("Customer not found")

        print(f"FACTURA: {invoice_number}")
        print(f"FECHA: {datetime.now().strftime('%d/%m/%Y')}\n")
        print(f"CLIENTE:\t\t\tDNI:\t\t\tTELEFONO:")
        print(f"{customer.name}\t\t{customer.dni}\t\t{customer.phone}")
        print("================================================================")
        print(f"PRODUCTO\t\tCANTIDAD\tCOSTO\t\tSUBTOTAL")
        print("================================================================")

        total = 0.0
        for code, quantity in zip(product_codes, quantities):
            product = self.product_repository.get_product_by_code(code)
            if not product:
                raise Exception(f"Product with code {code} not found")

            subtotal = product.price * quantity
            total += subtotal
            print(f"{product.name.ljust(20)}\t{quantity}\t\t{product.price:.2f}\t\t{subtotal:.2f}")

        # Calcular el IVA y el total neto
        neto = total
        iva = neto * 0.18
        total_a_pagar = neto - iva

        print("===============================================================")
        print(f"\t\t\t\tNETO:\t\t{neto:.2f}")
        print(f"\t\t\t\tIVA 18%:\t{iva:.2f}")
        print(f"\t\t\tTOTAL A PAGAR:\t{total_a_pagar:.2f}")


class InMemoryProductsRepository(IProductRepository):
    def __init__(self):
        self.products = {
            "P001": Product("P001", "teclado", 100.00),
            "P002": Product("P002", "monitor", 100.00),
            "P003": Product("P003", "disco duro", 200.00),
            "P004": Product("P004", "memoria", 100.00),
            "P005": Product("P005", "mouse", 100.00)
        }

    def get_product_by_code(self, code: str) -> Product:
        return self.products.get(code)


class InMemoryCustomerRepository(ICustomerRepository):
    def __init__(self):
        self.customers = {
            "jose@example.com": Customer("Jose Manuel Figuera", "005222222", "9954355511", "jose@example.com")
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
    invoice_service.create_invoice(
        "0001",
        "jose@example.com",
        ["P001", "P002", "P003", "P004", "P005"],  # Productos
        [1, 1, 2, 2, 1]  # Cantidades
    )
except Exception as e:
    print(f"Error: {e}")

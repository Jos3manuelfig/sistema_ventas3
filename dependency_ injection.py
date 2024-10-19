from abc import ABC, abstractmethod

class ITaxService(ABC):
    @abstractmethod
    def calculate_tax(self, amount: float)-> float:
        pass

class IEmailService(ABC):
    @abstractmethod
    def send_invoice(self, invoice: dict)->None:
        pass


class TaxService(ITaxService):
    def calculate_tax(self, amount: float)->float:
        return amount * 0.15


class EmailService(IEmailService):
    def send_invoice(self, invoice: dict) ->None:
        print(f"Enviando factura a {invoice['email']} con total {invoice['total']}")


class BillingService:
    def __init__(self,tax_service: ITaxService, email_service: IEmailService):
        self.tax_service = tax_service
        self.email_service = email_service

    def create_invoice(self, customer:str, email:str, product_price: float):
        tax = self.tax_service.calculate_tax(product_price)
        total = product_price + tax
        invoice = {
            "customer": customer,
            "email": email,
            "total": total


        }
        self.email_service.send_invoice(invoice)
        return  invoice

tax_service = TaxService()
email_service = EmailService()

billing_service = BillingService(tax_service,email_service)

invoice = billing_service.create_invoice("Juan Perez", "jose@example.com", 100)
print(invoice)

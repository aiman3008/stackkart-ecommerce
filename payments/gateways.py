class JazzCashGateway:
    def initiate_payment(self, order):
        return {'status': 'initiated', 'reference': f'JC-{order.id}'}

class EasyPaisaGateway:
    def initiate_payment(self, order):
        return {'status': 'initiated', 'reference': f'EP-{order.id}'}

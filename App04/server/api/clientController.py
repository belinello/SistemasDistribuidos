from flask import request, Response

from .clientModel import ClientModel

class ClientController(object):
  TOPICS = ['quotes', 'subscriptions', 'listen', 'stocks', 'order']
  def __init__(self, model : ClientModel):
    self.model = model

  def error(self, what : str, reason : str = 'None'):
    return {'error': {'what': what, 'reason': reason}}
  
  def route_error(self):
    return self.error('Bad route', f'{request.path} not found')

  def get(self, topic : str):
    # /id/quotes
    if topic == 'quotes': 
      return {'data': self.model.get_quotes()}
    # /id/listen/subscriptions
    if topic == 'subscriptions' and request.path.split('/')[-2] == 'listen': 
      return Response(self.model.check_subscriptions(), mimetype='text/event-stream')
    # /id/subscriptions
    if topic == 'subscriptions':  
      return {'data': self.model.get_subscriptions()}
    # /id/listen/stocks
    if topic == 'stocks' and request.path.split('/')[-2] == 'listen': 
      return Response(self.model.check_transactions(), mimetype='text/event-stream')
    # /id/stocks
    if topic == 'stocks':  
      return {'data': self.model.get_stocks()}

    return self.route_error()

  def put(self, topic : str):
    try:
      json : dict = request.get_json()
    except Exception as e:
      return self.error('Failed to get JSON from request'), 400

    if topic == 'quotes':
      ok, reason = self.model.add_quote(json.get('symbol'))
      return  ({'data': json}, 201) if ok else (self.error('PUT failed', reason), 400)
    if topic == 'subscriptions':
      ok, reason = self.model.add_subscription(json.get('symbol'), json.get('lower'), json.get('upper'))
      return  ({'data': json}, 201) if ok else (self.error('PUT failed', reason), 400)
    if topic == 'order':
      symbol, operation, price, amount, timeout = json.get('symbol'), json.get('operation'), json.get('price'), json.get('amount'), json.get('timeout')
      ok, reason = self.model.add_order(symbol, operation, price, amount, timeout)
      return  ({'data': json}, 201) if ok else (self.error('PUT failed', reason), 400)

    return self.route_error()

  def delete(self, topic : str):
    try:
      json : dict = request.get_json()
    except Exception:
      return self.error('Failed to get JSON from request'), 400

    if topic == 'quotes':
      ok, reason = self.model.del_quote(json.get('symbol'))
      return ({}, 204) if ok  else (self.error('DELETE failed', reason), 400)

    return self.route_error()
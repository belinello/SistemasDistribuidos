from ..model.clientModel import ClientModel
from flask import request, Response

class ClientController(object):
  TOPICS = ['quotes', 'subscriptions', 'listen', 'stocks', 'buy_stocks']
  def __init__(self, model : ClientModel):
    self.model = model

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
    # /id/stocks
    if topic == 'stocks':  
      return {'data': self.model.get_stocks()}
    return {'error': f'BAD ROUTE {request.path}'}

  def put(self, topic : str):
    json : dict = request.get_json()
    if topic == 'quotes':
      ok, reason = self.model.add_quote(json.get('symbol'))
      return  ({'data': json}, 201) if ok else ({'error': f'PUT failed, reason: {reason}'}, 400)
    if topic == 'subscriptions':
      ok, reason = self.model.add_subscription(json.get('symbol'), json.get('lower'), json.get('upper'))
      return  ({'data': json}, 201) if ok else ({'error': f'PUT failed, reason: {reason}'}, 400)
    if topic == 'buy_stocks':
      ok, reason = self.model.add_buy
    return {'error': f'BAD ROUTE {request.path}'}

  def delete(self, topic : str):
    json : dict = request.get_json()
    if topic == 'quotes':
      ok, reason = self.model.del_quote(json.get('symbol'))
      return ({}, 204) if ok  else ({'error': f'DELETE failed, reason: {reason}'}, 400)
    if topic == 'subscriptions':
      ok, reason = self.model.del_subscription(json.get('symbol'), json.get('lower'), json.get('upper'))
      return  ({}, 204) if ok else ({'error': f'DELETE failed, reason: {reason}'}, 400)
    return {'error': f'BAD ROUTE {request.path}'}
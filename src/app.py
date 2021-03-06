# -*- coding: utf-8 -*-
import hug
import random


@hug.get('/')
def index():
    return 'hello'


@hug.format.content_type('text/xml')
@hug.format.content_type('application/xml')
@hug.format.content_type('application/xhtml+xml')
def output_xml(data, response):
    '''The data parameter is the text to be encoded with XML'''
    if isinstance(data, dict) and 'errors' in data:
        response.content_type = 'application/json'
        return hug.output_format.json(data)
    import xml.dom.minidom
    return xml.dom.minidom.parseString(data).toxml().encode()


@hug.get('/xml', output=output_xml)
def index():
    return '<?xml version="1.0"?><response><status>' + (
        'success'
        if random.randint(1, 20) > 5 else 'failed') + '</status><price>' + str(
            random.randint(1, 20) * random.randint(0, 100) /
            100) + '</price></response>'


@hug.get('/json')
def index():
    return {
        'status': ('success' if random.randint(1, 20) > 5 else 'failed'),
        'price': random.randint(1, 20) * random.randint(0, 100) / 100
    }


@hug.get("/ping")
def ping():
    return "pong"


@hug.not_found()
def not_found():
    return {'Nothing': 'to see'}


@hug.authentication.basic
def basic_authentication(username, password):
    return "test" == username and "test" == password


@hug.authentication.token
def token_verify(token):
    return "test" == token


@hug.authentication.api_key
def api_key_verify(api_key):
    return "test" == api_key


def app_authenticate(username=None, password=None, token=None, api_key=None):
    return basic_authentication(username, password) or \
        token_verify(token) or api_key_verify(api_key)


@hug.post('/token_generation')  # noqa
def token_gen_call(password, username=None, email=None):
    """Authenticate and return a token"""
    return 'test'


api = hug.API(__name__)

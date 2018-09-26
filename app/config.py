class Config(object):
    pass

class ProductionConfig(Config):
    ELASTICSEARCH_HOST = 'elasticsearch'
    JANUS_HOST = 'janus'

class DevelopmentConfig(Config):
    ELASTICSEARCH_HOST = '127.0.0.1'
    JANUS_HOST = '127.0.0.1'

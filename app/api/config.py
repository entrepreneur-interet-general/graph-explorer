class Config(object):
    pass


class Production(Config):
    ELASTICSEARCH_HOST = 'elasticsearch'
    JANUS_HOST = 'janus'


class Development(Config):
    ELASTICSEARCH_HOST = '127.0.0.1'
    JANUS_HOST = '127.0.0.1'

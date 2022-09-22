from confluent_kafka import Producer, KafkaError, KafkaException

def error_cb(err):
  print("Client error: {}".format(err))
  if err.code() == KafkaError._ALL_BROKERS_DOWN or \
     err.code() == KafkaError._AUTHENTICATION:
    raise KafkaException(err)

def delivery_report(err, msg):
  if err is not None:
    print("Delivery failed for User record {}: {}".format(msg.key(), err))
    return
  print('User record {} successfully produced to {} [{}] at offset {}'.format(
    msg.key(), msg.topic(), msg.partition(), msg.offset()))


def kafka_producer (server):
  p = Producer({
    'bootstrap.servers': server,
    'error_cb': error_cb
  })
  return p

def acked(err, msg):
  if err is not None:
    print('Failed to deliver message: {}'.format(err.str()))

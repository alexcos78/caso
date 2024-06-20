# -*- coding: utf-8 -*-

# Copyright 2014 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Module containing a Logstask cASO messenger."""

import socket

from oslo_config import cfg
from oslo_log import log
import six

from caso import exception
import caso.messenger
#add json lib
import json
#add datetime lib
import datetime
from confluent_kafka import Producer, Consumer

opts = [
    cfg.StrOpt("brokers", default="localhost:9092", help="Kafka host to send records to."),
    cfg.StrOpt("topic", default="caso", help="Kafka server topic."),
    cfg.StrOpt("serviceName", default="caso", help="Kafka server service name."),
    cfg.StrOpt("username", default="username", help="Kafka server username."),
    cfg.StrOpt("password", default="password", help="Kafka server password."),
]

CONF = cfg.CONF
CONF.register_opts(opts, group="kafka")

LOG = log.getLogger(__name__)


class KafkaMessenger(caso.messenger.BaseMessenger):
    """Format and send records to a kafka host."""

    def __init__(self, brokers=CONF.kafka.brokers, topic=CONF.kafka.topic, serviceName=CONF.kafka.serviceName, username=CONF.kafka.username, password=CONF.kafka.password):
        """Get a logstash messenger for a given host and port."""
        super(KafkaMessenger, self).__init__()
        self.brokers = CONF.kafka.brokers
        self.topic = CONF.kafka.topic
        self.serviceName = CONF.kafka.serviceName
        self.username = CONF.kafka.username
        self.password = CONF.kafka.password

#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))



    def push(self, records):

        # NOTE(acostantini): code for the serialization and push of the
        # records in logstash. JSON format to be used and encoding UTF-8
        """Serialization of records to be sent to logstash via kafka"""
        if not records:
            return

        #Actual timestamp to be added on each record       
        cdt = datetime.datetime.now()
        ct = int(datetime.datetime.now().timestamp())

        # Producer
        conf = {
            'bootstrap.servers': self.brokers,
#            'ssl.truststore.location': "/var/private/ssl/accounting/client.truststore.jks",
#            'ssl.truststore.password': "admin123",
            'ssl.ca.location': "/var/private/ssl/accounting/ca.crt",
#            'ssl.enabled.protocols': "TLSv1.2",
#            'security.protocol': 'SASL_PLAINTEXT',
            'security.protocol': 'SASL_SSL',
#            'enable.ssl.certificate.verification': 'False',
            'sasl.mechanisms': 'PLAIN',
            'sasl.kerberos.service.name': self.serviceName,
            'sasl.username': self.username,
            'sasl.password': self.password
#            'Falsessl.ca.location': '/home/kafka_dev_ai4eosc_eu_interm_ROOT.cFalseer',
#            'ssl.key.location': '/home/kafka.dev.ai4eosc.eu.key',
#            'ssl.certificate.location': '/home/kafka_dev_ai4eosc_eu_cert.cer'
    }

        # We can tune as args batch_size and linger_ms
        producer = Producer(**conf)


        """Push records to logstash using tcp."""
        for record in records:
        #serialization of record
              rec=record.serialization_message()
        #cASO timestamp added to each record
              rec['caso-timestamp']=ct
        
        #Send the record to Kafka


              try:
                  producer.poll(0)
                  producer.produce(self.topic, value=json.dumps(rec).encode('utf-8'),
                            callback=self.delivery_report)
  
              except ValueError as err:
                  print("This alert can't be read" % (err))

        producer.flush()











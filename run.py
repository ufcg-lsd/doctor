import sleekxmpp
import logging
import traceback
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config')

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s')

xmpp = sleekxmpp.ClientXMPP(config.get('xmpp', 'jid'), config.get('xmpp', 'password'))
xmpp.connect((config.get('xmpp', 'host'), (config.getint('xmpp', 'port'))))
xmpp.process(block=False)

components = config.get("doctor", "components")
for component in components.split(','):
  try:
    iq = xmpp.make_iq_get(queryxmlns='http://jabber.org/protocol/disco#info', 
                        ito=component, ifrom=xmpp.boundjid)
    response = iq.send(block=True, timeout=10)
  except Exception, e:
    xmpp.disconnect()
    raise e

xmpp.disconnect()
from base64 import b64encode
from struct import unpack

import glog as log
import requests

from gerrit_ldap_sync import config


class IpaSshKey(object):
    def __init__(self, client, key):
        self.client = client
        if key.startswith('ssh-'):
            self.key = key.decode('utf-8')
        else:
            key_type_length = unpack('>l', key[:4])[0]
            key_type = key[4:4 + key_type_length]
            self.key = ' '.join([key_type, b64encode(key)])

    def __eq__(self, other):
        return other.key in self.key

    def add(self):
        if config.dry_run:
            log.info(u'Would add key for {0}'.format(self.client.user))
            return

        log.debug(u'Adding key {0} for {1}'.format(self.key, self.client.user))
        r = self.client.make_request('/a/accounts/self/sshkeys', method='POST', data=self.key)
        if not r.status_code == requests.codes.created:
            raise RuntimeError

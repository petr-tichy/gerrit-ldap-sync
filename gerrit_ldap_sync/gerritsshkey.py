import glog as log
import requests

from gerrit_ldap_sync import config


class GerritSshKey(object):
    def __init__(self, client, key):
        self.client = client
        self.seq = key['seq']
        self.key = key['encoded_key'].strip()

    def __eq__(self, other):
        return self.key in other.key

    def remove(self):
        if config.dry_run:
            log.info(u'Would remove key {1} for {0}'.format(self.client.user, self.seq))
        else:
            log.debug('Removing key {0}'.format(self.seq))
            r = self.client.make_request('/a/accounts/self/sshkeys/{0}'.format(self.seq), method='DELETE')
            if not r.status_code == requests.codes.no_content:
                raise RuntimeError

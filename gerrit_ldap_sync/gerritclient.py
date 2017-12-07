import json

import glog as log
import requests

from gerrit_ldap_sync import config
from gerrit_ldap_sync.gerritsshkey import GerritSshKey
from gerrit_ldap_sync.ipdasshkey import IpaSshKey


class GerritClient(object):
    def __init__(self, ldap_data):
        self.user = ldap_data['uid'][0]
        self.auth_cookie = None
        self.ipa_keys = [IpaSshKey(self, key) for key in ldap_data.get('ipaSshPubKey', [])]
        self.gerrit_keys = []

    def make_request(self, url, method='GET', data=None):
        headers = config.DEFAULT_HEADERS
        headers.update({'REMOTE_USER': self.user})
        url = config.GERRIT_URL + url
        cookie = {'GerritAccount': self.auth_cookie}

        if method == 'GET':
            return requests.get(url, headers=headers, allow_redirects=False, cookies=cookie)
        elif method == 'DELETE':
            return requests.delete(url, headers=headers, cookies=cookie)
        elif method == 'POST':
            return requests.post(url, headers=headers, cookies=cookie, data=data)

    def login(self):
        if self.auth_cookie is not None:
            return

        log.info('Gerrit login with {!r}'.format(self.user))

        r = self.make_request('/login')

        if r.status_code == requests.codes.found:
            location = r.headers.get('location')
            if location.startswith(config.GERRIT_REDIRECT_LOCATION):
                self.auth_cookie = r.cookies.get('GerritAccount')
            if location.startswith(config.GERRIT_REDIRECT_LOCATION + '/#/register'):
                log.info('Registered user {!r}'.format(self.user))
        else:
            raise RuntimeError

    def get_gerrit_keys(self):
        self.login()
        r = self.make_request('/a/accounts/self/sshkeys')
        content = r.content
        content = content[content.find('\n') + 1:]
        json_data = json.loads(content)
        self.gerrit_keys = [GerritSshKey(self, key) for key in json_data]

    def sync_keys(self):
        self.get_gerrit_keys()
        [key.remove() for key in self.gerrit_keys if key not in self.ipa_keys]
        [key.add() for key in self.ipa_keys if key not in self.gerrit_keys]

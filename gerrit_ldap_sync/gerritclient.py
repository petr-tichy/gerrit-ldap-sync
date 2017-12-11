import json

import glog as log
import requests

import config
from .gerritsshkey import GerritSshKey
from .ipdasshkey import IpaSshKey
from .exceptions import *


def _strip_content(content):
    return content[content.find('\n') + 1:]


def _parse_json(content):
    content = _strip_content(content)
    return json.loads(content)


class GerritClient(object):
    def __init__(self, ldap_data):
        self.user = ldap_data['uid'][0]
        self.auth_cookie = None
        self.ipa_keys = [IpaSshKey(self, key) for key in ldap_data.get('ipaSshPubKey', [])]
        self.gerrit_keys = []

    def make_request(self, url, method='GET', data=None, user=None):
        headers = config.DEFAULT_HEADERS
        headers.update({'REMOTE_USER': user or self.user})
        url = config.GERRIT_URL + url
        cookie = {'GerritAccount': self.auth_cookie}

        if method == 'GET':
            return requests.get(url, headers=headers, allow_redirects=False, cookies=cookie)
        elif method == 'DELETE':
            return requests.delete(url, headers=headers, cookies=cookie)
        elif method == 'POST':
            return requests.post(url, headers=headers, cookies=cookie, data=data)

    def user_exists(self):
        r = self.make_request('/a/accounts/?q=username:' + self.user, user=config.ADMINISTRATOR)
        if r.status_code == requests.codes.ok:
            json_data = _parse_json(r.content)
            if len(json_data) == 1:
                return True

    def login(self, register=False):
        if self.auth_cookie is not None:
            return

        if not register and not self.user_exists():
            raise UserNotRegistered

        log.info('Gerrit login with {!r}'.format(self.user))

        r = self.make_request('/login')

        if r.status_code == requests.codes.found:
            location = r.headers.get('location')
            if location.startswith(config.GERRIT_REDIRECT_LOCATION):
                self.auth_cookie = r.cookies.get('GerritAccount')
            if location.startswith(config.GERRIT_REDIRECT_LOCATION + '/#/register'):
                log.info('Registered user {!r}'.format(self.user))
        else:
            raise RuntimeError('Failed to login as {!r}'.format(self.user))

    def get_user(self):
        try:
            self.login()
        except UserNotRegistered:
            log.info('User {!r} not registered'.format(self.user))
            try:
                self.login(register=True)
            except UserNotRegistered:
                raise RuntimeError('Failed to register user {!r}'.format(self.user))

    def get_gerrit_keys(self):
        self.get_user()
        r = self.make_request('/a/accounts/self/sshkeys')
        if r.status_code == requests.codes.ok:
            json_data = _parse_json(r.content)
            self.gerrit_keys = [GerritSshKey(self, key) for key in json_data]
        else:
            raise RuntimeError('Failed to get kes for {!r}'.format(self.user))

    def sync_keys(self):
        self.get_gerrit_keys()
        [key.remove() for key in self.gerrit_keys if key not in self.ipa_keys]
        [key.add() for key in self.ipa_keys if key not in self.gerrit_keys]

#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
from struct import unpack

import ldap
import requests
from base64 import b64encode

import logging
import glog as log
import fire

from httplib import HTTPConnection

HTTPConnection.debuglevel = 1
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

GERRIT_URL = 'http://127.0.0.1:8080'
GERRIT_HOSTNAME = '''ms-gerrit-stg.na.intgdc.com'''
DEFAULT_HEADERS = {'Host': GERRIT_HOSTNAME, 'User-Agent': 'Python-LDAP-Gerrit-sync'}

LDAP_USER = 'uid=viewer,cn=sysaccounts,cn=etc,dc=intgdc,dc=com'
LDAP_PASS = '9PT0M41gBkIelHrTKmv8cer16IiU416l4Y3Hi9SR'

LDAP_URL = 'ldaps://freeipa01.intgdc.com ldaps://freeipa02.intgdc.com ldaps://freeipa04.intgdc.com ldaps://freeipa05.intgdc.com ldaps://freeipa06.intgdc.com ldaps://freeipa07.intgdc.com '
LDAP_BASE = 'cn=users,cn=accounts,dc=intgdc,dc=com'
LDAP_FILTER = '(&(objectClass=inetOrgPerson)(memberOf=cn=gerrit-user-groups,cn=groups,cn=accounts,dc=intgdc,dc=com))'
LDAP_ATTRS = ['uid', 'ipaSshPubKey']

DUMMY_KEY_CONTENT = u''')]}'
[
  {
    "seq": 1,
    "ssh_public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA7CBjWNevcHv80u889nWxCHKLlR5hMCB1GPNKWlRBwCNGVrkoEUOa9cdAwOZUvgtTnh7YQJo114OdEz6bi53cfHIBBA2bNYoRVVOZJrYV34mx24mUZrPZtSefIS/B3BmfzzzI4YC2rrHDnHnl6rZQGMpX9OawBkDMEG7+VoOqHaCjTybsXMHxVsmLxwGA19WhEiX4Pzi/mjdZGpaM2FqlgUdMe0nBUOR2Aky72AU6dfVVucxHer/hv1t+qmUCzmRzofGqu+T9+rL3OJKBrTIpF8KOF5Eui9AHRWeDilnwKfVjaeQSzimX9qmF9wWh11ps7eAcy1pVSxBtWsXpKZQFGw== john.doe@example.com",
    "encoded_key": "AAAAB3NzaC1yc2EAAAABIwAAAQEA7CBjWNevcHv80u889nWxCHKLlR5hMCB1GPNKWlRBwCNGVrkoEUOa9cdAwOZUvgtTnh7YQJo114OdEz6bi53cfHIBBA2bNYoRVVOZJrYV34mx24mUZrPZtSefIS/B3BmfzzzI4YC2rrHDnHnl6rZQGMpX9OawBkDMEG7+VoOqHaCjTybsXMHxVsmLxwGA19WhEiX4Pzi/mjdZGpaM2FqlgUdMe0nBUOR2Aky72AU6dfVVucxHer/hv1t+qmUCzmRzofGqu+T9+rL3OJKBrTIpF8KOF5Eui9AHRWeDilnwKfVjaeQSzimX9qmF9wWh11ps7eAcy1pVSxBtWsXpKZQFGw==",
    "algorithm": "ssh-rsa",
    "comment": "john.doe@example.com",
    "valid": true
  },
  {
    "seq": 2,
    "ssh_public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA7CBjWNevcHv80u889nWxCHKLlR5hMCB1GPNKWlRBwCNGVrkoEUOa9cdAwOZUvgtTnh7YQJo114OdEz6bi53cfHIBBA2bNYoRVVOZJrYV34mx24mUZrPZtSefIS/B3BmfzzzI4YC2rrHDnHnl6rZQGMpX9OawBkDMEG7+VoOqHaCjTybsXMHxVsmLxwGA19WhEiX4Pzi/mjdZGpaM2FqlgUdMe0nBUOR2Aky72AU6dfVVucxHer/hv1t+qmUCzmRzofGqu+T9+rL3OJKBrTIpF8KOF5Eui9AHRWeDilnwKfVjaeQSzimX9qmF9wWh11ps7eAcy1pVSxBtWsXpKZQFGw== john.doe@example.com",
    "encoded_key": "AAAAB3NzaC1yc2EAAAABIwAAAQEA7CBjWNevcHv80u889nWxCHKLlR5hMCB1GPNKWlRBwCNGVrkoEUOa9cdAwOZUvgtTnh7YQJo114OdEz6bi53cfHIBBA2bNYoRVVOZJrYV34mx24mUZrPZtSefIS/B3BmfzzzI4YC2rrHDnHnl6rZQGMpX9OawBkDMEG7+VoOqHaCjTybsXMHxVsmLxwGA19WhEiX4Pzi/mjdZGpaM2FqlgUdMe0nBUOR2Aky72AU6dfVVucxHer/hv1t+qmUCzmRzofGqu+T9+rL3OJKBrTIpF8KOF5Eui9AHRWeDilnwKfVjaeQSzimX9qmF9wWh11ps7eAcy1pVSxBtWsXpKZQFGw==",
    "algorithm": "ssh-rsa",
    "comment": "john.doe@example.com",
    "valid": true
  }
]
'''


class NameSpace(object):
    pass


config = NameSpace()
config.debug = config.test = config.dry_run = None


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
        else:
            log.debug(u'Adding key {0} for {1}'.format(self.key, self.client.user))
            r = self.client.make_request('/a/accounts/self/sshkeys', method='POST', data=self.key)
            if not r.status_code == requests.codes.created:
                raise RuntimeError


class GerritClient(object):
    def __init__(self, ldap_data):
        self.user = ldap_data['uid'][0]
        self.registered = False
        self.auth_cookie = None
        self.ipa_keys = [IpaSshKey(self, key) for key in
                         ldap_data['ipaSshPubKey']] if 'ipaSshPubKey' in ldap_data else []
        self.gerrit_keys = []

    def make_request(self, url, method='GET', data=None):
        headers = DEFAULT_HEADERS
        headers.update({'REMOTE_USER': self.user})
        url = GERRIT_URL + url
        cookie = {'GerritAccount': self.auth_cookie}

        if config.test:
            r = NameSpace()
            if method == 'GET':
                r.status_code = requests.codes.ok
            elif method == 'DELETE':
                r.status_code = requests.codes.no_content
            elif method == 'POST':
                r.status_code = requests.codes.created
            return r
        else:
            if method == 'GET':
                return requests.get(url, headers=headers, allow_redirects=False, cookies=cookie)
            elif method == 'DELETE':
                return requests.delete(url, headers=headers, cookies=cookie)
            elif method == 'POST':
                return requests.post(url, headers=headers, cookies=cookie, data=data)

    def login(self):
        if self.auth_cookie is not None:
            return

        log.debug('Gerrit login with {!r}'.format(self.user))

        if config.test:
            self.auth_cookie = 'DUMMY'
            return

        r = self.make_request('/login')

        if r.status_code == requests.codes.found and r.headers['location'].startswith('https://' + GERRIT_HOSTNAME):
            self.auth_cookie = r.cookies.get('GerritAccount')
            if not r.headers['location'].startswith('https://' + GERRIT_HOSTNAME + '/#/register'):
                self.registered = True
        else:
            raise RuntimeError

    def register(self):
        self.login()
        if not self.registered:
            if config.dry_run:
                log.info('Would register user {!r}'.format(self.user))
            else:
                self.make_request('/#/register/')
            self.registered = True

    def get_gerrit_keys(self):
        self.register()
        if config.test:
            content = DUMMY_KEY_CONTENT
        else:
            r = self.make_request('/a/accounts/self/sshkeys')
            content = r.content
        content = content[content.find('\n') + 1:]
        json_data = json.loads(content)
        self.gerrit_keys = [GerritSshKey(self, key) for key in json_data]

    def sync_keys(self):
        self.get_gerrit_keys()
        [key.remove() for key in self.gerrit_keys if key not in self.ipa_keys]
        [key.add() for key in self.ipa_keys if key not in self.gerrit_keys]


class LDAPClient:
    def __init__(self):
        self.ldap = None

    def connect(self):
        if self.ldap is None:
            self.ldap = ldap.initialize(LDAP_URL)
            self.ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
            # self.ldap.start_tls_s()
            self.ldap.bind_s(LDAP_USER, LDAP_PASS)

    def get_ldap_users(self):
        self.connect()
        return self.ldap.search_st(
            LDAP_BASE, ldap.SCOPE_SUBTREE, filterstr=LDAP_FILTER, attrlist=LDAP_ATTRS, timeout=30)


def main(debug=False, dry_run=True, test=False):
    config.debug = debug
    config.dry_run = dry_run
    config.test = test

    if config.debug or config.dry_run:
        log.setLevel('DEBUG')

    ldap_client = LDAPClient()

    for dn, data in ldap_client.get_ldap_users():
        log.info('Processing user {!r}'.format(dn))
        GerritClient(data).sync_keys()


if __name__ == '__main__':
    fire.Fire(main)

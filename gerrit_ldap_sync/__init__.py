#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import glog as log
import fire

from httplib import HTTPConnection

import gerrit_ldap_sync.config
from gerrit_ldap_sync.ldapclient import LDAPClient
from gerrit_ldap_sync.gerritclient import GerritClient

HTTPConnection.debuglevel = 1
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def main(debug=False, dry_run=True):
    config.debug = debug
    config.dry_run = dry_run

    if config.debug or config.dry_run:
        log.setLevel('DEBUG')

    ldap_client = LDAPClient()

    for dn, data in ldap_client.get_ldap_users():
        log.info('Processing user {!r}'.format(dn))
        GerritClient(data).sync_keys()


if __name__ == '__main__':
    fire.Fire(main)

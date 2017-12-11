#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sure import expect
import httpretty

import tests

import gerrit_ldap_sync
from gerrit_ldap_sync import config

httpretty.HTTPretty.allow_net_connect = False


@httpretty.activate
def test_dry_run():
    # config.debug = True

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/login',
                           status=302,
                           location=config.GERRIT_REDIRECT_LOCATION + '/#/register#/',
                           cookie='GerritAccount: DUMMY'
                           )

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/a/accounts/self/sshkeys',
                           body=tests.GERRIT_DUMMY_KEY_BODY)

    expect(gerrit_ldap_sync.main()).when.called_with().to.return_value(None)
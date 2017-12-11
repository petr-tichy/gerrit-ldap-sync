#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sure import expect
import httpretty
import re

import tests

from gerrit_ldap_sync import GerritClient
from gerrit_ldap_sync import config

httpretty.HTTPretty.allow_net_connect = False


@httpretty.activate
def test_register_dry_run():
    config.debug = True
    config.dry_run = True

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/a/accounts/?q=new.user.name',
                           match_querystring=True,
                           body=tests.GERRIT_NEW_USER_QUERY_REPLY)

    data = dict()
    data['uid'] = ['new.user.name']
    GerritClient(data).get_user()

    expect(httpretty.has_request()).to.be.ok


@httpretty.activate
def test_register():
    config.debug = True
    config.dry_run = False

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/a/accounts/?q=user.name',
                           match_querystring=True,
                           body=tests.GERRIT_EXISTING_USER_QUERY_REPLY)

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/login',
                           status=302,
                           location=config.GERRIT_REDIRECT_LOCATION + '/#/register#/',
                           cookie='GerritAccount: DUMMY'
                           )

    data = dict()
    data['uid'] = ['user.name']
    GerritClient(data).get_user()

    expect(httpretty.has_request()).to.be.ok


@httpretty.activate
def test_list_ssh_keys():
    config.debug = True
    config.dry_run = False

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/a/accounts/self/sshkeys',
                           body=tests.GERRIT_DUMMY_KEY_BODY)

    httpretty.register_uri(httpretty.GET,
                           re.compile(config.GERRIT_URL + '/a/accounts/\?q=(\w+)'),
                           body=tests.GERRIT_EXISTING_USER_QUERY_REPLY)

    gerrit_client = GerritClient(tests.LDAP_DATA)
    gerrit_client.auth_cookie = 'DUMMY'
    gerrit_client.get_gerrit_keys()

    expect(httpretty.has_request()).to.be.ok
    expect(gerrit_client.gerrit_keys).to.not_be.empty


def test_load_user_name():
    config.debug = True

    gerrit_client = GerritClient(tests.LDAP_DATA_NO_KEYS)

    expect(gerrit_client.user).to.be.equal('user.name')


def test_load_ipa_keys_no_key():
    config.debug = True

    gerrit_client = GerritClient(tests.LDAP_DATA_NO_KEYS)

    expect(gerrit_client.ipa_keys).to.be.a(list)
    expect(gerrit_client.ipa_keys).to.have.length_of(0)

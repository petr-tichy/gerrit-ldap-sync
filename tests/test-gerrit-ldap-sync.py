#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sure import expect
import httpretty

from gerrit_ldap_sync import GerritClient
from gerrit_ldap_sync import config

LDAP_DATA = {'ipaSshPubKey': [
    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACUx0p3AEWt7f7nLdJytzDYApaVMOSVmoq9tMPD+2drlARavxJ9Zje5RPnYt4ZOq+I6GccNwN8UfSe4W6huMf/pXb2cXmfy7hRj/uElxiELMfV/VYdkIh5XS1jZlyjyygYWFlEFLPCCCuPZYQl//iWRKD0/noca43vSdDR5b06dy5Kc9V9m9o/Nb3oWbxjo6+lH83oBVWwxliyq6y0x+8T2Edogq+nCaNswfjbUjOpQvjARsVxHgJIZiY/uP++k3tHXhtLuojbQJq61ukS139uvUQLQ/XLQcaf9WTJVcv3vPjvjBeH3PTR7FP8RdCJ3E2dEYt/NyYgPY5/vX+F1/la1CwvZlQr925cYF1LxmIlUTYulpq4qfMa+543t7xnHN7Xlr4bKowP34dTA8MmlOjsyihE41MCw00dsGtFk8hxZKDsYzyc/NOcc+Ot/O+poUIVV5dFLj4x/foGYzrTFH1pjSskXW8sRzrCHsFL6ZIUo1G+HjaxvAu4OVBQk2XgTw9LRWaS7swx50f4psuEfD4wB11s4lHxKAPlNvSSmkfeQv+4En5+hLcSxc4V396esK4TdWID1l3esGrVecVwOq8X6wqMWGiBVktLK58sv9syPaJBsu2YsPIPhp1q4iihgCg3I9f9FEWj0vnD2RtVhUyosxOXNQgiuAS2QAjVUA9h+T2thgttXz4BIgEnvmNe6fmWZ17SitV91Gj24yW8tHJJIdUNY8LzIViJ4jOy7SktauER4z5d6mXbvYwfQ4Rm9QhKT5lzM/KYRoYv7pLXhbLw7KTJZ20= petr.tichy@gooddata.com',
    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDw2VTB9Lqx/n05YGrHJI5H/IBkFYxIaxTDqhY3dhaVRmTHDjC9xq4luHYJDmKhzjNCW6BOcHpylu+92WNXJf/4j6xaRrqnuGfHmLExgXjt7jsim9ea9fmWSFVQbbZ8zRef3inDPePDHAMzRy5OJvtNi80xVBuM78m0LT6w0LOQ6qNTK1a7lc325kkIJkXCNiTF5mi6mGLilUscy1Q24g30I52GZNRnVXjd77fCCLxqpIzyB8fJQ8zysMCtUY7HbluKbBxutZYD0IbMLYIuYuyfePZ3yKI12f0pe85cHxfEgatNDrcgAeBnF8KdR/SZTEXyb2BWwf43qZQbxZU62MZX petr.tichy+iphone@gooddata.com'],
    'uid': ['user.name']}

LDAP_DATA_NO_KEYS = {'ipaSshPubKey': [],
                     'uid': ['user.name']}

httpretty.HTTPretty.allow_net_connect = False


@httpretty.activate
def test_register():
    config.debug = True
    config.dry_run = False
    config.test = False

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/login',
                           status=302,
                           location=config.GERRIT_REDIRECT_LOCATION + '/#/register#/',
                           cookie='GerritAccount: DUMMY'
                           )

    GerritClient(LDAP_DATA).login()

    expect(httpretty.has_request()).to.be.ok


@httpretty.activate
def test_list_ssh_keys():
    config.debug = True
    config.dry_run = False
    config.test = False

    httpretty.register_uri(httpretty.GET, config.GERRIT_URL + '/a/accounts/self/sshkeys',
                           body=config.DUMMY_KEY_CONTENT)

    gerrit_client = GerritClient(LDAP_DATA)
    gerrit_client.auth_cookie = 'DUMMY'
    gerrit_client.get_gerrit_keys()

    expect(httpretty.has_request()).to.be.ok
    expect(gerrit_client.gerrit_keys).to.not_be.empty


def test_load_user_name():
    gerrit_client = GerritClient(LDAP_DATA_NO_KEYS)

    expect(gerrit_client.user).to.be.equal('user.name')


def test_load_ipa_keys_no_key():
    gerrit_client = GerritClient(LDAP_DATA_NO_KEYS)

    expect(gerrit_client.ipa_keys).to.be.a(list)
    expect(gerrit_client.ipa_keys).to.have.length_of(0)

def test_read_ldap():

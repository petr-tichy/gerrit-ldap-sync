import ldap

from gerrit_ldap_sync import config


class LDAPClient:
    def __init__(self):
        self.ldap = None

    def connect(self):
        if self.ldap is None:
            self.ldap = ldap.initialize(config.LDAP_URL)
            self.ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
            # self.ldap.start_tls_s()
            self.ldap.bind_s(config.LDAP_USER, config.LDAP_PASS)

    def get_ldap_users(self):
        self.connect()
        return self.ldap.search_st(
            config.LDAP_BASE, ldap.SCOPE_SUBTREE, filterstr=config.LDAP_FILTER, attrlist=config.LDAP_ATTRS, timeout=30)

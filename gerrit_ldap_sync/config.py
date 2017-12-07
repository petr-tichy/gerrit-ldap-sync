LDAP_USER = 'uid=viewer,cn=sysaccounts,cn=etc,dc=intgdc,dc=com'
LDAP_PASS = '9PT0M41gBkIelHrTKmv8cer16IiU416l4Y3Hi9SR'

LDAP_URL = 'ldaps://freeipa01.intgdc.com ldaps://freeipa02.intgdc.com ldaps://freeipa04.intgdc.com ldaps://freeipa05.intgdc.com ldaps://freeipa06.intgdc.com ldaps://freeipa07.intgdc.com '
LDAP_BASE = 'cn=users,cn=accounts,dc=intgdc,dc=com'
LDAP_FILTER = '(&(objectClass=inetOrgPerson)(memberOf=cn=gerrit-user-groups,cn=groups,cn=accounts,dc=intgdc,dc=com))'
LDAP_ATTRS = ['uid', 'ipaSshPubKey']

GERRIT_URL = 'http://127.0.0.1:8080'
GERRIT_PROTOCOL = 'https'
GERRIT_HOSTNAME = 'ms-gerrit-stg.na.intgdc.com'
GERRIT_REDIRECT_LOCATION = ''.join([GERRIT_PROTOCOL, '://', GERRIT_HOSTNAME])
DEFAULT_HEADERS = {'Host': GERRIT_HOSTNAME, 'User-Agent': 'Python-LDAP-Gerrit-sync'}

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

debug = False
dry_run = True

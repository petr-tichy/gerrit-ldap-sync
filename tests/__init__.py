#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sure

GERRIT_DUMMY_KEY_BODY = u''')]}'
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

LDAP_DATA = {'ipaSshPubKey': [
    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACUx0p3AEWt7f7nLdJytzDYApaVMOSVmoq9tMPD+2drlARavxJ9Zje5RPnYt4ZOq+I6GccNwN8UfSe4W6huMf/pXb2cXmfy7hRj/uElxiELMfV/VYdkIh5XS1jZlyjyygYWFlEFLPCCCuPZYQl//iWRKD0/noca43vSdDR5b06dy5Kc9V9m9o/Nb3oWbxjo6+lH83oBVWwxliyq6y0x+8T2Edogq+nCaNswfjbUjOpQvjARsVxHgJIZiY/uP++k3tHXhtLuojbQJq61ukS139uvUQLQ/XLQcaf9WTJVcv3vPjvjBeH3PTR7FP8RdCJ3E2dEYt/NyYgPY5/vX+F1/la1CwvZlQr925cYF1LxmIlUTYulpq4qfMa+543t7xnHN7Xlr4bKowP34dTA8MmlOjsyihE41MCw00dsGtFk8hxZKDsYzyc/NOcc+Ot/O+poUIVV5dFLj4x/foGYzrTFH1pjSskXW8sRzrCHsFL6ZIUo1G+HjaxvAu4OVBQk2XgTw9LRWaS7swx50f4psuEfD4wB11s4lHxKAPlNvSSmkfeQv+4En5+hLcSxc4V396esK4TdWID1l3esGrVecVwOq8X6wqMWGiBVktLK58sv9syPaJBsu2YsPIPhp1q4iihgCg3I9f9FEWj0vnD2RtVhUyosxOXNQgiuAS2QAjVUA9h+T2thgttXz4BIgEnvmNe6fmWZ17SitV91Gj24yW8tHJJIdUNY8LzIViJ4jOy7SktauER4z5d6mXbvYwfQ4Rm9QhKT5lzM/KYRoYv7pLXhbLw7KTJZ20= petr.tichy@gooddata.com',
    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDw2VTB9Lqx/n05YGrHJI5H/IBkFYxIaxTDqhY3dhaVRmTHDjC9xq4luHYJDmKhzjNCW6BOcHpylu+92WNXJf/4j6xaRrqnuGfHmLExgXjt7jsim9ea9fmWSFVQbbZ8zRef3inDPePDHAMzRy5OJvtNi80xVBuM78m0LT6w0LOQ6qNTK1a7lc325kkIJkXCNiTF5mi6mGLilUscy1Q24g30I52GZNRnVXjd77fCCLxqpIzyB8fJQ8zysMCtUY7HbluKbBxutZYD0IbMLYIuYuyfePZ3yKI12f0pe85cHxfEgatNDrcgAeBnF8KdR/SZTEXyb2BWwf43qZQbxZU62MZX petr.tichy+iphone@gooddata.com'],
    'uid': ['user.name']}

LDAP_DATA_NO_KEYS = {'ipaSshPubKey': [],
                     'uid': ['user.name']}

GERRIT_EXISTING_USER_QUERY_REPLY = u''')]}'
[
    {
      "_account_id": 1000001
    }
]
'''

GERRIT_NEW_USER_QUERY_REPLY = u''')]}'
[
]
'''

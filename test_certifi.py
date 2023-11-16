import os
os.environ['REQUESTS_CA_BUNDLE'] = '/myenv/lib/python3.11/site-packages/certifi/cacert.pem'

import certifi
print(certifi.where())

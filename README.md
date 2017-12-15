# pytaboola
Python client for Taboola API (https://github.com/taboola/Backstage-API).
Before any use of this client, you must have gotten your API client ID and client secret from yout Taboola account manager.

Client ID is required for any usage.


## Authentication and authorization

This client supports both access_token/refresh_token and
client_id/client_secret OAuth2 authorization methods.

The access_token/refresh_token method is the recommended one, but
following examples will use the other one as it is easier to implement.


### Simple Connection
Example of a simple connection using client_id/client_secret.
```python
CLIENT_ID = 'XXXXX'
CLIENT_SECRET = 'YYYYY'

from pytaboola import TaboolaClient
client = TaboolaClient(CLIENT_ID, client_secret=CLIENT_SECRET)
client.token_details
> {'account_id': 'my-taboola-account',
   'expires_in': 43189,
   'full_name': 'User Name',
   'username': 'user@mail.me'}
```

## Services
Here is a quick description of the services provided by this client.

### Account listing
A service with only one method, allowing to list advertiser accounts linked to your main Taboola account.

```python
CLIENT_ID = 'XXXXX'
CLIENT_SECRET = 'YYYYY'

from pytaboola import TaboolaClient
from pytaboola.services import AccountService
client = TaboolaClient(CLIENT_ID, client_secret=CLIENT_SECRET)
service = AccountService(client)
service.list()
> {'results': [{'account_id': 'my-first-acount',
   'campaign_types': ['PAID'],
   'id': 1111111,
   'name': 'My First Taboola Account',
   'partner_types': ['ADVERTISER'],
   'type': 'PARTNER'},
  {'account_id': 'my-other-account',
   'campaign_types': ['PAID'],
   'id': 2222222,
   'name': 'My Other Taboola Account',
   'partner_types': ['ADVERTISER'],
   'type': 'PARTNER'}]}
```

### Campaign CRUD
Simple CRUD service implementing listing, access, creation, edition.
All requests are scoped by an account. For example, It is impossible to list campaigns cross accounts.
```python
CLIENT_ID = 'XXXXX'
CLIENT_SECRET = 'YYYYY'

from pytaboola import TaboolaClient
from pytaboola.services import CammpaignService
client = TaboolaClient(CLIENT_ID, client_secret=CLIENT_SECRET)
service = CampaignService(client, 'my-account-id')
service.list()
>
```

### Reports

## Todo:
* Testing
* Service/client proxy
* Data validators
* user/password authentication method
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
This service is read-only. 

```python
CLIENT_ID = 'XXXXX'
CLIENT_SECRET = 'YYYYY'

from pytaboola import TaboolaClient
from pytaboola.services import AccountService
client = TaboolaClient(CLIENT_ID, client_secret=CLIENT_SECRET)
service = AccountService(client)
service.list()
>>> {'results': [{'account_id': 'my-first-acount',
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
All requests are scoped by an account. So, it is impossible to list campaigns cross accounts.


Service is instatiated as follow.
```python
CLIENT_ID = 'XXXXX'
CLIENT_SECRET = 'YYYYY'

from pytaboola import TaboolaClient
from pytaboola.services import CampaignService
client = TaboolaClient(CLIENT_ID, client_secret=CLIENT_SECRET)
service = CampaignService(client, 'my-account-id')
```

#### Methods
##### List all campaigns for an account :
```
service.list()
```

##### Get a campaign :
```
service.get('my-campaign-id')
```

##### Update a campaign :
```
service.get('my-campaign-id', **attrs)
```
Please note that update is partial. To delete a field, you will have to set it at None explicitely (if this attribute is nullable obviously).

##### Create a campaign :
```
service.create(**attrs)
```

In these last example, ```attrs``` is a dict containing attributes of the campaign.
For more informations on campaign attributes, please see the Backstage API documentation at
https://github.com/taboola/Backstage-API/blob/master/Backstage%20API%20-%20Campaigns.pdf


### Campaign Item CRUD
As Campaign CRUD service, this is a simple CRUD services implementing listing, access, creation, edition. 
All requests are scoped by a campaign.

```python
CLIENT_ID = 'XXXXX'
CLIENT_SECRET = 'YYYYY'

from pytaboola import TaboolaClient
client = TaboolaClient(CLIENT_ID, client_secret=CLIENT_SECRET)
service = CampaignItemService(client, 'my-account-id', 'my-campaign-id')
service.list()
```

#### Methods
Base CRUD methods are the same as the campaign service, with the same signature.

##### List all RSS Children for this campaign :
```
service.children()
```

##### Get a child item by its ID :
```
service.child('my-child-id')
```

##### Update a child :
```
service.child('my-child-id', **attrs)
```
For more informations on campaign item attributes and what are RSS Childs, please see the Backstage API documentation at
https://github.com/taboola/Backstage-API/blob/master/Backstage%20API%20-%20Campaign%20Items.pdf

### Reports

All report service have an only fetch method, which signature is :

```python
def fetch(self, dimension, start_date, end_date, **filters)
```
where dimension is the aggregation view of the report, start_date and end_date are the period to fetch the report on,
 and filters are ways to narrow down your report data.

For more information, please refer to the Backstage API documentation :
https://github.com/taboola/Backstage-API/blob/master/Backstage%20API%20-%20Reports.pdf

Available services are :
 * CampaignSummaryReport
 * TopCampaignContentReport
 * RevenueSummaryReport
 * VisitValueReport
 * RecirculationSummaryReport


## Todo:
### Resource services
Resource services are available in this client, but every endpoint are not available.
Also, it should have a proper documentation.

### Testing
There is not much intelligence in this wrapper,
but all utility functions (such as response parsing) and authentication /
refresh workflow should be tested to avoid regressions.

### Data validators
As for now, all data validation is delegated to the Taboola API. It may be usefull to had a small bit of data type checking before any call.

### Authentication
user/password authentication method is not implemented. It should be useless in any production environement,
but may be use as a fast POC/testing authentication system.

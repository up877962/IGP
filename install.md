# Creating config.yaml
In the top level directory create a file called config.py. The structure is as follows:

```yaml
network:
    server:
        domain: {string} user defined, %DOMAIN%
        port: {integer} user defined, %SERVERPORT%
        protocol: {string} web protocol, user defined, %PROTOCOL%
auth:
    SPA:
        domain: {string} from auth0, domain of application, %APPLICATIONDOMAIN%
    API:
        audience: {string} from auth0, identifier of api
    M2M:
        clientID: {string} from auth0, client ID of application, %CLIENTID%
        clientSecret: {string} from auth0, client secret of application, %CLIENTSECRET
```
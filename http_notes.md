# HTTP Notes

1. Fetch a list of products.
   Method: GET
   Expected status code: 200 OK

2. Submit a signup form.
   Method: POST
   Status code that means it worked: 201 Created (200 OK also works for some APIs)

3. Difference between 404 and 500:
   404 is a client error (4xx). The thing I asked for does not exist, for
   example a wrong URL or an id that is not there. 500 is a server error (5xx).
   My request was fine, but the server broke while handling it.

4. In https://api.store.com/orders/42?status=open
   Path: /orders/42
   Query parameter: status=open
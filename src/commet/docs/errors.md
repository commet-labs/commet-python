# Errors and request IDs

```python
from commet import CommetAPIError

try:
    commet.customers.get("cus_123")
except CommetAPIError as error:
    print(error.code)
    print(error.request_id)
    print(error.doc_url)
```

API errors expose type, code, message, status, parameter, details, the exact server request ID, and a versioned documentation URL. The installed error reference describes retry behavior. A request ID is absent when Platform did not return one and is never fabricated locally.

Preserve the same idempotency key when retrying an allowed write.

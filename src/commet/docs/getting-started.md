# Getting started

Install the SDK:

```bash
pip install commet-sdk
```

Create one server-side client. Never expose an API key to browser code.

```python
from commet import Commet

commet = Commet(api_key="ck_xxx")
```

Every resource and method in this release is generated from the versioned OpenAPI contract. Use the installed API reference instead of relying on remembered method names.

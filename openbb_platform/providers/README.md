# Providers

In this folder you can find the providers that were created or are supported by OpenBB.

## Recommended structure

Every provider is located within a directory, with the following structure:

```{.bash}
openbb_platform
└───providers
    └───<provider_name>
        |   README.md
        │   pyproject.toml
        │   poetry.lock
        |───tests
        └───openbb_<provider_name>
            │   __init__.py
            |───models
            |   |───<some model>.py
            |   └───...
            └───utils
                |───<some helper>.py
                └───...
```

The models define the data structures that are used to query the provider endpoints and store the response data.

See [CONTRIBUTING file](../CONTRIBUTING.md) for more details
\n## Upstox\n\nThe Upstox provider uses the official Upstox API. Install the `openbb-upstox` package and set your `access_token` in the credentials file to enable it.

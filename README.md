# LinodeApiManager

A small self-hosted panel for managing Linode cloud instances: a Flask API that wraps Linode's REST API v4, and a PHP front end that calls it.

## Why it exists

The Linode dashboard means clicking through a web UI for the same five operations, usually from a phone. This puts those five operations behind one token-protected HTTP call each, so a browser page (or a script) can list, create, delete and manage reverse DNS for instances.

## Pieces

| File | Role |
|---|---|
| `linodeApi.py` | `LinodeController`: Bearer-token client for Linode API v4. Lists instances (paginated, 100 per page), fetches one instance, creates an instance with a chosen region/type/image, and more. |
| `linode.py` | Standalone version of the same controller for use as a plain Python module. |
| `www/linode.php`, `create.php`, `delete.php`, `rdns.php` | PHP front end: instance table, creation form, deletion, reverse-DNS editor. |
| `www/linodeApi.py` | Copy of the Flask service that the PHP pages call. |
| `setupLinodeApi.sh` | Ubuntu install notes: dependencies, permissions for `www-data`, and a systemd unit so the API survives reboots. |

## Running it

```bash
pip install flask requests
python3 linodeApi.py          # serves the API the PHP pages talk to
```

Then serve `www/` with PHP and point it at the API. The Linode token is passed at runtime and is not stored in this repository.

## Notes

- Pagination is explicit (`page_size=100`) so a large account does not silently return the first page only.
- The systemd unit in `setupLinodeApi.sh` is the reason this can run unattended on a 5-dollar box.

## Stack

Python 3, Flask, the `requests` session API, PHP for the front end, systemd for the service. No
database: Linode itself is the only state.

## Example

The controller returns Linode's own JSON, trimmed by the caller. A single instance looks like this:

```json
{
  "id": 48211903,
  "label": "web-01",
  "region": "eu-west",
  "type": "g6-nanode-1",
  "status": "running",
  "ipv4": ["139.162.xxx.xxx"],
  "specs": { "vcpus": 1, "memory": 1024, "disk": 25600 }
}
```

Calling it directly, once the API is running:

```bash
curl -s http://localhost:5000/instances | python -m json.tool | head -20
```

## Status and licence

Working, used to manage real instances. No licence file yet: all rights reserved until one appears.

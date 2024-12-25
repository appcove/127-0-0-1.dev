# 127-0-0-1.dev - https for local development

This public repository provides a wildcard TLS certificate and key (`cert.pem` and `key.pem`) to enable HTTPS on `127-0-0-1.dev` or any subdomain of it.

## Why?

Setting up TLS on a local development environment is a nuisance.  Common options include not doing it, using a self signed certificate, or going to the effort of setting up a real certificate that points to localhost.  Even with all of these options, running multi-domain projects on localhost is an additional layer of complexity due to `*.localhost` not automatically resolving to `127.0.0.1`.

## How this fixes it?

We have registered the domain `127-0-0-1.dev` and setup two A records:

1. `127-0-0-1.dev` points to `127.0.0.1`
2. `*.127-0-0-1.dev` points to `127.0.0.1`

Additionally, we have provisioned a legitimate wildcard TLS certificate covering both, and made them available for download here.

## See it in action:

Note: requires python3 to be installed

1. clone this repository and cd into it
2. run `python3 serve-directory.py .`
3. visit `https://127-0-0-1.dev:8443/`

You should see this output:

```text
$ python3 serve-directory.py .
Visit https://127-0-0-1.dev:8443 to see files from /home/.../127-0-0-1.dev
```


## What about security?

Since the domain is only pointed to `127.0.0.1`, and no traffic is traversing the internet, there is no risk of a man-in-the-middle attack.

## How do I install it?

We recommend you just clone this repository.  That way it's a simple `git pull` to get the latest updates.

Alternatively, you can download the files directly from the repository.

## How do you recommend I use it?

For local development, we recommend you allocate specific non-privileged ports for each project.  This way you can run multiple projects on the same machine without conflicts, and without needing to run as root or setup CAP_NET_BIND_SERVICE.

For example, project 1 is a single domain project, and project 2 is a multi-domain project.


- Single-domain project:  
  `https://127-0-0-1.dev:8000/`

- Multi-domain project:  
  `https://www-example-com.127-0-0-1.dev:8001/`  
  `https://example-com.127-0-0-1.dev:8001/`

Note that the `*` in a wildcard TLS certificate is not able to span any `.` chatacters. That is why each `.` has been replaced with `-` in the domain name.

If you are setup properly to run the webserver on  443, you can omit the port number and just use the plain domain:

`https://127-0-0-1.dev/`

## Tips for projects that use multiple domains or subdomains from a database using bi-directional conversion.

We recommend you establish a function in your project for converting a plain domain name into a local development domain.  An example of this in python is:


```python
def convert_domain_to_local_dev(domain):
    return domain.replace(".", "--") + ".127-0-0-1.dev"
```

Also, a function to convert a local development domain back to a plain domain name is needed.  An example of this in python is:

```python
def convert_local_dev_to_domain(domain):
    if not domain.endswith(".127-0-0-1.dev"):
        raise ValueError("Not a local development domain")
    return domain.remove_suffix(".127-0-0-1.dev").replace("--", ".")
```

The reason for double dashes `--` is that it is very uncommon for a domain to have 2 subsequent dashes, but we need a clear way to convert back to the original `.` for purposes of database lookups.

## Tips for projects that use multiple domains or subdomains from a database using one-way conversion.

It is also possible to use a one-way conversion function, and run the same logic on the database side to find the domain in a table.  For example:

```python
def convert_domain_to_local_dev(domain):
    return domain.replace(".", "-") + ".127-0-0-1.dev"
```

And here is an example query on how to 

```sql
SELECT ... 
FROM customer_domain 
WHERE REPLACE(domain, ".", "-") || ".127-0-0-1.dev" = $1
```

If you have more than a few domains, you'd want to have an index which convers this expression.


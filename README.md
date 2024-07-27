# Web Statistics and Analytics

This package produces web statistics and analytical output based on nginx access log files.

[![PyPI package](https://img.shields.io/badge/pip%20install-a9x_webstatistics-brightgreen)](https://pypi.org/project/a9x-webstatistics/) [![version number](https://img.shields.io/pypi/v/a9x_webstatistics?color=green&label=version)](https://github.com/ava007/a9x-webstatistics/releases) [![Actions Status](https://github.com/ava007/a9x-webstatistics/workflows/Test/badge.svg)](https://github.com/ava007/a9x-webstatistics/actions) [![License](https://img.shields.io/badge/license-own-blue)](https://github.com/ava007/a9x-webstatistics/blob/main/LICENSE)

## Live Example

Visit the live example on [logikfabrik.com](https://www.logikfabrik.com/webstatsLF24.html).

## Installation

```bash
pip install a9x-webstatistics
```


## Requirements
- nginx standard access log file
- python3.9 onwards
- optional: maxmind db which need to be download by end user after registration


## Deployment

```bash
#!/bin/sh

export LOG=/usr/local/www/webstats.log
export PATH=/usr/local/www/django5/envpy311/bin:$PATH

python3.11 -m a9x_webstatistics.main \
   --infile /var/log/nginx-access.log \
   --geoip /usr/local/share/GeoIP/GeoLite2-Country.mmdb \
   --statfile /usr/local/www/lf_static/webstatsLF24.json &> $LOG

python3.11 -m a9x_webstatistics.gencockpit \
   --infile /usr/local/www/lf_static/webstatsLF24.json \
   --outfile /usr/local/www/lf_static/webstatsLF24.html &>> $LOG
```

Cron-Job Entry for Linux / FreeBSD:
```bash
#minute hour    mday    month   wday    who     command
13,58   *       *       *       *       dj1     /usr/local/www/cronjobs/cron_webstatistics.sh

```

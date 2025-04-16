# Web Statistics and Analytics

This package produces web statistics and analytical output based on nginx access log files.

[![PyPI package](https://img.shields.io/badge/pip%20install-a9x_webstatistics-brightgreen)](https://pypi.org/project/a9x-webstatistics/) [![version number](https://img.shields.io/pypi/v/a9x_webstatistics?color=green&label=version)](https://github.com/ava007/a9x-webstatistics/releases) [![Actions Status](https://github.com/ava007/a9x-webstatistics/workflows/Test/badge.svg)](https://github.com/ava007/a9x-webstatistics/actions) [![License](https://img.shields.io/badge/license-own-blue)](https://github.com/ava007/a9x-webstatistics/blob/main/LICENSE)

[![Downloads](https://img.shields.io/pypi/dm/a9x-webstatistics)](https://pypistats.org/packages/a9x-webstatistics)
[![Python](https://img.shields.io/pypi/pyversions/a9x-webstatistics)](https://pypi.org/project/a9x-webstatistics)

## Live Examples

Visit the live examples on [logikfabrik.com](https://www.logikfabrik.com/aboutwebstats.html).

<img src="https://github.com/ava007/a9x-webstatistics/blob/main/a9x-webstatistics_20241123.png">

## Installation

```bash
pip install a9x-webstatistics
```


## Requirements on Linux / Unix
- access log file from web server
  - standard access log file from nginx, freenginx or apache
  - access log file in json format
- python3.9 onwards
- optional: maxmind db which need to be download by end user after registration


## Deployment on Linux / Unix

```bash
#!/bin/sh

export LOG=/usr/local/www/webstats.log
export PATH=/usr/local/www/django5/envpy311/bin:$PATH

python3.11 -m a9x_webstatistics.main \
   --infile /var/log/nginx-access.log \
   --geoip /usr/local/share/GeoIP/GeoLite2-Country.mmdb \
   --domain https://www.logikfabrik.com \
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


## Installation on Windows

```bash
# install on windows:

## install a virtual env for python
python -m venv c:\temp\webstatsenv

## activate env
c:\temp\webstatsenv\Scripts\activate.bat

## install a9x-webstatistics
pip install a9x-webstatistics
python -m pip install --upgrade pip
python -m pip list
```

## Deployment on Windows

```bash
# run
c:
cd \temp
wget -URI https://www.logikfabrik.com/wlog/access.log -OutFile access.log

## active env
c:\temp\webstatsenv\Scripts\activate.bat

## create calculate statistics
## there are no country statistics created as not geoip defined
python -m a9x_webstatistics.main --infile access.log --statfile webstatsLF.json

## create html file for webstatistics
python -m a9x_webstatistics.gencockpit --infile webstatsLF.json --outfile webstatsLF.html
```

## Extended Example

```bash
#!/bin/sh

export LOG=/usr/local/www/webstats.log
export PATH=/usr/local/www/django5/envpy311/bin:$PATH

_YEARNUM="$(date +'%Y')";
_MONTHNUM="$(date +'%m')";

# make a archive copy for every month:
cp /usr/local/www/lf_static/webstatsLF24.json /usr/local/www/lf_static/webstatsLF24$_YEARNUM$_MONTHNUM.json
cp /usr/local/www/lf_static/webstatsLF24.html /usr/local/www/lf_static/webstatsLF24$_YEARNUM$_MONTHNUM.html

# updates all packages:
pip install -U `pip list --outdated | awk 'NR > 2 {print $1}'` >> $LOG


python3.11 -m a9x_webstatistics.main \
   --infile /var/log/nginx-access.log \
   --geoip /usr/local/share/GeoIP/GeoLite2-Country.mmdb \
   --domain https://www.logikfabrik.com \
   --statfile /usr/local/www/lf_static/webstatsLF24.json &> $LOG

python3.11 -m a9x_webstatistics.gencockpit \
   --infile /usr/local/www/lf_static/webstatsLF24.json \
   --outfile /usr/local/www/lf_static/webstatsLF24.html &>> $LOG
```
# Supported Access Log Formats



## Nginx Combined Format

predefined combined format:    access_log /.../logs/nginx-access.log combined;


## Nginx Json Format

```bash
log_format a9x_logs escape=json '{'
  '"tl":"$time_local",'
  '"ip":"$remote_addr",'                 # must; client IP
  '"rq":"$request_uri",'                 # must; full original request URI (with arguments)
  '"qs":"$query_string",'                # optional
  '"st":"$status",'                      # must; response status code
  '"ru":"$remote_user",'                 # optional; client HTTP username
  '"bs":"$bytes_sent", '                 # must; the number of bytes sent to a client
  '"rf":"$http_referer",'                # optional;
  '"rt":"$upstream_response_time", '     # optional; time spend receiving upstream body
  '"sc":"$scheme", '                     # optional; http or https
  '"ua":"$http_user_agent",'             # optional
  '"cs":"$upstream_cache_status",'       # optional
  '"al":"$http_accept_language",'        # optional
'}';

access_log     /.../log/nginx-access-log.json a9x_logs buffer=1k;
```

## Apache Combined Format


CustomLog /.../log/apache2/apache_access.log combined



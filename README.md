![MBARI logo](bin/etc/assets/logo-mbari-3b.png)

# m3-quickstart

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Release](https://img.shields.io/github/v/release/mbari-org/m3-quickstart)](https://github.com/mbari-org/m3-quickstart/releases)
[![License](https://img.shields.io/github/license/mbari-org/m3-quickstart)](LICENSE)

A simple way to run MBARI's **Video Annotation and Reference System (VARS)**, a component of MBARI's media management system (M3). The original instructions for this project are in [README_ORIGINAL.md](README_ORIGINAL.md)

> [!WARNING]
> This project is no longer supported. Users are recommended to use or migrate to <https://github.com/mbari-org/vars-quickstart-public> instead.

## Migrating to vars-quickstart-public

Migration is very straightforward. Essentially, you clone vars-quickstart-public. 

```sh
git clone https://github.com/mbari-org/vars-quickstart-mbari.git
cd vars-quickstart-mbari
```

Then copy or move the following directories:

1. Copy or move `m3-quickstart/temp/postgres` to `vars-quickstart-public/temp/postgres`
2. Copy or move `m3-quickstart/temp/framegrabs` to `vars-quickstart-public/temp/framegrabs`
3. Copy or move `m3-quickstart/temp/media` to `vars-quickstart-public/temp/media`

Finally, continue to follow the [Quick Start instructions](https://github.com/mbari-org/vars-quickstart-public?tab=readme-ov-file#quick-start) in `vars-quickstart-public`.

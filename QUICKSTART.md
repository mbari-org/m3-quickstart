# Quickstart

## Prerequisites

Install the following:

- [Docker](https://www.docker.com) - Required to launch the VARS microservices
- [Python >= 3.7](https://www.python.org) - Runs the supporting scripts. The additional python requirements are in [bin/etc/python/requirements.txt](requirements.txt)
- [ffmpeg](https://ffmpeg.org) - Required to use the python video registration scripts
- [VARS Annotation](https://github.com/mbari-org/vars-annotation/releases) - The annotation application
- A VARS Friendly-video player. It can be one of the following:
  - [Sharktopoda](https://github.com/mbari-org/Sharktopoda/releases) - macOS-only (Recommended)
  - [jsharktopoda](https://github.com/mbari-org/jsharktopoda/releases) - cross-platform

Optional:

- [Git](https://git-scm.com/) - Useful for getting the m3-quickstart code

## Start

```sh
# Get the source code.
git clone https://github.com/mbari-org/m3-quickstart.git  

# Start the web server, database, and VARS services
# The first time it's run it takes a while. Be patient.
cd m3-quickstart
bin/docker_start.sh
```

Note, that if you don't have git installed, you can download the m3-quickstart project as a zip file from <https://github.com/mbari-org/m3-quickstart>. Just click on the green "Code" button on the upper right of the web page and select Download ZIP.

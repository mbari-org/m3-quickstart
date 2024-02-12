![MBARI logo](bin/etc/assets/logo-mbari-3b.png)

# m3-quickstart

A simple and easy method to run MBARI's Video Annotation and Reference System.

## News

### February 8, 2024

We are currently doing some major updates to the backend services, [annosaurus](https://github.com/mbari-org/annosaurus/pull/41) and [vampire-squid](https://github.com/mbari-org/vampire-squid/pull/9).

f you're currently using m3-quickstart to run a VARS system, run `git pull`. Beyond that, there's no need for you to do anything at the moment. I've pinned the correct versions of the services for you to continue running VARS uninterrupted on your systems.

 Going forward, I will provide migration scripts to update PostgreSQL and SQL Server databases to work with the updated services, providing a migration path for users.

 If you are planning to set up a new VARS system in the near future, I would advise you to wait until about the end of February 2024. At that point, I will have updated this project to work with the new services, and you can run with the latest and greatest changes.

## Prerequisites

- [Docker](https://www.docker.com) - Required to launch the VARS microservices
- [Python >= 3.7](https://www.python.org) - Runs the supporting scripts. The additional python requirements are in [bin/etc/python/requirements.txt](requirements.txt)
- [ffmpeg](https://ffmpeg.org) - Required to use the pyhon video registration scripts
- [Java 17+](https://jdk.java.net/17/) - Builds the VARS Query and VARS Knowledgebase applications.
- [scala-cli](https://scala-cli.virtuslab.org) - Runs some of the supporting scripts.
- [VARS Annotation v1.5.3 or earlier](https://github.com/mbari-org/vars-annotation/releases/tag/1.5.3) - The annotation application
- A VARS Friendly-video player. It can be anyone of the following:
  - [Sharktopoda](https://github.com/mbari-media-management/Sharktopoda/releases) - macOS-only
  - [jsharktopoda](https://github.com/mbari-media-management/jsharktopoda/releases) - cross-platform
  - [Cthulhu](https://github.com/mbari-media-management/cthulhu/releases/tag/1.0.0) - macOS (amd64, not support on arm64) and Linux. This video player allows users to draw bounding boxes directly on video. Requires that [VLC](https://www.videolan.org) is installed too.

## tl;dr

### Build everyting

To get M3/VARS built and running on your own server. Do the following in a terminal:

```bash
# Get setup
git clone git@github.com:mbari-media-management/m3-quickstart.git
cd m3-quickstart

# Start the web server, database, and VARS services
# The first time it's run it takes a while. Be patient.
bin/docker_start.sh

# Builds some custom VARS apps under temp/apps
# You need GITHUB_TOKEN and GITHUB_USERNAME environment variables set.
#   see https://github.com/mbari-org/maven#gradle
export GITHUB_TOKEN=<your github token>
export GITHUB_USERNAME=<your github username>
bin/vars_build.sh

# Next steps needed to run python support scripts
pip install -r bin/etc/python/requirements.txt
```

### Next Steps

1. Open a browser to <http://localhost> to verify that things are working.
2. Run the _VARS Knowledgebase_ application. The first time it's run it will ask you to create an admin account. It will be located in `m3-quickstart/temp/apps`. __Remember your admin password!!__
3. Register your first video with VARS. You can use any video with a URL or you can put them in `m3-quickstart/temp/media` and browse to it (e.g. <http://localhost>). Once you have a URL use `bin/vars_register_media.sh` to register it in the VARS Video Asset Manager.
4. Download [VARS Annotation](https://github.com/mbari-media-management/vars-annotation/releases) and configure it as described [here](https://docs.mbari.org/vars-annotation/setup/).

Any computer on you network can connect to the VARS services you're running. You can annotate from other machines on your network.

### Clean up

If you want to shutdown the M3/VARS software stack, run `m3-quickstart/bin/docker_stop.sh`.

## Details

### Registering a video

Before a video can be annotated, VARS needs to know about it. The first step is to make your video web accessible. If you've already run `docker_start.sh`, you have a web server running that is capable of serving video. You can put the video in `m3-quickstart/temp/media` and browse to it under <http://localhost/media>.

The next step is to register the video. It's highly recommended that you follow a naming convention described [here](https://github.com/underwatervideo/UnderwaterVideoWorkingGroup/blob/master/Meetings/2016_Workshop/Documents/FINAL-2016VideoWorkshopReport.pdf). To help you get started, there's a script <bin/vars_register_media.sh> you can use to register a video with VARS. It's usage is:

```bash
cd m3-quickstart
bin/vars_register_media.sh <camera id> <deployment id> <video url>
```

- __camera-id__ - An identifier for the camera or platform that collected the video
- __deployment id__ - An identifier for the deployment of the camera
- __video url__ - The URL to your video. Don't use localhost!! You can browse to your machine using it's network name instead.

```bash
# Example
bin/vars_register_media.sh "Doc Ricketts" "Doc Ricketts 2309" "http://m3.shore.mbari.org/videos/master/2021/11/2309/D2309_20211109T132100.3Z_prores.mov"
```

### VARS Annotation

VARS Annotation will run on Window, macOS, and Linux. At MBARI, we use macOS. If you need a build of VARS Annotation for your operating system submit create a request [here](https://github.com/mbari-media-management/vars-annotation/issues)

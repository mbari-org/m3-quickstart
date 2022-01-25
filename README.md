# m3-quickstart

A simple and easy method to run MBARI's Video Annotation and Reference System.

## Prerequisites

- [Docker](https://www.docker.com) - Required to launch the VARS microservices
- [Python >= 3.7](https://www.python.org) - Runs the supporting scripts. The additional python requirements are in [bin/etc/python/requirements.txt](requirements.txt)
- [Java 17](https://jdk.java.net/17/) - Builds the VARS Query and VARS Knowledgebase applications.
- [VARS Annotation](https://github.com/mbari-media-management/vars-annotation/releases) - The annotation application
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
pip install -r bin/etc/python/requirements.txt

# Start the web server, database, and VARS services
# The first time it's run it takes a while. Be patient.
bin/docker_start.sh

# Load a phylogenetic tree of marine terms into the VARS database
bin/vars_init_kb.sh

# Builds some custom VARS apps under temp/apps
# You need GITHUB_TOKEN and GITHUB_USERNAME environment variables set.
#   see https://github.com/mbari-org/maven#gradle
vars_build.sh
```

### Next Steps

1. Open a browser to <http://localhost> to verify that things are working.
2. Run the _VARS Knowledgebase_ application. The first time it's run it will ask you to create an admin account. It will be located in `temp/apps`.
3. Register your first video with VARS. You can use any video with a URL or you can put them in `temp/media` and browse to it (e.g. <http://localhost>). Once you have a URL use `bin/vars_register_media.sh` to register it in the VARS Video Asset Manager.
4. Download [VARS Annotation](https://github.com/mbari-media-management/vars-annotation/releases) and configure it as described [here](https://docs.mbari.org/vars-annotation/setup/).

Any computer on you network can connect to the VARS services you're running. You can annotated from other machines on your network.

### Clean up

If you want to shutdown the M3/VARS software stack, run `bin/docker_stop.sh`.

## Details


### Creating a knowledgebase

A knowledgebase is used to constrain the terms and associations used for annotations. To help get you started, this project provides a script that can initialize the knowledgebase with a subset of MBARI's data. You can use this a starter to help uild and refine your own lexicon of terms. Note that this is not required, you an use the VARS knowledgebase application to build your own from scratch.

```bash
bin/vars_init_kb.sh
```

### Registering a video

Before a video can be annotated, VARS needs to know about it. The first step is to make your video web accessible. If you've already run `docker_start.sh`, you have a web server running that is capable of serving video. You can put the video in `temp/media` and browse to it under <http://localhost/media>.

The next step is to register the video. It's highly recommended that you follow a naming convention described [here](https://github.com/underwatervideo/UnderwaterVideoWorkingGroup/blob/master/Meetings/2016_Workshop/Documents/FINAL-2016VideoWorkshopReport.pdf). To help you get started, there's a script <bin/vars_register_media.sh> you can use to register a video with VARS. It's usage is:

```bash
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

![MBARI logo](bin/etc/assets/logo-mbari-3b.png)

# m3-quickstart

A simple and easy method to run MBARI's Video Annotation and Reference System.

## tl;dr

To start a web server, database, and VARS services you will need to have [Docker](https://www.docker.com) installed. Then run the following:

```sh
# Get the source code.
git clone https://github.com/mbari-org/m3-quickstart.git  

# Start the web server, database, and VARS services
# The first time it's run, it takes a while. Be patient.
cd m3-quickstart
bin/docker_start.sh
```

A default account is created as user: `admin`, pwd: `admin`. If an application asks for a configuration URL, it is typically `http://<server-running-m3-quickstarts-name>/config`. 

## Getting Started

### Software Prerequisites

#### For Services and Supporting Scripts

- [Docker](https://www.docker.com) - Required to launch the VARS microservices
- [Python >= 3.7](https://www.python.org) - Runs the supporting scripts. The additional python requirements are in [bin/etc/python/requirements.txt](requirements.txt)
- [ffmpeg](https://ffmpeg.org) - Required to use the python video registration scripts
- [Scala](https://www.scala-lang.org) - (Optional) Runs some of the supporting scripts.

#### For Basic Video Annotation

- [VARS Annotation](https://github.com/mbari-org/vars-annotation/releases) - The annotation application
- A VARS Friendly-video player. It can be one of the following:
  - [Sharktopoda](https://github.com/mbari-org/Sharktopoda/releases) - macOS-only (Recommended)
  - [jsharktopoda](https://github.com/mbari-org/jsharktopoda/releases) - cross-platform

### Next Steps

1. Open a browser to <http://localhost> to verify that things are working.
2. Register your first video with VARS. You can use any video with a URL or you can put them in `m3-quickstart/temp/media` and browse to it (e.g. <http://localhost>). Once you have a URL use `bin/vars_register_media.sh` to register it in the VARS Video Asset Manager.
3. Download [VARS Annotation](https://github.com/mbari-media-management/vars-annotation/releases) and configure it as described [in the VARS Annotation docs](https://docs.mbari.org/vars-annotation/setup/).

Any computer on you network can connect to the VARS services you're running. You can annotate from other machines on your network. You just need to know the name of the machine that you are running it on. You can test this by going to `http://<yourmachinename>`, if it's working you will see the `Welcome to the MBARI Media Managment (M3) Server` page.

### Clean up

If you want to shutdown the M3/VARS software stack, run `m3-quickstart/bin/docker_stop.sh`.

## Applications

> [!IMPORTANT]
> The web applications, VARS Query and VARS Knowledgebase Editor, work best when the web server if configured with SSL/HTTPS. We're working on providing a build and docs to help you with that.

### VARS Annotation

VARS Annotation is one of the applications used to create annotations on video. It will run on Window, macOS, and Linux. At MBARI, we use macOS. If you need a build of VARS Annotation for your operating system submit create a request [here](https://github.com/mbari-media-management/vars-annotation/issues). It requires a separate VARS-compatible video player. (See the [Prebuilt Applications section above](#Prebuilt-applications)).

### VARS Query (beta)

VARS Query is a web application that can be used to search for and retrieve annotations, videos, and images. A link to open it will be on `Welcome to the MBARI Media Managment (M3) Server` page. On a single machine you can get to that page using `http://localhost`.

### VARS Knowledgebase Editor (alpha)

VARS Knowledgebase Editor is a web application that is used to modify the knowledge-base, a lexicon and phylogenetic tree of terms that can be used to annotate in various VARS applications.

### VARS Gridview

[VARS Gridview](https://github.com/mbari-org/vars-gridview) is a bulk editing tool for reviewing and correcting bounding box annotations, such as machine learning generated annotations.

### Mondrian (alpha)

[Mondrian](https://github.com/mbari-org/mondrian) is an image annotation application. Please be aware that images must be registered in VARS before they can be annotated. There's a script for image registration in `m3-quickstart/bin/vars_register_images.sh`

## FAQ

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

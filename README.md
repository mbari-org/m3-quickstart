![MBARI logo](bin/etc/assets/logo-mbari-3b.png)

# m3-quickstart

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/) 
[![Release](https://img.shields.io/github/v/release/mbari-org/m3-quickstart)](https://github.com/mbari-org/m3-quickstart/releases)
[![License](https://img.shields.io/github/license/mbari-org/m3-quickstart)](LICENSE)

A simple way to run MBARI's **Video Annotation and Reference System (VARS)**.

---

## 📑 Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Getting Started](#getting-started)
  - [Software Prerequisites](#software-prerequisites)
  - [Next Steps](#next-steps)
  - [Clean Up](#clean-up)
- [Applications](#applications)
- [FAQ](#faq)
  - [Registering a Video](#registering-a-video)

---

## Overview

MBARI's Video Annotation and Reference System (VARS) consists of a database, a web server, multiple back-end microservices, web applications, and desktop applications.  
The **m3-quickstart** project makes it easy for organizations to spin up everything needed to get started with VARS for video and image annotation. 

---

## Quick Start

To start a web server, database, and VARS services, you’ll need [Docker](https://www.docker.com) installed. Then run:

```sh
# Get the source code
git clone https://github.com/mbari-org/m3-quickstart.git  

# Start the web server, database, and VARS services
# The first run takes a while—be patient.
cd m3-quickstart
bin/docker_start.sh
```

> [!Note]
> A default account is created as user: `admin`, pwd: `admin`. 
>
> If an application asks for a configuration URL, it is typically `http://<server-running-m3-quickstarts-name>/config`.

## Getting Started

### Software Prerequisites

#### Services and Supporting Scripts

- [Docker](https://www.docker.com) - Required to launch the VARS microservices
- [Python >= 3.7](https://www.python.org) - Required for supporting scripts. Additional requirements: [bin/etc/python/requirements.txt](requirements.txt)
- [ffmpeg](https://ffmpeg.org) - Required for the Python video registration scripts
- [Scala](https://www.scala-lang.org) - (Optional) Used by some supporting scripts.

#### For Basic Video Annotation

- [VARS Annotation](https://github.com/mbari-org/vars-annotation/releases) - The annotation application
- A VARS Friendly-video player. It can be one of the following:
  - [Sharktopoda](https://github.com/mbari-org/Sharktopoda/releases) - macOS-only (Recommended)
  - [jsharktopoda](https://github.com/mbari-org/jsharktopoda/releases) - cross-platform

### Next Steps

1. Open a browser to <http://localhost> to verify the system is running.
2. [Register your first video](#Registering-a-video):
    - Place videos in m3-quickstart/temp/media and browse to them (e.g., http://localhost/media). Note videos can be hosted on other servers and still registered in VARS too.
    - Once you have a video URL, run `bin/vars_register_media.sh` to register it in the VARS Video Asset Manager
3. Download [VARS Annotation](https://github.com/mbari-media-management/vars-annotation/releases) and configure it as described [in the setup docs](https://docs.mbari.org/vars-annotation/setup/).

> [!NOTE]
> Any computer on you network can connect to the VARS services. You can annotate from other machines on your network. Use the hostname of the machine running m3-quickstart (e.g. `http://<yourmachinename>`) for configuring the VARS Annotation app. if successful, you will see the `Welcome to the MBARI Media Managment (M3) Server` page.

### Clean up

To shut down the M3/VARS software stack, run:

```sh
m3-quickstart/bin/docker_stop.sh
```

## Applications

> [!IMPORTANT]
> The web applications, VARS Query and VARS Knowledgebase Editor, work best when the web server is configured with SSL/HTTPS. We're working on providing a build and documentation to help with this.

### VARS Annotation

Used to create annotations on video. Runs on Windows, macOS, and Linux. If you nee a build for your OS, request one [here](https://github.com/mbari-media-management/vars-annotation/issues).

Requires a VARS-compatible video player (See  ["Basic Video Annotation"](#For-Basic-Video-Annotation)).

### VARS Query (beta)

A web application for searching and retrieving annotations, videos, and images. A link is available on the Welcome to the MBARI Media Management (M3) Server page (http://localhost).

### VARS Knowledgebase Editor (alpha)

A web application for editing the knowledge base (lexicon and phylogenetic tree of annotation terms). A link is available on the Welcome to the MBARI Media Management (M3) Server page (http://localhost).

### VARS Gridview

[VARS Gridview](https://github.com/mbari-org/vars-gridview) is a bulk editing tool for reviewing and correcting bounding box annotations, such as machine learning generated annotations.

### Mondrian (alpha)

[Mondrian](https://github.com/mbari-org/mondrian) is an image annotation application.

> [!IMPORTANT]
> Images must be registered in VARS before they can be annotated. Use: `m3-quickstart/bin/vars_register_images.sh`

## FAQ

### What's M3?

M3 stands for "MBARI Media Managment". VARS (the Video Annotation and Reference System) is the largest component of M3.

### Registering a Video

Before annotating, VARS must know about your video.

1. Make the video web-accessible.
    - If you’ve run docker_start.sh, the included web server can serve videos.
    - Place videos in m3-quickstart/temp/media and browse to them at http://localhost/media.
2. Register the video with VARS.
    - Follow the recommended naming convention.
    - Use the helper script:

```bash
cd m3-quickstart
bin/vars_register_media.sh <camera id> <deployment id> <video url>
```

- __camera-id__ - An identifier for the camera or platform that collected the video.
- __deployment id__ - An identifier for the deployment of the camera.
- __video url__ - The URL to your video. (Do not use `localhost`; use the machine's hostname instead).

```bash
# Example
bin/vars_register_media.sh "Doc Ricketts" "Doc Ricketts 2309" "http://m3.shore.mbari.org/videos/master/2021/11/2309/D2309_20211109T132100.3Z_prores.mov"
```

## 🤝 Contributing

Contributions are welcome!

- Found a bug? Open an [issue](https://github.com/mbari-org/m3-quickstart/issues).
- Want to add a feature or fix something? Submit a [pull request](https://github.com/mbari-org/m3-quickstart/pulls).
- For larger changes, please start a discussion in the issues first.

When contributing:

1. Fork the repo and create a feature branch (git checkout -b feature/your-feature).
2. Make your changes with clear commit messages.
3. Run tests and ensure everything works.
4. Open a pull request describing your changes.

## 📜 License

This project is licensed under the [MIT License]().

# Syncthing for hass.io

![Addon Stage][stage-badge]
![Supports aarch64 Architecture][aarch64-badge]
![Supports amd64 Architecture][amd64-badge]
![Supports armhf Architecture][armhf-badge]
![Supports armv7 Architecture][armv7-badge]
![Supports i386 Architecture][i386-badge]

[![Add repository on my Home Assistant][repository-badge]][repository-url]
[![Install on my Home Assistant][install-badge]][install-url]
[![Sponsor][sponsor-badge]][sponsor-url]

[aarch64-badge]: https://img.shields.io/badge/aarch64-yes-green.svg?style=for-the-badge
[amd64-badge]: https://img.shields.io/badge/amd64-yes-green.svg?style=for-the-badge
[armhf-badge]: https://img.shields.io/badge/armhf-yes-green.svg?style=for-the-badge
[armv7-badge]: https://img.shields.io/badge/armv7-yes-green.svg?style=for-the-badge
[i386-badge]: https://img.shields.io/badge/i386-yes-green.svg?style=for-the-badge
[stage-badge]: https://img.shields.io/badge/Addon%20stage-stable-green.svg?style=for-the-badge
[install-badge]: https://img.shields.io/badge/Install%20on%20my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge
[sponsor-badge]: https://img.shields.io/badge/Sponsor-%23d32f2f?logo=github&style=for-the-badge&logoColor=white
[sponsor-url]: https://github.com/sponsors/agileek
[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge

[install-url]: https://my.home-assistant.io/redirect/supervisor_addon?addon=243ffc37_syncthing
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fagileek%2Fhassio-addons

## Description

This addon provide a [syncthing](https://syncthing.net/) container for hass.io.

> Syncthing replaces proprietary sync and cloud services with something open, trustworthy and decentralized. Your data is your data alone and you deserve to choose where it is stored, if it is shared with some third party and how it's transmitted over the Internet.

When creating a new folder with the webui, you must set the folder path to something that will be persistent in case of container reboot/upgrade. You can use any of the following path :

 - `/data/<subfolder/path>` : `subfolder/path` will be created in the addon persistent volume,
 - `/data/<subfolder/path>` : `subfolder/path` will be created in the share directory, which can be accessed with samba,
 - `/config` : to synchronize home assistant configuration,
 - `/backup` : to synchronize home assistant backups,
 - `/addons` :  to synchronize hassio addons.
 
## Configuration
There are no configuration options.

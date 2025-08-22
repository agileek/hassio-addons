# Signal integration

![Addon Stage][stage-badge]
![Supports aarch64 Architecture][aarch64-badge]
![Supports amd64 Architecture][amd64-badge]
![Supports armv7 Architecture][armv7-badge]
![Supports i386 Architecture][i386-badge]

[![Add repository on my Home Assistant][repository-badge]][repository-url]
[![Install on my Home Assistant][install-badge]][install-url]
[![Sponsor][sponsor-badge]][sponsor-url]

[aarch64-badge]: https://img.shields.io/badge/aarch64-yes-green.svg?style=for-the-badge
[amd64-badge]: https://img.shields.io/badge/amd64-yes-green.svg?style=for-the-badge
[armv7-badge]: https://img.shields.io/badge/armv7-yes-green.svg?style=for-the-badge
[i386-badge]: https://img.shields.io/badge/i386-yes-green.svg?style=for-the-badge
[stage-badge]: https://img.shields.io/badge/Addon%20stage-stable-green.svg?style=for-the-badge
[install-badge]: https://img.shields.io/badge/Install%20on%20my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge
[sponsor-badge]: https://img.shields.io/badge/Sponsor-%23d32f2f?logo=github&style=for-the-badge&logoColor=white
[sponsor-url]: https://github.com/sponsors/agileek
[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge

[install-url]: https://my.home-assistant.io/redirect/supervisor_addon?addon=4a36bbd1-signal
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fagileek%2Fhassio-addons

## Setup

### The signal-cli data

First, follow https://github.com/AsamK/signal-cli

Once you registered your phone number on signal-cli, move the storage (https://github.com/AsamK/signal-cli#storage) in the configuration folder of home assistant.

You should have something like that

```bash
/config
└── .signal
    ├── attachments
    ├── avatars
    └── data
        ├── +331234567
        └── +331234567.d
```
After that, you can install the hassio signal addon

### The home assistant plugin

You have to install the homeassistant part too, if you want it to work.
This part right now is a manual process, I don't know if we can automate it.

Just copy signalmessenger to the custom_components folder in your configuration directory
`cp -R signalmessenger/ /config/custom_components/signalmessenger/`

Activate the plugin in your configuration.yaml 

```
signalmessenger:
notify:
  - name: signal
    platform: signalmessenger
    destinations: 
        - '+the_number_receiving_the_notifications'
        - 'the_group_id_receiving_the_notifications'
```

restart home assistant and it should work.

You can try it in by calling the `notify.signal` service in the developer tools

![Developer Tools](images/developer_tools_yaml.png?raw=true "Developer Tools")


## Usage

You can for example create an automation to send a message when a door is opened:

```
- id: 'door-opened'
  alias: Door opened
  trigger:
  - entity_id: binary_sensor.front_door
    platform: state
    from: 'off'
    to: 'on'
  condition: []
  action:
  - alias: ''
    data:
      message: Door opened
    service: notify.signal
```

Or send a screenshot when a movement is detected
```
- id: 'movement-detected'
  alias: Movement detected
  trigger:
  - entity_id: binary_sensor.terrace_sensor
    platform: state
    from: 'off'
    to: 'on'
  condition: []
  action:
  - alias: ''
    data:
      message: Who is it?
      data:
        file: /path/to/my/screenshot.png
    service: notify.signal
```

### Groups

You can send messages to groups. The tricky part here is to get the group Id.

To do that, a service exists that lists the different groups the user is in.

![Groups](images/get_groups.png?raw=true "Retrieve Groups")

This will log something like that in home assistant:

```
2019-12-16 08:51:41 INFO (SyncWorker_18) [custom_components.signalmessenger] retrieve groups (status: 200), {'GroupName': 'hexadecimalgroupid1', 'Group name 2': 'hexadecimalgroupid2'}
```

Once you have the group ids, you can easily send messages by using the `notify.signal` service. Just use the groupid in the target parameter.

![Send to Group](images/send_to_group.png?raw=true "Send to group")


### Talking to homeassistant

Added in 10.6.0, you can now talk to homeassistant using intents.

If you are not familiar with intents, here is a quick setup to see if everything works fine.

First, Configure your conversations:

```yaml
conversation:
  intents:
    Test:
      - Test
      - This is a test
```

Then configure your intents replies:
```yaml
intent_script:
  Test:
    speech:
      text: "Hello there"
```

Once home assistant is restarted, by sending `Test` or `This is a test` to signal, you should get `Hello there`.

## Docker image deployment

Deployed using `docker run --rm --privileged -v ~/.docker:/root/.docker:ro -v $PWD:/data homeassistant/amd64-builder --all -t /data`

## Dbus debug

look into the man page https://github.com/AsamK/signal-cli/blob/master/man/signal-cli-dbus.5.adoc

* list identities : dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.listIdentities
* get identity information: `dbus-send --system --dest=org.asamk.Signal --print-reply $OBJECT_PATH org.freedesktop.DBus.Properties.GetAll string:org.asamk.Signal.Identity`
* trust number: `dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" $OBJECT_PATH org.asamk.Signal.trust`
* trust verify : `dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" $OBJECT_PATH org.asamk.Signal.trustVerified string:"LIST OF NUMBERS"`

where OBJECT_PATH is obtained with the listIdendities


## [Changelog](CHANGELOG.md)

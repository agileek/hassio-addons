# Signal integration


## Setup

### The signal-cli data

First, follow https://github.com/AsamK/signal-cli

Once you registered your phone number on signal-cli, move the storage (https://github.com/AsamK/signal-cli#storage) in the configuration folder of home assistant.

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
        - 'the_group_id_receiveng_the_notifications'
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



## [Changelog](CHANGELOG.md)

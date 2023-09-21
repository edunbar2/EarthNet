import {writable} from "svelte/store"

const found_devices = writable(
    [
        {"ip": "192.168.1.1", "type": "", "vendor": "Cisco", "os": ""},
        {"ip": "192.168.1.128", "type": "", "vendor": "Cisco", "os": ""},
        {"ip": "192.168.1.59", "type": "", "vendor": "Juniper", "os": ""},
        {"ip": "192.168.1.1", "type": "", "vendor": "Cisco", "os": ""},
        {"ip": "192.168.1.128", "type": "", "vendor": "Cisco", "os": ""},
        {"ip": "192.168.1.59", "type": "", "vendor": "Juniper", "os": ""},
        {"ip": "192.168.1.1", "type": "", "vendor": "Cisco", "os": ""},
        {"ip": "192.168.1.128", "type": "", "vendor": "Cisco", "os": ""},
        {"ip": "192.168.1.59", "type": "", "vendor": "Juniper", "os": ""}


    ]
);

export default found_devices;
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from scapy.all import ARP, Ether, srp
from manuf import manuf
import netifaces
import ipaddress
import concurrent.futures

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://10.11.12.26:5173"}})

@app.route('/')
def home():
    return "hello, world"



def get_vendor_of_ip(target_ip):
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff") # Broadcast ethernet frame
    packet = ether/arp
    result = srp(packet, timeout=1, verbose=0)[0]
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        mac_parser = manuf.MacParser()
        vendor = mac_parser.get_manuf(mac)
        if vendor:
            return vendor
        else:
            return "invalid vendor"

def get_all_ip_addresses():
    ip_info = {}
    for interface_name in netifaces.interfaces():
        try:
            interface_info = netifaces.ifaddresses(interface_name)
            if netifaces.AF_INET in interface_info:
                if '127' in interface_info[netifaces.AF_INET][0]['addr'].split('.')[0]:
                        continue
                ip_info[interface_name] = {
                    'ip_address': interface_info[netifaces.AF_INET][0]['addr'],
                    'subnet_mask': interface_info[netifaces.AF_INET][0]['netmask']
                }
        except (KeyError, ValueError):
            pass
    return ip_info

def get_ip_range(ip_str, subnet_mask):
    ip = ipaddress.IPv4Address(ip_str)
    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)

    ip_list = [str(ip) for ip in network.hosts()]
    return ip_list


def get_network_devices():
    num_threads = 256
    all_ip_info = get_all_ip_addresses()

    if all_ip_info:
        for interface, info in all_ip_info.items():
            print(f"Interface: {interface}")
            print(f"IP Address: {info['ip_address']}")
            print(f"Subnet Mask: {info['subnet_mask']}")

            ip_list = get_ip_range(info['ip_address'], info['subnet_mask'])
            # Number of threads to use for concurrent execution

        # Use ThreadPoolExecutor to process IP addresses concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Map the get_vendor function to each IP address and retrieve the results
            results = list(executor.map(get_vendor_of_ip, ip_list))

        # print(results)

        accepted_vendors = ['Cisco', 'Juniper']
        viable_devices = []
        for ip, vendor in zip(ip_list, results):
            if vendor in accepted_vendors:
                viable_devices.append({"ip": ip, "vendor": vendor})
#             print(f"IP: {ip}, Vendor: {vendor}")

        # Print the results
        return viable_devices
    else:
        print("No active network interfaces found.")

@app.route('/update_device_list', methods=['GET'])
@cross_origin()
def update_device_list():
    print("Gathering updated list...")
    viable_devices = { "data": get_network_devices() }
    print(f"Devices Updated, Printing Devices: {jsonify(viable_devices)}")
    return jsonify(viable_devices)




@app.route('/handle_form_data', methods=['POST'])
@cross_origin()
def handle_form_data():
    print("starting...")
    data = request.get_json()
    print(request)
    print("getting data")
    login_information = data['login_information']
    devices = data['devices']
    tool_config_script = data['tool_config_script']
    manual_script = data['manual']
    config_type = data['config_type']

    script = []
    if manual_script: script = tool_config_script.slice("\n")
    
    else: 
        print(f"Starting config with {tool_config_script} and config type: {config_type}")
        if 'cisco' in devices[0]['os']:
            script = parse_cisco_commands(tool_config_script, config_type)
        elif 'juniper' in devices[0]['os']:
            script = parse_juniper_commands(tool_config_script, config_type)

        print(f"Converted to commands appropriate for {devices[0]['os']}")
    try:
    # configure devices with login_info, devices, and parsed commands
        data = configure_devices(devices, login_information, script)
        return_data = {
            'success': True,
            'message': "Devices were successfully configured",
            'data': data

         }     
    except Exception as e:
        print("Error in configuring devices")
        return_data = {
            'success' : False,
            'message': "One or more devices were not successfully configured.",
            'data' : e
        }
    print("testing print")
    print("returning data", jsonify(return_data))
    return jsonify(return_data)
    # return jsonify({'success': True, 'message': "Succeeded in connecting", 'data': 'yay'})

def configure_devices(devices, login_info, config_commands):
    data = {}  # to store the running config data for all devices
    for device in devices:
        device_info = {
            'device_type': device['os'],
            'ip': device['ip'],
            'username': login_info['username'] if len(login_info['username']) > 0 else None,
            'password': login_info['password'],
            'secret': login_info['secret'],
            'port': 22 if "telnet" not in device['os'] else 23,
            'verbose': False,
        }

        if device['device_type'] == "":
            device['device_type'] = 'autodetect'
            guesser = SSHDetect(**remote_device)
            best_match = guesser.autodetect()
            device['device_type'] = best_match

        if device['vendor'] == 'Cisco':
            if device['os'] == 'cisco_ios' or device['os'] == 'cisco_ios_telnet':
                net_connect = ConnectHandler(**device_info)
                net_connect.enable()
                output = net_connect.send_config_set(config_commands)
                # Save running config on device
                net_connect.send_command_expect('write memory')
                # Get running config from device
                running_config = net_connect.send_command_expect('show running-config')
                data[device['ip']] = running_config
                print('Configuration output for device ' + device['ip'] + ':\n' + output)
                net_connect.disconnect()
            else:
                print('Unsupported operating system: ' + device['os'])
        else:
            print('Unsupported vendor: ' + device['vendor'])

    return data

def parse_juniper_commands(config_obj, config_type):
    cmds = []

    if config_type == 'interface config':
        cmds.append(f'set interfaces {config_obj["interface_name"]} unit 0 family inet address {config_obj["ip_address"]}/{config_obj["subnet_mask"]}')
        cmds.append(f'set interfaces {config_obj["interface_name"]} description "{config_obj["description"]}"')

    elif config_type == 'static routing':
        cmds.append(f'set routing-options static route {config_obj["destination_network"]}/{config_obj["subnet_mask"]} next-hop {config_obj["next_hop"]}')

    elif config_type == 'dynamic routing':
        cmds.append(f'set protocols {config_obj["routing_protocol"]} router-id {config_obj["router_id"]}')
        cmds.append(f'set protocols {config_obj["routing_protocol"]} area {config_obj["area_id"]} interface {config_obj["interface"]}')
        if config_obj['ospf_leader']:
            cmds.append('set protocols {config_obj["routing_protocol"]} area {config_obj["area_id"]} interface {config_obj["interface"]} priority 255')

    elif config_type == 'vlan config':
        if config_obj['delete']:
            cmds.append(f'delete vlans {config_obj["vlan_id"]}')
        else:
            cmds.append(f'set vlans {config_obj["vlan_id"]} vlan-id {config_obj["vlan_id"]}')
            cmds.append(f'set vlans {config_obj["vlan_id"]} l3-interface vlan.{config_obj["vlan_id"]}')
            cmds.append(f'set vlans {config_obj["vlan_id"]} description "{config_obj["vlan_description"]}"')
            if not config_obj['vlan_state']:
                cmds.append(f'set vlans {config_obj["vlan_id"]} l3-interface vlan.{config_obj["vlan_id"]} disable')
            if config_obj['vlan_mtu'] != "-1":
                cmds.append(f'set vlans {config_obj["vlan_id"]} mtu {config_obj["vlan_mtu"]}')
            if config_obj['vlan_ip_address'] != "":
                cmds.append(f'set interfaces vlan unit 0 family inet address {config_obj["vlan_ip_address"]}/{config_obj["vlan_ip_mask"]}')
            for intf in config_obj['vlan_tagged_interfaces']:
                cmds.append(f'set interfaces {intf} unit 0 family ethernet-switching interface-mode trunk')
                cmds.append(f'set interfaces {intf} unit 0 family ethernet-switching vlan members {config_obj["vlan_id"]}')
            for intf in config_obj['vlan_untagged_interfaces']:
                cmds.append(f'set interfaces {intf} unit 0 family ethernet-switching interface-mode access')
                cmds.append(f'set interfaces {intf} unit 0 family ethernet-switching vlan members {config_obj["vlan_id"]}')

    elif config_type == 'vtp config':
        # Juniper does not have an equivalent to Cisco's VTP, so this part is left empty
        pass

    else:
        raise ValueError('Invalid configuration type: ' + config_type)

    return cmds


def parse_cisco_commands(config_obj, config_type):
    if config_type == 'interface config':
        cmds = []
        cmds.append("interface " + config_obj['interface_name'])
        cmds.append("ip address " + config_obj['ip_address'] + " " + config_obj['subnet_mask'])
        cmds.append("description " + config_obj['description'])
        return cmds

    elif config_type == 'static routing':
        cmds = []
        cmds.append("ip route " + config_obj['destination_network'] + " " + config_obj['subnet_mask'] + " " + config_obj['next_hop'])
        return cmds

    elif config_type == 'dynamic routing':
        cmds = []
        cmds.append(config_obj['routing_protocol'] + " router")
        cmds.append("network " + config_obj['network'] + " " + config_obj['subnet_mask'])
        cmds.append("interface " + config_obj['interface'])
        cmds.append("area " + config_obj['areas'])
        if config_obj['ospf_leader']:
            cmds.append("ospf priority 255")
        return cmds

    elif config_type == 'vlan config':
        cmds = []
        if config_obj['delete']:
            cmds.append("no vlan " + config_obj['vlan_id'])
        else:
            cmds.append(f"vlan {config_obj['vlan_id']}")
            cmds.append(f"name {config_obj['vlan_name']}")
            cmds.append(f"description {config_obj['vlan_description']}")
            if not config_obj['vlan_state']:
                cmds.append("shutdown")
            if config_obj['vlan_mtu'] != "-1":
                cmds.append(f"mtu {config_obj['vlan_mtu']}")
            if config_obj['vlan_ip_address'] != "":
                cmds.append("ip address {config_obj['vlan_ip_address']} {config_obj['vlan_ip_mask']}")
            for intf in config_obj['vlan_tagged_interfaces']:
                cmds.append(f"interface {intf}")
                cmds.append("switchport mode trunk")
                cmds.append(f"switchport trunk allowed vlan add {config_obj['vlan_id']}")
            for intf in config_obj['vlan_untagged_interfaces']:
                cmds.append(f"interface {intf}")
                cmds.append("switchport mode access")
                cmds.append(f"switchport access vlan {config_obj['vlan_id']}")
        return cmds

    elif config_type == 'vtp config':
        cmds = []
        if config_obj['vtp_domain'] != "":
            cmds.append("vtp domain " + config_obj['vtp_domain'])
        if config_obj['vtp_password'] != "":
            cmds.append("vtp password " + config_obj['vtp_password'])
        return cmds

    else:
        raise ValueError('Invalid configuration type: ' + config_type)



if __name__ == '__main__':
    app.run(host='10.11.12.26', port=5000, debug=True)

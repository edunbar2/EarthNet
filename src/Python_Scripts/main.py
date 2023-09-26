from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from netmiko import ConnectHandler

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "hello, world"

@app.route('/update_device_list')
@cross_origin()
def update_device_list():
    print("Gathering updated list...")



@app.route('/handle_form_data', methods=['POST'])
@cross_origin()
def handle_form_data():
    print("starting...")
    data = request.get_json()
    login_information = data['login_information']
    devices = data['devices']
    tool_config_script = data['tool_config_script']
    manual_script = data['manual']
    config_type = data['config_type']

    
    if manual_script: script = tool_config_script.slice("\n")
    
    else: 
        print(f"Starting config with {tool_config_script} and config type: {config_type}")
        script = parse_commands(tool_config_script, config_type)
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


def parse_commands(config_obj, config_type):
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
    app.run()

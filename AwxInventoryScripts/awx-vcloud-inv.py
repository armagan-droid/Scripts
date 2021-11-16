#!/usr/bin/env python3
import sys
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vapp import VApp
from pyvcloud.vcd.vm    import VM
import sys
import json

host = 'vcloud.vmware.local'
org = '12345212'
user = 'readonlyuser'
password = 'TopSecret'
vdc = 'OVDC-12345212-LNDC01-12345212'


def parse_arg(argument):
    try:
        if len(argument) == 6 and argument == "--list":
            return "list"
        elif len(argument) == 6 and argument == "--host":
            return "host"
        else:
            print("Please use one of these arguments '--list' or '--host'")
            return False       
    except:
        print('Something went wrong..')

def get_all_host(host, org, user, password, vdc):

    #Linux guest hosts
    linux_os_list = ['CentOS 7 (64-bit)', 'Ubuntu Linux (64-bit)', 'CentOS 8 (64-bit)']

    #Windows guest hosts
    win_os_list = ['Microsoft Windows Server 2016 or later (64-bit)', 'Microsoft Windows Server 2019 (64-bit)']

    #Host list of all Vapps
    host_list = {}


    client = Client(host,
                verify_ssl_certs=True,#SSL 
                log_requests=False,
                log_headers=False,
                log_bodies=False)
    client.set_highest_supported_version()
    client.set_credentials(BasicLoginCredentials(user, org, password))

    org_resource = client.get_org()
    org = Org(client, resource=org_resource)

    vdc_resource = org.get_vdc(vdc)
    vdc = VDC(client, resource=vdc_resource)

    vapps = vdc.list_resources()

    win_list = []
    linux_list = []
    other_os_list = []
    hostvars = {}
    for vapp in vapps:
        if vapp["type"] == "application/vnd.vmware.vcloud.vApp+xml":
            currentHref = vdc.get_vapp_href(vapp["name"])
            currentVapp = VApp(client, href=currentHref)
            for vm in currentVapp.get_all_vms():
                vmName = vm.get('name')
                vmOs = VM(client, resource=vm)
                vmIp = currentVapp.get_primary_ip(vmName)
                vOs = vmOs.get_operating_system_section()
                if vmIp is not None:
                    if vOs.Description in win_os_list:
                        win_list.append(vmName)
                        hostvars.update({vmName:{'ansible_host':vmIp}})
                    elif vOs.Description in linux_os_list:
                        linux_list.append(vmName)
                        hostvars.update({vmName:{'ansible_host':vmIp}})
                    else:
                        other_os_list.append(vmName)
                        hostvars.update({vmName:{'ansible_host':vmIp}})
                    host_list.update({'windows':{'hosts':win_list}})
                    host_list.update({'linux':{'hosts':linux_list}})
                    host_list.update({'others':{'hosts':other_os_list}})
                    host_list.update({'_meta':{'hostvars':hostvars}})
    return host_list
def get_host():
    return {'_meta': {'hostvars': {}}}

if __name__ == "__main__":
    if parse_arg(sys.argv[1]) == "list":
        h_list = get_all_host(host, org, user, password, vdc)
        print(json.dumps(h_list))
    elif parse_arg(sys.argv[1]) == "host":
        h = get_host()
        print(json.dumps(h))
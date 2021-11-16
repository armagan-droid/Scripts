# Vcloud Inventory Script For Ansible AWX 

This python3 script is a custom inventory script for Ansible Awx.

## Installation

Use the package manager [pip](https://pypi.org/project/pyvcloud/) to install pyvcloud in the awx task container or add to Dockerfile of the awx task.

```bash
pip install pyvcloud
```

## Usage

```python
host = 'vcloud.vmware.local'
org = '12345212'
user = 'readonlyuser'
password = 'TopSecret'
vdc = 'OVDC-12345212-LNDC01-12345212'

#Linux guest host os systems
linux_os_list = ['CentOS 7 (64-bit)', 'Ubuntu Linux (64-bit)', 'CentOS 8 (64-bit)']

#Windows guest host os systems
win_os_list = ['Microsoft Windows Server 2016 or later (64-bit)', 'Microsoft Windows Server 2019 (64-bit)']

```

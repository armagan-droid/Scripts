#Powershell , Bash and Python scripts.
#remove uuid from ifcfg scripts
/bin/sed -i '/^(HWADDR|UUID)=/d' /etc/sysconfig/network-scripts/ifcfg-ens192

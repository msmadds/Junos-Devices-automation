from jnpr.junos import Device
from lxml import etree
from pprint import pprint
import getpass

def software_check(host, username, password, port):
    """function to get the software details for the given host"""
    with Device(host=host, user=username,  password=password, port=port, gather_facts=False) as dev:
        
        # To print to content of object returned, use below function (etree.tostring)
        raw_data = dev.rpc.get_software_information({'format':'text'})
        
        data_str = str(etree.tostring(raw_data)) 
        data = data_str.split('\\n')
        with open('software_info.txt','a') as file:
            for line in data:
                if 'Hostname' in line:
                    file.write(line)
                    file.write('\t')
                elif 'Model' in line:
                    file.write(line)
                    file.write('\t')                    
                elif 'Junos:' in line:
                    file.write(line+'\n')           
                            
def main():
    """main function"""
    host_file = 'hosts.txt'
    password= getpass.getpass()
    username = input("Enter the username: ")
    port ='22'
    with open(host_file, 'r') as file:
        hosts = file.readlines()
        for host in hosts:
            software_check(host.strip('\n'),username, password, port)
    
    
if __name__ == '__main__':
    main()

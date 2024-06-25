from jnpr.junos import Device
from lxml import etree
from pprint import pprint
import getpass


def get_license_info(host, username, password,port):
    with Device(host=host, user=username, password=password, port=port, gather_facts=False) as dev:
        # rpc call to return object in text format, and the data type for op will be  bytes
        output= dev.rpc.get_license_summary_information({'format':'text'})
        # To print object returned as bytes, uncomment below line (etree.tostring)
        #pprint (etree.tostring(output))
        #to assign the output to a variable so we can manipulate the output
        license_ = etree.tostring(output)
        output = str(license_)
        output_=output.split('\\n')
        for line in output_:
            print(line)
    
def main():
    password  = getpass.getpass()
    username = input("insert username: ")
    host= 'x.x.x.x'
    port = '22'  #incase the device is not using the default netconf port
    get_license_info(host,username,password,port)

if __name__ == '__main__':
    main()





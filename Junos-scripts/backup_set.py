#Importing the needed Libraries

from jnpr.junos import Device
from jnpr.junos.exception import *
import getpass
from datetime import datetime
from lxml import etree
from jnpr.junos.utils.config import Config
import os


def config_check(host,username,password,port):
    """Retrieving the configuration, and send the config into a folder. The configuration in format of set. But """
    
    try:
        #if the netconf port used is the default value, remove the port in below
        with Device(host=host, user =username, password= password, port=port) as dev:
            data= dev.rpc.get_config(options= {'format':'set'})
            date = datetime.now().strftime('%D').replace('/','_')
            host_ = get_hostname(host,username, password, port) #get the hostname to use in the naming for the config file
            try:
                os.makedirs(datetime.now().strftime('%D').replace('/','_')) #create the folder to store the configs backup for that day
                config_file = datetime.now().strftime('%D').replace('/','_') +'/'+  host_+'_'+date+'.txt'
                with open(config_file, 'w') as f:
                    f.write(etree.tostring(data, encoding ='unicode', pretty_print=True))
            except FileExistsError:  #if the folder exist this code will run to store the config backup in that folder
                config_file = datetime.now().strftime('%D').replace('/','_') +'/'+  host_+'_'+date+'.txt'
                with open(config_file, 'w') as f:
                    f.write(etree.tostring(data, encoding ='unicode', pretty_print=True))
            
            #uncomment below if you want to display the config on the terminal.
            #print(etree.tostring(data, encoding ='unicode', pretty_print=True))
    except ConnectAuthError:
        #if the Authentication fail due to the fact that not all device use the same login, you can use
        #this exception to insert a new username, and/or password. Comment and uncomment the part needed
        username = input (f"Insert the username for {host}: ")
        password = getpass.getpass(f"Enter the password for this {host}: ")
      
        #if the netconf port used is the default value, remove the port in below
        with Device(host=host, user=username, password=password, port=port) as dev:
            data= dev.rpc.get_config(options= {'format':'set'})
            date = datetime.now().strftime('%D').replace('/','_')
            host_ = get_hostname(host,'madeline', password, port)
            try:
                os.makedirs(datetime.now().strftime('%D').replace('/','_'))
                config_file = datetime.now().strftime('%D').replace('/','_') +'/'+  host_+'_'+date+'.txt'
                with open(config_file, 'w') as f:
                    f.write(etree.tostring(data, encoding ='unicode', pretty_print=True))                

            except FileExistsError:  
                config_file = datetime.now().strftime('%D').replace('/','_') +'/'+  host_+'_'+date+'.txt'
                with open(config_file, 'w') as f:
                    f.write(etree.tostring(data, encoding ='unicode', pretty_print=True))

        
    except RpcTimeoutError:
        """ When timeout occur, when running the RPC, this error handling will capture that"""
        print("RPC execution timeout, waiting %s, to try again"%hold_time)

  
    except RpcError:
        print("RPC error, kindly check the call")
      
    except SyntaxError:
      print("Syntax error")
      
                

def get_hostname(host, username, password, port):
    """ To retrive the hostname for the device"""
    #if the netconf port used is the default value, remove the port in below
    with Device (host=host, user =username,password=password, port=port) as dev:
        data = dev.facts
        for k, v in data.items():
            if k == 'hostname':
                return v

           
def main():
    #main function
    host_file = 'HOSTS.txt' #file that contains the address of the devices you want to connect to
    username = 'USERNAME' #replace with a username to login to the devices
    #uncomment below to input the username
    #username = input("Enter the username: ")
    password = getpass.getpass()
    port = 'PORT' #insert the netconf port incase the netconf was configured to use nondefault port, default port for netconf is 830
    #open the host_file
    with open(host_file, 'r') as f:
            hosts = f.readlines()
      
            for host in hosts:
                config_check(host.strip('\n'),username,password,port) #the strip method is called to the remove the newline character

        
if __name__ =="__main__":
    main()

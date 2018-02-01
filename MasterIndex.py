import ipaddress
import netmiko
import pathlib
import datetime
from netmiko import ConnectHandler
now_time = datetime.datetime.now()
import pip

def import_or_install_packages():
    try:
        __import__("netmiko")
    except ImportError:
        print("Please Connect To internet for downloading Python Modules and Run the program again")

        pip.main(['install', package])


def menu_show():
        first_menu = "1. Test Connectivity of Devices"
        second_menu = "2. Backup running-config of devices"
        third_menu = "3. Ping test from devices to specific IP address"
        forth_menu = "4. Inject config to devices with input or CSV file"
        fifth_menu = "5. Search in Range of routers"
        user_selection = input("Please insert your choice: ")



def ip_loop_maker(start_ip,end_ip):

    for ip_int in range(int(start_ip), int(end_ip)):
        print(ipaddress.IPv4Address(ip_int))

def backups(ip,user_name,pass_word):
    try:
        session = ConnectHandler( device_type='cisco_ios', ip=ip , username=user_name , password=pass_word)
        output = session.send_command("terminal lenght 0")
        running_config = session.send_command("show running-config")
        pathlib.Path('./backups').mkdir(parents=True, exist_ok=True)
        with open("./backups/backp %s.txt" % ip, "a") as backups_file:
            backups_file.write("\n\n\n ****IP = %s \n\n\n" % ip + running_config + "\n\n\n!!!End of Backup in "+str(now_time)+"!!!\n\n")
        backups_file.close()
        session.disconnect()

    except netmiko.NetMikoAuthenticationException:
        print ("%s Not connected - TACACS problem" % ip)

    except netmiko.NetMikoTimeoutException:
        print (" %s Time Out" % ip)

    except socket.error('Socket is closed'):
        print ("NO SSH")
    #end of backups Def

def get_ip(ip, unit_ip, username, password):
    try:
        user_name = username
        pass_word = password
        session = ConnectHandler( device_type='cisco_ios', ip=ip , username=user_name , password=pass_word)
        command_make = "sh run | inc ip address 10."
        output = session.send_command(command_make)
        print (output)
        with open("IP.txt", "a") as backups_file:
             backups_file.write(output + "\n")
        backups_file.close()

    except netmiko.NetMikoAuthenticationException:
        print ("%s Not connected" % ip)

    except netmiko.NetMikoTimeoutException:
        print ("%s Time out" % ip)

def get_userpass(usertry):
    try:
        userfile = open("username.txt","r")
        usernames = userfile.read().splitlines()
        #print(usernames[usertry*2],usernames[usertry*2+1])
        username = usernames[usertry*2]
        password = usernames[usertry*2+1]
        return username,password

    except IOError:
        print("Can not Open File")


def ping_test(username,password,ip):
    try:
        user_name = username
        pass_word = password
        # cmd_file = "config.txt"
        session = ConnectHandler( device_type='cisco_ios', ip=ip , username=user_name , password=pass_word)
        # session.config_mode()
        command_make = "ping 10.16.1.1"
        output = session.send_command(command_make)
        #print (output)
        finder = output.find("percent")
        #print(finder)
        success_rate = output[finder-4:finder-1]
        print("success Rate for router "+ip+" is "+success_rate+"%")
        session.disconnect()
        return

    except netmiko.NetMikoAuthenticationException:
        print ("%s Not connected" % ip)

    except netmiko.NetMikoTimeoutException:
        print ("%s Time out" % ip)


def command_injection(username , password , ip):
    try:

        from netmiko import ConnectHandler
        # backups(ip,username,password) # if you want to  get backup before sending commands.
        session = ConnectHandler( device_type='cisco_ios', ip=ip , username=username , password=password)
        # output = session.find_prompt()
        session.config_mode()
        with open("config/configs.txt",'r') as config_file:
            for line in config_file:
                command_make = line
                output = session.send_command(command_make)

        config_file.close()
        session.send_command("do wr")
        session.disconnect()
        return

    except netmiko.NetMikoAuthenticationException:
        print("%s: Not connected" % ip)
    except netmiko.NetmikoTimeoutError:
        print("%s: Time Out" % ip)

def finder(username,password,ip):

    try:
        user_name = username
        pass_word = password
        session = ConnectHandler( device_type='cisco_ios', ip=ip , username=user_name , password=pass_word)
        # session.config_mode()
        files_path = "./search/results-"+datetime.date.today().strftime("%j")+".txt"
        search_q = input("Please Input your search Query: ")
        output = session.send_command("sh run | sec "+search_q)
        with open(files_path, 'a') as resutls_file:

            resutls_file.write("\n--------------------------------\nFor Unit: "+ip+"  :\n\n"+output+'\n--------------------------------\n')
        session.disconnect()
        resutls_file.close()
        return

    except netmiko.NetMikoAuthenticationException:
        print ("%s Not connected" % ip)

    except netmiko.NetMikoTimeoutException:
        print ("%s Time out" % ip)








current_auth = get_userpass(0)
import_or_install_packages()
# command_injection(current_auth[0],current_auth[1],"182.18.147.1")
# YOU NEED TO WRITE YOUR DESIRED FUNCTION HERE

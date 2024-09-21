import time
import requests
from stdnum import imei
import base64
import argparse

# required requests and python-stdnum
# pip install requests
# pip install python-stdnum


class clm920:
    def __init__(self, ip, password, newimei):
        self.clm920_ip = ip
        self.clm920_password = password
        self.clm920_newimei = newimei
        self.clm920_oldimei = ""
        self.clm920_modelversion = ""
        self.clm920_model = ""
        self.httpheaders = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': f'http://{ip}',
        'Connection': 'keep-alive',
        'Referer': f'http://{ip}/index.html',
        'Priority': 'u=0',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        }

    def at_cmd(self, atcmd):


        data = {
            'goformId': 'ID_SENDAT',
            'isTest': 'false',
            'at_str_data': atcmd,
        }

        response = requests.post(f'http://{self.clm920_ip}/reqproc/proc_post', headers=self.httpheaders, data=data)
        result = response.json()
        #print(f"--DEBUG : AT CMD Result = {result}")
        return(result)

    def get_imei(self):
        result =  self.at_cmd("AT+CGSN")
        if "__OK_OK" in result["result"]:
            self.clm920_oldimei = str(result["result"]).split("_+CGSN: ")[1].split("__OK_OK")[0]
            return self.clm920_oldimei
        else:
            self.clm920_oldimei = None
            return False
    def get_device_model(self):

        # Model
        # print(at_cmd('AT+CGMW'))
        # Model Version
        # print(at_cmd('AT+CGMR'))

        result =  self.at_cmd("AT+CGMW")
        if "__OK_OK" in result["result"]:
            self.clm920_model = str(result["result"]).split("_+CGMW: ")[1].split("__OK_OK")[0]
            return self.clm920_model
        else:
            self.clm920_model = None
            return False

    def get_device_version(self):

        # Model
        # print(at_cmd('AT+CGMW'))
        # Model Version
        # print(at_cmd('AT+CGMR'))

        result = self.at_cmd("AT^ZVERSION")
        if "__OK_OK" in result["result"]:
            self.clm920_modelversion = str(result["result"]).split("_+ZVERSION: ")[1].split("__OK_OK")[0]
            return self.clm920_modelversion
        else:
            self.clm920_modelversion = None
            return False

    def get_device_info_from_ui(self):
        #

        params = {
            'isTest': 'false',
            'cmd': 'remo_cus_software_version,remo_cus_hardware_version,remo_board_sn',
            'multi_data': '1',
            '_': '1725883489150',
        }

        response = requests.get(f'http://{self.clm920_ip}/reqproc/proc_get', headers=self.httpheaders, params=params)
        result = response.json()
        #print(f"--DEBUG : Result = {result}")
        return result


    def checkAtCommand(self):
        AT_dict = ["AT+CGMR", "AT+ZGMR", "AT^ZVERSION", "AT+HVER",
                   "AT+SSID?", "AT+WIFIKEY?,", "AT^READIMEI", "AT+MAC?", "AT+MAC2?", "AT+GMAC?", "AT+ETHMAC?",
                   "AT+USBMAC?", "AT+BOARDNUM?", "AT+LOCKLEVEL?"]

        for at in AT_dict:
            print(f"Debug AT command : {at} ")
            result = self.at_cmd(at)
            print(result)


    def set_imei(self):
        #AT^MODIMEI=' + imei_num)
        result = self.at_cmd(f"AT^MODIMEI={self.clm920_newimei}")
        if "__OK_OK" in result["result"]:
            return True
        else:
            return False


    def loggin_cmd(self):

        password = base64.b64encode(self.clm920_password.encode('utf-8')).decode('utf-8')

        data = {
            'goformId': 'LOGIN',
            'isTest': 'false',
            'password': password,
            'username' : ''
        }

        response = requests.post(f'http://{self.clm920_ip}/reqproc/proc_post', headers=self.httpheaders, data=data)
        result = response.json()
        if result["result"] == '0':
            return True
        else:
            return False

    def reboot_cmd(self):
        try:

            data = {
                'isTest': 'false',
                'goformId': 'REBOOT_DEVICE',
            }
            response = requests.post(f'http://{self.clm920_ip}/reqproc/proc_post', headers=self.httpheaders, data=data)
            result = response.json()
            if result["result"] == '0':
                return True
            else:
                return False
        except:
            return True

def confirmation():
    reponse = input("Process change ? (y/n) : ").lower()
    if reponse in ['y', 'yes']:
        print("Start IMEI change process!")
        return True
    elif reponse in ['n', 'no']:
        print("Not confirmed!.")
        return False
    else:
        print("Please press 'y' or 'n'.")
        return confirmation()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Modem IMEI Repair tools for CLM920")

    parser.add_argument(
        "--ip",
        type=str,
        required=True,
        help="CLM920 Ip address. Eg : '192.168.0.1'."
    )

    parser.add_argument(
        "--password",
        type=str,
        required=True,
        help="Admin password Eg: admin"
    )

    parser.add_argument(
        "--imei",
        type=str,
        required=True,
        help="New imei to flash. Exemple: '335841028069386'."
    )
    args = parser.parse_args()

    print("IMEI Repair tools for CLM920 LTE router")
    print("Version 0.1 - 21 sept 2024")
    print("Copyright (C) PoC.ng - contact CLM920@poc.ng")
    print('---')
    print('''This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.''')


    imei_num = args.imei
    ip = args.ip
    password = args.password

    if imei.validate(imei_num):
        modem = clm920(ip=ip, password=password, newimei=imei_num)
        if modem.loggin_cmd() == True:
            print("-> Login : OK")
            # check router
            print("-> Check router builtin chipset...")
            chipset = modem.get_device_model()
            chipset_software = modem.get_device_version()
            if chipset.startswith("7520V3"):
                print("-> Compatible chipset found...")
                print("\t" + chipset + "/" + chipset_software)
            else:
                print("/!\\ Warning : Not tested chipset found! ")
                print("\t" + chipset + "/" + chipset_software)

            #modem.checkAtCommand()
            hw_info = modem.get_device_info_from_ui()
            if str(hw_info["remo_cus_software_version"]).startswith("CLM920"):
                print(f"-> Detected CLM920 Router: {hw_info["remo_cus_hardware_version"]} serial number : {hw_info["remo_board_sn"]}")
            else:
                print("Warning this router is not compatible... (not yet test with this tools)")
                print("...continue at your own risk?")
                if confirmation() == False:
                    exit(1)

            print(f"-> Your current IMEI is {modem.get_imei()}")

            print("\nWARNING: Altering a phone/router's IMEI, or possessing equipment that allows it to be altered,\n"
                  " is a criminal offense (by law) in certain circumstances and location.\n"
                  " Do not use this tool for illegal purposes, and comply with your local legislation.\n")

            print(f"You resquet to change to {modem.clm920_newimei}")
            print(f"(note: After change your router reboot!)")
            if confirmation():
                print(f"change IMEI to {modem.clm920_newimei}")
                if modem.set_imei() == True:
                    print(f"OK!!! IMEI is now modified! to {modem.clm920_newimei}")
                    print("New imei is effective after restart....")
                    if modem.reboot_cmd() == False:
                        print("Error on reboot command, please poweroff/poweron your device!")
            else:
                print("Process stopped! (user response : no).")
                exit(1)

        else:
            print("error : Check password and IP!")

    else:
        print("Please check your new IMEI!")

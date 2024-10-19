import requests

class LinodeController:
    def __init__(self,auth) -> None:
        self.auth = auth
    def getInstances(self):
        api_url = 'https://api.linode.com/v4/linode/instances?page=1&page_size=100'
        auth_token = self.auth

        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {auth_token}'
        }

        response = requests.get(api_url, headers=headers)
        return response.json()
    def getInstance(self,id):
        url = f"https://api.linode.com/v4/linode/instances/{id}"

        headers = {
            "accept": "application/json",
            "authorization": f'Bearer {self.auth}'
        }

        response = requests.get(url, headers=headers)

        return response.json()
    def createInstance(self,label,region='us-east',type='g6-nanode-1',os='linode/almalinux8',rootPass='e3af15a57b2422c'):
        # URL for creating a Linode instance
        url = "https://api.linode.com/v4/linode/instances"

        # Payload with the instance details
        payload = {
            "type": type,  # Linode instance type
            "region": region,  # Region where the instance will be created
            "image": os,  # OS image for the instance
            "root_pass": rootPass,  # Root password for the instance
            "booted": True,  # Whether the instance should be booted immediately
            "interfaces": [{"purpose": "public"}],  # Network interface configuration
            "swap_size": 512,  # Swap size in MB
            "label": label,  # Optional: Label for the instance
            "tags": ["example"]  # Optional: Tags for the instance
        }

        # Headers including authorization token
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        # Send POST request to create the Linode instance
        response = requests.post(url, json=payload, headers=headers)

        # Print the response status code and JSON response
        if response.status_code != 200:
            return
        return response.json()
    def getRegions(self):
        url = "https://api.linode.com/v4/regions"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        return response.json()['data']
    def updateInstance(self,id,newLabel):
        url = f"https://api.linode.com/v4/linode/instances/{id}"

        payload = { "label": newLabel }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = requests.put(url, json=payload, headers=headers)

        return response.json()
    def deleteInstance(self,id):
        url = f"https://api.linode.com/v4/linode/instances/{id}"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.auth}"
        }
        response = requests.delete(url, headers=headers)
        return response.status_code == 200

    def bootInstance(self,id):
        url = f"https://api.linode.com/v4/linode/instances/{id}/boot"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = requests.post(url, headers=headers)

        return response.status_code == 200
    def cloneInstance(self,id,targetId):
        url = f"https://api.linode.com/v4/linode/instances/{id}/clone"

        payload = { "linode_id": targetId }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.status_code == 200
    def resetRootPass(self,id,password):
        url = f"https://api.linode.com/v4/linode/instances/{id}/password"

        payload = { "root_pass": password }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.status_code == 200
    def setRdns(self,id,ip,rdns):
        url = f"https://api.linode.com/v4/linode/instances/{id}/ips/{ip}"

        payload = { "rdns": rdns }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = requests.put(url, json=payload, headers=headers)

        return response.status_code ==200
    def deleteInstanceIp(self,id,ip):
        url = f"https://api.linode.com/v4/linode/instances/{id}/ips/{ip}"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = requests.delete(url, headers=headers)

        return response.status_code == 200
    def createIp(self,id):
        url = f"https://api.linode.com/v4/linode/instances/{id}/ips"

        payload = {
            "public": True,
            "type": "ipv4"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = requests.post(url, json=payload, headers=headers)


        return response.status_code == 200

if __name__ == '__main__':
    controller = LinodeController('e9193c60d46342469dec04943265fb5a24565c8c4a1de0992d02a4160f2add6a')

    id = 65548889
    print(controller.getInstances())
    # i = controller.getInstance(id)
    # print(i)
    
    # controller.createInstance('apiTest')
    # regs = controller.getRegions()

    # print(regs[0])


    # print(controller.updateInstance(id,'apiTest2'))

    # if controller.deleteInstance(id):
    #     print('done')
    # controller.bootInstance(id)
    # print(controller.createIp(id))

    # print(controller.setRdns(id,'172.104.209.239','vsdawdasczsdz.mooo.com'))
    # print(controller.getInstance(id))
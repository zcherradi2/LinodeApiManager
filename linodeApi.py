from typing import List, Optional, Dict
import requests

myRequest = requests.Session()

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
        response = myRequest.get(api_url, headers=headers)
        return response.json()
    def getInstance(self,id):
        url = f"https://api.linode.com/v4/linode/instances/{id}"

        headers = {
            "accept": "application/json",
            "authorization": f'Bearer {self.auth}'
        }

        response = myRequest.get(url, headers=headers)

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
        response = myRequest.post(url, json=payload, headers=headers)

        # Print the response status code and JSON response
        if response.status_code != 200:
            return
        return response.json()
    def getRegions(self):
        url = "https://api.linode.com/v4/regions"

        headers = {"accept": "application/json"}

        response = myRequest.get(url, headers=headers)

        return response.json()['data']
    def updateInstance(self,id,newLabel):
        url = f"https://api.linode.com/v4/linode/instances/{id}"

        payload = { "label": newLabel }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = myRequest.put(url, json=payload, headers=headers)

        return response.json()
    def deleteInstance(self,id):
        url = f"https://api.linode.com/v4/linode/instances/{id}"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.auth}"
        }
        response = myRequest.delete(url, headers=headers)
        return response.status_code == 200

    def bootInstance(self,id):
        url = f"https://api.linode.com/v4/linode/instances/{id}/boot"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = myRequest.post(url, headers=headers)

        return response.status_code == 200
    def cloneInstance(self,id,targetId):
        url = f"https://api.linode.com/v4/linode/instances/{id}/clone"

        payload = { "linode_id": targetId }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = myRequest.post(url, json=payload, headers=headers)

        return response.status_code == 200
    def resetRootPass(self,id,password):
        url = f"https://api.linode.com/v4/linode/instances/{id}/password"

        payload = { "root_pass": password }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = myRequest.post(url, json=payload, headers=headers)

        return response.status_code == 200
    def setRdns(self,id,ip,rdns):
        url = f"https://api.linode.com/v4/linode/instances/{id}/ips/{ip}"

        payload = { "rdns": rdns }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = myRequest.put(url, json=payload, headers=headers)
        return response.status_code ==200
    def deleteInstanceIp(self,id,ip):
        url = f"https://api.linode.com/v4/linode/instances/{id}/ips/{ip}"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.auth}"
        }

        response = myRequest.delete(url, headers=headers)

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

        response = myRequest.post(url, json=payload, headers=headers)


        return response.status_code == 200
class LinodeInstance:
    def __init__(self, id: int, label: str, group: str, status: str, created: str, updated: str, type: str,
                 ipv4: List[str], ipv6: str, image: str, region: str, site_type: str, specs: Dict[str, int],
                 alerts: Dict[str, int], backups: Dict[str, Optional[bool]], hypervisor: str, watchdog_enabled: bool,
                 tags: List[str], host_uuid: str, has_user_data: bool, placement_group: Optional[str], 
                 lke_cluster_id: Optional[str],manager):
        self.id = id
        self.label = label
        self.group = group
        self.status = status
        self.created = created
        self.updated = updated
        self.type = type
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.image = image
        self.region = region
        self.site_type = site_type
        self.specs = specs
        self.alerts = alerts
        self.backups = backups
        self.hypervisor = hypervisor
        self.watchdog_enabled = watchdog_enabled
        self.tags = tags
        self.host_uuid = host_uuid
        self.has_user_data = has_user_data
        self.placement_group = placement_group
        self.lke_cluster_id = lke_cluster_id
        self.manager = manager
        self.controller = manager.controller

    def __repr__(self):
        return (f"LinodeInstance(id={self.id}, label={self.label}, group={self.group}, status={self.status}, "
                f"created={self.created}, updated={self.updated}, type={self.type}, ipv4={self.ipv4}, ipv6={self.ipv6}, "
                f"image={self.image}, region={self.region}, site_type={self.site_type}, specs={self.specs}, "
                f"alerts={self.alerts}, backups={self.backups}, hypervisor={self.hypervisor}, "
                f"watchdog_enabled={self.watchdog_enabled}, tags={self.tags}, host_uuid={self.host_uuid}, "
                f"has_user_data={self.has_user_data}, placement_group={self.placement_group}, "
                f"lke_cluster_id={self.lke_cluster_id})")
    def setValues(self, newData):
        self.id = newData['id'],
        self.label = newData["label"],
        self.group = newData["group"],
        self.status = newData["status"],
        self.created = newData["created"],
        self.updated = newData['updated'],
        self.type = newData['type'],
        self.ipv4 = newData['ipv4'],
        self.ipv6 = newData['ipv6'],
        self.image = newData['image'],
        self.region = newData['region'],
        self.site_type = newData['site_type'],
        self.specs = newData['specs'],
        self.alerts = newData['alerts'],
        self.backups = newData['backups'],
        self.hypervisor = newData['hypervisor'],
        self.watchdog_enabled = newData['watchdog_enabled'],
        self.tags = newData['tags'],
        self.host_uuid = newData['host_uuid'],
        self.has_user_data = newData['has_user_data'],
        self.placement_group = newData['placement_group'],
        self.lke_cluster_id = newData['lke_cluster_id']
    def update(self):
        newData = self.controller.getInstance(self.id)
        self.setValues(newData)
    def delete(self):
        return self.controller.deleteInstance(self.id)
    def changeRdns(self,domain):
        return self.controller.setRdns(self.id,self.ipv4[0],domain)
    def setLabel(self,newLabel):
        newData = self.controller.updateInstance(self.id,newLabel)
        self.setValues(newData)
    def resetRootPass(self,newpass):
        return self.controller.resetRootPass(self.id,newpass)
    def boot(self):
        return self.controller.bootInstance(self.id)
    @classmethod
    def fromData(cls,data,manager):
        return LinodeInstance(
            id = data['id'],
            label = data["label"],
            group = data["group"],
            status = data["status"],
            created = data["created"],
            updated = data['updated'],
            type = data['type'],
            ipv4 = data['ipv4'],
            ipv6 = data['ipv6'],
            image = data['image'],
            region = data['region'],
            site_type = data['site_type'],
            specs = data['specs'],
            alerts = data['alerts'],
            backups = data['backups'],
            hypervisor = data['hypervisor'],
            watchdog_enabled = data['watchdog_enabled'],
            tags = data['tags'],
            host_uuid = data['host_uuid'],
            has_user_data = data['has_user_data'],
            placement_group = data['placement_group'],
            lke_cluster_id = data['lke_cluster_id'],
            manager=manager
            )
    def toJson(self):
        return {
            'id':self.id,
            'label':self.label,
            'status':self.status,
            'type':self.type,
            'ip':self.ipv4[0],
            'image':self.image,
            'region':self.region,
        }
class LinodeManager:
    def __init__(self,auth) -> None:
        self.auth =auth
        self.controller = LinodeController(auth)
        self.instances = []
        self.getInstances()
    def getInstances(self,json=False):
        data = self.controller.getInstances()['data']
        instances = [LinodeInstance.fromData(data[i],self) for i in range(len(data))]
        self.instances = instances
        if not json:
            return instances
        return [inst.toJson() for inst in instances]
    def createInstance(self,label: str, region: str = 'us-east', type: str = 'g6-nanode-1', os: str = 'linode/almalinux8', rootPass: str = 'e3af15a57b2422c'):
        res = self.controller.createInstance(label,region,type,os,rootPass)
        if res:
            inst = LinodeInstance.fromData(res,self)
            self.instances.append(inst)
            return inst
        return None
    def _getInstanceById(self, instance_id):
        for instance in self.instances:
            if instance.id == instance_id:
                return instance
        return None
    def deleteInstance(self,id):
        if self.controller.deleteInstance(id):
            self.instances = [instance for instance in self.instances if instance.id != id]
            return True
        return False
            
# res = {'data': [{'id': 61775768, 'label': 'almalinux-es-mad', 'group': '', 'status': 'running', 'created': '2024-07-23T11:38:06', 'updated': '2024-07-23T11:39:16', 'type': 'g6-nanode-1', 'ipv4': ['172.233.115.160'], 'ipv6': '2a01:7e02::f03c:94ff:fef6:7a21/128', 'image': 'linode/almalinux8', 'region': 'es-mad', 'site_type': 'core', 'specs': {'disk': 25600, 'memory': 1024, 'vcpus': 1, 'gpus': 0, 'transfer': 1000}, 'alerts': {'cpu': 90, 'network_in': 10, 'network_out': 10, 'transfer_quota': 80, 'io': 10000}, 'backups': {'enabled': False, 'available': False, 'schedule': {'day': None, 'window': None}, 'last_successful': None}, 'hypervisor': 'kvm', 'watchdog_enabled': True, 'tags': [], 'host_uuid': '944edff40d1a78722a891ea002c846a6c6523c72', 'has_user_data': False, 'placement_group': None, 'lke_cluster_id': None}, {'id': 61874454, 'label': 
# 'serv_00', 'group': '', 'status': 'running', 'created': '2024-07-25T17:50:36', 'updated': '2024-07-25T17:51:25', 'type': 'g6-standard-2', 'ipv4': ['172.232.132.111'], 'ipv6': '2600:3c09::f03c:94ff:feaf:8237/128', 'image': 'linode/centos-stream9', 'region': 'se-sto', 'site_type': 'core', 'specs': {'disk': 81920, 'memory': 4096, 'vcpus': 2, 'gpus': 0, 'transfer': 4000}, 'alerts': {'cpu': 180, 'network_in': 10, 'network_out': 10, 'transfer_quota': 80, 'io': 10000}, 'backups': {'enabled': False, 'available': False, 'schedule': {'day': None, 'window': None}, 'last_successful': None}, 'hypervisor': 
# 'kvm', 'watchdog_enabled': True, 'tags': [], 'host_uuid': '1096a7a9cd8f4f098fd67552f4e36833249167e3', 'has_user_data': False, 'placement_group': None, 'lke_cluster_id': None}, {'id': 61874474, 'label': 'serv_01', 'group': '', 'status': 'running', 'created': '2024-07-25T17:50:57', 'updated': '2024-07-25T17:51:46', 'type': 'g6-standard-2', 'ipv4': ['172.232.32.95'], 'ipv6': '2600:3c07::f03c:94ff:feaf:827a/128', 'image': 'linode/centos-stream9', 'region': 'fr-par', 'site_type': 
# 'core', 'specs': {'disk': 81920, 'memory': 4096, 'vcpus': 2, 'gpus': 0, 'transfer': 4000}, 'alerts': {'cpu': 180, 'network_in': 10, 'network_out': 10, 'transfer_quota': 80, 'io': 10000}, 'backups': {'enabled': False, 'available': False, 'schedule': {'day': None, 'window': None}, 'last_successful': None}, 'hypervisor': 'kvm', 'watchdog_enabled': True, 'tags': [], 'host_uuid': '043b12106b50482accee06c8f3937eb0feda24fc', 'has_user_data': False, 'placement_group': None, 'lke_cluster_id': None}, {'id': 61874502, 'label': 'serv_02', 'group': '', 'status': 'running', 'created': '2024-07-25T17:51:19', 'updated': '2024-07-25T17:52:02', 'type': 'g6-standard-2', 'ipv4': ['45.33.115.173'], 'ipv6': '2600:3c00::f03c:94ff:feaf:8226/128', 'image': 'linode/centos-stream9', 'region': 'us-central', 'site_type': 'core', 'specs': {'disk': 81920, 'memory': 4096, 'vcpus': 2, 'gpus': 0, 'transfer': 4000}, 'alerts': {'cpu': 180, 'network_in': 10, 'network_out': 10, 'transfer_quota': 80, 'io': 10000}, 'backups': {'enabled': False, 'available': False, 'schedule': {'day': None, 'window': None}, 'last_successful': None}, 'hypervisor': 'kvm', 'watchdog_enabled': True, 'tags': [], 'host_uuid': 'aaaab9c3c552250dbd474f27f2b8136f2216eced', 'has_user_data': False, 'placement_group': None, 'lke_cluster_id': None}, {'id': 61874527, 'label': 'serv_03', 'group': '', 'status': 'running', 'created': '2024-07-25T17:51:45', 'updated': '2024-07-25T17:52:28', 'type': 'g6-standard-2', 'ipv4': ['178.79.140.216'], 'ipv6': '2a01:7e00::f03c:94ff:feaf:8246/128', 'image': 'linode/centos-stream9', 'region': 'eu-west', 'site_type': 'core', 'specs': {'disk': 81920, 'memory': 4096, 'vcpus': 2, 'gpus': 0, 'transfer': 4000}, 'alerts': {'cpu': 180, 'network_in': 10, 'network_out': 10, 'transfer_quota': 80, 'io': 10000}, 'backups': {'enabled': False, 'available': False, 'schedule': {'day': None, 'window': None}, 'last_successful': None}, 'hypervisor': 'kvm', 'watchdog_enabled': True, 'tags': [], 'host_uuid': '53e4a52a1fc1e459ffa48d6d56b511ff54985871', 'has_user_data': False, 'placement_group': None, 'lke_cluster_id': None}], 'page': 1, 'pages': 1, 'results': 5}

# print(res.keys())
# num = res['results']
# print(f'found {num} instances')
# data = res['data']
# instances = [LinodeInstance(**data[i]) for i in range(num)]
# instance = instances[0]
# print(instance.id)
if __name__ == "__main__":
    auth = 'e9193c60d46342469dec04943265fb5a24565c8c4a1de0992d02a4160f2add6a'
    manager = LinodeManager(auth)
    instances = manager.getInstances()
    ipt = ''
    while ipt!= 'exit':
        ipt = input('')
        eval(ipt)
    # i = manager._getInstanceById(65549652)
    # print(i.ipv4)
    # print(i.label)
    # print(i.changeRdns('fgewfdadad.iceage.com.my'))
    # print(i)


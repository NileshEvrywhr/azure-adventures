#
# purpose: queries Azure subs for a list of running VMs
# date: January 3rd, 2022
#

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import SubscriptionClient

from icecream import ic
ic.configureOutput("DEBUG • ")

# authenticate using any available mechanism
credential = DefaultAzureCredential()

# get names of all subscriptions accesibile
subscription_client = SubscriptionClient(credential)
sub_it = subscription_client.subscriptions.list()
tenants_it = subscription_client.tenants.list()
sub_list = [sub.subscription_id for sub in sub_it]

# vm_list = compute_client.virtual_machines.list('resource_group_name')

# get all VMs list
vm_list = []
for sub in sub_list:
    compute_client = ComputeManagementClient(credential, sub)
    vm_it = compute_client.virtual_machines.list_all()
    vm_list += [ic(vm.name) for vm in vm_it]

ic(len(vm_list))

# for vm in vm_list:
    #     array = vm.id.split("/")
    #     resource_group = array[4]
    #     vm_name = array[-1]
    #     statuses = compute_client.virtual_machines.instance_view(resource_group, vm_name).statuses
    #     status = len(statuses) >= 2 and statuses[1]
        
    #     vm_list += ic(vm_name)
    #     if status and status.code == 'PowerState/running':
    #         print(vm_name)

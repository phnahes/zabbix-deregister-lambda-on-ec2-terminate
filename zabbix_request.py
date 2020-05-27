from pyzabbix import ZabbixAPI, ZabbixAPIException
import boto3
import json
import os
import sys

server = os.environ['SERVER']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

st_disabled = 1
st_enabled = 0
status = st_disabled
    

def lambda_handler(event, context):
    #print json.dumps(event)
    
    thisInstanceID = event['detail']['instance-id']

    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(thisInstanceID)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
            #print("instance-id: " + thisInstanceID + " Instance-name: " +  instancename )
            
    zapi = ZabbixAPI(server, user=username, password=password)
    host_name = instancename
    #print "host_name " + host_name
    hosts = zapi.host.get(filter={"host": host_name})
    #print "hosts " + str(hosts)
    if hosts:
        host_id = hosts[0]["hostid"]
        #print("Found host id {0}".format(host_id))
    
        try:
            item = zapi.host.update(
                hostid=host_id,
                status=status
            )
        except ZabbixAPIException as e:
            print(e)
            sys.exit()
        print("Status Changed to: {0} - Host: {1} {2}".format(status, host_id, host_name))
    else:
        print("Host {0} not found on zabbix - Ignoring".format(host_name))




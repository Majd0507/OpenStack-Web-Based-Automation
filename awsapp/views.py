from django.shortcuts import get_object_or_404,render
from django.http import Http404,HttpResponseRedirect
from .main import CustemEC2AWS

from .models import *

import boto3



def login(request):
    if request.method == 'GET':
        return render(request,'login.html' )

    access_key=request.POST['access_key']
    access_scriptkey=request.POST['access_scriptkey']
    region=request.POST['region']

    ec2main=CustemEC2AWS()
    res=ec2main.login(access_key,access_scriptkey,region)
    if res==True:
        # request.session['identity']=ec2main
        # print(request.session['identity'].list_instances())
        return HttpResponseRedirect("/aws/")
    return render(request,'login.html',{'err_msg':'incorrect creds'})



    return render(request,'login.html' )


def index(request):
    instances=CustemEC2AWS().list_instances()
    # instances=request.session['identity'].list_instances()
    for instance in instances:
        instance.custemStatus=instance.state['Name']
        if instance.tags != None:
            for i in instance.tags:
                if i['Key'] == 'Name':
                    instance.custemName=i['Value']
    context = {
        'instances': instances,
    }
    return render(request,'instances/index.html',context )



def details(request,instance_id):
    instance= CustemEC2AWS().get_instance(instance_id)
    instance.custemStatus=instance.state['Name']

    volumes=instance.volumes.all()
    volumes_names=list(volumes)
    for i in volumes_names:
        setattr(i,'custemStatus',i.attachments[0]['Device'])
        print(i.custemStatus)

    return render(request, 'instances/detail.html', {'instance':instance,'volumes':volumes_names})


def create(request):
    if request.method == 'GET':
        # keyname=request.session['identity']
        return render(request, 'instances/create.html', {'images': Image.objects.all()})

    CustemEC2AWS().create_instances(request.POST['name'],request.POST['imageId'],int(request.POST['volume']))
    return HttpResponseRedirect("/aws/")
    # return render(request, 'instances/create.html', {'images': Image.objects.all(),'msg':"instance added"})


def createAtacheVolume(request,instance_id):
    CustemEC2AWS().CreateAttacheVolume(instance_id,int(request.POST['volume']),request.POST['deviceName'])
    return HttpResponseRedirect("/aws/details/"+instance_id)

def listVolumes(request):
    volumes=CustemEC2AWS().listVolumes()
    return render(request, 'instances/indexVolume.html', {'volumes':volumes})


def test_page(request):
    return render(request,'instances/test_page.html',{'msg':None} )


def start_instance(request,instance_id):
    CustemEC2AWS().startInstance(instance_id)
    return HttpResponseRedirect("/aws/details/"+instance_id)

def stop_instance(request,instance_id):
    CustemEC2AWS().stopInstance(instance_id)
    return HttpResponseRedirect("/aws/details/"+instance_id)



def detatchVolume(request,instance_id,volume_id):
    CustemEC2AWS().detachVolume(instance_id,volume_id)
    print(instance_id,volume_id)
    return HttpResponseRedirect("/aws/details/"+instance_id)

def deleteVolume(request,volume_id):
    CustemEC2AWS().deleteVolume(volume_id)
    return HttpResponseRedirect("/aws/volumes/")

def detatchDeleteVolume(request,instance_id,volume_id):
    print(instance_id,volume_id)
    CustemEC2AWS().detatchDeleteVolume(instance_id,volume_id)
    return HttpResponseRedirect("/aws/details/"+instance_id)

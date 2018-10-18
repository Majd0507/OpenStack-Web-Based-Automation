import boto3
import time



class CustemEC2AWS():
    ec2Client=None
    ec2Resource=None

    def __init__(self):
        self.ec2Resource=boto3.resource('ec2')
        self.ec2Client=boto3.client('ec2')

    def login(self,arg1,arg2,arg3):
        try:
            client=boto3.client('sts',aws_access_key_id=arg1,aws_secret_access_key=arg2,region_name=arg3)
            print(client.get_caller_identity().get('Account'))
            self.ec2Resource=boto3.resource('ec2',aws_access_key_id=arg1,aws_secret_access_key=arg2,region_name=arg3)
            self.ec2Client=boto3.client('ec2',aws_access_key_id=arg1,aws_secret_access_key=arg2,region_name=arg3)
            return True
        except:
            print('wrong access keys')
            return False


    def list_instances(self):
        instances = self.ec2Resource.instances.all()  # get all instances from above region
        return list(instances)

    def get_instance(self,arg):
        return self.ec2Resource.Instance(arg)

    def create_instances(self,name,imageId,volumeSize):
        volumes=list()
        volumes.append({'DeviceName': '/dev/sdf','Ebs': {'VolumeSize': volumeSize,'VolumeType': 'gp2'},})
        instance=self.ec2Resource.create_instances(ImageId=imageId, MinCount=1, MaxCount=1,Placement={'AvailabilityZone':'eu-west-1a'},BlockDeviceMappings=volumes)[0]
        instance.create_tags(Tags=[{'Key': 'Name','Value': name},])



    def create_key_pair(self,arg):
        response=self.ec2Client.create_key_pair(KeyName=arg)
        return response['KeyMaterial']

    def list_key_pairs(self):
        response=self.ec2Client.describe_key_pairs()
        return response['KeyPairs']

    def startInstance(self,arg):
        try:
            self.ec2Resource.Instance(arg).start()
            return 'ok'
        except:
            pass

    def stopInstance(self,arg):
        try:
            self.ec2Resource.Instance(arg).stop()
            return 'ok'
        except:
            pass

    def listVolumes(self):
        return self.ec2Client.describe_volumes()['Volumes']

    def CreateAttacheVolume(self,instanceid,size,deviceName):

        volume=self.ec2Client.create_volume(AvailabilityZone='eu-west-1a',Size=size,VolumeType='gp2',)
        volumeId=volume['VolumeId']
        volumeStatus=volume['State']
        while volumeStatus!="available":
            time.sleep(2)
            volumeStatus=self.ec2Resource.Volume(volumeId).state


        self.ec2Client.attach_volume(Device=deviceName,VolumeId=volumeId,InstanceId=instanceid)



    def detachVolume(self,instance_id,volume_id):
        volume=self.ec2Resource.Volume(volume_id)
        volume.detach_from_instance(Force=True,InstanceId=instance_id)

    def deleteVolume(self,volume_id):
        self.ec2Resource.Volume(volume_id).delete()

    def detatchDeleteVolume(self,instance_id,volume_id):
        print(instance_id,volume_id)
        volume=self.ec2Resource.Volume(volume_id)
        volume.detach_from_instance(Force=True,InstanceId=instance_id)
        volumeStatus=volume.state
        while volumeStatus!="available":
            time.sleep(2)
            volumeStatus=self.ec2Resource.Volume(volume_id).state
        volume.delete()

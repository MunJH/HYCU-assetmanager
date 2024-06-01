from Sync.InstanceSync import instanceSync
from Sync.amiSync import amiSync
from Sync.rdsSync import rdsSync
from Sync.s3Sync import s3Sync
from Sync.vpcSync import vpcSync
import pandas as pd
import copy

profileList = ["assetmanager"]
# 여러개의 Console 결과를 통합할 수 있도록

amiDict = dict()
instanceDict = dict()
rdsDict = dict()
s3Dict = dict()
vpcDict = dict()


for profile in profileList:  # AMI 데이터 작업
    dataDict = amiSync(profile)
    KeyList = dataDict.keys()

    if len(amiDict) == 0:
        amiDict = copy.deepcopy(dataDict)
    else:
        for Key in KeyList:
            amiDict[Key] += dataDict[Key]


for profile in profileList:  # 인스턴스 데이터 작업
    dataDict = instanceSync(profile)
    KeyList = dataDict.keys()

    if len(instanceDict) == 0:
        instanceDict = copy.deepcopy(dataDict)
    else:
        for Key in KeyList:
            instanceDict[Key] += dataDict[Key]


for profile in profileList:  # RDS 데이터 작업
    dataDict = rdsSync(profile)
    KeyList = dataDict.keys()

    if len(rdsDict) == 0:
        rdsDict = copy.deepcopy(dataDict)
    else:
        for Key in KeyList:
            rdsDict[Key] += dataDict[Key]


for profile in profileList:  # S3 데이터 작업
    dataDict = s3Sync(profile)
    KeyList = dataDict.keys()

    if len(s3Dict) == 0:
        s3Dict = copy.deepcopy(dataDict)
    else:
        for Key in KeyList:
            s3Dict[Key] += dataDict[Key]


for profile in profileList:  # 람다펑션 데이터 작업
    dataDict = vpcSync(profile)
    KeyList = dataDict.keys()

    if len(vpcDict) == 0:
        vpcDict = copy.deepcopy(dataDict)
    else:
        for Key in KeyList:
            vpcDict[Key] += dataDict[Key]


ami_inventors = pd.DataFrame(amiDict)
instance_inventors = pd.DataFrame(instanceDict)
rds_inventors = pd.DataFrame(rdsDict)
s3_inventors = pd.DataFrame(s3Dict)
vpc_inventors = pd.DataFrame(vpcDict)

with pd.ExcelWriter("asset.xlsx") as writer:
    ami_inventors.to_excel(writer, sheet_name="AMI", index=False)
    instance_inventors.to_excel(writer, sheet_name="Instance", index=False)
    rds_inventors.to_excel(writer, sheet_name="RDS", index=False)
    s3_inventors.to_excel(writer, sheet_name="S3", index=False)
    vpc_inventors.to_excel(writer, sheet_name="VPC", index=False)

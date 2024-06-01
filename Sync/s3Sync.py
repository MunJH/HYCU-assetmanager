import boto3


def s3Sync(profile):
    """
    IN: profile 이름
    OUT: 인스턴스 목록 딕셔너리
    """
    dictData = {
        "consoleProfile": [],
        "Name": [],
        "tagPurpose": [],
        "tagDepartment": [],
        "tagManager": [],
        "tagConfidentiality": [],
        "tagIntegrity": [],
        "tagAvailability": []
    }
    bucketNameList = list()  # 버킷 이름을 저장하는 리스트

    session = boto3.Session(profile_name=profile)
    s3_client = session.client("s3")

    bucketNameLowData = s3_client.list_buckets()["Buckets"]

    for bucket in bucketNameLowData:
        bucketNameList.append(bucket.get("Name"))

    for bucketName in bucketNameList:
        dictData["consoleProfile"].append(profile)
        dictData["Name"].append(bucketName)

        Tags = getBucketTag(session, bucketName)
        dictData["tagPurpose"].append(Tags.get("tagPurpose"))
        dictData["tagDepartment"].append(Tags.get("tagDepartment"))
        dictData["tagManager"].append(Tags.get("tagManager"))
        dictData["tagConfidentiality"].append(Tags.get("tagConfidentiality"))
        dictData["tagIntegrity"].append(Tags.get("tagIntegrity"))
        dictData["tagAvailability"].append(Tags.get("tagAvailability"))

    return dictData


def getBucketTag(session, bucketName):
    s3_client2 = session.client("s3")
    result = {
        "tagPurpose": [],
        "tagDepartment": [],
        "tagManager": [],
        "tagConfidentiality": [],
        "tagIntegrity": [],
        "tagAvailability": []
    }
    tagKeyList = list()

    try:
        tagLowData_list = s3_client2.get_bucket_tagging(Bucket=bucketName)["TagSet"]
    except:
        tagLowData_list = None

    if tagLowData_list is None:
        result["tagPurpose"].append("Tags에서 Purpose Key값이 없음")
        result["tagDepartment"].append("Tags에서 Department Key값이 없음")
        result["tagManager"].append("Tags에서 Manager Key값이 없음")
        result["tagConfidentiality"].append("Tags에서 Confidentiality Key값이 없음")
        result["tagIntegrity"].append("Tags에서 Integrity Key값이 없음")
        result["tagAvailability"].append("Tags에서 Availability Key값이 없음")
    else:
        for tagData_dict in tagLowData_list:
            tagKeyList.append(tagData_dict.get("Key"))

        if "Purpose" not in tagKeyList:  # Tags의 Key값이 누락되었을 경우
            result["tagPurpose"].append("Tags에서 Purpose Key값이 없음")
        if "Department" not in tagKeyList:
            result["tagDepartment"].append("Tags에서 Department Key값이 없음")
        if "Manager" not in tagKeyList:
            result["tagManager"].append("Tags에서 Manager Key값이 없음")
        if "Confidentiality" not in tagKeyList:
            result["tagConfidentiality"].append("Tags에서 Confidentiality Key값이 없음")
        if "Integrity" not in tagKeyList:
            result["tagIntegrity"].append("Tags에서 Integrity Key값이 없음")
        if "Availability" not in tagKeyList:
            result["tagAvailability"].append("Tags에서 Availability Key값이 없음")

        for tagData_dict in tagLowData_list:
            if tagData_dict["Key"] == "Purpose":
                result["tagPurpose"].append(tagData_dict.get("Value"))
            if tagData_dict["Key"] == "Department":
                result["tagDepartment"].append(tagData_dict.get("Value"))
            if tagData_dict["Key"] == "Manager":
                result["tagManager"].append(tagData_dict.get("Value"))
            if tagData_dict["Key"] == "Confidentiality":
                result["tagConfidentiality"].append(tagData_dict.get("Value"))
            if tagData_dict["Key"] == "Integrity":
                result["tagIntegrity"].append(tagData_dict.get("Value"))
            if tagData_dict["Key"] == "Availability":
                result["tagAvailability"].append(tagData_dict.get("Value"))

    return result

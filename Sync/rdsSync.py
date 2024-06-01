import boto3


def rdsSync(profile):
    """
    IN: profile 이름
    OUT: 인스턴스 목록 딕셔너리
    """
    dictData = {
        "consoleProfile": [],
        "DbiResourceId": [],
        "DBInstanceArn": [],
        "CreationDate": [],
        "StorageEncrypted": [],
        "Engine": [],
        "EngineVersion": [],
        "PreferredBackupWindow": [],  # 백업시간
        "BackupRetentionPeriod": [],  # 백업보관주기
        "tagPurpose": [],
        "tagDepartment": [],
        "tagManager": [],
        "tagConfidentiality": [],
        "tagIntegrity": [],
        "tagAvailability": []
    }

    session = boto3.Session(profile_name=profile)
    rds_client = session.client("rds")

    rdsLowData_list = rds_client.describe_db_instances()["DBInstances"]

    for rdsData_dict in rdsLowData_list:
        dictData["consoleProfile"].append(profile)
        dictData["DbiResourceId"].append(rdsData_dict.get("DbiResourceId"))
        dictData["DBInstanceArn"].append(rdsData_dict.get("DBInstanceArn"))
        dictData["CreationDate"].append(rdsData_dict.get("CreationDate"))
        dictData["StorageEncrypted"].append(rdsData_dict.get("StorageEncrypted"))
        dictData["Engine"].append(rdsData_dict.get("Engine"))
        dictData["EngineVersion"].append(rdsData_dict.get("EngineVersion"))
        dictData["PreferredBackupWindow"].append(
            rdsData_dict.get("PreferredBackupWindow")
        )
        dictData["BackupRetentionPeriod"].append(
            rdsData_dict.get("BackupRetentionPeriod")
        )

        tagList = rdsData_dict.get("TagList")

        if tagList is None:  # Tag가 1개도 설정되지 않은 경우 None을 반환하기 때문
            dictData["tagPurpose"].append("Tags에서 Purpose Key값이 없음")
            dictData["tagDepartment"].append("Tags에서 Department Key값이 없음")
            dictData["tagManager"].append("Tags에서 Manager Key값이 없음")
            dictData["tagConfidentiality"].append("Tags에서 Confidentiality Key값이 없음")
            dictData["tagIntegrity"].append("Tags에서 Integrity Key값이 없음")
            dictData["tagAvailability"].append("Tags에서 Availability Key값이 없음")
            continue

        tagKeyList = list()

        for tag in tagList:
            tagKeyList.append(tag.get("Key"))

        if "Purpose" not in tagKeyList:  # Tags의 Key값이 누락되었을 경우
            dictData["tagPurpose"].append("Tags에서 Purpose Key값이 없음")
        if "Department" not in tagKeyList:
            dictData["tagDepartment"].append("Tags에서 Department Key값이 없음")
        if "Manager" not in tagKeyList:
            dictData["tagManager"].append("Tags에서 Manager Key값이 없음")
        if "Confidentiality" not in tagKeyList:
            dictData["tagConfidentiality"].append("Tags에서 Confidentiality Key값이 없음")
        if "Integrity" not in tagKeyList:
            dictData["tagIntegrity"].append("Tags에서 Integrity Key값이 없음")
        if "Availability" not in tagKeyList:
            dictData["tagAvailability"].append("Tags에서 Availability Key값이 없음")

        for tag in tagList:
            if tag["Key"] == "Purpose":
                dictData["tagPurpose"].append(tag.get("Value"))
            if tag["Key"] == "Department":
                dictData["tagDepartment"].append(tag.get("Value"))
            if tag["Key"] == "Manager":
                dictData["tagManager"].append(tag.get("Value"))
            if tag["Key"] == "Confidentiality":
                dictData["tagConfidentiality"].append(tag.get("Value"))
            if tag["Key"] == "Integrity":
                dictData["tagIntegrity"].append(tag.get("Value"))
            if tag["Key"] == "Availability":
                dictData["tagAvailability"].append(tag.get("Value"))

    return dictData

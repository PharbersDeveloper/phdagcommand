# -*- coding: utf-8 -*-

import subprocess
import json
import time
from ph_storage import static as st


class PhHdfsStorage:
    """
    HDFS 存储，操作，目前只有Buck Up数据到S3
    """

    def __init__(self, local_storage=None, s3_storage=None):
        self.__local_storage = local_storage
        self.__s3_storage = s3_storage

    def get_path(self, path):
        """
        根据传入路径，列出该目录下的所有
        return [string]
        """
        cmd = "hdfs dfs -ls " + path + " | awk '!/inprogress/ {print $8}'"
        res = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        paths = []
        for line in res.stdout.readlines():
            content = line.decode("utf-8").replace("\n", "")
            if content != "" and content.find("WARN") == -1:
                paths.append(content)
        return paths

    def __down_load(self, path, output):
        cmd = "hdfs dfs -get " + path + " " + output + ""
        res = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in res.stdout.readlines():
            print(line)

        return output

    def back_up(self, paths):
        if self.__local_storage is None or self.__s3_storage is None:
            return False
        try:
            hdfs_path = []
            for item in json.loads(paths):
                hdfs_path.extend(self.get_path(item))

            for item in hdfs_path:
                file_name = item.split("/")[-1]
                upload_path = st.UPLOADPATH + "/".join(
                    [elem for elem in item.split("/")[1:-1] if elem.find(":") < 0]) + "/" + file_name
                self.__down_load(item, st.DOWNLOADPATH)
                self.__s3_storage.upload(st.DOWNLOADPATH + "/" + file_name, st.BUCKET, upload_path)
                self.__local_storage.remove(st.DOWNLOADPATH + "/" + file_name)
        except BaseException as e:
            print("Error: ", e)
            return False
        else:
            return True


# -*- coding: utf-8 -*-
from __future__ import print_function  # 兼容 print 函数

import os
import time
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def process_lines(lines, start_timestamp, cutoff_timestamp, group_name, config_path, is_test_mode):
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 3:
            continue

        timestamp = int(parts[0])  # 获取时间戳
        operation = parts[1].lower()  # 操作类型 (C - create, D - delete, etc.)
        file_path = parts[2]  # 文件路径

        if timestamp >= cutoff_timestamp:
            print("超过截止日期，停止处理该文件。")
            return False

        if start_timestamp <= timestamp < cutoff_timestamp and operation == 'c':
            full_file_path = "{}/{}".format(group_name, file_path)
            delete_command = "fdfs_delete_file {} {}".format(config_path, full_file_path)
            if not is_test_mode:
                print("执行: {}".format(delete_command))
                os.system(delete_command)
            else:
                print("[测试模式] 将执行: {}".format(delete_command))

    return True

def read_large_file_in_chunks(file_path, start_timestamp, cutoff_timestamp, group_name, config_path, is_test_mode):
    with open(file_path, 'r') as file:
        with ThreadPoolExecutor(max_workers=8) as executor:
            while True:
                lines = file.readlines(1024 * 1024 * 2)
                if not lines:
                    break
                future = executor.submit(process_lines, lines, start_timestamp, cutoff_timestamp, group_name, config_path, is_test_mode)
                if not future.result():
                    break

def delete_old_files(group_name, log_directory, start_date, cutoff_date, is_test_mode, config_path):
    start_timestamp = int(time.mktime(start_date.timetuple()))
    cutoff_timestamp = int(time.mktime(cutoff_date.timetuple())) + 86400

    for file_name in os.listdir(log_directory):
        # 只处理 binlog.000、binlog.001、binlog.002 等文件
        if file_name.startswith('binlog.') and file_name[7:].isdigit():
            file_path = os.path.join(log_directory, file_name)
            print("正在处理日志文件: {}".format(file_path))

            read_large_file_in_chunks(file_path, start_timestamp, cutoff_timestamp, group_name, config_path, is_test_mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据 binlog 条目删除旧的 FastDFS 文件.")
    parser.add_argument('group_name', type=str, help="FastDFS 文件组名")
    parser.add_argument('log_directory', type=str, help="日志目录的路径")
    parser.add_argument('start_date', type=str, help="开始日期，格式为 YYYY-MM-DD")
    parser.add_argument('cutoff_date', type=str, help="截止日期，格式为 YYYY-MM-DD")
    parser.add_argument('--test', action='store_true', help="测试模式，默认为测试模式")
    parser.add_argument('--config', type=str, default='/etc/fdfs/client.conf', help="FastDFS 配置文件路径 (默认为 /etc/fdfs/client.conf)")

    args = parser.parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        cutoff_date = datetime.strptime(args.cutoff_date, "%Y-%m-%d")
    except ValueError:
        print("日期格式无效，请使用 YYYY-MM-DD 格式.")
        exit(1)

    print("删除时间段 {} 至 {} 之间的文件".format(start_date, cutoff_date))
    delete_old_files(args.group_name, args.log_directory, start_date, cutoff_date, args.test, args.config)
    print("删除操作完成.")

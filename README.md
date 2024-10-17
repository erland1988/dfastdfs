~~# FastDFS 文件删除工具

## 概述

该工具根据指定的日志文件（binlog）中的操作记录，删除旧的 FastDFS 文件。用户可以通过命令行参数灵活配置开始日期、截止日期和操作模式（测试或实际执行）。

## 特性

- 逐块读取大文件，减少内存使用
- 支持多线程处理，提高文件删除效率
- 提供测试模式，允许用户在不实际执行删除的情况下验证操作

## 安装

1. 确保您的系统已安装 Python 3.x。
2. 克隆此仓库或下载源代码：
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
3. 如果需要，创建一个虚拟环境并激活：
   ```bash
   python -m venv venv
   source venv/bin/activate  # 对于 Linux 或 macOS
   venv\Scripts\activate  # 对于 Windows
   ```
4. （可选）安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

使用以下命令行参数运行该工具：

```bash
python main.py <group_name> <log_directory> <start_date> <cutoff_date> [--test] [--config <config_path>]
```

### 参数说明

- `group_name`：FastDFS 文件组名
- `log_directory`：日志文件所在的目录路径
- `start_date`：开始日期，格式为 `YYYY-MM-DD`
- `cutoff_date`：截止日期，格式为 `YYYY-MM-DD`
- `--test`：可选参数，启用测试模式，默认情况下不执行删除操作，仅打印将要执行的命令
- `--config <config_path>`：可选参数，FastDFS 配置文件路径，默认为 `/etc/fdfs/client.conf`

### 示例

```bash
python main.py group_name /path/to/logs 2023-01-01 2023-01-31 --test
```

在测试模式下，以上命令将仅打印将要执行的删除命令，而不实际删除文件。

## 注意事项

- 确保提供的日志目录中存在以 `binlog.` 开头的日志文件。
- 请谨慎使用该工具，以避免意外删除重要文件。
- 本工具仅适用于 FastDFS 文件管理，确保在适当的环境中运行。

## 贡献

欢迎任何对本项目的贡献！请通过提交问题或拉取请求与我们联系。

## 许可证

该项目遵循 MIT 许可证。有关详细信息，请查看 LICENSE 文件。~~

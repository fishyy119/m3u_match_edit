import os
import json
from LoadFileTree import SettingLoader

# 与scan_file_tree的区别：无需提取路径，只生成歌曲名集合
def scan_file_tree_for_song(node: dict,
                            scan_result: set
                            ) -> None:
    for name, new_node in node.items():
            if isinstance(new_node, dict):  # 如果是目录节点
                scan_file_tree_for_song(new_node, scan_result)
            else:  # 如果是文件节点
                scan_result.add(name + new_node)

def scan_m3u(m3u_directory: str,
             search_result: set,
             target: set
             ) -> int:
    count = 0
    for filename in os.listdir(m3u_directory):
        if filename.endswith(".m3u"):
            file_path = os.path.join(m3u_directory, filename)
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        song_name = os.path.basename(line)
                        if song_name not in target:
                            search_result.add(song_name)
                            count = count + 1
    return count


if __name__ == "__main__":
    setting_loader = SettingLoader('setting.json')
    settings = setting_loader.read_settings()
    root_dir = settings['root_dir']  # 音乐库文件
    m3u_directory = settings['m3u_directory']  # m3u存储路径
    scan_result = set()
    search_result = set()

    try:
        with open('file_tree.json', 'r', encoding='utf-8') as f:
            file_tree = json.load(f)
    except FileNotFoundError:
        print('请首先运行"LoadFileTree.py"获取file_tree文件')
        exit()

    scan_file_tree_for_song(file_tree, scan_result)
    count_not_found = scan_m3u(m3u_directory, search_result, scan_result)
    with open('report_not_found.json', 'w', encoding='utf-8') as f:
        print(f"在m3u中发现{count_not_found}个失效项")
        f.write(json.dumps(list(search_result), ensure_ascii=False, indent=4))
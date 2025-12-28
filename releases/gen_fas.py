#!/usr/bin/env python3
"""
生成文件树索引页面
扫描当前目录及其子目录，为每个目录生成index.html文件
"""

import os
import html
import re  # 导入re模块，用于正则表达式匹配
from pathlib import Path
from datetime import datetime

def get_file_size(file_path):
    """获取文件大小，返回格式化字符串"""
    try:
        size = os.path.getsize(file_path)
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size/(1024*1024):.1f} MB"
        else:
            return f"{size/(1024*1024*1024):.1f} GB"
    except:
        return "未知"

def get_file_icon(filename):
    """根据文件扩展名返回对应的Font Awesome图标类名[citation:9]"""
    ext = os.path.splitext(filename)[1].lower()
    
    # 常见文件类型的Font Awesome图标映射[citation:9]
    # 使用Font Awesome 5免费版，前缀为'fas'（实心）或'far'（轮廓）
    icon_map = {
        # 文档
        '.pdf': 'fas fa-file-pdf',
        '.doc': 'fas fa-file-word', '.docx': 'fas fa-file-word',
        '.txt': 'fas fa-file-lines', '.md': 'fas fa-file-lines',
        '.ppt': 'fas fa-file-powerpoint', '.pptx': 'fas fa-file-powerpoint',
        '.xls': 'fas fa-file-excel', '.xlsx': 'fas fa-file-excel',
        
        # 代码
        '.py': 'fas fa-file-code', '.js': 'fas fa-file-code', '.java': 'fas fa-file-code',
        '.html': 'fas fa-file-code', '.css': 'fas fa-file-code', '.php': 'fas fa-file-code',
        '.c': 'fas fa-file-code', '.cpp': 'fas fa-file-code', '.h': 'fas fa-file-code',
        '.json': 'fas fa-file-code', '.xml': 'fas fa-file-code',
        
        # 压缩文件
        '.zip': 'fas fa-file-zipper', '.rar': 'fas fa-file-archive', '.7z': 'fas fa-file-archive',
        '.tar': 'fas fa-file-archive', '.gz': 'fas fa-file-archive',
        
        # 媒体
        '.jpg': 'fas fa-file-image', '.jpeg': 'fas fa-file-image', '.png': 'fas fa-file-image',
        '.gif': 'fas fa-file-image', '.bmp': 'fas fa-file-image',
        '.mp3': 'fas fa-file-audio', '.wav': 'fas fa-file-audio', '.flac': 'fas fa-file-audio',
        '.mp4': 'fas fa-file-video', '.avi': 'fas fa-file-video', '.mkv': 'fas fa-file-video',
        
        # 其他
        '.exe': 'fas fa-file-code', '.msi': 'fas fa-file-code',
        '.iso': 'fas fa-compact-disc', '.dmg': 'fas fa-compact-disc',
    }
    
    return icon_map.get(ext, 'fas fa-file')  # 默认使用通用文件图标[citation:9]

def generate_index_html(directory, root_dir):
    """为指定目录生成index.html文件"""
    # 获取目录中的文件和子目录
    items = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item.startswith('.'):  # 跳过隐藏文件
            continue

        if item == 'index.html' or item == 'gen_fas.py' or item == 'gen_emj.py':  # 跳过已有的index.html
            continue
            
        is_dir = os.path.isdir(item_path)
        items.append({
            'name': item,
            'is_dir': is_dir,
            'size': get_file_size(item_path) if not is_dir else '',
            'modified': datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%Y-%m-%d %H:%M'),
            'icon': 'fas fa-folder' if is_dir else get_file_icon(item)  # 目录使用文件夹图标[citation:9]
        })
    
    # 按目录在前，文件在后，然后按名称排序
    items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    
    # 计算相对路径
    rel_path = os.path.relpath(directory, root_dir)
    if rel_path == '.':
        rel_path = ''
    
    # 生成父目录链接
    parent_link = ''
    if directory != root_dir:
        parent_dir = os.path.dirname(directory)
        parent_rel = os.path.relpath(parent_dir, root_dir)
        if parent_rel == '.':
            parent_rel = ''
        parent_link = f'<li><a href="../index.html"><i class="fas fa-level-up-alt"></i> .. (返回上一级)</a></li>'
    
    # 生成HTML内容
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>下载Stamon - {html.escape(rel_path if rel_path else '根目录')}</title>
    <!-- 引入 Font Awesome 5 CDN[citation:2] -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #2c3e50, #4a6491);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .nav-bar {{
            background: #34495e;
            padding: 0.8rem 1.5rem;
            border-radius: 6px;
            margin-bottom: 1rem;
        }}
        
        .nav-bar a {{
            color: #ecf0f1;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        .nav-bar a:hover {{
            color: #3498db;
            text-decoration: underline;
        }}
        
        .current-path {{
            background: white;
            padding: 1rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid #3498db;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .file-list {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .list-header {{
            display: grid;
            grid-template-columns: 3fr 1fr 1fr;
            background: #ecf0f1;
            padding: 1rem;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 2px solid #bdc3c7;
        }}
        
        .list-item {{
            display: grid;
            grid-template-columns: 3fr 1fr 1fr;
            padding: 1rem;
            border-bottom: 1px solid #eee;
            text-decoration: none;
            color: inherit;
            transition: background 0.2s;
        }}
        
        .list-item:hover {{
            background: #f8f9fa;
        }}
        
        .list-item:last-child {{
            border-bottom: none;
        }}
        
        .item-name {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .icon {{
            font-size: 1.2em;
            width: 20px;
            text-align: center;
        }}
        
        footer {{
            margin-top: 2rem;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9rem;
            padding: 1rem;
        }}
        
        @media (max-width: 768px) {{
            .list-header, .list-item {{
                grid-template-columns: 2fr 1fr;
            }}
            .modified-time {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1><i class="fas fa-folder-tree"></i> 下载Stamon</h1>
    </header>
    
    <div class="nav-bar">
        <a href="https://stamon-rsc.github.io/releases/index.html"><i class="fas fa-home"></i> 回到首页</a>
        {' | ' if parent_link else ''}
        {parent_link.replace('<li><a href="../index.html">', '<a href="../index.html">').replace('</a></li>', '</a>') if parent_link else ''}
    </div>
    
    <div class="current-path">
        <strong><i class="fas fa-folder-open"></i> 当前路径:</strong> {html.escape(rel_path if rel_path else '/')}
    </div>
    
    <div class="file-list">
        <div class="list-header">
            <div>名称</div>
            <div>大小</div>
            <div class="modified-time">修改时间</div>
        </div>
        
        {parent_link}
        
'''

    # 添加目录和文件项
    for item in items:
        if item['is_dir']:
            link = f"{item['name']}/index.html"
            size_html = f"<span style='color:#27ae60;'>目录</span>"
        else:
            link = item['name']
            size_html = item['size']
        
        html_content += f'''        <a href="{html.escape(link)}" class="list-item">
            <div class="item-name">
                <span class="icon"><i class="{item['icon']}"></i></span>
                {html.escape(item['name'])}{'/' if item['is_dir'] else ''}
            </div>
            <div>{size_html}</div>
            <div class="modified-time">{item['modified']}</div>
        </a>
'''

    # 添加页脚
    html_content += f'''    </div>
    
    <footer>
        <p><i class="far fa-clock"></i> 最后生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><i class="fas fa-list-ol"></i> 共 {len(items)} 个项目</p>
    </footer>
</body>
</html>'''

    # 写入文件
    index_path = os.path.join(directory, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已生成: {index_path}")

def main():
    """主函数"""
    print("开始生成文件树索引...")
    print("-" * 50)
    
    # 获取当前目录作为根目录
    root_dir = os.getcwd()
    print(f"根目录: {root_dir}")
    
    # 遍历所有目录
    dirs_generated = 0
    files_generated = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过隐藏目录
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]

        # 跳过根目录和一些需要忽略的目录
        if re.search(r'\b\.git\b', dirpath) or re.search(r'\b__pycache__\b', dirpath):
            continue
        
        # 为该目录生成index.html
        generate_index_html(dirpath, root_dir)
        dirs_generated += 1
        
        # 统计文件数量（排除index.html）
        files_count = len([f for f in filenames if not f.startswith('.') and f != 'index.html'])
        files_generated += files_count
    
    print("-" * 50)
    print(f"完成！")
    print(f"生成了 {dirs_generated} 个目录的索引页面")
    print(f"共索引了 {files_generated} 个文件")
    print(f"\n打开 {os.path.join(root_dir, 'index.html')} 查看首页")

if __name__ == "__main__":
    main()
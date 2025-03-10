#!/usr/bin/env python3
"""
文件管理器模块
"""

import os
import shutil
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Tuple, Optional

class FileInfo:
    """文件信息类"""
    def __init__(self, path: str, content: str = None):
        self.path = path
        self._content = content
        
    @property
    def content(self) -> str:
        """获取文件内容"""
        if self._content is None:
            with open(self.path, 'r', encoding='utf-8') as f:
                self._content = f.read()
        return self._content

class FileManager:
    """文件管理器类"""
    def __init__(self):
        self.similarity_threshold = 0.5
        self.cache = {}
        self.encoding = 'utf-8'
        
    def find_similar_files(self, filename: str, search_path: str = None) -> List[FileInfo]:
        """查找相似文件"""
        similar_files = []
        search_path = search_path or os.getcwd()
        
        for root, _, files in os.walk(search_path):
            for file in files:
                if file == filename:
                    file_path = os.path.join(root, file)
                    similar_files.append(FileInfo(file_path))
                    
        return similar_files
    
    def suggest_directory(self, filename: str) -> str:
        """根据文件名建议目录"""
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in ['.yml', '.yaml', '.json']:
            return 'config'
        elif ext == '.py':
            return 'scripts'
        elif ext in ['.md', '.rst']:
            return 'docs'
        else:
            return 'misc'
            
    def create_or_update_file(self, filename: str, content: str, target_dir: str) -> Tuple[bool, str]:
        """创建或更新文件"""
        target_path = os.path.join(target_dir, filename)
        
        # 检查目标目录是否存在
        os.makedirs(target_dir, exist_ok=True)
        
        # 如果文件不存在，直接创建
        if not os.path.exists(target_path):
            with open(target_path, 'w', encoding=self.encoding) as f:
                f.write(content)
            return True, f"创建新文件：{target_path}"
            
        # 读取现有文件内容
        with open(target_path, 'r', encoding=self.encoding) as f:
            existing_content = f.read()
            
        # 计算内容相似度
        similarity = SequenceMatcher(None, existing_content, content).ratio()
        
        # 内容完全相同
        if similarity == 1.0:
            return True, f"文件已存在：{target_path}"
            
        # 内容相似度高，更新文件
        if similarity >= self.similarity_threshold:
            with open(target_path, 'w', encoding=self.encoding) as f:
                f.write(content)
            return True, f"更新文件：{target_path}"
            
        # 内容差异较大，建议创建新文件
        new_filename = f"{os.path.splitext(filename)[0]}_new{os.path.splitext(filename)[1]}"
        new_path = os.path.join(target_dir, new_filename)
        with open(new_path, 'w', encoding=self.encoding) as f:
            f.write(content)
        return True, f"内容差异较大，创建新文件：{new_path}"
        
    def move_file(self, source: str, target: str) -> Tuple[bool, str]:
        """移动文件"""
        try:
            # 确保目标目录存在
            target_dir = os.path.dirname(target)
            os.makedirs(target_dir, exist_ok=True)
            
            # 移动文件
            shutil.move(source, target)
            return True, f"文件已移动到：{target}"
        except Exception as e:
            return False, f"移动文件失败：{str(e)}"

def get_file_manager() -> FileManager:
    """获取文件管理器实例"""
    return FileManager() 
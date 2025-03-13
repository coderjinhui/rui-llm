import re
import os
import hashlib
from typing import List, Tuple
from langchain_community.document_loaders import ImageCaptionLoader



class MarkdownFormatter:
    def __init__(self):
        """初始化Markdown格式化器"""
        pass

    def __calculate_md5(self, file_path: str) -> str:
        """计算文件的MD5值
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件的MD5值
        """
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def __extract_images(self, markdown_text: str) -> List[Tuple[str, str, str]]:
        """从Markdown文本中提取图片信息
        
        Args:
            markdown_text: Markdown文本
            
        Returns:
            List[Tuple[str, str, str]]: 图片信息列表，每个元素为(原始文本, 图片路径, 原始描述)
        """
        # Markdown图片正则表达式
        pattern = r'!\[(.*?)\]\((.*?)(?:\s+"(.*?)")?\)'
        return [(match.group(0), match.group(2), match.group(3) or '')
                for match in re.finditer(pattern, markdown_text)]

    def __get_captions(self, images: List[Tuple[str, str, str]]) -> List[str]:
        """
        List[Tuple[str, str, str]]: 图片信息列表，每个元素为(原始文本, 图片路径, 原始描述)
        """
        img_files = []
        for image in images:
            img_path = image[1]
            if os.path.exists(img_path):
                img_files.append(img_path)

        # 使用ImageCaptionLoader生成描述
        loader = ImageCaptionLoader(images=img_files)
        print("start caption extraction")
        docs = loader.load()
        print("end caption extraction")
        captions = []
        for doc in docs:
            captions.append(doc.page_content if doc else None)
        return captions

    def process_markdown_images(self, markdown_text: str) -> str:
        """处理Markdown文本中的图片
        
        Args:
            markdown_text: 原始Markdown文本
            
        Returns:
            str: 处理后的Markdown文本
        """
        # 提取所有图片信息
        images = self.__extract_images(markdown_text)

        # 获取所有图片的描述信息
        captions = self.__get_captions(images)

        # 处理每个图片
        for (original, img_path, _), caption in zip(images, captions):
            if not os.path.exists(img_path):
                continue
                
            # 计算图片MD5
            img_md5 = self.__calculate_md5(img_path)
            
            # 根据是否有描述使用不同格式
            if caption:
                new_text = f'![{img_md5}]({img_path} "{caption}")'                
            else:
                new_text = f'![{img_md5}]({img_path})'
                
            # 替换原始文本
            markdown_text = markdown_text.replace(original, new_text)
        
        return markdown_text

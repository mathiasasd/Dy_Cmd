import requests
import json
import re
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class VideoInfo:
    """视频信息数据类"""
    parse_type: str = ""
    video_id: str = ""
    video_url_watermark: str = ""
    video_url_no_watermark: str = ""
    download_url_watermark: str = ""
    download_url_no_watermark: str = ""
    description: str = ""
    author_nickname: str = ""
    author_id: str = ""
    api_url: str = ""
    api_url_pro: str = ""


class DouyinParser:
    """抖音视频解析器"""
    
    def __init__(self):
        self.base_url = "https://dy.gglz.cn/api/hybrid/video_data"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_url_from_share_text(self, share_text: str) -> Optional[str]:
        """从分享文本中提取抖音链接"""
        # 匹配抖音分享链接的正则表达式
        patterns = [
            r'https?://v\.douyin\.com/[a-zA-Z0-9\-_]+/?',
            r'https?://www\.douyin\.com/video/\d+',
            r'https?://www\.iesdouyin\.com/share/video/\d+',
            r'https?://www\.douyin\.com/discover\?modal_id=\d+'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, share_text)
            if match:
                return match.group(0)
        
        return None
    
    def parse_video(self, url: str) -> Optional[VideoInfo]:
        """解析抖音视频信息"""
        try:
            # 调用API
            params = {'url': url}
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # 检查API响应状态
            if data.get('code') != 200:
                print(f"API错误: {data.get('msg', '未知错误')}")
                return None
            
            # 解析视频信息
            video_data = data.get('data', {})
            video_info = VideoInfo()
            
            # 基本信息
            video_info.parse_type = "视频"
            video_info.video_id = video_data.get('aweme_id', '')  # 修复：使用aweme_id作为视频ID
            video_info.description = video_data.get('desc', '')
            
            # 作者信息
            author_info = video_data.get('author', {})
            video_info.author_nickname = author_info.get('nickname', '')
            video_info.author_id = author_info.get('uid', '')
            
            # 视频链接
            video_info.video_url_watermark = video_data.get('video', {}).get('play_addr', {}).get('url_list', [''])[0]
            video_info.video_url_no_watermark = video_data.get('video', {}).get('play_addr', {}).get('url_list', [''])[0]
            
            # 下载链接（通常与播放链接相同）
            video_info.download_url_watermark = video_info.video_url_watermark
            video_info.download_url_no_watermark = video_info.video_url_no_watermark
            
            # API链接
            video_info.api_url = f"{self.base_url}?url={url}"
            video_info.api_url_pro = f"{self.base_url}?url={url}&pro=true"
            
            return video_info
            
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"解析过程中发生错误: {e}")
            return None
    
    def validate_url(self, url: str) -> bool:
        """验证URL是否为有效的抖音链接"""
        if not url:
            return False
        
        # 检查是否为抖音域名
        douyin_domains = [
            'douyin.com',
            'iesdouyin.com',
            'v.douyin.com'
        ]
        
        return any(domain in url for domain in douyin_domains)

import os
import sys
from colorama import init, Fore, Back, Style
from prettytable import PrettyTable
from douyin_parser import DouyinParser, VideoInfo

# 初始化colorama以支持Windows终端颜色
init(autoreset=True)


class DouyinCLI:
    """抖音解析命令行界面"""
    
    def __init__(self):
        self.parser = DouyinParser()
        self.running = True
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """打印程序横幅"""
        banner = f"""{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}抖音视频解析工具{Fore.CYAN}                        ║
║                    {Fore.YELLOW}Douyin Video Parser{Fore.CYAN}                     ║
╚══════════════════════════════════════════════════════════════╝"""
        print(banner)
    
    def print_menu(self):
        """打印主菜单"""
        menu = f"""{Fore.GREEN}请选择操作:
{Fore.WHITE}1. {Fore.CYAN}解析抖音视频链接或分享文本
{Fore.WHITE}2. {Fore.CYAN}查看使用说明
{Fore.WHITE}3. {Fore.CYAN}退出程序

{Fore.YELLOW}请输入选项 (1-3): {Fore.WHITE}"""
        print(menu)
    
    def print_help(self):
        """打印使用说明"""
        help_text = f"""{Fore.CYAN}══════════════════════════════════════════════════════════════
{Fore.YELLOW}使用说明:
{Fore.WHITE}1. 支持解析的链接格式:
   • https://v.douyin.com/xxxxx/
   • https://www.douyin.com/video/xxxxx
   • https://www.iesdouyin.com/share/video/xxxxx
   • https://www.douyin.com/discover?modal_id=xxxxx

2. 支持从分享文本中自动提取抖音链接
   可以直接粘贴完整的分享文本，程序会自动提取其中的抖音链接

3. 解析结果包含:
   • 视频ID
   • 视频链接（有水印/无水印）
   • 下载链接
   • 视频描述
   • 作者信息
   • API链接

{Fore.CYAN}══════════════════════════════════════════════════════════════"""
        print(help_text)
        input(f"{Fore.YELLOW}按回车键返回主菜单...")
    
    def get_user_input(self, prompt: str) -> str:
        """获取用户输入"""
        return input(f"{Fore.CYAN}{prompt}: {Fore.WHITE}").strip()
    
    def display_video_info(self, video_info: VideoInfo):
        """显示视频信息"""
        if not video_info:
            print(f"{Fore.RED}解析失败，请检查链接是否正确")
            return
        
        # 显示基本信息
        print(f"{Fore.CYAN}══════════════════════════════════════════════════════════════")
        print(f"{Fore.YELLOW}解析结果:")
        print(f"{Fore.CYAN}══════════════════════════════════════════════════════════════")
        
        # 基本信息表格
        basic_table = PrettyTable()
        basic_table.field_names = [f"{Fore.CYAN}类型", f"{Fore.CYAN}内容"]
        basic_table.align = "l"
        basic_table.max_width = 60
        
        basic_table.add_row([f"{Fore.WHITE}解析类型", f"{Fore.GREEN}{video_info.parse_type}"])
        basic_table.add_row([f"{Fore.WHITE}视频ID", f"{Fore.GREEN}{video_info.video_id}"])
        basic_table.add_row([f"{Fore.WHITE}视频描述", f"{Fore.GREEN}{video_info.description}"])
        basic_table.add_row([f"{Fore.WHITE}作者昵称", f"{Fore.GREEN}{video_info.author_nickname}"])
        basic_table.add_row([f"{Fore.WHITE}作者ID", f"{Fore.GREEN}{video_info.author_id}"])
        
        print(basic_table)
        print(f"{Fore.CYAN}══════════════════════════════════════════════════════════════")
        
        # 显示链接信息
        print(f"\n{Fore.YELLOW}链接信息:")
        print(f"{Fore.CYAN}══════════════════════════════════════════════════════════════")
        print(f"{Fore.WHITE}视频链接-水印: {Fore.BLUE}{video_info.video_url_watermark}")
        print(f"{Fore.WHITE}视频链接-无水印: {Fore.BLUE}{video_info.video_url_no_watermark}")
        print(f"{Fore.WHITE}视频下载-水印: {Fore.BLUE}{video_info.download_url_watermark}")
        print(f"{Fore.WHITE}视频下载-无水印: {Fore.BLUE}{video_info.download_url_no_watermark}")
        print(f"{Fore.WHITE}API链接: {Fore.BLUE}{video_info.api_url}")
        print(f"{Fore.WHITE}API链接-专业版: {Fore.BLUE}{video_info.api_url_pro}")
        print(f"{Fore.CYAN}══════════════════════════════════════════════════════════════")
    
    def parse_video_url(self):
        """解析视频链接"""
        print(f"{Fore.CYAN}══════════════════════════════════════════════════════════════")
        print(f"{Fore.YELLOW}请输入抖音视频链接或分享文本:")
        print(f"{Fore.CYAN}══════════════════════════════════════════════════════════════")
        
        user_input = self.get_user_input("抖音链接或分享文本")
        
        if not user_input:
            print(f"{Fore.RED}输入不能为空")
            return
        
        # 首先尝试从输入中提取抖音链接
        extracted_url = self.parser.extract_url_from_share_text(user_input)
        
        if extracted_url:
            # 如果从分享文本中提取到了链接
            print(f"{Fore.GREEN}从分享文本中提取到链接: {extracted_url}")
            url = extracted_url
        else:
            # 如果没有提取到链接，检查输入是否为直接的抖音链接
            if self.parser.validate_url(user_input):
                url = user_input
            else:
                print(f"{Fore.RED}未找到有效的抖音链接，请检查输入格式")
                return
        
        print(f"{Fore.YELLOW}正在解析中，请稍候...")
        
        video_info = self.parser.parse_video(url)
        self.display_video_info(video_info)
    

    
    def run(self):
        """运行主程序"""
        while self.running:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = self.get_user_input("").strip()
            
            if choice == '1':
                self.parse_video_url()
            elif choice == '2':
                self.print_help()
                continue
            elif choice == '3':
                print(f"\n{Fore.GREEN}感谢使用抖音视频解析工具！")
                self.running = False
                break
            else:
                print(f"\n{Fore.RED}无效选项，请输入 1-3")
            
            if self.running:
                input(f"\n{Fore.YELLOW}按回车键返回主菜单...")


def main():
    """主函数"""
    try:
        cli = DouyinCLI()
        cli.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}程序运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

import os
from openai import OpenAI
import concurrent.futures
from tqdm import tqdm
import time
import signal
import sys

# 初始化OpenAI客户端
client = OpenAI(
    api_key='sk-6407bdd26df4402ea56aa9b5da7b9ddd',
    base_url='https://api.deepseek.com/v1'
)

# 全局变量，用于处理中断信号
interrupted = False


def signal_handler(sig, frame):
    global interrupted
    interrupted = True
    print("\n中断信号接收，正在停止处理...")


# 注册信号处理函数
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def get_all_files(directory):
    """获取指定目录下所有文件的路径"""
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.txt', '.md', '.py')):
                file_paths.append(os.path.join(root, file))
    return file_paths


def read_file_content(file_path):
    """读取单个文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {str(e)}")
        return None


def generate_summary(content):
    """
    生成内容摘要，提示词更精准：
    - 包含函数或方法示例
    - 注意文档格式与准确度
    """
    try:
        prompt = (
            "请阅读以下文件内容，并为其中出现的函数或方法提供简要示例，"
            "输出需包含以下要点：\n1. 函数或方法描述\n2. 示例用法\n3. 注意事项\n\n"
            f"文件内容：\n\n{content}\n\n请按照上述要求为该文件输出标准化提示词。"
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"生成摘要时出错: {str(e)}")
        return None


def save_summary(summary, original_file_path):
    """保存摘要到对应的summary文件"""
    directory = os.path.dirname(original_file_path)
    file_name = os.path.basename(original_file_path)
    summary_dir = os.path.join(directory, 'summaries')

    if not os.path.exists(summary_dir):
        os.makedirs(summary_dir)

    summary_file = os.path.join(summary_dir, f"{file_name}_summary.md")

    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"摘要已保存到: {summary_file}")
    except Exception as e:
        print(f"保存摘要文件时出错: {str(e)}")


def process_single_file(file_path):
    """处理单个文件并支持重试"""
    if interrupted:
        return False
    print(f"处理文件: {file_path}")
    content = read_file_content(file_path)
    if not content:
        return False
    retry_count = 3
    while retry_count > 0:
        try:
            summary = generate_summary(content)
            if summary:
                save_summary(summary, file_path)
                return True
            break
        except Exception as e:
            retry_count -= 1
            if retry_count == 0:
                print(f"处理文件 {file_path} 失败，已重试3次: {str(e)}")
            time.sleep(1)
    return False


def process_directory(directory, max_workers=5):
    """使用线程池并发处理整个目录，显示进度并统计结果"""
    files = get_all_files(directory)
    success_count = 0
    failed_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_file, file_path): file_path
            for file_path in files
        }
        with tqdm(total=len(files), desc="处理进度") as pbar:
            for future in concurrent.futures.as_completed(futures):
                if interrupted:
                    break
                file_path = futures[future]
                try:
                    if future.result():
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    print(f"处理文件 {file_path} 时发生异常: {str(e)}")
                    failed_count += 1
                pbar.update(1)

    print("\n处理完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {failed_count} 个文件")


if __name__ == "__main__":
    target_directory = "./integrations"
    process_directory(target_directory, max_workers=5)

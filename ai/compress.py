import json

def compress_to_single_line(input_file, output_file):
    try:
        # 读取输入文件
        with open(input_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)

        # 初始化列表存放压缩后的数据
        compressed_data = []

        for item in data:
            # 遍历每个项目，将其压缩为一行 JSON 字符串
            compressed_item = {"messages": []}
            for message in item.get("messages", []):
                role = message.get("role", "")
                content = " ".join(message.get("content", "").split())
                compressed_item["messages"].append({"role": role, "content": content})
            compressed_data.append(compressed_item)

        # 将压缩后的数据转为单行字符串
        with open(output_file, "w", encoding="utf-8") as outfile:
            for entry in compressed_data:
                json_line = json.dumps(entry, ensure_ascii=False)
                outfile.write(json_line + "\n")

        print(f"压缩完成！结果已保存到 {output_file}")

    except FileNotFoundError:
        print(f"输入文件 {input_file} 未找到。")
    except json.JSONDecodeError:
        print("输入文件不是有效的 JSON 格式。")
    except Exception as e:
        print(f"出现错误：{e}")

# 示例调用
compress_to_single_line("output.json", "output.jsonl")

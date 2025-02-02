import json


def transform_data(input_data):
    # Prepare the transformed output
    transformed = []
    for item in input_data:
        # Extract the system message
        system_message = {
            "role": "system",
            "content": "Your role as an assistant involves thoroughly exploring questions through a systematic long thinking process before providing the final precise and accurate solutions. This requires engaging in a comprehensive cycle of analysis, summarizing, exploration, reassessment, reflection, backtracing, and iteration to develop well-considered thinking process. Please structure your response into two main sections: Thought and Solution. In the Thought section, detail your reasoning process using the specified format: <|begin_of_thought|> {thought with steps separated with '\n\n'} <|end_of_thought|> Each step should include detailed considerations such as analisying questions, summarizing relevant findings, brainstorming new ideas, verifying the accuracy of the current steps, refining any errors, and revisiting previous steps. In the Solution section, based on various attempts, explorations, and reflections from the Thought section, systematically present the final solution that you deem correct. The solution should remain a logical, accurate, concise expression style and detail necessary step needed to reach the conclusion, formatted as follows: <|begin_of_solution|> {final formatted, precise, and clear solution} <|end_of_solution|> Now, try to solve the following question through the above guidelines:"
        }

        # Iterate through conversations and extract the messages
        for conversation in item["conversations"]:
            user_message = {
                "role": "user",
                "content": conversation["value"]
            }
            assistant_message = {
                "role": "assistant",
                "content": conversation["value"]
            }

            # Append system, user, and assistant messages as a single interaction
            transformed.append({
                "messages": [
                    system_message,
                    user_message,
                    assistant_message
                ]
            })

    return transformed


# Example Input
input_data = [
    {
        "system": "Your role as an assistant involves thoroughly exploring questions through a systematic long thinking process before providing the final precise and accurate solutions.",
        "conversations": [
            {
                "from": "user",
                "value": "What is the critical temperature of a superconducting thin film made of lead with a thickness of 100 nm?"
            },
            {
                "from": "assistant",
                "value": "The critical temperature of a superconducting thin film made of lead with a thickness of 100 nm can be estimated using..."
            }
        ]
    },
    {
        "system": "Your role as an assistant involves thoroughly exploring questions through a systematic long thinking process before providing the final precise and accurate solutions.",
        "conversations": [
            {
                "from": "user",
                "value": "How many different four-digit numbers can be formed by rearranging the four digits in 2004?"
            },
            {
                "from": "assistant",
                "value": "The total number of different four-digit numbers that can be formed by rearranging the digits in 2004 is..."
            }
        ]
    }
]

# File paths
input_file = "input.json"   # 输入文件名
output_file = "output.json" # 输出文件名

try:
        # Read input JSON file
        with open(input_file, "r", encoding="utf-8") as file:
            input_data = json.load(file)

        # Transform the data
        output_data = transform_data(input_data)

        # Write transformed data to output JSON file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output_data, file, ensure_ascii=False, indent=2)

except FileNotFoundError:
        print(f"文件 {input_file} 未找到，请检查文件路径！")
except json.JSONDecodeError:
        print("输入文件格式错误，请确保其为有效的 JSON 文件！")


# Print the transformed data
for item in output_data:
    print(json.dumps(item, ensure_ascii=False, indent=2))

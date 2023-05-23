import openai
import os
import csv
import time

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv('YOUR-OPENAI-KAY')


def get_completion(prompt, model="gpt-4-0314", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


texts = []

with open('../datasets/ag-news/train.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')

    header = next(reader)

    for line in reader:
        entry = [
            line[3]
        ]
        texts.append(entry)

# print(texts)
# print(len(texts))# 12000

translated = []
for i, text in enumerate(texts):
    prompt = f"""
    Translate the following English text to Chinese: \ 
    {text}
    """
    response_start_time = time.time()  # 记录get_completion(prompt)运行前的时间
    response = get_completion(prompt)
    translated.append(response)
    response_end_time = time.time()  # 记录translated.append(response)运行后的时

    time_difference = response_end_time - response_start_time
    if time_difference < 1:
        time.sleep(1 - time_difference)
    else:
        continue

print(translated)

import openai
import os
import csv
import time
import pandas as pd

openai.api_key = os.getenv('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')


def get_completion(prompt, model="gpt-4-0314", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


texts = []

with open('../datasets/ag-news/test.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')

    header = next(reader)

    for line in reader:
        entry = [
            line[3]
        ]
        texts.append(entry)

# print(texts)

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

# print(translated)

print("length of original text:" + len(texts))
print("length of translated text:" + len(translated))

if len(texts) == len(translated):
    # Load the dataset
    df = pd.read_csv('../datasets/ag-news/test.csv')

    # Update the 'texts_translated' column in the DataFrame
    df['texts_translated'] = pd.dataframe(translated)

    # Save the updated DataFrame to the CSV file
    df.to_csv('../datasets/ag-news/test.csv', index=False)

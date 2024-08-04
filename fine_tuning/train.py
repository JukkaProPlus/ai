import datasets
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModel
from transformers import AutoModelForCausalLM
from transformers import TrainingArguments, Seq2SeqTrainingArguments
from transformers import Trainer, Seq2SeqTrainer
import transformers
from transformers import DataCollatorWithPadding
from transformers import TextGenerationPipeline
import torch
import numpy as np
import os, re
from tqdm import tqdm
import torch.nn as nn

import pprint

# 数据集
DATASET_NAME = "rotten_tomatoes"
# 加载数据集
raw_datasets = load_dataset(DATASET_NAME)

# 训练集
raw_train_dataset = raw_datasets["train"]
# print(len(raw_train_dataset)) # 8530

# print(raw_train_dataset[10])        #  {'text': 'this is a film well worth seeing , talking and singing heads and all .', 'label': 1}

# 验证集
raw_valid_dataset = raw_datasets["validation"]
print(len(raw_valid_dataset))   #1066

# print(raw_valid_dataset[10])        # {'text': "a mischievous visual style and oodles of charm make 'cherish' a very good ( but not great ) movie .", 'label': 1}
# print(type(raw_valid_dataset))      # <class 'datasets.arrow_dataset.Dataset'>

# 模型名称
MODEL_NAME = "gpt2"

# 加载模型
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

# 加载 tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.add_special_tokens({"pad_token": "[PAD]"})
tokenizer.pad_token_id = 0

# # 其他相关公共变量赋值
# pass


#设置随机种子：同个种子的随机序列可复现
transformers.set_seed(42)

#标签集
named_labels = ['neg', 'pos']

# 标签转 token_id
label_ids = [
    tokenizer(named_labels[i], add_special_tokens=False)["input_ids"][0]
    for i in range(len(named_labels))
]

# print("label_ids = ")
# print(label_ids)                #[12480, 1930]
# pprint.pprint(named_labels)     #['neg', 'pos']
# pprint.pprint(label_ids)        #[12480, 1930]

# print("type(label_ids) = ")
# print(type(label_ids))              #<class 'list'>


MAX_LEN=32   #最大序列长度（输入+输出）
DATA_BODY_KEY = "text" # 数据集中的输入字段名
DATA_LABEL_KEY = "label" #数据集中输出字段名

# 定义数据处理函数，把原始数据转成input_ids, attention_mask, labels
def process_fn(examples):
    model_inputs = {
            "input_ids": [],
            "attention_mask": [],
            "labels": [],
        }
    # print("*****************examples = ")             #*****************examples = 
    # pprint.pprint(examples)                           # {
    #                                                   # 	'text':['this is a good movie', 'i like this movie', 'a boring movie', ..., 'i hate this movie'],   # one thousands samples
    #                                                   # 	'label':[1, 1, 0, ..., 0]                   # one thousands samples
    #                                                   # } 
    # print("####################################")
    # print(len(examples[DATA_BODY_KEY]))                   # 1000
    # print(len(examples[DATA_LABEL_KEY]))                  # 1000
    # print("************************************")
    for i in range(len(examples[DATA_BODY_KEY])):
        # 自定义 Prompt 格式
        prompt = f"{examples[DATA_BODY_KEY][i]} Sentiment: "            # "this is a good movie Sentiment: ", 'Sentiment' in chinese means "情感"
        inputs = tokenizer(prompt, add_special_tokens=False)
        label = label_ids[examples[DATA_LABEL_KEY][i]]
        input_ids = inputs["input_ids"] + [tokenizer.eos_token_id, label]

        raw_len = len(input_ids)

        if raw_len >= MAX_LEN:
            input_ids = input_ids[-MAX_LEN:]
            attention_mask = [1] * MAX_LEN
            labels = [-100]*(MAX_LEN - 1) + [label]
        else:
            input_ids = input_ids + [tokenizer.pad_token_id] * (MAX_LEN - raw_len)
            attention_mask = [1] * raw_len + [0] * (MAX_LEN - raw_len)
            labels = [-100]*(raw_len-1) + [label] + [-100] * (MAX_LEN - raw_len)
        # print(prompt)                       # 提示词，类似 nicely serves as an examination of a society in transition . Sentiment:
        # print("raw_len = ", raw_len)        # 18
        # print("MAX_LEN = ", MAX_LEN)        # 32 
        # print("*******input_ids****************")     
        # pprint.pprint(input_ids)    # [44460, 306, 9179, 355, 281, 12452, 286, 257, 3592, 287, 6801, 764, 11352, 3681, 25, 220, 50256, 1930, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # print("#######################")

        # print(prompt)                       # 提示词，类似 merely as a technical , logistical feat , russian ark marks a cinematic milestone . Sentiment:
        # print("raw_len = ", raw_len)        # 24
        # print("MAX_LEN = ", MAX_LEN)        # 32 
        # print("*******attention_mask****************")     
        # pprint.pprint(attention_mask)    # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        # print("#######################")

        # print(prompt)                       # 提示词，类似 a very funny movie . Sentiment:
        # print("raw_len = ", raw_len)        # 11
        # print("MAX_LEN = ", MAX_LEN)        # 32 
        # print("*******labels****************")     
        # pprint.pprint(labels)    # [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, 1930, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100]
        # print("#######################")
        model_inputs["input_ids"].append(input_ids)
        model_inputs["attention_mask"].append(attention_mask)
        model_inputs["labels"].append(labels)
    # print("*****************model_inputs = ")
    # pprint.pprint(model_inputs)
    # print("************************************")
    return model_inputs

# 处理训练数据集
tokenized_train_dataset = raw_train_dataset.map(
    process_fn,
    batched=True,
    # remove_columns=raw_train_dataset.columns,
    remove_columns=raw_train_dataset.column_names,
    desc="Running tokenizer on train dataset",
)

# 处理验证数据集
tokenized_valid_dataset = raw_valid_dataset.map(
    process_fn,
    batched=True,
    # remove_columns=raw_valid_dataset.columns,
    remove_columns=raw_valid_dataset.column_names,
    desc="Running tokenizer on validation dataset",
)

# 定义数据校准器（自动生成batch）
collater = DataCollatorWithPadding(
    tokenizer=tokenizer, return_tensors="pt",
)


LR=2e-5         # 学习率
BATCH_SIZE=8    # Batch大小
INTERVAL=100    # 每多少步打一次 log / 做一次 eval

# 定义训练参数
training_args = TrainingArguments(
    output_dir="./output",              # checkpoint保存路径
    evaluation_strategy="steps",        # 按步数计算eval频率
    overwrite_output_dir=True,
    num_train_epochs=1,                 # 训练epoch数
    per_device_train_batch_size=BATCH_SIZE,     # 每张卡的batch大小
    gradient_accumulation_steps=1,              # 累加几个step做一次参数更新
    per_device_eval_batch_size=BATCH_SIZE,      # evaluation batch size
    eval_steps=INTERVAL,                # 每N步eval一次
    logging_steps=INTERVAL,             # 每N步log一次
    save_steps=INTERVAL,                # 每N步保存一个checkpoint
    learning_rate=LR,                   # 学习率
)


# 节省显存
model.gradient_checkpointing_enable()

# 定义训练器
trainer = Trainer(
    model=model, # 待训练模型
    args=training_args, # 训练参数
    data_collator=collater, # 数据校准器
    train_dataset=tokenized_train_dataset,  # 训练集
    eval_dataset=tokenized_valid_dataset,   # 验证集
    # compute_metrics=compute_metric,         # 计算自定义评估指标
)


# 开始训练
trainer.train()



# from transformers import AutoTokenizer, AutoModelForCausalLM

# # 加载训练后的 checkpoint
# model = AutoModelForCausalLM.from_pretrained("output/checkpoint-1000")

# # 模型设为推理模式
# model.eval()

# # 加载 tokenizer
# tokenizer = AutoTokenizer.from_pretrained("gpt2")

# # 待分类文本
# text = "This is a good movie!"

# # 文本转 token ids - 与训练时一样
# inputs = tokenizer(f"{text} Sentiment: ", return_tensors="pt")

# # 推理：预测标签
# output = model.generate(**inputs, do_sample=False, max_new_tokens=1)

# # label token 转标签文本
# tokenizer.decode(output[0][-1])





# 加载 checkpoint 并继续训练（选）


# trainer.train(resume_from_checkpoint="/path/to/checkpoint")



# # 此处只列出需修改的超参，其它超参与之前配置一致
# training_args = TrainingArguments(
#     per_device_train_batch_size=1,     # 减小每张卡的训练时 batch 大小
#     gradient_accumulation_steps=8,     # 增大累计参数更新的步数
#     per_device_eval_batch_size=1,      # 减小每张卡的评估时 batch 大小
# )

# trainer = Trainer(
#     model=model, 
#     args=training_args, 
#     data_collator=collater, 
#     train_dataset=tokenized_train_dataset,  
#     eval_dataset=tokenized_valid_dataset,   
#     # compute_metrics=compute_metric,         # 注释掉！不使用自定义评估器
# )


















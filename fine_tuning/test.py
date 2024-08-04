from transformers import AutoTokenizer, AutoModelForCausalLM

# 加载训练后的 checkpoint
model = AutoModelForCausalLM.from_pretrained("output/checkpoint-1067")

# 模型设为推理模式
model.eval()

# 加载 tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# 待分类文本
text = "This is a good movie!"

# 文本转 token ids - 与训练时一样
inputs = tokenizer(f"{text} Sentiment: ", return_tensors="pt")

# 推理：预测标签
output = model.generate(**inputs, do_sample=False, max_new_tokens=1)

# label token 转标签文本
print(tokenizer.decode(output[0][-1]))

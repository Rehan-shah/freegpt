import torch
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

model_name = "enoch/llama-65b-hf"
# You could also use "meta-llama/Llama-2-70b-hf", "meta-llama/Llama-2-70b-chat-hf", or
# "bigscience/bloom" - basically, any Hugging Face Hub repo with a supported model architecture



def main():
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, add_bos_token=False)
    model = AutoDistributedModelForCausalLM.from_pretrained(model_name)
    model = model.cuda()


    fake_token = tokenizer("^")["input_ids"][0]  # Workaround to make tokenizer.decode() keep leading spaces

    text = "What is a good chatbot? Answer:"
    prefix = tokenizer(text, return_tensors="pt")["input_ids"].cuda()

    with model.inference_session(max_length=30) as sess:
        for i in range(20):
            # Prefix is passed only for the 1st token of the outputs
            inputs = prefix if i == 0 else None

            # Let's use sampling with temperature = 0.9 and top_p = 0.6 to get more diverse results
            outputs = model.generate(inputs, max_new_tokens=1, session=sess,
                                     do_sample=True, temperature=0.9, top_p=0.6)

            text += tokenizer.decode([fake_token, outputs[0, -1].item()])[1:]
            print(text)

if __name__ == '__main__':
    main()





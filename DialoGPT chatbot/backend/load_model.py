from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

model_name = "microsoft/DialoGPT-medium"
AutoTokenizer.from_pretrained(model_name).save_pretrained("./model")
AutoModelForCausalLM.from_pretrained(model_name).save_pretrained("./model")

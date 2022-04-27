from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)
import torch


class ChatModel:
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    chat_history_ids = None

    print(f"I'm using {device} to generate answers.")

    def __init__(self):
        """Initialize model and tokenizer."""
        self.model = AutoModelForCausalLM.from_pretrained("./model")
        if "cuda" in self.device:
            self.model = self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("./model")

    def get_reply(self, user_query):
        """Take user input and return bot reply.
        
        Input: "What day is it?"
        Ourput: "It's Thursday!"
        """
        print(user_query)
        inputs = self.tokenizer.encode(
            user_query + self.tokenizer.eos_token, return_tensors="pt"
        )
        if "cuda" in self.device:
            inputs = inputs.to(self.device)
        print(inputs)
        if self.chat_history_ids is not None:
            print("Not None!")
        bot_input_ids = (
            torch.cat([self.chat_history_ids, inputs], dim=-1)
            if self.chat_history_ids is not None
            else inputs
        )
        if bot_input_ids.size(dim=1) >= 75:
            bot_input_ids = torch.narrow(bot_input_ids, 1, -75, 75)

        self.chat_history_ids = self.model.generate(
            bot_input_ids, max_length=1000, top_k=10, repetition_penalty=1.35
        )

        return "{}".format(
            "".join(
                self.tokenizer.batch_decode(
                    self.chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                    skip_special_tokens=True,
                )
            )
        )

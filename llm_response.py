from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class LLMGenerator:
    def __init__(self):
        # ✅ Switch to a smaller model to reduce memory usage
        self.model_name = "google/flan-t5-small"  # Change back to small
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # ✅ Offload weights to CPU (use "cuda" if you have GPU)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, device_map="auto")

    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cpu")  # ✅ Run on CPU
        outputs = self.model.generate(**inputs, max_length=100)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    llm = LLMGenerator()
    print(llm.generate_response("Explain quantum computing in simple terms."))

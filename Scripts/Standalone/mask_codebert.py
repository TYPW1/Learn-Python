from transformers import RobertaTokenizer, RobertaForMaskedLM, pipeline

model = RobertaForMaskedLM.from_pretrained("microsoft/codebert-base-mlm")
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base-mlm")

code = """if (x > 0) {
    y <mask> x - 1;
} else {
    y = x + 1;
}"""

fillmask = pipeline(
    "fill-mask",
    model=model,
    tokenizer=tokenizer,
)	

output = fillmask(code)

predictions = []
for i in range(len(output)):
    predictions.append(output[i]["token_str"])

print(predictions)

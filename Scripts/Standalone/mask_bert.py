from transformers import pipeline

# Create the fill-mask pipeline
fillmask = pipeline(
    "fill-mask",
    model='bert-large-cased-whole-word-masking'
)

# Example usage
code = """if (x > 0) {
    y [mask] x - 1;
} else {
    y = x + 1;
}"""
outputs = fillmask(code)

# Print predictions
for output in outputs:
    print(f"Token: {output['token_str']}, Score: {output['score']:.3f}")

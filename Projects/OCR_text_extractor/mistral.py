from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import os
from dotenv import load_dotenv
from huggingface_hub import login
from ocr_utils import extract_text_from_first_page

# === Load environment variables ===
load_dotenv()
login(token=os.getenv("HF_TOKEN"))

# === Load the model and tokenizer (CPU optimized) ===
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create text generation pipeline (CPU only)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

# === Llama Prompt Logic ===
def format_ocr_text_to_json(text):
    prompt = f"""Extract the following fields from the provided text and return them in JSON format:
    - Full Name: Combine the first name and last name.
    - Travel: Specify the city and country of travel.
    - Travel Start Date: Provide the date in YYYY-MM-DD format.

    Text:
    {text}

    JSON format:
    {{
        "fullName": "",
        "travel": "",
        "travelStartDate": ""
    }}
    """

    output = pipe(
        prompt, 
        max_new_tokens=500, 
        do_sample=False, 
        num_return_sequences=1
    )[0]['generated_text']    

    # Extract only the JSON part from the output
    json_start = output.find("{")
    json_end = output.rfind("}") + 1
    json_str = output[json_start:json_end]
                                            
    return json_str


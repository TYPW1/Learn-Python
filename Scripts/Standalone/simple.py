import streamlit as st
from transformers import pipeline
import torch


# Use a cache to load the model only once
@st.cache_resource
def load_model():
    # --- MAJOR UPGRADE: Using Google's Gemma model ---
    # This is a powerful and knowledgeable model for excellent conversations.
    model = pipeline(
        "text-generation",
        model="google/gemma-2b-it",
        model_kwargs={"torch_dtype": torch.bfloat16}  # Optimizes for performance
    )
    return model


# --- Helper Functions for Buttons ---
def set_edit_state(question, answer):
    st.session_state.edit_question = question
    st.session_state.edit_answer = answer


def delete_rule(question):
    if question in st.session_state.taught_rules:
        del st.session_state.taught_rules[question]
    st.rerun()


# --- The App's Interface ---
st.title("🧑‍🏫 The AI Classroom 🧠")
st.write("Teach your AI, manage its memory, and chat with it!")

# Load the AI model
try:
    chatbot = load_model()
except Exception as e:
    st.error(f"Error loading AI model: {e}")
    st.error("This might be due to a missing Hugging Face access token. Please add it to your Streamlit secrets.")
    st.stop()

# --- Initialize session state ---
if 'taught_rules' not in st.session_state:
    st.session_state.taught_rules = {}  # The "Memory Brain"
if 'history' not in st.session_state:
    st.session_state.history = []
if 'edit_question' not in st.session_state:
    st.session_state.edit_question = ""
if 'edit_answer' not in st.session_state:
    st.session_state.edit_answer = ""

# --- Section 1: Teach the AI ---
st.header("Step 1: Teach the AI")
with st.expander("👉 Click here to teach or edit rules!"):
    question_to_teach = st.text_input(
        "If a user says this:",
        value=st.session_state.edit_question,
        key="q_input"
    ).lower()

    answer_to_teach = st.text_input(
        "The AI should reply with this:",
        value=st.session_state.edit_answer,
        key="a_input"
    )

    if st.button("✅ Save to AI Memory"):
        if question_to_teach and answer_to_teach:
            st.session_state.taught_rules[question_to_teach] = answer_to_teach
            st.success("✅ Rule saved!")
            st.session_state.edit_question = ""
            st.session_state.edit_answer = ""
            st.rerun()
        else:
            st.warning("⚠️ Please fill in both fields.")

# --- Section 2: The AI Memory Pool ---
st.header("🧠 AI Memory Pool")
if not st.session_state.taught_rules:
    st.info("The AI's memory is empty. Teach it something!")
else:
    for question, answer in list(st.session_state.taught_rules.items()):
        col1, col2, col3, col4 = st.columns([3, 4, 1, 1])
        with col1:
            st.write(f"**If user says:**\n\n`{question}`")
        with col2:
            st.write(f"**AI replies:**\n\n`{answer}`")
        with col3:
            st.button("✏️ Edit", key=f"edit_{question}", on_click=set_edit_state, args=(question, answer))
        with col4:
            st.button("🗑️ Delete", key=f"delete_{question}", on_click=delete_rule, args=(question,))
    st.markdown("---")

# --- Section 3: Chat with the AI ---
st.header("Step 2: Chat with Your AI")
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Talk to your custom AI...")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    cleaned_input = user_input.lower().strip("?!.,")
    if cleaned_input in st.session_state.taught_rules:
        ai_response = st.session_state.taught_rules[cleaned_input]
        response_source = "🤖 (From my memory)"
        final_response = f"{response_source}: {ai_response}"
    else:
        # Using a short-term memory to keep the AI fast
        recent_history = st.session_state.history[-6:]

        # Create a formatted prompt for the instruction-tuned model
        messages = []
        for msg in recent_history:
            messages.append({"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]})

        prompt = chatbot.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        # Generate the response
        raw_output = chatbot(prompt, max_new_tokens=250, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

        # More robust way to get the response
        ai_response = raw_output[0]['generated_text'][len(prompt):].strip()
        response_source = "✨ (From my creative brain)"
        final_response = f"{response_source}: {ai_response}"

    st.session_state.history.append({"role": "assistant", "content": final_response})
    with st.chat_message("assistant"):
        st.markdown(final_response)


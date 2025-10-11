import streamlit as st
from thefuzz import process


# --- NO AI MODEL NEEDED! ---

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

# --- Initialize session state ---
if 'taught_rules' not in st.session_state:
    st.session_state.taught_rules = {}  # The AI's entire brain is here!
if 'history' not in st.session_state:
    st.session_state.history = []
if 'edit_question' not in st.session_state:
    st.session_state.edit_question = ""
if 'edit_answer' not in st.session_state:
    st.session_state.edit_answer = ""

# --- Section 1: Teach the AI ---
st.header("Step 1: Build the AI's Brain")
with st.expander("👉 Click here to teach or edit rules!"):
    question_to_teach = st.text_input(
        "If a user says something like this:",
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

    # --- NEW SIMPLIFIED BRAIN LOGIC ---

    # Brain #1: Check for a perfect match first.
    if cleaned_input in st.session_state.taught_rules:
        ai_response = st.session_state.taught_rules[cleaned_input]
        response_source = "🤖 (From my memory - perfect match!)"

    # Brain #2: If no perfect match, use fuzzy matching to find the closest one.
    else:
        known_questions = list(st.session_state.taught_rules.keys())

        if known_questions:
            # Find the best match from the list of known questions
            best_match, score = process.extractOne(cleaned_input, known_questions)

            # We set a "confidence score" of 80. If the match is >= 80%, we use it.
            if score >= 80:
                ai_response = st.session_state.taught_rules[best_match]
                response_source = f"🤔 (Close enough! This reminded me of '{best_match}')"
            else:
                ai_response = "I don't know the answer to that. Please teach me using the section above!"
                response_source = "🤷 (I'm not sure)"
        else:
            # This happens if the AI's memory is completely empty.
            ai_response = "My brain is empty! Please teach me something."
            response_source = "🧠 (Empty)"

    # --- Display the response ---
    final_response = f"{response_source}: {ai_response}"
    st.session_state.history.append({"role": "assistant", "content": final_response})
    with st.chat_message("assistant"):
        st.markdown(final_response)


import streamlit as st
import ast
import astunparse
import subprocess
from datetime import datetime
import hashlib
import os


# --------------- Core Logic (Same as previous) ---------------

class Mutator:
    @staticmethod
    def mutate_operators(code):
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Add):
                node.op = ast.Sub()
            elif isinstance(node, ast.Sub):
                node.op = ast.Add()
        return astunparse.unparse(tree)

    @staticmethod
    def mutate_functions(code):
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                node.name = f"mutated_{node.name}"
        return astunparse.unparse(tree)


class FileHandler:
    @staticmethod
    def save_temp_file(code):
        filename = f"temp_{hashlib.md5(code.encode()).hexdigest()[:8]}.py"
        with open(filename, 'w') as f:
            f.write(code)
        return filename

    @staticmethod
    def read_uploaded_file(uploaded_file):
        return uploaded_file.read().decode()


class ResultComparer:
    @staticmethod
    def run_test(filepath):
        try:
            result = subprocess.run(
                ['pytest', filepath],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False


# --------------- Streamlit Interface ---------------

def main():
    st.set_page_config(page_title="Mutation Tester", layout="wide")

    st.title("🧬 Python Mutation Testing Tool")
    st.markdown("Upload a Python file to test mutation survival rates")

    # File Upload Section
    with st.sidebar:
        st.header("Configuration")
        uploaded_file = st.file_uploader("Upload Python File", type=["py"])
        mutation_types = st.multiselect(
            "Select Mutation Types",
            ["Operators", "Functions"],
            default=["Operators"]
        )
        run_button = st.button("Run Mutation Testing")

    # Main Content Area
    col1, col2 = st.columns(2)

    if run_button and uploaded_file:
        with st.spinner("Analyzing your code..."):
            try:
                # Read and process file
                original_code = FileHandler.read_uploaded_file(uploaded_file)

                # Original Code Display
                with col1:
                    st.subheader("Original Code")
                    st.code(original_code, language='python')

                # Mutation Results
                results = []
                mutated_files = []

                # Perform mutations
                for m_type in mutation_types:
                    if m_type == "Operators":
                        mutated_code = Mutator.mutate_operators(original_code)
                    elif m_type == "Functions":
                        mutated_code = Mutator.mutate_functions(original_code)

                    # Save mutated file
                    mutated_path = FileHandler.save_temp_file(mutated_code)
                    mutated_files.append(mutated_path)

                    # Run tests
                    original_result = ResultComparer.run_test(uploaded_file.name)
                    mutated_result = ResultComparer.run_test(mutated_path)

                    # Store results
                    results.append({
                        "type": m_type,
                        "original_passed": original_result,
                        "mutated_passed": mutated_result,
                        "killed": original_result and not mutated_result
                    })

                # Display Results
                with col2:
                    st.subheader("Test Results")

                    # Metrics Card
                    total_mutations = len(results)
                    killed = sum(1 for r in results if r["killed"])
                    st.metric("Mutation Score", f"{(killed / total_mutations) * 100:.1f}%")

                    # Results Table
                    for result in results:
                        status = "✅ Killed" if result["killed"] else "❌ Survived"
                        st.markdown(f"""
                        **{result['type']} Mutation**
                        - Original Tests: {"Passed" if result["original_passed"] else "Failed"}
                        - Mutated Tests: {"Passed" if result["mutated_passed"] else "Failed"}
                        - Status: {status}
                        """)

                    # Mutated Code Preview
                    with st.expander("View Mutated Code"):
                        st.code(mutated_code, language='python')

                # Cleanup
                FileHandler.cleanup(mutated_files)

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    elif run_button and not uploaded_file:
        st.warning("Please upload a Python file first!")


if __name__ == "__main__":
    main()
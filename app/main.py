import streamlit as st
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch

model_name = "./model"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

st.title("Question Answering DistilBERT")
st.write("""
This project demonstrates a question answering system based on a DistilBERT model fine-tuned on the SQuAD dataset.
The model takes a context and a question as inputs and returns the most likely answer found in the context.
""")

st.subheader("Context")
context = st.text_area("Enter the context here:", height=150)

st.subheader("Question")
question = st.text_input("Enter your question here:")

if st.button("Run"):
    inputs = tokenizer(question, context, return_tensors="pt", truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    answer_start_index = outputs.start_logits.argmax()
    answer_end_index = outputs.end_logits.argmax()
    
    answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
    answer = tokenizer.decode(answer_tokens)
    
    st.subheader("Answer")
    st.write(answer)

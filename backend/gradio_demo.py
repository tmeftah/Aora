from question_and_answer import resp as QA
from rag_docs import resp as RAG
import gradio as gr


qa_chain = gr.Interface(fn=QA,
                        inputs=[gr.TextArea(lines=3, label="Text"), gr.Number(
                                minimum=1, maximum=10, value=3, label="Anzahl der Fragen")],
                        outputs=gr.TextArea(),
                        title="K-Averroes",)
rag_chain = gr.ChatInterface(RAG,
                             title="K-Averroes", examples=["what do we need for a request?",
                                                           "which .NET version is used with Power Pick System?",
                                                           "what can we do with WTA?",
                                                           "since when we can use gpx?"
                                                           ])


demo = gr.TabbedInterface([qa_chain, rag_chain], ["QA", "RAG"])

if __name__ == "__main__":
    demo.launch()

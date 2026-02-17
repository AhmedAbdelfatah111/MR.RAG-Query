
import gradio as gr
import requests
import os

BACKEND_URL = "http://localhost:8000"

CUSTOM_CSS = """
/* ── Global Reset ──────────────────────────────────────────────────────────── */
.gradio-container {
    max-width: 860px !important;
    margin: 0 auto !important;
    background: #1a1a1a !important;
    font-family: 'Söhne', 'Inter', 'Segoe UI', -apple-system, sans-serif !important;
}

body, .dark {
    background: #1a1a1a !important;
}

/* ── Header ────────────────────────────────────────────────────────────────── */
.app-header {
    text-align: center;
    padding: 40px 20px 20px 20px;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 8px;
}
.app-header h1 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #e5e5e5 !important;
    letter-spacing: -0.02em;
    margin: 0 0 6px 0 !important;
}
.app-header p {
    color: #888 !important;
    font-size: 0.85rem !important;
    margin: 0 !important;
    font-weight: 400;
}

/* ── Tabs ──────────────────────────────────────────────────────────────────── */
.tab-nav {
    background: transparent !important;
    border: none !important;
    justify-content: center !important;
    gap: 4px !important;
    padding: 8px 0 !important;
}
.tab-nav button {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #888 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 20px !important;
    transition: all 0.15s ease !important;
}
.tab-nav button:hover {
    color: #ccc !important;
    background: #2a2a2a !important;
}
.tab-nav button.selected {
    color: #e5e5e5 !important;
    background: #2a2a2a !important;
    border: none !important;
    font-weight: 600 !important;
}

/* ── Upload Area ───────────────────────────────────────────────────────────── */
.upload-container {
    padding: 24px 0;
}

.how-it-works {
    background: #222 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
    margin-bottom: 20px !important;
    color: #aaa !important;
    font-size: 0.85rem !important;
    line-height: 1.7 !important;
}
.how-it-works strong {
    color: #ccc !important;
}
.how-it-works .step-num {
    display: inline-block;
    width: 20px;
    height: 20px;
    background: #333;
    color: #aaa;
    border-radius: 50%;
    text-align: center;
    line-height: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-right: 8px;
}

/* File upload widget */
.file-upload-area .wrap {
    border: 1px dashed #444 !important;
    border-radius: 8px !important;
    background: #222 !important;
    transition: all 0.2s ease !important;
}
.file-upload-area .wrap:hover {
    border-color: #666 !important;
    background: #282828 !important;
}

/* Ingest button */
.ingest-btn {
    background: #e5e5e5 !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 24px !important;
    border-radius: 8px !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    letter-spacing: -0.01em;
}
.ingest-btn:hover {
    background: #fff !important;
}

/* Status output */
.status-output {
    background: #222 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    min-height: 50px;
}

/* ── Chat ──────────────────────────────────────────────────────────────────── */
.chat-container .chatbot {
    background: #1a1a1a !important;
    border: none !important;
}

/* Chat bubbles */
.chatbot .message {
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}

/* User messages */
.chatbot .user {
    background: #2a2a2a !important;
    border: none !important;
}

/* Bot messages */
.chatbot .bot {
    background: transparent !important;
    border: none !important;
}

/* Chat input */
.chat-container textarea {
    background: #2a2a2a !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
    color: #e5e5e5 !important;
    font-size: 0.9rem !important;
    padding: 12px 16px !important;
}
.chat-container textarea:focus {
    border-color: #555 !important;
    outline: none !important;
}
.chat-container textarea::placeholder {
    color: #666 !important;
}

/* Submit button in chat */
.chat-container button[type="submit"],
.chat-container .submit-btn {
    background: #e5e5e5 !important;
    color: #1a1a1a !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Example buttons */
.chat-container .example-btn,
.chat-container .examples button {
    background: #2a2a2a !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #aaa !important;
    font-size: 0.82rem !important;
    padding: 8px 14px !important;
    transition: all 0.15s ease !important;
}
.chat-container .example-btn:hover,
.chat-container .examples button:hover {
    border-color: #555 !important;
    color: #ccc !important;
    background: #333 !important;
}

/* ── Labels & Inputs ───────────────────────────────────────────────────────── */
label, .label-wrap span {
    color: #aaa !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

input, textarea, select {
    background: #222 !important;
    border: 1px solid #333 !important;
    color: #e5e5e5 !important;
    border-radius: 8px !important;
}

/* ── Footer ────────────────────────────────────────────────────────────────── */
.app-footer {
    text-align: center;
    padding: 20px 0;
    border-top: 1px solid #2a2a2a;
    margin-top: 16px;
}
.app-footer p {
    color: #555 !important;
    font-size: 0.75rem !important;
    margin: 0 !important;
}

/* ── Scrollbar ─────────────────────────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #1a1a1a;
}
::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #444;
}

/* ── Remove Gradio branding ────────────────────────────────────────────────── */
footer {
    display: none !important;
}
"""

# ── Backend functions ─────────────────────────────────────────────────────────

def ingest_file(file, progress=gr.Progress()):
    if file is None:
        return "No file selected. Please upload a PDF or DOCX file."

    try:
        progress(0.2, desc="Uploading...")
        files = {"file": open(file, "rb")}

        progress(0.5, desc="Processing document...")
        response = requests.post(f"{BACKEND_URL}/ingest", files=files, timeout=120)

        progress(1.0, desc="Done")
        if response.status_code == 200:
            data = response.json()
            chunks = data.get("chunks", "unknown")
            filename = os.path.basename(file)
            return (
                f"**Document ingested successfully.**\n\n"
                f"File: `{filename}`\n"
                f"Chunks created: `{chunks}`\n\n"
                f"You can now switch to the **Chat** tab to ask questions."
            )
        else:
            return f"Error: {response.text}"
    except requests.exceptions.Timeout:
        return "The server took too long to respond. Please try again."
    except requests.exceptions.ConnectionError:
        return "Cannot reach the backend server. Make sure it's running on port 8000."
    except Exception as e:
        return f"Error: {e}"


def chat_response(message, history):
    if not message.strip():
        return "Please enter a question."
    try:
        response = requests.post(
            f"{BACKEND_URL}/rag/invoke",
            json={"input": message},
            timeout=120,
        )
        if response.status_code == 200:
            return response.json()["output"]
        else:
            return f"Error: {response.text}"
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Cannot connect to the backend server."
    except Exception as e:
        return f"Error: {e}"



theme = gr.themes.Base(
    primary_hue="neutral",
    secondary_hue="neutral",
    neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
).set(
    body_background_fill="#1a1a1a",
    body_background_fill_dark="#1a1a1a",
    block_background_fill="#1a1a1a",
    block_background_fill_dark="#1a1a1a",
    block_border_width="0px",
    block_label_text_color="#aaa",
    block_title_text_color="#ccc",
    input_background_fill="#222",
    input_background_fill_dark="#222",
    input_border_color="#333",
    input_border_color_dark="#333",
    button_primary_background_fill="#e5e5e5",
    button_primary_background_fill_dark="#e5e5e5",
    button_primary_text_color="#1a1a1a",
    button_primary_text_color_dark="#1a1a1a",
    button_secondary_background_fill="#2a2a2a",
    button_secondary_background_fill_dark="#2a2a2a",
    button_secondary_text_color="#aaa",
    button_secondary_text_color_dark="#aaa",
    border_color_primary="#333",
    border_color_primary_dark="#333",
)

with gr.Blocks(title="Smart Contract Assistant") as demo:

    gr.HTML("""
        <div class="app-header">
            <h1>Smart Contract Assistant</h1>
            <p>Upload contracts and ask questions — powered by AI</p>
        </div>
    """)

    with gr.Tabs():

        with gr.Tab("Upload", id="upload"):
            with gr.Column(elem_classes=["upload-container"]):

                gr.HTML("""
                    <div class="how-it-works">
                        <strong>Getting started</strong><br><br>
                        <span class="step-num">1</span> Upload a PDF or DOCX contract<br>
                        <span class="step-num">2</span> Click <strong>Process Document</strong> to analyze it<br>
                        <span class="step-num">3</span> Switch to <strong>Chat</strong> to ask questions about it
                    </div>
                """)

                file_input = gr.File(
                    label="Contract file",
                    file_types=[".pdf", ".docx"],
                    type="filepath",
                    elem_classes=["file-upload-area"],
                )

                upload_btn = gr.Button(
                    "Process Document",
                    variant="primary",
                    elem_classes=["ingest-btn"],
                    size="lg",
                )

                upload_output = gr.Markdown(
                    value="No document processed yet.",
                    elem_classes=["status-output"],
                )

                upload_btn.click(
                    ingest_file,
                    inputs=file_input,
                    outputs=upload_output,
                )

        with gr.Tab("Chat", id="chat"):
            gr.ChatInterface(
                fn=chat_response,
                examples=[
                    "Summarize the key terms of this contract",
                    "What are the payment terms?",
                    "What encryption standard is required?",
                    "What are the termination clauses?",
                    "What are the confidentiality obligations?",
                ],
                submit_btn="Send",
                fill_height=True,
            )

    gr.HTML("""
        <div class="app-footer">
            <p>Smart Contract Assistant &middot; LangChain &middot; OpenRouter</p>
        </div>
    """)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=theme, css=CUSTOM_CSS)

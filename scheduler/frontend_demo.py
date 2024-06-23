from pathlib import Path
from event_recommender import csv_to_event
import gradio as gr

def upload_file(filepath):
    name = Path(filepath).name
    text = csv_to_event(filepath)
    return [gr.UploadButton(visible=False), gr.DownloadButton(label=f"Download {name}", value=filepath, visible=True), gr.Textbox(value=f"Uploaded to Google Calendar:\n{text}", label="Exported Spreadsheet")]

def download_file():
    return [gr.UploadButton(visible=True), gr.DownloadButton(visible=False)]

with gr.Blocks() as demo:
    gr.Markdown("Upload your Health Data")
    with gr.Row():
        u = gr.UploadButton("Upload a file", file_count="single", file_types=["file"])
        d = gr.DownloadButton("Download the file", visible=False)
    
    stored = gr.Textbox(value="", label="Last Spreadsheet Uploaded")

    u.upload(upload_file, u, [u, d, stored])
    d.click(download_file, None, [u, d])

if __name__ == "__main__":
    demo.launch()
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import PyPDF2
import os
from tkinter import Tk, Canvas, Frame, Label, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

# Load the embedding model
embedding_model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")

# Function to extract text from PDFs
def extract_text_from_pdfs(pdf_paths):
    extracted_data = []
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                sentences = text.split(". ")  # Simple sentence split
                for sentence in sentences:
                    extracted_data.append((sentence.strip(), os.path.basename(pdf_path), page_num + 1))
    return extracted_data

# Build FAISS Index
def build_faiss_index(sentences):
    embeddings = embedding_model.encode([s[0] for s in sentences])
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

# Query the index
def query_index(query, index, sentences):
    query_vector = embedding_model.encode([query])
    distances, indices = index.search(query_vector, k=5)  # Top 5 results
    results = [(sentences[i], distances[0][n]) for n, i in enumerate(indices[0])]
    return results

# Main logic
def answer_question(query, pdf_data, faiss_index):
    results = query_index(query, faiss_index, pdf_data)
    answer_candidates = []
    for result, _ in results:
        sentence, pdf_name, page_num = result
        answer_candidates.append(f"From {pdf_name} (Page {page_num}): {sentence}")
    return "\n".join(answer_candidates)

def select_pdfs_via_drag_and_drop():
    root = TkinterDnD.Tk()
    root.title("Drag and Drop PDF Files")
    root.geometry("600x400")

    selected_files = []

    def on_drop(event):
        files = root.tk.splitlist(event.data)
        for file in files:
            if file.endswith(".pdf") and file not in selected_files:
                selected_files.append(file)
                file_label = Label(file_frame, text=os.path.basename(file), anchor="w")
                file_label.pack(fill="x")

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<Drop>", on_drop)

    instruction_label = Label(root, text="Drag and Drop up to 5 PDF Files Here", font=("Arial", 14))
    instruction_label.pack(pady=10)

    file_frame = Frame(root)
    file_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def confirm_selection():
        root.destroy()

    confirm_button = Label(root, text="Confirm Selection", font=("Arial", 12), bg="green", fg="white", cursor="hand2")
    confirm_button.pack(pady=10)
    confirm_button.bind("<Button-1>", lambda e: confirm_selection())

    root.mainloop()

    return selected_files[:5]

# Example usage
if __name__ == "__main__":
    print("Select your PDF files using drag-and-drop.")

    pdf_paths = select_pdfs_via_drag_and_drop()

    if not pdf_paths:
        print("No files selected. Exiting.")
        exit()

    try:
        pdf_data = extract_text_from_pdfs(pdf_paths)
        faiss_index, _ = build_faiss_index(pdf_data)

        print("System ready! You can now ask questions. Type 'exit' to quit.")
        while True:
            user_query = input("Ask your question: ")
            if user_query.lower() == "exit":
                print("Exiting. Goodbye!")
                break
            response = answer_question(user_query, pdf_data, faiss_index)
            print(f"\nAnswer:\n{response}\n")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

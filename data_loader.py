from groq import Groq
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv

load_dotenv()

# We use FastEmbed for completely free, local embeddings
embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
EMDEDDING_DIM=384

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)

def load_and_chunk_pdf(path:str):
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts:list[str])->list[list[float]]:
    # get_text_embedding_batch returns a list of embeddings (lists of floats)
    return embed_model.get_text_embedding_batch(texts)
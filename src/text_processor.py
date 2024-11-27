import re

def clean_text(text):
    """Clean and normalize text content."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def split_into_chunks(text, max_tokens=1000):
    """Split text into smaller chunks to handle API token limits."""
    # Simple splitting by paragraphs first
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        # Rough estimate of tokens (words * 1.3)
        para_tokens = len(para.split()) * 1.3
        
        if current_length + para_tokens > max_tokens:
            # Save current chunk and start new one
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_length = para_tokens
        else:
            current_chunk.append(para)
            current_length += para_tokens
    
    # Add the last chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks 
from pypdf import PdfReader
from nltk.corpus import stopwords

def delete_stopwords(document):
    processed_pages = []
    for i, page in enumerate(document):
        processed_pages.append([])
        for token in page:
            if token not in stopwords:
                processed_pages[i].append(token)
    
    return processed_pages

if __name__ == "__main__":
    reader = PdfReader('./documents/N2331126.pdf')
    raw_pages = [page.extract_text() for page in reader.pages]
    tokenized_pages = [page.split(' ') for page in raw_pages]

    processed_text = delete_stopwords(tokenized_pages)

    print(processed_text)




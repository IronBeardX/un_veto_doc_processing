from pypdf import PdfReader

reader = PdfReader('./documents/N2331126.pdf')

print(len(reader.pages))



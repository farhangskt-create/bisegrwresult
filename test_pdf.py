import fitz

doc = fitz.open("gazette.pdf")

page = doc[5388]   # Page 5389 (0-based index)

text = page.get_text()

print(text)

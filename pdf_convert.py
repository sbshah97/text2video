from io import StringIO, BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re

def convert_pdf_to_messy_txt(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = BytesIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    pdf_file = file(fname, 'rb')
    for page in PDFPage.get_pages(pdf_file, pagenums):
        interpreter.process_page(page)
    pdf_file.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


def convert_txt_to_clean(fname):
    fr = open('./txt/' + fname[:-4] + '.txt')
    full_text = ''
    for line in fr:
        if line == '\n':
            full_text += line + '\n'
            continue
        line = line.replace('\n', '')
        line = re.sub(r"[^a-zA-Z0-9'\".,!-]+", ' ', line)
        if len(line) > 3:
            full_text += line + ' '
    print full_text
    fr.close()
    # final text final is stored as filename_clean.txt
    fw = open('./txt/' + fname[:-4] + '_clean.txt', 'w')
    fw.write(full_text.replace('Fig.', 'Figure'))
    fw.close()


pdf_file = 'sample.pdf'
text = convert_pdf_to_messy_txt(pdf_file)

fw = open('./txt/' + pdf_file[:-4] + '.txt', 'w')
fw.write(text)
fw.close()

convert_txt_to_clean(pdf_file)

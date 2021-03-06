from PyPDF2 import PdfFileReader
import fitz
import pandas as pd
import os
import keyword
import numpy as np
def _parse_highlight(annot, wordlist):
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = ['' for i in range(quad_count)]
    for i in range(quad_count):
        r = fitz.Quad(points[i * 4: i * 4 + 4]).rect
        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences[i] = ' '.join(w[4] for w in words)
    sentence = ' '.join(sentences)
    return sentence

# name.remove('main.py')
def file_name(file_dir):
    name= []
    dirs_name = []
    for root, dirs, files in os.walk(file_dir):
        # print('root_dir:', root)  # 当前目录路径

        # print('files:', files)  # 当前路径下所有非目录子文件
        name.append(files)
        print(files)
    return name
name = []
temp= file_name('D:\onedrive\学术\第三篇论文\借鉴文献')

# import os 
# def file_name(file_dir):
#     name = []
#     for root, dirs, files in os.walk(file_dir): 


#         return name
# name = file_name("E:\onedrive\学术\第三篇论文\借鉴文献")

temp = np.unique([j for i in temp for j in i])
temp = list(temp)
key= ".pdf" 
for i in temp:
    print(key in i)
    if key in i:
        name.append(i)
    else:
        pass
last_str = pd.DataFrame()
for i in range(len(name)):
    temp = []
    temp1 = []
    pypdf_doc = PdfFileReader(open(name[i], "rb"))
    num = pypdf_doc.getNumPages()
    pypdf_page = pypdf_doc.getPage(0-num)
    temp.append('--------------------------------------'+name[i]+'--------------------------------------')
    temp.append('------------------------------------------------------------------------------------------------------------')
    temp1.append('--------------------------------------'+name[i]+'--------------------------------------')
    temp1.append('------------------------------------------------------------------------------------------------------------')
    
    pdf_input = PdfFileReader(open(name[i], "rb"))
    n_pages = pdf_input.getNumPages()
    print("This document has %d pages." % n_pages)
    mupdf_doc = fitz.open(name[i])
    for k in range(n_pages) :
    # get the data from this PDF page (first line of text, plus annotations)
        page = pdf_input.getPage(k)
        text = page.extractText()
    
        try :
            if '/Annots' in page:
                # print("Page comments num: %d" % len(page["/Annots"]))
                for annot in page['/Annots'] :
                    # Other subtypes, such as /Link, cause errors
                    #for key in annot.getObject().keys():
                            #print(annot.getObject()[key])
                    subtype = annot.getObject()['/Subtype']
                    #if subtype == "/Popup":
                    #    print(annot.getObject()['/Parent']['/Popup'])
                    if subtype == "/Highlight":
                        print(annot.getObject()['/Contents'])
                        temp.append(str(annot.getObject()['/Contents']))
        except :
            pass

    

    
        try :
            mupdf_page = mupdf_doc.loadPage(k)
            wordlist = mupdf_page.getText("words")  # list of words on page
            wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x
            for annot in mupdf_page.annots():
                # underline / highlight / strikeout / squiggly : 8 / 9 / 10 / 11
                if annot.type[0] == 8:
                    print(_parse_highlight(annot, wordlist))
                    temp1.append(_parse_highlight(annot, wordlist))
        except :
            pass
        
        

    temp.append('.')
    temp1.append('.')
    temp = pd.DataFrame(temp)
    temp1 = pd.DataFrame(temp1)
    result = pd.concat([temp,temp1],axis =1)
    last_str = pd.concat([result,last_str])
last_str.to_csv('pdf注释汇总.csv', encoding='utf_8_sig')

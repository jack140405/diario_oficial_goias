import os, fitz
from unidecode import unidecode

def extrair_texto_pagina(doc, page_index):
    try:
        return doc[page_index].get_text('text') or ''
    except Exception:
        return ''

def salvar_paginas_filtradas(caminho_pdf, paginas, sufixo='_filtrado'):
    base = os.path.splitext(caminho_pdf)[0]
    novo = f"{base}{sufixo}.pdf"
    doc = fitz.open(caminho_pdf); novo_doc = fitz.open()
    for p in paginas:
        novo_doc.insert_pdf(doc, from_page=p-1, to_page=p-1)
    novo_doc.save(novo); novo_doc.close(); doc.close()
    return novo

def buscar_palavra_no_pdf(caminho_pdf, palavra_chave, usar_ocr_fallback=False):
    palavra_norm = unidecode(palavra_chave).lower()
    paginas_encontradas = []
    try:
        doc = fitz.open(caminho_pdf)
    except Exception as e:
        print('Erro abrir PDF', e); return [], None
    for i in range(len(doc)):
        texto = extrair_texto_pagina(doc, i)
        texto_norm = unidecode(texto).lower()
        if palavra_norm in texto_norm:
            paginas_encontradas.append(i+1)
    doc.close()
    if paginas_encontradas:
        filtrado = salvar_paginas_filtradas(caminho_pdf, paginas_encontradas)
        return paginas_encontradas, filtrado
    return [], None

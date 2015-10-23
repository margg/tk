import os
import sys
import re
import codecs


def find_meta(text, name):
    pattern = r"<meta[^>]* name=\"" + name + r"\"[^>]* content=\"([^\"]*)\""
    return re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

def process_file(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    autorzy = find_meta(content, "autor")
    dzialy = find_meta(content, "dzial")
    kluczowe = find_meta(content, "kluczowe_.")

    fp.close()

    print("nazwa pliku: {0}".format(filepath))
    for autor in autorzy:
        print("autor: {0}".format(autor))
    for dzial in dzialy:
        print("dzial: {0}".format(dzial))
    print("slowa kluczowe: "),
    for klucz in kluczowe:
        print("{0}, ".format(klucz)),
    print
    print("liczba zdan:")
    print("liczba skrotow:")
    print("liczba liczb calkowitych z zakresu int:")
    print("liczba liczb zmiennoprzecinkowych:")
    print("liczba dat:")
    print("liczba adresow email:")
    print("\n")


# try:
#     path = sys.argv[1]
# except IndexError:
#     print("Brak podanej nazwy katalogu")
#     sys.exit(0)
#
#
# tree = os.walk(path)
#
# for root, dirs, files in tree:
#     for f in files:
#         if f.endswith(".html"):
#             filePath = os.path.join(root, f)
#             processFile(filePath)

process_file("1993-01/199301040001.html")
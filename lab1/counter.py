import os
import sys
import re
import codecs

def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    meta = re.findall(r"(<META [^>]*>)", content, re.DOTALL | re.IGNORECASE)
    meta.append("<META CONTENT=\"Jacek Czarnecki\" NAME=\"AUTOR\">")

    nameAttr = r"(?P<name>NAME(?:\s*)=(?:\s*)\"AUTOR\")"
    contentAttr = r"(?P<content>CONTENT(?:\s*)=(?:\s*)\"(?P<autor>[^\"]*)\")"
    authorPattern1 = re.compile(nameAttr + r"(?P<other>.*)" + contentAttr, re.DOTALL | re.IGNORECASE)
    authorPattern2 = re.compile(contentAttr + r"(?P<other>.*)" + nameAttr, re.DOTALL | re.IGNORECASE)

    for m in meta:
        mat = authorPattern1.search(m) or authorPattern2.search(m)
        if mat:
            author = mat.group('autor')


    fp.close()
    print("nazwa pliku: {0}".format(filepath))
    print("autor:")
    print("dzial:")
    print("slowa kluczowe:")
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

processFile("1993-01/199301030001.html")
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

    zdania = []

    skroty = re.findall(r"[ ^]+([a-z]{1,3}\.)[ \n$]+", content, re.IGNORECASE | re.MULTILINE)



    fp.close()
    print("nazwa pliku: {0}".format(filepath))
    try:
        for autor in autorzy:
            print("autor: {0}".format(autor))
    except UnicodeEncodeError:      # problem przy wypisywaniu polskich znakow
        print "Unicode Encode Error\n"
        pass

    try:
        for dzial in dzialy:
            print("dzial: {0}".format(dzial))
    except UnicodeEncodeError:
        print "Unicode Encode Error\n"
        pass

    print("slowa kluczowe: "),
    try:
        for klucz in kluczowe:
            if klucz:   # pomin puste slowa kluczowe
                print("{0},".format(klucz)),
        print
    except UnicodeEncodeError:
        print "Unicode Encode Error\n"
        pass

    print("liczba zdan:")

    skroty = set(skroty)
    print("liczba skrotow: {0}\n\t".format(len(skroty))),
    for s in skroty:
        print("{0},".format(s)),
    print
    print("liczba liczb calkowitych z zakresu int:")
    print("liczba liczb zmiennoprzecinkowych:")
    print("liczba dat:")
    print("liczba adresow email:")
    print("\n")
    print("======================================================\n")


try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filePath = os.path.join(root, f)
            process_file(filePath)


import os
import sys
import re
import codecs


def find_meta(text, name):
    # dla czytelnosci pomienieta mozliwosc uzycia bialych znakow przed i po [=<>] (\s*)
    pattern = r"<meta[^>]* name=\"" + name + r"\"[^>]* content=\"([^\"]*)\""
    return re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

def process_file(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    authors = find_meta(content, "autor")
    sections = find_meta(content, "dzial")
    keywords = find_meta(content, "kluczowe_.")

    article = (re.search(r"<p>(.*?)<meta ", content, re.IGNORECASE | re.DOTALL)).group(1)
    sentences = []
    abbreviations = set(re.findall(r"[ ^]+([a-z]{1,3}\.)[ \n$]+", article, re.IGNORECASE | re.MULTILINE))



    fp.close()
    print("nazwa pliku: {0}".format(filepath))
    try:
        for author in authors:
            print("autor: {0}".format(author))
    except UnicodeEncodeError:      # problem przy wypisywaniu polskich znakow
        print "Unicode Encode Error\n"
        pass

    try:
        for section in sections:
            print("dzial: {0}".format(section))
    except UnicodeEncodeError:
        print "Unicode Encode Error\n"
        pass

    print("slowa kluczowe: "),
    try:
        for key in keywords:
            if key:   # pomin puste slowa keywords
                print("{0},".format(key)),
        print
    except UnicodeEncodeError:
        print "Unicode Encode Error\n"
        pass

    print("liczba zdan:")

    print("liczba skrotow: {0}\n\t".format(len(abbreviations))),
    for abb in abbreviations:
        print("{0},".format(abb)),
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


import os
import sys
import re
import codecs
from datetime import datetime


def find_meta(text, name):
    # dla czytelnosci pomienieta mozliwosc uzycia bialych znakow przed i po [=<>] (\s*)
    pattern = r'<meta[^>]* name="' + name + r'"[^>]* content="([^"]*)"'
    return re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

def process_file(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    authors = find_meta(content, "autor")
    sections = find_meta(content, "dzial")
    keywords = find_meta(content, "kluczowe_\d+")

    article = re.search(r"<p[^>]*>(.*?)<meta", content, re.IGNORECASE | re.DOTALL)
    article = article.group(1) if article else ""

    sentences = re.findall(r'[a-zA-Z0-9\s]*[^\s\.\?!\d><]{4,}(?:(?:[\?\.!]+)|(?:\s*<[^>]*>\s*\n))', article, re.IGNORECASE | re.DOTALL)
    for a in sentences:
        print(u'%s ::::', a)

    abbreviations = set(re.findall(r"(?:^|\s|\b)+([a-z]{1,3}\.)(?:$|\s|\b)+", article, re.IGNORECASE))
    # -32768 - 32767, przed: bialy znak, po: bialy znak lub kropka i bialy znak, lub przecinek i bialy znak
    integers = set(map(lambda x: x[1], re.findall(
        r"(\s|^)((-?)(\d{1,4}|[1-2]\d{4}|3[01]\d{3}|32[1-6]\d{2}|327[0-5]\d|3276[0-7])|-32768)((\s)|(,\s)|\.(\s|$)|$)", article)))

    floats = set(map(lambda x: x[2], re.findall(r"((\s|^)(([1-9]\d*\.\d+(e(\+|-)\d+)?)|([0]?\.\d+)|([1-9]\d*\.)))(\s|\.(\s|$)|$)",
        article, re.IGNORECASE | re.MULTILINE)))

    dates = set()
    dates = dates.union(set([":".join([y for y in x if y]) for x in 
        re.findall(r"(?:(\d{4})\.(0\d|1[0-2])\.([0-2]\d))|(?:(\d{4})-(0\d|1[0-2])-([0-2]\d))|(?:(\d{4})/(0\d|1[0-2])/([0-2]\d))", 
        article, re.IGNORECASE | re.MULTILINE)]))
    dates = dates.union(set([":".join([y for y in x if y][::-1]) for x in 
        re.findall(r"(?:([0-2]\d)\.(0\d|1[0-2])\.(\d{4}))|(?:([0-2]\d)-(0\d|1[0-2])-(\d{4}))|(?:([0-2]\d)/(0\d|1[0-2])/(\d{4}))", 
        article, re.IGNORECASE | re.MULTILINE)]))
    print(dates)

    emails = set(map(lambda x: x[1], re.findall(
        r"(\b|\s|^)(([a-z0-9]\.?\-?_?\+?)*([a-z0-9])@(([a-z0-9]\-?_?\+?)+(\.([a-z0-9]\-?_?\+?)+)+))(\b|\s|\.(\s|$)|$)",
        content, re.IGNORECASE)))


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

    print("liczba zdan: %s" % len(sentences))

    print("liczba roznych skrotow: {0}\n\t".format(len(abbreviations))),
    for abb in abbreviations:
        print("{0},".format(abb)),
    print

    print("liczba roznych liczb calkowitych z zakresu int: {0}\n\t".format(len(integers))),
    for i in integers:
        print("{0},".format(i)),
    print

    print("liczba roznych liczb zmiennoprzecinkowych: {0}\n\t".format(len(floats))),
    for f in floats:
        print("{0},".format(f)),
    print

    print("liczba roznych dat: {0}".format(len(dates)))
    for d in dates:
        print("\t%s" % d)

    print("liczba roznych adresow email: {0}\n\t".format(len(emails))),
    for e in emails:
        print("{0},".format(e)),
    print
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

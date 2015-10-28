import os
import sys
import re
import codecs


def find_meta(text, name):
    # dla czytelnosci pomienieta mozliwosc uzycia bialych znakow przed i po [=<>] (\s*)
    pattern = r'<meta[^>]* name="' + name + r'"[^>]* content="([^"]*)"'
    return re.findall(pattern, text, re.DOTALL | re.IGNORECASE | re.UNICODE)


def process_file(filepath):
    verbose = False

    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    authors = find_meta(content, "autor")
    sections = find_meta(content, "dzial")
    keywords = find_meta(content, "kluczowe_\d+")

    article = re.search(r'<p(?:\s[^>]*)*>(.*?)<meta\s', content, re.IGNORECASE | re.DOTALL | re.UNICODE)
    article = article.group(1) if article else content

    # sentences = re.findall(r'[a-zA-Z0-9\s]*[^\s\.\?!\d><]{4,}(?:(?:[\?\.!]+)|(?:\s*<[^>]*>\s*\n))',
    #                        article, re.IGNORECASE | re.DOTALL | re.UNICODE)

    sentences = map(lambda x: x[1], re.findall(r'(((?<![^.?!]\s)[A-Z0-9].{4,}?([.|?|!]+))(?=((\s)+([A-Z]|$|<))))',
                                               article, re.DOTALL | re.UNICODE))
    if verbose:
        for a in sentences:
            print(a)
            print "-----"

    abbreviations = set(re.findall(r'(?:^|\s|\b)+([a-z]{1,3}\.)(?:$|\s|\b)+', article, re.IGNORECASE))
    # -32768 - 32767, przed: bialy znak, po: bialy znak lub kropka i bialy znak, lub przecinek i bialy znak
    integers = set(map(lambda x: x[1], re.findall(
        r'(\s|^)((-?)(\d{1,4}|[1-2]\d{4}|3[01]\d{3}|32[1-6]\d{2}|327[0-5]\d|3276[0-7])|-32768)((\s)|(,\s)|\.(\s|$)|$)',
        article)))

    floats = set(map(lambda x: x[2], re.findall(
        r'((\s|^)(([1-9]\d*\.\d+(e(\+|-)\d+)?)|([0]?\.\d+)|([1-9]\d*\.)))(\s|\.(\s|$)|$)',
        article, re.IGNORECASE | re.MULTILINE)))

    dats = re.findall(r'(?:(\d{4})(?P<delim>\.|-|/)(?:(?:(0\d|1[0-2])(?P=delim)([0-2]\d))|(?:(0[13578]|10|12)(?P=delim)(30|31))|(?:(0[469]|11)(?P=delim)(30))))', article)
    dates = set()
    for d in dats:
        dates = dates.union({(":".join([d[0], d[2] or d[4] or d[6], d[3] or d[5] or d[7]]))})
    dats = re.findall(r'(?:(?:(?:([0-2]\d)(?P<delim>\.|-|/)(0\d|1[0-2]))|(?:(30|31)(?P=delim)(0[13578]|10|12))|(?:(30)(?P=delim)(0[469]|11)))(?P=delim)(\d{4}))', article)
    for d in dats:
        dates = dates.union({":".join([d[7], d[2] or d[4] or d[6], d[0] or d[3] or d[5]])})
    if verbose:
        print(dates)

    emails = set(map(lambda x: x[1], re.findall(
        r'(\b|\s|^)(([a-z0-9]\.?\-?_?\+?)*([a-z0-9])@(([a-z0-9]\-?_?\+?)+(\.([a-z0-9]\-?_?\+?)+)+))(\b|\s|\.(\s|$)|$)',
        content, re.IGNORECASE)))

    fp.close()
    print(u"nazwa pliku: {0}".format(filepath))
    for author in authors:
        print(u"autor: {0}".format(author))

    for section in sections:
        print(u"dzial: {0}".format(section))

    print("slowa kluczowe: "),
    for key in keywords:
        if key:  # pomin puste slowa kluczowe
            print(u"{0},".format(key)),
    print

    print("liczba zdan: %s" % len(sentences))

    print("liczba roznych skrotow: {0}".format(len(abbreviations)))
    if verbose:
        print("\t")
    for abb in abbreviations:
        print(u"{0},".format(abb)),
    print

    print("liczba roznych liczb calkowitych z zakresu int: {0}".format(len(integers)))
    if verbose:
        print("\t")
    for i in integers:
        print("{0},".format(i)),
    print

    print("liczba roznych liczb zmiennoprzecinkowych: {0}".format(len(floats)))
    if verbose:
        print("\t")
    for f in floats:
        print("{0},".format(f)),
    print

    print("liczba roznych dat: {0}".format(len(dates)))
    if verbose:
        for d in dates:
            print("\t%s" % d),
    print

    print("liczba roznych adresow email: {0}".format(len(emails)))
    if verbose:
        print("\t")
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

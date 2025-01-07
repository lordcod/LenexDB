import difflib
dfr = difflib.HtmlDiff()

r = dfr.make_file(
    open('result/result.xml').read().splitlines(keepends=True),
    open('result/result2.xml').read().splitlines(keepends=True),
)
with open('result/diff.html', 'w+') as f: 
    f.write(r)
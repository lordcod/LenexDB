import difflib
dfr = difflib.HtmlDiff()

r = dfr.make_file(
    open('result/official.lef').read().splitlines(keepends=True),
    open('result/test2.lef').read().splitlines(keepends=True),
)
with open('result/diff.html', 'w+') as f: 
    f.write(r)
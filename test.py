"""
このファイルに解答コードを書いてください
"""
INPUT_TXT = "input.txt"

tmp = []
ans = ''

with open(INPUT_TXT, "r") as f:
    for txt in f.readlines():
        "改行を削除する"
        txt = txt.strip()

        "一行ずつ解析 :がくるまでが整数i"
        i = ''
        for index, t in enumerate(txt):
            if t == ':':
                "[数字i, 文字s]を格納する"
                tmp.append([int(i), txt[index + 1:]])
                break
            i += t

    "最後に受け取った数字"
    m = int(txt)

    "sortを行い, 判別をする"
    tmp.sort()
    for i, s in tmp:
        if m % i == 0:
            ans += s
    if ans == '':
        ans = str(m)
    print(ans)

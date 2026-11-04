#!/usr/bin/env python3
"""填完 report.html 后自检：占位符残留、文件树/doc/大纲三处 id 对齐、死锚点。

用法：python3 check_report.py <报表.html>
退出码 0 表示通过，1 表示有错。
"""
import re
import sys

PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}")


def main(path):
    s = open(path, encoding="utf-8").read()
    errors = []

    left = PLACEHOLDER.findall(s)
    if left:
        errors.append(f"占位符未替换：{sorted(set(left))}")

    docs = re.findall(r'<section class="doc[^"]*" id="doc-([^"]+)"', s)
    tree = re.findall(r'class="file[^"]*" data-doc="([^"]+)"', s)
    outs = re.findall(r'class="outline-panel[^"]*" data-doc="([^"]+)"', s)

    for name, got in (("文件树", tree), ("大纲", outs)):
        missing = set(docs) - set(got)
        extra = set(got) - set(docs)
        if missing:
            errors.append(f"{name}缺项：{sorted(missing)}")
        if extra:
            errors.append(f"{name}多出：{sorted(extra)}")
    if len(set(docs)) != len(docs):
        errors.append("doc id 有重复")

    ids = set(re.findall(r'id="([^"]+)"', s))
    dead = sorted({h for h in re.findall(r'href="#([^"]+)"', s) if h not in ids})
    if dead:
        errors.append(f"死锚点：{dead}")

    for e in errors:
        print("✗", e)
    if not errors:
        print(f"✓ 通过：{len(docs)} 篇，文件树/大纲/锚点一致")
    return 0 if not errors else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip())
        sys.exit(2)
    sys.exit(main(sys.argv[1]))

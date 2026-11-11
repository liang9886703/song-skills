#!/usr/bin/env python3
"""创建共享源码、由用户独立配置 .agents 的验证目录。"""

import argparse
import os
from contextlib import ExitStack
from pathlib import Path


def link_workspace(source_path, output_path=None):
    source = source_path.expanduser().resolve(strict=True)
    if not source.is_dir():
        raise ValueError(f"源路径不是目录：{source}")

    if output_path is None:
        output = source.with_name(f"{source.name}-agent-verify")
    else:
        requested = output_path.expanduser()
        output = requested.parent.resolve(strict=True) / requested.name

    if output == source or source in output.parents:
        raise ValueError(f"输出目录必须在源目录之外：{output}")

    entries = [entry for entry in source.iterdir() if entry.name != ".agents"]
    output.mkdir()
    with ExitStack() as cleanup:
        cleanup.callback(output.rmdir)
        for entry in entries:
            link = output / entry.name
            link.symlink_to(os.path.relpath(entry, start=output))
            cleanup.callback(link.unlink)
        cleanup.pop_all()

    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="已有的源目录")
    parser.add_argument("output", type=Path, nargs="?", help="尚不存在的输出目录")
    args = parser.parse_args()

    try:
        output = link_workspace(args.source, args.output)
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f"{error}\n")

    print(output)


if __name__ == "__main__":
    main()

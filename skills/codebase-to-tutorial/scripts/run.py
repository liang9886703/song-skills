#!/usr/bin/env python3
"""Run unchanged upstream nodes with responses supplied by the host agent."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import types


def save_json(path, value):
    tmp = path.with_name(path.name + '.new')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser(description='使用当前智能体，把代码库转为中文教程。')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--dir', type=Path)
    source.add_argument('--repo')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--work-dir', type=Path)
    parser.add_argument('--name')
    parser.add_argument('--language', default='Chinese')
    parser.add_argument('--include', nargs='+')
    parser.add_argument('--exclude', nargs='+')
    parser.add_argument('--max-size', type=int, default=100000)
    parser.add_argument('--max-abstractions', type=int, default=10)
    args = parser.parse_args()
    python = Path(os.environ.get('CODEBASE_TUTORIAL_PYTHON', str(Path.home() / '.local/share/codebase-to-tutorial/venv/bin/python'))).expanduser()
    if python.exists() and Path(sys.prefix).resolve() != python.parent.parent.resolve():
        os.execv(str(python), [str(python), str(Path(__file__).resolve()), *sys.argv[1:]])
    try:
        import pocketflow, yaml, dotenv, requests, git, pathspec  # noqa: F401
    except ImportError as exc:
        parser.error(f'缺少运行依赖：{exc.name}。请在独立虚拟环境安装 requirements-host.txt。')
    upstream = Path(__file__).resolve().parents[1] / 'assets/upstream'
    output = args.output.expanduser().resolve()
    work = (args.work_dir or output / '.codebase-to-tutorial').expanduser().resolve()
    local = args.dir.expanduser().resolve() if args.dir else None
    if local and not local.is_dir():
        parser.error('本地源码目录不存在。')
    name = args.name or (local.name if local else args.repo.rstrip('/').split('/')[-1].removesuffix('.git'))
    if not name or name in {'.', '..'} or '/' in name or '\\' in name:
        parser.error('项目名称不能是路径。')
    if local and (output == local or local in output.parents or work == local or local in work.parents):
        parser.error('请选择源码目录之外的输出目录和工作目录。')
    config = {'source': str(local) if local else args.repo, 'output': str(output), 'name': name,
              'language': args.language, 'include': args.include, 'exclude': args.exclude,
              'max_size': args.max_size, 'max_abstractions': args.max_abstractions}
    if (work / 'run.json').exists():
        if json.loads((work / 'run.json').read_text(encoding='utf-8')) != config:
            parser.error('工作目录用于另一组参数，请换一个工作目录。')
        if (work / 'completed.json').exists():
            completed = json.loads((work / 'completed.json').read_text(encoding='utf-8'))
            print('已有完成的教程快照：' + completed['index'])
            return
    elif (output / name).exists():
        parser.error('教程目标已存在，请选择新的输出位置或项目名称。')
    work.mkdir(parents=True, exist_ok=True)
    spool = work / 'model-exchange'
    spool.mkdir(exist_ok=True)
    save_json(work / 'run.json', config)
    pending = work / 'pending.json'
    state = {'calls': 0, 'reused': 0}

    def host_llm(prompt, use_cache=True):
        state['calls'] += 1
        key = hashlib.sha256(prompt.encode()).hexdigest()
        prompt_path = spool / (key + '.prompt.txt')
        response_path = spool / (key + '.response.txt')
        if not prompt_path.exists():
            prompt_path.write_text(prompt, encoding='utf-8')
        if response_path.exists() and response_path.read_text(encoding='utf-8').strip():
            response = response_path.read_text(encoding='utf-8')
            if use_cache:
                state['reused'] += 1
                return response
            rejected = spool / (key + '.rejected-' + hashlib.sha256(response.encode()).hexdigest()[:12] + '.txt')
            response_path.replace(rejected)
        save_json(pending, {'id': key, 'call': state['calls'], 'prompt': str(prompt_path),
                            'response': str(response_path), 'chars': len(prompt)})
        print('等待当前智能体提供响应：' + str(pending))
        raise SystemExit(75)

    module = types.ModuleType('utils.call_llm')
    module.call_llm = host_llm
    sys.modules['utils.call_llm'] = module
    sys.path.insert(0, str(upstream))
    os.chdir(work)
    import main as native
    from nodes import FetchRepo
    original_post = FetchRepo.post

    def record_crawl(self, shared, prep, execution):
        original_post(self, shared, prep, execution)
        save_json(work / 'crawl-files.json', shared['files'])
        save_json(work / 'crawl-manifest.json', [
            {'index': i, 'path': path, 'chars': len(content), 'sha256': hashlib.sha256(content.encode()).hexdigest()}
            for i, (path, content) in enumerate(shared['files'])])

    FetchRepo.post = record_crawl
    argv = ['main.py', '--dir' if local else '--repo', str(local) if local else args.repo,
            '--name', name, '--output', str(output), '--language', args.language,
            '--max-size', str(args.max_size), '--max-abstractions', str(args.max_abstractions)]
    if args.include:
        argv += ['--include', *args.include]
    if args.exclude:
        argv += ['--exclude', *args.exclude]
    sys.argv = argv
    native.main()
    destination = output / name
    chinese = args.language.lower() in {'chinese', '中文', 'zh', 'zh-cn'}
    source_link = str(local) if local else args.repo
    for path in destination.glob('*.md'):
        text = path.read_text(encoding='utf-8')
        if chinese:
            text = re.sub(r'^# Tutorial: ', '# 项目代码阅读教程：', text, flags=re.M)
            text = re.sub(r'^# Chapter (\d+): ', lambda m: '# 第' + m[1] + '章：', text, flags=re.M)
            text = text.replace('\n## Chapters\n', '\n## 章节目录\n')
            text = text.replace('**Source Repository:**', '**源码位置：**')
            text = text.replace('\nGenerated by [AI Codebase Knowledge Builder]', '\n由 [AI Codebase Knowledge Builder]')
        text = text.replace('[None](None)', '[' + source_link + '](' + source_link + ')')
        path.write_text(text, encoding='utf-8')
    manifest = json.loads((work / 'crawl-manifest.json').read_text(encoding='utf-8'))
    report = f'''# 教程运行说明

- 源码：`{source_link}`
- 上游版本：`05b24cbbb0fe409c5e23c9791f0342f07524ffdc`
- 原生抓取文件数：{len(manifest)}；模型请求数：{state['calls']}。
- 方式：上游 PocketFlow 原生节点运行，当前智能体提供模型响应，未调用外部模型 API。
- 默认抓取排除测试、文档及超限文件。抓取不等于逐行审阅全部内容。
- 文件索引及内容哈希：`{work / 'crawl-manifest.json'}`。
- 原始提示词和响应：`{spool}`。

## 实际阅读与校验

由当前智能体在交付前补充实际阅读范围、源码链接检查及代码／图示校验结果。未执行的代码和测试不能标记为已通过。
'''
    (destination / 'run-report.md').write_text(report, encoding='utf-8')
    save_json(work / 'completed.json', {'index': str(destination / 'index.md'), 'files': len(manifest), **state})
    if pending.exists():
        pending.unlink()
    print('教程生成完成：' + str(destination / 'index.md'))


if __name__ == '__main__':
    main()

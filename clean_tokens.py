#!/usr/bin/env python3
import os, re, sys

# 匹配 GitHub token 模式
pattern = re.compile(r'ghp_[A-Za-z0-9]{36}')

def clean_file(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if pattern.search(content):
            new_content = pattern.sub('[REDACTED]', content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Cleaned: {path}')
            return True
    except Exception as e:
        pass
    return False

# 遍历所有 .md 和 .jsonl 文件
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.md', '.jsonl')):
            path = os.path.join(root, f)
            clean_file(path)

print('Token cleanup complete.')
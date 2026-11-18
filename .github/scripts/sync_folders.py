"""Mirror the folder structure of this repo (down to the book-name folder) into a target checkout.

Usage: python sync_folders.py <source_repo_dir> <target_repo_dir>

Rules
- A "book folder" is a folder under tech/ that contains Readme.md and has no ancestor folder
  (under tech/) that also contains Readme.md. Part/chapter folders below a book folder are skipped.
- For each book folder, the same relative path is created in the target with an empty .gitkeep
  (git cannot store empty folders).
- Existing non-empty target folders are left alone. Nothing in the target is ever deleted or renamed.
"""
import os
import sys

ROOT = 'tech'


def find_book_dirs(src):
    readme_dirs = set()
    for d, _, files in os.walk(os.path.join(src, ROOT)):
        if any(f.lower() == 'readme.md' for f in files):
            readme_dirs.add(os.path.relpath(d, src))
    books = []
    for d in sorted(readme_dirs):
        if any(d != a and d.startswith(a + os.sep) for a in readme_dirs):
            continue
        books.append(d)
    return books


def main():
    src, dst = sys.argv[1], sys.argv[2]
    books = find_book_dirs(src)
    created, kept = [], []
    for b in books:
        path = os.path.join(dst, b)
        if os.path.isdir(path) and os.listdir(path):
            kept.append(b)
            continue
        os.makedirs(path, exist_ok=True)
        open(os.path.join(path, '.gitkeep'), 'w').close()
        created.append(b)
    print('book folders in source: %d' % len(books))
    print('created in target: %d' % len(created))
    print('already present (left untouched): %d' % len(kept))
    for b in created:
        print('  + ' + b.replace(os.sep, '/'))


if __name__ == '__main__':
    main()

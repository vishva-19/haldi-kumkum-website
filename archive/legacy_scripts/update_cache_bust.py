with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add ?v=3 to all img/ references in src and url
import re
def repl(match):
    prefix = match.group(1)
    path = match.group(2)
    suffix = match.group(3)
    if '?' not in path:
        path = path + '?v=3'
    return f"{prefix}{path}{suffix}"

# replace src="img/..."
content = re.sub(r'(src=["\'])(img/[^"\']+)(["\'])', repl, content)
# replace url('img/...')
content = re.sub(r'(url\(["\']?)(img/[^"\'\)]+)(["\']?\))', repl, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cache bust query ?v=3 applied across index.html")

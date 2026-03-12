import zipfile, xml.etree.ElementTree as ET, re, sys

pptx_path = '/Users/kaku/WorkBuddy/20260312232602/DeepSeek_V4_Weekly_Report.pptx'
z = zipfile.ZipFile(pptx_path)

# Get ordered slides
slides = sorted(
    [f for f in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', f)],
    key=lambda x: int(re.search(r'(\d+)', x.split('/')[-1]).group())
)

print(f"Total slides: {len(slides)}\n")

for slide_path in slides:
    num = re.search(r'(\d+)', slide_path.split('/')[-1]).group()
    tree = ET.fromstring(z.read(slide_path))
    texts = []
    for elem in tree.iter():
        if elem.tag.endswith('}t') and elem.text:
            texts.append(elem.text.strip())
    content = ' '.join(texts).strip()
    print(f'=== Slide {num} ===')
    print(content if content else '(no text content)')
    print()

z.close()

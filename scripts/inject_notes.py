#!/usr/bin/env python3
"""
inject_notes.py — Inject speaker notes into a PPTX file (fast, in-memory).

Usage:
    python inject_notes.py <pptx_file> <notes_json> [output_file]

Arguments:
    pptx_file   : Path to the source .pptx file
    notes_json  : Path to a JSON file containing notes to inject
    output_file : (Optional) Output path. Defaults to <pptx_file_stem>_with_notes.pptx

The notes JSON format:
{
    "slide_notes": {
        "1": "Speaker notes for slide 1 (Script + Transition only)",
        "2": "Speaker notes for slide 2",
        ...
    }
}

"slide_notes" maps slide numbers (1-indexed, by presentation order) to their
speaker note text. Only [Script] and [Transition] content should be included.

Performance: This script operates entirely in memory — no temp directory
extraction. Typical injection for a 20-slide deck completes in <1 second.
"""

import json
import io
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# ──────────────────────────────────────────────────────────────
# OOXML constants
# ──────────────────────────────────────────────────────────────

NS = {
    'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r':   'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p':   'http://schemas.openxmlformats.org/presentationml/2006/main',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
    'ct':  'http://schemas.openxmlformats.org/package/2006/content-types',
}

# Register namespaces so ET output uses clean prefixes
for _pfx, _uri in NS.items():
    if _pfx != 'ct':
        ET.register_namespace(_pfx, _uri)
ET.register_namespace('', NS['rel'])  # default ns for .rels files
ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')
ET.register_namespace('o',  'urn:schemas-microsoft-com:office:office')
ET.register_namespace('v',  'urn:schemas-microsoft-com:vml')

NOTES_CT   = 'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml'
NOTES_REL  = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide'
SLIDE_REL  = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide'
NMASTER_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster'
NMASTER_CT = 'application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml'

REL_NS     = NS['rel']
CT_NS      = NS['ct']

# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def _escape(text: str) -> str:
    """Escape XML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))


def _build_notes_xml(text: str) -> str:
    """Build a complete notesSlide XML string from plain text."""
    paras = []
    for line in text.split('\n'):
        paras.append(
            f'<a:p><a:r><a:rPr lang="zh-CN" dirty="0"/>'
            f'<a:t>{_escape(line)}</a:t></a:r></a:p>'
        )
    body = '\n'.join(paras)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
         xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
         xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr/>
    <p:sp>
      <p:nvSpPr><p:cNvPr id="2" name="Slide Image Placeholder"/>
        <p:cNvSpPr><a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr>
        <p:nvPr><p:ph type="sldImg"/></p:nvPr></p:nvSpPr>
      <p:spPr/>
    </p:sp>
    <p:sp>
      <p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder"/>
        <p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
        <p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>
      <p:spPr/>
      <p:txBody><a:bodyPr/><a:lstStyle/>
        {body}
      </p:txBody>
    </p:sp>
  </p:spTree></p:cSld>
</p:notes>'''


def _build_notes_rels(slide_basename: str) -> str:
    """Build the .rels file for a notesSlide."""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="{SLIDE_REL}" Target="../slides/{slide_basename}"/>
  <Relationship Id="rId2" Type="{NMASTER_REL}" Target="../notesMasters/notesMaster1.xml"/>
</Relationships>'''


def _minimal_notes_master() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notesMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
               xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
               xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr/>
  </p:spTree></p:cSld>
</p:notesMaster>'''


def _minimal_notes_master_rels() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>'''


def _next_rid(rels_root: ET.Element) -> str:
    """Find the next available rId in a .rels root."""
    max_id = 0
    for rel in rels_root:
        m = re.match(r'rId(\d+)', rel.get('Id', ''))
        if m:
            max_id = max(max_id, int(m.group(1)))
    return f'rId{max_id + 1}'


def _et_to_bytes(tree_or_root, xml_declaration: bool = True) -> bytes:
    """Serialize an ElementTree or Element to bytes."""
    buf = io.BytesIO()
    if isinstance(tree_or_root, ET.ElementTree):
        tree_or_root.write(buf, xml_declaration=xml_declaration, encoding='UTF-8')
    else:
        et = ET.ElementTree(tree_or_root)
        et.write(buf, xml_declaration=xml_declaration, encoding='UTF-8')
    return buf.getvalue()


def _parse_xml(data: bytes) -> ET.Element:
    return ET.fromstring(data)


# ──────────────────────────────────────────────────────────────
# Main injection logic (in-memory ZIP)
# ──────────────────────────────────────────────────────────────

def inject_notes(pptx_path: str, notes_json_path: str, output_path: str = None):
    """Inject speaker notes into PPTX entirely in memory."""
    pptx_path = Path(pptx_path)
    if output_path is None:
        output_path = pptx_path.parent / f'{pptx_path.stem}_with_notes.pptx'
    else:
        output_path = Path(output_path)

    # Load notes data
    with open(notes_json_path, 'r', encoding='utf-8') as f:
        notes_data = json.load(f)
    slide_notes = notes_data.get('slide_notes', {})
    if not slide_notes:
        print("⚠️  No slide_notes found in JSON. Nothing to inject.")
        return str(output_path)

    # Read entire PPTX into memory as a dict: arcname -> bytes
    file_map: dict[str, bytes] = {}
    with zipfile.ZipFile(pptx_path, 'r') as zin:
        for item in zin.infolist():
            file_map[item.filename] = zin.read(item.filename)

    # ── Step 1: Determine slide order from presentation.xml ──
    pres_xml = _parse_xml(file_map['ppt/presentation.xml'])
    pres_rels = _parse_xml(file_map['ppt/_rels/presentation.xml.rels'])

    rid_to_target = {}
    for rel in pres_rels:
        if rel.get('Type') == SLIDE_REL:
            rid_to_target[rel.get('Id')] = rel.get('Target')  # e.g. slides/slide1.xml

    sld_id_lst = pres_xml.find(f'.//{{{NS["p"]}}}sldIdLst')
    ordered_slides = []  # list of "slides/slideN.xml"
    if sld_id_lst is not None:
        for sld_id in sld_id_lst:
            rid = sld_id.get(f'{{{NS["r"]}}}id')
            if rid in rid_to_target:
                ordered_slides.append(rid_to_target[rid])

    print(f"📊 Found {len(ordered_slides)} slides, injecting notes for {len(slide_notes)} slides")

    # ── Step 2: Ensure notesMaster exists ──
    nm_path = 'ppt/notesMasters/notesMaster1.xml'
    nm_rels_path = 'ppt/notesMasters/_rels/notesMaster1.xml.rels'
    need_nm = nm_path not in file_map

    if need_nm:
        file_map[nm_path] = _minimal_notes_master().encode('utf-8')
        file_map[nm_rels_path] = _minimal_notes_master_rels().encode('utf-8')

        # Add to presentation.xml.rels
        new_rid = _next_rid(pres_rels)
        new_rel = ET.SubElement(pres_rels, f'{{{REL_NS}}}Relationship')
        new_rel.set('Id', new_rid)
        new_rel.set('Type', NMASTER_REL)
        new_rel.set('Target', 'notesMasters/notesMaster1.xml')
        file_map['ppt/_rels/presentation.xml.rels'] = _et_to_bytes(pres_rels)

    # ── Step 3: Parse [Content_Types].xml once ──
    ct_root = _parse_xml(file_map['[Content_Types].xml'])
    ct_dirty = False

    if need_nm:
        existing_parts = {o.get('PartName') for o in ct_root}
        if '/ppt/notesMasters/notesMaster1.xml' not in existing_parts:
            ov = ET.SubElement(ct_root, f'{{{CT_NS}}}Override')
            ov.set('PartName', '/ppt/notesMasters/notesMaster1.xml')
            ov.set('ContentType', NMASTER_CT)
            ct_dirty = True

    # ── Step 4: Inject notes per slide ──
    for idx, slide_target in enumerate(ordered_slides, start=1):
        slide_num_str = str(idx)
        if slide_num_str not in slide_notes:
            continue

        note_text = slide_notes[slide_num_str]
        slide_basename = slide_target.split('/')[-1]  # slide1.xml
        slide_num = re.search(r'(\d+)', slide_basename).group(1)

        notes_arc = f'ppt/notesSlides/notesSlide{slide_num}.xml'
        notes_rels_arc = f'ppt/notesSlides/_rels/notesSlide{slide_num}.xml.rels'
        slide_rels_arc = f'ppt/slides/_rels/{slide_basename}.rels'

        # 4a. Create or replace notesSlide XML
        file_map[notes_arc] = _build_notes_xml(note_text).encode('utf-8')
        file_map[notes_rels_arc] = _build_notes_rels(slide_basename).encode('utf-8')

        # 4b. Wire slide → notesSlide in slide .rels
        if slide_rels_arc in file_map:
            srels = _parse_xml(file_map[slide_rels_arc])
        else:
            srels = ET.Element(f'{{{REL_NS}}}Relationships')

        has_notes = False
        for rel in srels:
            if rel.get('Type') == NOTES_REL:
                rel.set('Target', f'../notesSlides/notesSlide{slide_num}.xml')
                has_notes = True
                break
        if not has_notes:
            nr = ET.SubElement(srels, f'{{{REL_NS}}}Relationship')
            nr.set('Id', _next_rid(srels))
            nr.set('Type', NOTES_REL)
            nr.set('Target', f'../notesSlides/notesSlide{slide_num}.xml')
        file_map[slide_rels_arc] = _et_to_bytes(srels)

        # 4c. Register in [Content_Types].xml
        part_name = f'/ppt/notesSlides/notesSlide{slide_num}.xml'
        existing_parts = {o.get('PartName') for o in ct_root}
        if part_name not in existing_parts:
            ov = ET.SubElement(ct_root, f'{{{CT_NS}}}Override')
            ov.set('PartName', part_name)
            ov.set('ContentType', NOTES_CT)
            ct_dirty = True

        print(f"  📝 Slide {idx}: {len(note_text)} chars injected")

    # ── Step 5: Write back [Content_Types].xml if changed ──
    if ct_dirty:
        file_map['[Content_Types].xml'] = _et_to_bytes(ct_root)

    # ── Step 6: Write output PPTX (single pass) ──
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for arcname, data in file_map.items():
            zout.writestr(arcname, data)

    print(f"✅ Done! Output: {output_path}")
    return str(output_path)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    result = inject_notes(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else None,
    )

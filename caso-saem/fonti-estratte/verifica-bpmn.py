"""Verifica strutturale e geometrica. --schema accetta BPMN20.xsd ufficiale OMG."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import json
from lxml import etree

arg = argparse.ArgumentParser()
arg.add_argument('--schema', type=Path)
args = arg.parse_args()
base = Path(__file__).resolve().parent
folder = base.parent / 'esempi-apqc' / '02-gestione-ordine'
ns = {'b': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
      'di': 'http://www.omg.org/spec/BPMN/20100524/DI',
      'dc': 'http://www.omg.org/spec/DD/20100524/DC',
      'way': 'http://www.omg.org/spec/DD/20100524/DI'}
schema = etree.XMLSchema(etree.parse(str(args.schema))) if args.schema else None
reports = []
flowtypes = {'task', 'userTask', 'serviceTask', 'manualTask', 'sendTask', 'receiveTask',
             'subProcess', 'startEvent', 'endEvent', 'intermediateCatchEvent',
             'exclusiveGateway', 'parallelGateway'}
for file in sorted(folder.rglob('*.bpmn')):
    root = etree.parse(str(file))
    errors = []
    index = {e.get('id'): e for e in root.xpath('//*[@id]')}
    counts = Counter(e.get('id') for e in root.xpath('//*[@id]'))
    errors.extend(f'Duplicate id: {key}' for key, count in counts.items() if count > 1)
    if schema is not None and not schema.validate(root):
        errors.extend(str(e) for e in schema.error_log)
    for element in root.iter():
        for name in ['sourceRef', 'targetRef', 'bpmnElement', 'dataStoreRef', 'dataObjectRef', 'processRef', 'default']:
            if element.get(name) and element.get(name) not in index:
                errors.append(f'Unresolved {name}: {element.get(name)}')
        if etree.QName(element).localname in ['sourceRef', 'targetRef', 'incoming', 'outgoing', 'flowNodeRef', 'dataInputRefs', 'dataOutputRefs']:
            if (element.text or '').strip() not in index:
                errors.append(f'Unresolved reference: {element.text}')
    for scope in root.xpath('//b:process|//b:subProcess', namespaces=ns):
        nodes = {e.get('id'): e for e in scope if etree.QName(e).localname in flowtypes}
        forward, backward = defaultdict(set), defaultdict(set)
        for flow in scope.findall('b:sequenceFlow', ns):
            a, z = flow.get('sourceRef'), flow.get('targetRef')
            if a not in nodes or z not in nodes:
                errors.append(f'Flow outside scope: {flow.get("id")}')
            forward[a].add(z)
            backward[z].add(a)
        def closure(seed, graph):
            seen, todo = set(seed), list(seed)
            while todo:
                for target in graph[todo.pop()]:
                    if target not in seen:
                        seen.add(target); todo.append(target)
            return seen
        starts = [k for k, e in nodes.items() if etree.QName(e).localname == 'startEvent']
        ends = [k for k, e in nodes.items() if etree.QName(e).localname == 'endEvent']
        errors.extend(f'Unreachable node: {k}' for k in nodes.keys() - closure(starts, forward))
        errors.extend(f'No path to end: {k}' for k in nodes.keys() - closure(ends, backward))
    for plane in root.xpath('//di:BPMNPlane', namespaces=ns):
        shapes = []
        for shape in plane.findall('di:BPMNShape', ns):
            ref = shape.get('bpmnElement')
            if etree.QName(index[ref]).localname in ['lane', 'participant']:
                continue  # containment is intentional, not an overlap
            bounds = shape.find('dc:Bounds', ns)
            shapes.append((ref, {k: float(bounds.get(k)) for k in ['x', 'y', 'width', 'height']}))
        for i, (aid, a) in enumerate(shapes):
            for zid, z in shapes[i+1:]:
                if a['x'] < z['x']+z['width'] and a['x']+a['width'] > z['x'] and a['y'] < z['y']+z['height'] and a['y']+a['height'] > z['y']:
                    errors.append(f'Shape overlap: {aid}, {zid}')
        for edge in plane.findall('di:BPMNEdge', ns):
            ref = edge.get('bpmnElement')
            element = index[ref]
            if etree.QName(element).localname != 'sequenceFlow':
                continue
            points = [(float(p.get('x')), float(p.get('y'))) for p in edge.findall('way:waypoint', ns)]
            for a, z in zip(points, points[1:]):
                if a[0] != z[0] and a[1] != z[1]:
                    errors.append(f'Diagonal flow: {ref}')
                for sid, b in shapes:
                    if sid in [element.get('sourceRef'), element.get('targetRef')]:
                        continue
                    if a[0] == z[0]:
                        hit = b['x'] < a[0] < b['x']+b['width'] and max(a[1], z[1]) > b['y'] and min(a[1], z[1]) < b['y']+b['height']
                    else:
                        hit = b['y'] < a[1] < b['y']+b['height'] and max(a[0], z[0]) > b['x'] and min(a[0], z[0]) < b['x']+b['width']
                    if hit:
                        errors.append(f'Flow {ref} crosses {sid}')
    reports.append({'file': str(file.relative_to(folder)), 'schema_checked': schema is not None,
                    'tasks': len(root.xpath('//b:task|//b:userTask|//b:serviceTask|//b:manualTask|//b:sendTask', namespaces=ns)),
                    'data_references': len(root.xpath('//b:dataObjectReference|//b:dataStoreReference', namespaces=ns)),
                    'data_associations': len(root.xpath('//b:dataInputAssociation|//b:dataOutputAssociation', namespaces=ns)),
                    'errors': sorted(set(errors))})
report = {'checked_on': '2026-09-06', 'files': reports,
          'note': 'La verifica geometrica esclude i contenitori lane/pool. Non dimostra la correttezza eseguibile delle condizioni di business.'}
(folder / 'verifica.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
for item in reports:
    print(item['file'], 'OK' if not item['errors'] else item['errors'])
raise SystemExit(1 if any(item['errors'] for item in reports) else 0)

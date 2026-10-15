"""Source-bound dispatch semantics; conservative receiver typing, never route acceptance."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import hashlib
import json
import re
import subprocess
from lark import Tree, Token
from gdtoolkit.parser import parser

P = Path(__file__).resolve().parent
R = P.parents[3]
BASE = 'e17c929d22fdf749fffb1ad2acdaeff7059c21a1'
DISPATCH = {'Callable', 'call', 'callv', 'call_deferred', 'call_thread_safe', 'call_deferred_thread_group'}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

EXECUTION_SOURCE_SHA = sha(Path(__file__).read_bytes())

def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8', newline='\n')

def unwrap(node):
    while isinstance(node, Tree) and str(node.data) in {'expr', 'par_expr'} and len(node.children) == 1:
        node = node.children[0]
    return node

def literal(node):
    node = unwrap(node)
    if isinstance(node, Tree) and str(node.data) == 'string_name' and len(node.children) == 1:
        return literal(node.children[0])
    if isinstance(node, Tree) and str(node.data) == 'string' and node.children:
        try:
            value = json.loads(str(node.children[0]))
            return value if isinstance(value, str) else None
        except ValueError:
            return None
    return None

def call_parts(node):
    if str(node.data) == 'standalone_call':
        return str(node.children[0]), None, list(node.children[1:]), 'self'
    head = node.children[0]
    if isinstance(head, Tree) and str(head.data) == 'getattr':
        before = list(head.children[:-2])
        receiver = before[0] if len(before) == 1 else Tree('getattr', before, meta=head.meta)
        return str(head.children[-1]), receiver, list(node.children[1:]), head.pretty().strip()
    return '', None, list(node.children[1:]), str(head)

class ScriptFacts:
    def __init__(self, text, path='<fixture>', revision=None):
        self.text, self.path, self.revision = text, path, revision
        self.lines = text.splitlines()
        self.tree = parser.parse(text, gather_metadata=True)
        self.root_class = 'script:' + path
        self.global_name = next((str(n.children[0]) for n in self.tree.children if isinstance(n, Tree) and str(n.data) == 'classname_stmt'), None)
        self.scopes = {self.root_class: {'parent': None, 'class': self.root_class, 'kind': 'class', 'symbols': defaultdict(list)}}
        self.classes = {self.root_class: {'name': self.global_name, 'base': 'RefCounted', 'methods': {}, 'scope': self.root_class}}
        self.calls, self.assignments = [], []
        self.ordinal = Counter()
        self.walk(self.tree, '<top>', self.root_class, self.root_class, [])

    def excerpt(self, node):
        start, end = node.meta.line, node.meta.end_line
        return '\n'.join(self.lines[start - 1:end])

    def walk(self, node, label, scope, klass, ancestors):
        if not isinstance(node, Tree):
            return
        kind = str(node.data)
        outer_scope = scope
        block_kinds = {'if_branch', 'elif_branch', 'else_branch', 'match_branch', 'while_stmt', 'for_stmt', 'for_stmt_typed'}
        if kind in block_kinds:
            scope += '/' + kind + '@' + str(node.meta.line) + ':' + str(node.meta.column)
            self.scopes[scope] = {'parent': outer_scope, 'class': klass, 'kind': 'block', 'symbols': defaultdict(list)}
            if kind in {'for_stmt', 'for_stmt_typed'}:
                self.scopes[scope]['symbols'][str(node.children[0])].append({'name': str(node.children[0]), 'kind': kind, 'type': str(node.children[1]) if kind == 'for_stmt_typed' else None, 'static_inference': False, 'constant': False, 'line': node.meta.line, 'scope': scope, 'expr': None, 'source': self.lines[node.meta.line - 1]})
        if kind == 'class_def':
            klass = klass + '::' + str(node.children[0])
            scope = klass
            self.scopes[scope] = {'parent': None, 'class': klass, 'kind': 'class', 'symbols': defaultdict(list)}
            self.classes[klass] = {'name': None, 'base': 'RefCounted', 'methods': {}, 'scope': scope}
        if kind == 'extends_stmt':
            base = node.children[0]
            self.classes[klass]['base'] = literal(base) if literal(base) is not None else str(base)
        if kind == 'func_def':
            header = next(c for c in node.children if isinstance(c, Tree) and str(c.data) == 'func_header')
            label = str(header.children[0])
            scope = klass + '/' + label + '@' + str(node.meta.line) + ':' + str(node.meta.column)
            self.scopes[scope] = {'parent': klass, 'class': klass, 'kind': 'function', 'symbols': defaultdict(list)}
            returns = [str(c) for c in header.children[1:] if isinstance(c, Token)]
            self.classes[klass]['methods'][label] = {'return_type': returns[-1] if returns else None, 'line': node.meta.line}
        if kind == 'lambda':
            parent = scope
            scope += '/lambda@' + str(node.meta.line) + ':' + str(node.meta.column)
            self.scopes[scope] = {'parent': parent, 'class': klass, 'kind': 'lambda', 'symbols': defaultdict(list)}
        declaration = kind.startswith(('class_var_', 'func_var_', 'const_')) or kind in {'func_arg_typed', 'func_arg_regular', 'func_arg'}
        if declaration and node.children and isinstance(node.children[0], Token):
            name = str(node.children[0])
            typed = 'typed' in kind
            typ = str(node.children[1]) if typed and isinstance(node.children[1], Token) else None
            expressions = [c for c in node.children[2 if typed else 1:] if isinstance(c, Tree) and str(c.data) == 'expr']
            expr = expressions[-1] if expressions else None
            decl = {'name': name, 'kind': kind, 'type': typ, 'static_inference': kind.endswith('_inf'), 'constant': kind.startswith('const_'), 'line': node.meta.line, 'scope': scope, 'expr': expr, 'source': self.excerpt(node)}
            self.scopes[scope]['symbols'][name].append(decl)
        if kind == 'assnmnt_expr' and len(node.children) >= 3:
            lhs = unwrap(node.children[0])
            if isinstance(lhs, Token):
                self.assignments.append({'symbol': str(lhs), 'scope': scope, 'line': node.meta.line, 'source': self.excerpt(node)})
        if kind in {'standalone_call', 'getattr_call'}:
            name, receiver, args, receiver_ast = call_parts(node)
            self.ordinal[(label, name)] += 1
            binding = self.path + '::' + label + '::' + name + '::' + str(self.ordinal[(label, name)])
            if name in DISPATCH:
                full = self.excerpt(node)
                self.calls.append({'binding_id': 'FVC-' + sha(binding.encode())[:12].upper(), 'path': self.path, 'function': label, 'line': node.meta.line, 'end_line': node.meta.end_line, 'method': name, 'receiver_AST': receiver_ast[:700], 'full_excerpt_sha256': sha(full.encode()), 'node': node, 'receiver': receiver, 'args': args, 'scope': scope, 'class': klass, 'ancestors': ancestors})
        for index, child in enumerate(node.children):
            header_expr = kind in block_kinds and isinstance(child, Tree) and str(child.data) == 'expr' and index < (3 if kind == 'for_stmt_typed' else 2)
            self.walk(child, label, outer_scope if header_expr else scope, klass, ancestors + [kind])

    def has_declaration(self, scope, name):
        while scope is not None:
            if name in self.scopes[scope]['symbols']:
                return True
            scope = self.scopes[scope]['parent']
        return False

    def lookup(self, scope, name, line):
        while scope is not None:
            info = self.scopes[scope]
            values = info['symbols'].get(name, [])
            if values:
                candidates = values if info['kind'] == 'class' else [d for d in values if d['line'] <= line or d['kind'].startswith('func_arg')]
                if candidates:
                    return candidates
                return []  # A local declaration shadows a field; do not guess its earlier type.
            scope = info['parent']
        return []

class Resolver:
    def __init__(self, scripts, native=None):
        self.scripts = scripts
        self.native = native or {}
        self.classes = {}
        self.aliases = {}
        for script in scripts:
            for ident, info in script.classes.items():
                self.classes[ident] = (script, info)
                if info['name']:
                    self.aliases[info['name']] = ident

    def class_id(self, typ):
        if typ in self.aliases:
            return self.aliases[typ]
        if typ and typ.startswith('res://'):
            ident = 'script:' + typ[6:]
            return ident if ident in self.classes else typ
        return typ

    def object_type(self, typ, seen=None):
        typ = self.class_id(typ)
        seen = set() if seen is None else set(seen)
        if not typ or typ in seen:
            return False
        seen.add(typ)
        if typ in self.classes:
            return self.object_type(self.classes[typ][1]['base'], seen)
        return bool(self.native.get(typ, {}).get('is_object', False))

    def method_info(self, typ, name, seen=None):
        typ = self.class_id(typ)
        seen = set() if seen is None else set(seen)
        if not typ or typ in seen:
            return None
        seen.add(typ)
        if typ in self.classes:
            _, info = self.classes[typ]
            if name in info['methods']:
                return dict(info['methods'][name], owner=typ, source='current exact script method declaration')
            return self.method_info(info['base'], name, seen)
        data = self.native.get(typ, {})
        if name in data.get('methods', {}):
            return {'return_type': data['methods'][name], 'owner': typ, 'source': 'actual approved-engine ClassDB'}
        return None

    def decl_type(self, script, declarations, seen):
        types = []
        for d in declarations:
            key = (script.path, d['scope'], d['name'], d['line'])
            if key in seen:
                return None
            if d['type']:
                typ = d['type']
            elif d['static_inference']:
                typ = self.expr_type(script, d['expr'], d['scope'], d['line'], seen | {key})
            else:
                return None
            if not typ or typ == 'Variant':
                return None
            types.append(self.class_id(typ))
        return types[0] if types and len(set(types)) == 1 else None

    def expr_type(self, script, node, scope, line, seen=None):
        seen = set() if seen is None else seen
        node = unwrap(node)
        if isinstance(node, Token):
            name = str(node)
            if name == 'self':
                return script.scopes[scope]['class']
            decls = script.lookup(scope, name, line)
            if decls:
                return self.decl_type(script, decls, seen)
            if not script.has_declaration(scope, name) and self.method_info(script.scopes[scope]['class'], name):
                return 'Callable'
            return None
        if not isinstance(node, Tree):
            return None
        kind = str(node.data)
        if kind == 'actual_type_cast':
            return str(node.children[-1]) if isinstance(node.children[-1], Token) else None
        if kind == 'lambda':
            return 'Callable'
        if kind in {'string', 'string_name'}:
            return 'StringName' if kind == 'string_name' else 'String'
        if kind == 'getattr':
            before = list(node.children[:-2])
            owner = before[0] if len(before) == 1 else Tree('getattr', before, meta=node.meta)
            typ = self.expr_type(script, owner, scope, line, seen)
            member = str(node.children[-1])
            if self.method_info(typ, member):
                return 'Callable'
            cid = self.class_id(typ)
            if cid in self.classes:
                owner_script, info = self.classes[cid]
                return self.decl_type(owner_script, owner_script.lookup(info['scope'], member, line), seen)
            return None
        if kind in {'standalone_call', 'getattr_call'}:
            name, receiver, args, _ = call_parts(node)
            if kind == 'standalone_call':
                if name == 'Callable':
                    return 'Callable'
                info = self.method_info(script.scopes[scope]['class'], name)
                return info['return_type'] if info else None
            if name == 'new' and isinstance(receiver, Token):
                typ = self.class_id(str(receiver))
                if typ in self.classes or self.object_type(typ):
                    return typ
            typ = self.expr_type(script, receiver, scope, line, seen)
            if typ == 'Callable' and name in {'bind', 'bindv', 'unbind'}:
                return 'Callable'
            info = self.method_info(typ, name)
            return info['return_type'] if info else None
        return None

    def selector_literal(self, script, node, scope, line, seen=None):
        value = literal(node)
        if value is not None:
            return value, 'string or StringName AST literal'
        node = unwrap(node)
        if isinstance(node, Token):
            values = script.lookup(scope, str(node), line)
            if len(values) == 1 and values[0]['constant']:
                value = literal(values[0]['expr'])
                if value is not None:
                    return value, 'exact constant literal declaration at line ' + str(values[0]['line'])
        return None, 'not a closed literal/constant method selector'

    def bound_selector(self, script, receiver, scope, line):
        receiver = unwrap(receiver)
        if isinstance(receiver, Token):
            name = str(receiver)
            if not script.has_declaration(scope, name) and self.method_info(script.scopes[scope]['class'], name):
                return name, 'unshadowed local/inherited method reference'
        if isinstance(receiver, Tree) and str(receiver.data) == 'getattr':
            before = list(receiver.children[:-2])
            owner = before[0] if len(before) == 1 else Tree('getattr', before, meta=receiver.meta)
            member = str(receiver.children[-1])
            if self.method_info(self.expr_type(script, owner, scope, line), member):
                return member, 'bound member method reference'
        if isinstance(receiver, Tree) and str(receiver.data) in {'getattr_call', 'standalone_call'}:
            name, owner, args, _ = call_parts(receiver)
            if name == 'Callable' and len(args) == 2:
                return self.selector_literal(script, args[1], scope, line)
            if name in {'bind', 'bindv', 'unbind'} and self.expr_type(script, owner, scope, line) == 'Callable':
                return self.bound_selector(script, owner, scope, line)
        return None, 'callback value/binding port remains unresolved; initializer candidates are not full write/caller closure'

    def classify(self, script, row):
        name, args, scope = row['method'], row['args'], row['scope']
        result = {'invocation_expression': name != 'Callable', 'receiver_type': None, 'method_selector': None, 'selector_evidence': None, 'first_argument_literal': literal(args[0]) if args else None, 'argument_count': len(args), 'type_scope': scope}
        if name == 'Callable':
            selector, proof = self.selector_literal(script, args[1], scope, row['line']) if len(args) == 2 else (None, None)
            result.update(category='CONSTRUCTOR_EMPTY' if not args else ('CONSTRUCTOR_NAMED_BINDING' if len(args) == 2 and selector is not None else 'CONSTRUCTOR_COMPUTED_OR_OTHER_BINDING'), method_selector=selector, selector_evidence=proof, source_role='parameter default' if 'func_header' in row['ancestors'] else 'binding/default/reset expression')
            return result
        if row['receiver'] is None:
            if script.has_declaration(scope, name):
                result.update(category='UNKNOWN_SHADOWED_STANDALONE_DISPATCH', selector_evidence='local/parameter binding shadows apparent native dispatcher; no implicit-self method selector assumed')
                return result
            typ = script.scopes[scope]['class']
            result['implicit_self_receiver'] = True
        else:
            typ = self.expr_type(script, row['receiver'], scope, row['line'])
        result['receiver_type'] = typ
        tokens = [row['receiver']] if isinstance(row['receiver'], Token) else list(row['receiver'].scan_values(lambda v: isinstance(v, Token))) if isinstance(row['receiver'], Tree) else []
        declarations = {}
        for token in tokens:
            for d in script.lookup(scope, str(token), row['line']):
                declarations[(d['scope'], d['name'], d['line'])] = {k: d[k] for k in ['scope','name','kind','type','static_inference','constant','line']} | {'source_excerpt': d['source'][:450], 'full_source_excerpt_sha256': sha(d['source'].encode())}
        result['scoped_receiver_declarations'] = list(declarations.values())
        if typ == 'Callable':
            selector, proof = self.bound_selector(script, row['receiver'], scope, row['line'])
            result.update(category='CALLABLE_DEFERRED_INVOCATION' if name != 'call' else 'CALLABLE_INVOCATION', method_selector=selector, selector_evidence=proof, first_argument_role='callback data; never inferred as a target method name')
        elif self.object_type(typ):
            # Do not silently certify an overridden dispatch method as native Object semantics.
            info = self.method_info(typ, name)
            if info and info['source'] == 'current exact script method declaration':
                result.update(category='UNKNOWN_OVERRIDDEN_DISPATCH_METHOD', selector_evidence='script overrides the apparent dispatcher; inspect its body separately')
            else:
                selector, proof = self.selector_literal(script, args[0], scope, row['line']) if args else (None, 'no method selector argument')
                result.update(category='OBJECT_LITERAL_DISPATCH' if selector is not None else 'OBJECT_COMPUTED_DISPATCH', method_selector=selector, selector_evidence=proof, first_argument_role='Object method selector, only because receiver Object ancestry is proved')
        else:
            result.update(category='UNKNOWN_RECEIVER_DISPATCH', selector_evidence='receiver Object/Callable semantics not proved from current scoped declarations; literal argument remains conditional data, not an edge')
        return result

def load_current():
    old = json.loads((P.parent / 'r44_creature_route_caller_audit/SOURCE_CALL_GRAPH.json').read_text(encoding='utf-8'))
    scripts, equivalence = [], []
    for item in old['files']:
        raw = subprocess.check_output(['git', 'show', BASE + ':' + item['path']], cwd=R, stderr=subprocess.PIPE)
        assert sha(raw) == item['sha256'], item['path']
        scripts.append(ScriptFacts(raw.decode('utf-8-sig'), item['path'], BASE))
        equivalence.append(dict(path=item['path'],current_revision=BASE,current_sha256=sha(raw),r44_revision=item['revision'],r44_sha256=item['sha256'],equal=True))
    current = {row['binding_id']: (script,row) for script in scripts for row in script.calls}
    assert set(current) == {x['binding_id'] for x in old['dispatch_sites']}
    for x in old['dispatch_sites']:
        row = current[x['binding_id']][1]
        assert all(row[k] == x[k] for k in ['path','function','line','end_line','method','receiver_AST','full_excerpt_sha256']), x['binding_id']
    return old, scripts, equivalence, current

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare',action='store_true')
    ap.add_argument('--native-index',type=Path)
    args = ap.parse_args()
    old,scripts,equivalence,current = load_current()
    if args.prepare:
        names = {'Object','RefCounted','Node','SceneTree','Control','Node2D','Node3D','Camera3D','Window','SubViewport','Resource','Script','PackedScene','Callable','StringName'}
        for script in scripts:
            names.update(info['base'] for info in script.classes.values())
            for scope in script.scopes.values():
                for declarations in scope['symbols'].values():
                    names.update(d['type'] for d in declarations if d['type'])
        names = sorted(x for x in names if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',x))
        write(P/'CLASS_QUERY_INPUT.json',{'baseline':BASE,'class_names':names,'scope':'Native ClassDB ancestry/method signatures only; no instances of queried classes are created.'})
        write(P/'SOURCE_BASELINE_EQUIVALENCE.json',{'baseline':BASE,'source_files':equivalence,'raw_dispatch_rows':len(current),'raw_binding_ids_and_source_spans_exact':True,'production_changed_paths':subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','scripts','scenes','shaders','addons','project.godot'],cwd=R,text=True).splitlines()})
        print('R45_SOURCE_PREPARED',len(scripts),len(current),len(names),flush=True)
        return
    assert args.native_index
    index = json.loads(args.native_index.read_text(encoding='utf-8'))
    native = {}
    for item in index['classes']:
        raw = (args.native_index.parent/item['file']).read_bytes()
        assert sha(raw)==item['sha256']
        data=json.loads(raw)
        native[data['class_name']]=data
    resolver=Resolver(scripts,native)
    output=[]
    for original in old['dispatch_sites']:
        script,row=current[original['binding_id']]
        output.append({'binding_id':row['binding_id'],'r44_record':original,'current_source_revision':BASE,'current_source_sha256':next(x['current_sha256'] for x in equivalence if x['path']==script.path),'classification':resolver.classify(script,row)})
    stats={}
    for label,probe in [('non_test_candidates',False),('probe_or_test',True)]:
        selected=[x for x in output if x['r44_record']['probe']==probe]
        stats[label]={'raw_expressions':len(selected),'categories':dict(Counter(x['classification']['category'] for x in selected)),'constructor_expressions':sum(not x['classification']['invocation_expression'] for x in selected),'invocation_expressions':sum(x['classification']['invocation_expression'] for x in selected),'invocations_with_unresolved_selector_or_receiver':sum(x['classification']['invocation_expression'] and x['classification']['method_selector'] is None for x in selected),'invocations_with_known_selector':sum(x['classification']['invocation_expression'] and x['classification']['method_selector'] is not None for x in selected)}
    raw95=[x for x in output if not x['r44_record']['probe'] and x['r44_record']['literal_target'] is None]
    stats['r44_raw95_reconciliation']={'raw_rows':len(raw95),'categories':dict(Counter(x['classification']['category'] for x in raw95)),'literal_rows_reclassified_as_callable_data':[x['binding_id'] for x in output if not x['r44_record']['probe'] and x['r44_record']['literal_target'] is not None and x['classification']['category'].startswith('CALLABLE_')]}
    write(P/'DISPATCH_SEMANTICS.json',{'schema':'reef.dispatch_semantics_audit/1','baseline':BASE,'classifier_module_sha256':EXECUTION_SOURCE_SHA,'native_class_index_sha256':sha(args.native_index.read_bytes()),'raw_source_graph_revision':old['baseline'],'records':output,'summary':stats,'limits':'Current source expression semantics only. Known method selectors do not prove navigation, runtime implementation, visibility or acceptance. Callback ports, all writes/callers and unknown receivers remain separate open work. R44 records/IDs retained verbatim. No route/art context credit or full compositor runtime closure.','accepted_removed':0,'mission_complete':False})
    print('R45_DISPATCH_CLASSIFIED',json.dumps(stats),flush=True)

if __name__ == '__main__':
    main()

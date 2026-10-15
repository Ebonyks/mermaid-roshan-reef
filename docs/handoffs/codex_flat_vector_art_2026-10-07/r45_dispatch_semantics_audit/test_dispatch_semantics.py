"""Adversarial semantic boundaries, checked against the actual engine query evidence."""
from pathlib import Path
import importlib.util
import json
import unittest

P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('r45_dispatch',P/'classify_dispatch.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
index=json.loads((P/'engine/evidence/NATIVE_CLASS_INDEX.json').read_text(encoding='utf-8'))
native={}
for item in index['classes']:
    raw=(P/'engine/evidence'/item['file']).read_bytes()
    assert audit.sha(raw)==item['sha256']
    native[item['class_name']]=json.loads(raw)

def rows(text):
    script=audit.ScriptFacts(text)
    resolver=audit.Resolver([script],native)
    return [(row,resolver.classify(script,row)) for row in script.calls]

def invocation_rows(text):
    return [(row,result) for row,result in rows(text) if result['invocation_expression']]

class DispatchSemanticBoundaries(unittest.TestCase):
    def test_empty_constructor_is_not_invocation(self):
        result=rows('extends RefCounted\nvar cb: Callable = Callable()\n')[0][1]
        self.assertEqual(result['category'],'CONSTRUCTOR_EMPTY')
        self.assertFalse(result['invocation_expression'])

    def test_named_constructor_is_binding_not_invocation(self):
        result=rows('extends RefCounted\nfunc handler(): pass\nfunc test():\n\tvar cb := Callable(self, "handler")\n')[0][1]
        self.assertEqual(result['category'],'CONSTRUCTOR_NAMED_BINDING')
        self.assertEqual(result['method_selector'],'handler')
        self.assertFalse(result['invocation_expression'])

    def test_callable_literal_argument_is_data(self):
        result=invocation_rows('extends RefCounted\nvar cb: Callable\nfunc test():\n\tcb.call("_start_stuffie_battle")\n')[0][1]
        self.assertEqual(result['category'],'CALLABLE_INVOCATION')
        self.assertIsNone(result['method_selector'])
        self.assertIn('data',result['first_argument_role'])

    def test_Object_literal_selector(self):
        result=invocation_rows('extends RefCounted\nvar receiver: Node\nfunc test():\n\treceiver.call("_tick_room")\n')[0][1]
        self.assertEqual(result['category'],'OBJECT_LITERAL_DISPATCH')
        self.assertEqual(result['method_selector'],'_tick_room')

    def test_Object_StringName_selector(self):
        result=invocation_rows('extends RefCounted\nvar receiver: Node\nfunc test():\n\treceiver.call(&"make_current")\n')[0][1]
        self.assertEqual(result['method_selector'],'make_current')
        self.assertEqual(result['category'],'OBJECT_LITERAL_DISPATCH')

    def test_constant_is_closed_selector(self):
        result=invocation_rows('extends RefCounted\nconst SELECTOR: StringName = &"handler"\nvar receiver: Node\nfunc test():\n\treceiver.call(SELECTOR)\n')[0][1]
        self.assertEqual(result['method_selector'],'handler')

    def test_mutable_selector_stays_unknown(self):
        result=invocation_rows('extends RefCounted\nvar receiver: Node\nfunc test():\n\tvar method: StringName = &"handler"\n\treceiver.call(method)\n')[0][1]
        self.assertIsNone(result['method_selector'])
        self.assertEqual(result['category'],'OBJECT_COMPUTED_DISPATCH')

    def test_untyped_receiver_literal_is_not_certified(self):
        result=invocation_rows('extends RefCounted\nfunc test(receiver):\n\treceiver.call("_tick_room")\n')[0][1]
        self.assertIsNone(result['method_selector'])
        self.assertEqual(result['category'],'UNKNOWN_RECEIVER_DISPATCH')

    def test_method_reference_deferred(self):
        result=invocation_rows('extends RefCounted\nfunc startup(value): pass\nfunc test():\n\tstartup.call_deferred("payload")\n')[0][1]
        self.assertEqual(result['category'],'CALLABLE_DEFERRED_INVOCATION')
        self.assertEqual(result['method_selector'],'startup')

    def test_native_getter_and_bound_member(self):
        result=invocation_rows('extends Node\nfunc test():\n\tget_parent().add_child.call_deferred(null)\n')[0][1]
        self.assertEqual(result['category'],'CALLABLE_DEFERRED_INVOCATION')
        self.assertEqual(result['method_selector'],'add_child')

    def test_branch_shadow_does_not_leak(self):
        results=invocation_rows('extends RefCounted\nvar cb: Node\nfunc test():\n\tif true:\n\t\tvar cb: Callable\n\t\tcb.call("data")\n\tcb.call("handler")\n')
        self.assertEqual([r['category'] for _,r in results],['CALLABLE_INVOCATION','OBJECT_LITERAL_DISPATCH'])
        self.assertEqual(results[1][1]['method_selector'],'handler')

    def test_untyped_parameter_shadows_field(self):
        result=invocation_rows('extends RefCounted\nvar cb: Callable\nfunc test(cb):\n\tcb.call("handler")\n')[0][1]
        self.assertEqual(result['category'],'UNKNOWN_RECEIVER_DISPATCH')
        self.assertIsNone(result['method_selector'])

    def test_lambda_parameter_scope(self):
        results=invocation_rows('extends RefCounted\nvar cb: Callable\nfunc test():\n\tvar f: Callable = func(cb: Node): cb.call("handler")\n\tcb.call("data")\n')
        self.assertEqual([r['category'] for _,r in results],['OBJECT_LITERAL_DISPATCH','CALLABLE_INVOCATION'])

    def test_untyped_loop_variable_shadows_method_reference(self):
        result=invocation_rows('extends RefCounted\nfunc startup(value): pass\nfunc test():\n\tfor startup in []:\n\t\tstartup.call("payload")\n')[0][1]
        self.assertEqual(result['category'],'UNKNOWN_RECEIVER_DISPATCH')
        self.assertIsNone(result['method_selector'])

    def test_typed_loop_receiver(self):
        result=invocation_rows('extends RefCounted\nfunc test():\n\tfor node: Node in []:\n\t\tnode.call("handler")\n')[0][1]
        self.assertEqual(result['category'],'OBJECT_LITERAL_DISPATCH')
        self.assertEqual(result['method_selector'],'handler')

    def test_loop_iterable_uses_outer_binding(self):
        results=invocation_rows('extends RefCounted\nvar cb: Node\nfunc test():\n\tfor cb: Callable in cb.call("items"):\n\t\tcb.call("data")\n')
        self.assertEqual([r['category'] for _,r in results],['OBJECT_LITERAL_DISPATCH','CALLABLE_INVOCATION'])

    def test_inner_class_fields_do_not_leak(self):
        results=invocation_rows('extends RefCounted\nclass Inner:\n\textends RefCounted\n\tvar cb: Callable\n\tfunc run(): cb.call("data")\nfunc run(cb): cb.call("handler")\n')
        self.assertEqual([r['category'] for _,r in results],['CALLABLE_INVOCATION','UNKNOWN_RECEIVER_DISPATCH'])

    def test_implicit_self_Object_dispatch(self):
        result=invocation_rows('extends Node\nfunc test():\n\tcall_deferred("handler")\n')[0][1]
        self.assertEqual(result['category'],'OBJECT_LITERAL_DISPATCH')
        self.assertTrue(result['implicit_self_receiver'])
        self.assertEqual(result['method_selector'],'handler')

    def test_shadowed_standalone_dispatcher_is_not_assumed_native(self):
        result=invocation_rows('extends Node\nfunc test(call_deferred):\n\tcall_deferred("handler")\n')[0][1]
        self.assertEqual(result['category'],'UNKNOWN_SHADOWED_STANDALONE_DISPATCH')
        self.assertIsNone(result['method_selector'])

    def test_overridden_dispatcher_not_assumed_native(self):
        result=invocation_rows('extends RefCounted\nfunc call(value): pass\nfunc test():\n\tself.call("handler")\n')[0][1]
        self.assertEqual(result['category'],'UNKNOWN_OVERRIDDEN_DISPATCH_METHOD')
        self.assertIsNone(result['method_selector'])

if __name__=='__main__':
    unittest.main(verbosity=2)

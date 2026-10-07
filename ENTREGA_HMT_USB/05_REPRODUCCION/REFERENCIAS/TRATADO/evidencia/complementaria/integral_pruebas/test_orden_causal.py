#!/usr/bin/env python3
"""Regresión del orden causal: mutaciones AST en memoria, sin ejecutar run.

Este control acredita sitios de llamada y separación del evaluador. No
certifica las demostraciones matemáticas ni modifica los archivos auditados.
"""
from __future__ import annotations

import ast
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
SOURCE = Path(__file__).resolve().with_name("verificar_generacion_infinita_nonadica.py")


class CausalOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("nonadic_order_under_test", SOURCE)
        if spec is None or spec.loader is None:
            raise RuntimeError("No se puede cargar el auditor")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.original_tree = ast.parse(cls.source)
        cls.stages = cls.module.audit_source()["call_order"]

    def fixture(self):
        tree = copy.deepcopy(self.original_tree)
        run = next(node for node in tree.body
                   if isinstance(node, ast.FunctionDef) and node.name == "run")
        return tree, run

    def stage_index(self, run, stage):
        return next(i for i, statement in enumerate(run.body)
                    if any(isinstance(node, ast.Call)
                           and isinstance(node.func, ast.Name)
                           and node.func.id == stage
                           for node in ast.walk(statement)))

    def assert_rejected(self, tree):
        text = ast.unparse(ast.fix_missing_locations(tree))
        with self.assertRaisesRegex(RuntimeError, "orden causal"):
            self.module.audit_source(text)

    def test_current_run_and_reformatted_source_pass(self):
        observed = self.module.audit_source()
        reformatted = self.module.audit_source(ast.unparse(self.original_tree))
        self.assertEqual(observed["call_order"], reformatted["call_order"])
        sites = observed["causal_order_call_sites"]
        self.assertEqual(len(sites), 8)
        lines = [sites[name]["line"] for name in self.stages]
        self.assertEqual(lines, sorted(lines))

    def test_each_adjacent_stage_inversion_is_rejected(self):
        for left, right in zip(self.stages, self.stages[1:]):
            with self.subTest(left=left, right=right):
                tree, run = self.fixture()
                a, b = self.stage_index(run, left), self.stage_index(run, right)
                run.body[a], run.body[b] = run.body[b], run.body[a]
                self.assert_rejected(tree)

    def test_original_evaluation_before_generation_regression(self):
        tree, run = self.fixture()
        evaluation = run.body.pop(self.stage_index(run, "evaluate_generated_characters"))
        run.body.insert(self.stage_index(run, "generate_structural_characters"), evaluation)
        self.assert_rejected(tree)

    def test_each_missing_stage_is_rejected(self):
        for stage in self.stages:
            with self.subTest(stage=stage):
                tree, run = self.fixture()
                del run.body[self.stage_index(run, stage)]
                self.assert_rejected(tree)

    def test_each_duplicate_stage_is_rejected(self):
        for stage in self.stages:
            with self.subTest(stage=stage):
                tree, run = self.fixture()
                index = self.stage_index(run, stage)
                run.body.insert(index, copy.deepcopy(run.body[index]))
                self.assert_rejected(tree)

    def test_literal_or_comment_cannot_replace_a_call(self):
        tree, run = self.fixture()
        index = self.stage_index(run, "generate_structural_characters")
        marker = ast.unparse(run.body.pop(index))
        run.body.insert(0, ast.Expr(value=ast.Constant(value=marker)))
        text = "# " + marker.replace("\n", "\n# ") + "\n"
        text += ast.unparse(ast.fix_missing_locations(tree))
        with self.assertRaisesRegex(RuntimeError, "orden causal"):
            self.module.audit_source(text)

    def test_uncalled_nested_function_cannot_supply_a_stage(self):
        tree, run = self.fixture()
        index = self.stage_index(run, "generate_structural_characters")
        hidden = ast.parse("def never_called():\n    pass\n").body[0]
        hidden.body = [run.body[index]]
        run.body[index] = hidden
        self.assert_rejected(tree)

    def test_conditional_or_loop_stage_is_rejected(self):
        templates = (
            "if False:\n    pass", "if condition:\n    pass",
            "for item in sequence:\n    pass", "while condition:\n    pass",
            "try:\n    pass\nfinally:\n    pass",
        )
        for template in templates:
            with self.subTest(template=template):
                tree, run = self.fixture()
                index = self.stage_index(run, "generate_structural_characters")
                wrapper = ast.parse(template).body[0]
                wrapper.body = [run.body[index]]
                run.body[index] = wrapper
                self.assert_rejected(tree)

    def test_lambda_boolean_and_conditional_expression_are_rejected(self):
        wrappers = ("lambda: PLACEHOLDER", "condition and PLACEHOLDER",
                    "PLACEHOLDER if condition else None")
        for template in wrappers:
            with self.subTest(template=template):
                tree, run = self.fixture()
                index = self.stage_index(run, "generate_structural_characters")
                assignment = run.body[index]
                call_text = ast.unparse(assignment.value)
                assignment.value = ast.parse(template.replace("PLACEHOLDER", call_text),
                                             mode="eval").body
                self.assert_rejected(tree)

    def test_stage_alias_is_rejected(self):
        tree, run = self.fixture()
        run.body.insert(0, ast.parse("deferred = generate_structural_characters").body[0])
        self.assert_rejected(tree)

    def test_duplicate_run_definition_is_rejected(self):
        tree, run = self.fixture()
        tree.body.append(copy.deepcopy(run))
        self.assert_rejected(tree)

    def test_filtered_or_multigenerator_publication_is_rejected(self):
        for mutation in ("filter", "extra_generator", "async"):
            with self.subTest(mutation=mutation):
                tree, run = self.fixture()
                index = self.stage_index(run, "publish_archimedean_blocks")
                value = run.body[index].value
                self.assertIsInstance(value, ast.DictComp)
                if mutation == "filter":
                    value.generators[0].ifs.append(ast.Constant(value=False))
                elif mutation == "extra_generator":
                    value.generators.append(copy.deepcopy(value.generators[0]))
                else:
                    value.generators[0].is_async = 1
                self.assert_rejected(tree)

    def test_transitive_reader_is_still_rejected(self):
        tree, _ = self.fixture()
        generator = next(node for node in tree.body
                         if isinstance(node, ast.FunctionDef)
                         and node.name == "generate_structural_characters")
        generator.body.insert(0, ast.parse("hidden_reader()").body[0])
        tree.body.extend(ast.parse(
            "def hidden_reader():\n    return closure_bounds({}, 1)\n"
        ).body)
        text = ast.unparse(ast.fix_missing_locations(tree))
        with self.assertRaisesRegex(RuntimeError, "lector arquimediano"):
            self.module.audit_source(text)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CausalOrderTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("PASS_ORDEN_CAUSAL_AST_RUN")

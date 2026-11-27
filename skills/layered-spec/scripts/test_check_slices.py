from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from importlib.util import module_from_spec, spec_from_file_location

spec = spec_from_file_location("slice_checker", Path(__file__).with_name("check-slices.py"))
checker = module_from_spec(spec)
spec.loader.exec_module(checker)


def contract(slice_id, tier, owns, depends="none"):
    return f"""## {slice_id} {tier}. Projection
Owns: `{owns}`.
Forbidden: everything else.
Depends: {depends}
Done when: the counted public read stays at one query.
Size: {tier}. The label matches the header.
"""


def review(slice_id, owns, lens, extra=""):
    return contract(slice_id, "hard", owns, "all earlier layers merged") + f"Kind: review\nLens: {lens}\n{extra}"


def build_layers(count):
    return "".join(contract(f"L{n}A", "easy", f"app/l{n}.py", "all earlier layers merged") for n in range(1, count + 1))


class SliceContractTests(unittest.TestCase):
    def inspect(self, *parts):
        with TemporaryDirectory() as directory:
            paths = []
            for index, text in enumerate(parts):
                path = Path(directory) / f"part-{index}.md"
                path.write_text(text)
                paths.append(path)
            return checker.check(paths)

    def test_collision_in_reserved_path_across_parts_is_rejected(self):
        count, errors = self.inspect(contract("L1A", "easy", "new/projection.py"), contract("L1B", "hard", "new/projection.py"))
        self.assertEqual(count, 2)
        self.assertIn("L1B overlaps L1A: new/projection.py", errors)

    def test_same_file_in_later_layer_is_allowed(self):
        count, errors = self.inspect(contract("L1A", "easy", "app/rows.py"), contract("L2A", "hard", "app/rows.py", "all L1 merged"))
        self.assertEqual((count, errors), (2, []))

    def test_mixed_labels_are_allowed_and_same_layer_dependency_is_rejected(self):
        count, errors = self.inspect(contract("L1A", "hard-ui", "ui/page.tsx"), contract("L1B", "easy", "app/rows.py", "L1A"))
        self.assertEqual(count, 2)
        self.assertEqual(errors, ["L1B: same-layer dependency"])

    def test_z_then_aa_uses_letter_sequence(self):
        count, errors = self.inspect(contract("L1Z", "hard", "app/z.py"), contract("L1AA", "hard-ui", "ui/aa.tsx"))
        self.assertEqual((count, errors), (2, []))

    def test_empty_field_cannot_borrow_next_line(self):
        _, errors = self.inspect(contract("L1A", "easy", "app/rows.py").replace("Depends: none", "Depends:"))
        self.assertIn("L1A: missing Depends", errors)

    def test_unknown_label_is_rejected(self):
        _, errors = self.inspect(contract("L1A", "easy", "app/a.py") + contract("L1B", "tiny", "app/b.py"))
        self.assertIn("L1B: label tiny is not one of easy, easy-ui, hard, hard-ui", errors)

    def test_model_line_on_slice_is_rejected(self):
        with_model = contract("L1A", "easy", "app/a.py") + "Model: custom-model\n"
        _, errors = self.inspect(with_model)
        self.assertIn("L1A: Model line is not allowed; slices inherit the caller's default model", errors)
        self.assertEqual(self.inspect(contract("L1A", "easy", "app/a.py"))[1], [])

    def test_malformed_heading_is_not_silently_skipped(self):
        text = contract("L1A", "easy", "app/a.py") + "## L1B missing period in heading\nOwns: `app/b.py`.\n"
        _, errors = self.inspect(text)
        self.assertTrue(any("malformed slice heading" in error for error in errors))

    def test_missing_size_line_is_rejected(self):
        body = contract("L1A", "easy", "app/rows.py").replace("Size: easy. The label matches the header.\n", "")
        _, errors = self.inspect(body)
        self.assertIn("L1A: missing 'Size: easy. <reason>'", errors)

    def test_size_line_must_match_header(self):
        body = contract("L1A", "easy", "app/rows.py").replace("Size: easy.", "Size: hard.")
        _, errors = self.inspect(body)
        self.assertIn("L1A: Size line says hard, header says easy", errors)

    def test_noncanonical_and_ancestor_paths_are_rejected(self):
        _, errors = self.inspect(contract("L1A", "easy", "app"), contract("L1B", "hard", "app/rows.py"), contract("L1C", "hard", "app/../rows.py"))
        self.assertTrue(any("ancestor ownership overlap" in error for error in errors))
        self.assertIn("L1C: noncanonical owner path app/../rows.py", errors)

    def test_one_slice_per_layer_may_own_a_shared_control_path(self):
        self.assertEqual(self.inspect(contract("L1A", "easy", "AGENTS.md"))[1], [])
        self.assertEqual(self.inspect(contract("L1A", "hard", "backend/alembic/versions/add_role_a1.py"))[1], [])

    def test_two_slices_in_a_layer_cannot_share_a_shared_group(self):
        _, errors = self.inspect(contract("L1A", "hard", "backend/alembic/versions/a.py"), contract("L1B", "hard", "backend/alembic/versions/b.py"))
        self.assertIn("L1B and L1A both own shared backend/alembic/versions/ in L1; give it to one slice and move the other to the next layer", errors)
        later = self.inspect(contract("L1A", "hard", "backend/alembic/versions/a.py"), contract("L2A", "hard", "backend/alembic/versions/b.py", "all L1 merged"))
        self.assertEqual(later[1], [])

    def test_router_and_alembic_paths_are_ordinary_slice_files(self):
        router = "backend/app/services/router.py"
        models = "backend/app/services/router_models.py"
        agentic = "backend/app/services/agentic.py"
        env = "backend/alembic/env.py"
        revision = "backend/alembic/versions/add_role_a1.py"
        self.assertEqual(self.inspect(contract("L1A", "hard", router), contract("L1B", "hard", models), contract("L1C", "hard", agentic), contract("L1D", "hard", env), contract("L1E", "hard", revision)), (5, []))
        _, errors = self.inspect(contract("L1A", "hard", router), contract("L1B", "hard", router))
        self.assertIn(f"L1B overlaps L1A: {router}", errors)
        self.assertEqual(self.inspect(contract("L1A", "hard", router), contract("L2A", "hard", router, "all L1 merged"))[1], [])

    def test_parent_queues_setup_steps_and_pq_ids_are_rejected(self):
        for text in ("Parent queues are not rows.", "One parent queue merges first.", "Run the setup step before L1.", "## Setup", "### PQ2. Remove the SDK", "L1 waits on PQ0.", "Depends: PQ3 merged", "### R0. Router presets"):
            with self.subTest(text=text):
                _, errors = self.inspect(contract("L1A", "easy", "app/rows.py") + "\n" + text + "\n")
                self.assertTrue(any("work outside a layer" in error for error in errors), errors)
        for text in ("## Layer 6. Ship slices", "Setup: git fetch origin main --prune.", "### L1 slices", "The test setup builds a fake session."):
            with self.subTest(text=text):
                self.assertEqual(self.inspect(contract("L1A", "easy", "app/rows.py") + "\n" + text + "\n")[1], [])

    def test_work_outside_a_layer_is_rejected(self):
        for text in ("The parent PR R0 lands first.", "Router lane: R0 then R1.", "| M1 | parent | migration |", "| R0 | hard | presets |"):
            with self.subTest(text=text):
                _, errors = self.inspect(contract("L1A", "easy", "app/rows.py") + "\n" + text + "\n")
                self.assertTrue(any("work outside a layer" in error for error in errors), errors)
        self.assertEqual(self.inspect(contract("L1A", "easy", "app/rows.py") + "\n| L1A | easy | rows |\n")[1], [])

    def test_source_text_deletion_or_syntax_acceptance_is_rejected(self):
        for proof in ("static dead-owner absence check", "source-text deleted-name absence", "source-text syntax assertion"):
            with self.subTest(proof=proof):
                body = contract("L1A", "easy", "app/rows.py").replace("the counted public read stays at one query", proof)
                _, errors = self.inspect(body)
                self.assertIn("L1A: source-text deletion/syntax is not behavior proof; follow the test policy in build/references/tests.md", errors)

    def test_shipped_strings_and_compiled_contracts_remain_allowed(self):
        for proof in ("the shipped Dockerfile string matches", "the compiled public contract and counted read pass"):
            with self.subTest(proof=proof):
                body = contract("L1A", "easy", "app/rows.py").replace("the counted public read stays at one query", proof)
                self.assertEqual(self.inspect(body), (1, []))

    def test_no_contract_and_shared_control_do_not_pass(self):
        self.assertEqual(self.inspect("# No contracts\n")[1], ["no slice contracts found"])
        self.assertEqual(self.inspect(contract("L1A", "easy", "scripts/ci/local.sh"))[1], [])

    def test_heading_without_difficulty_label_is_rejected(self):
        text = contract("L1A", "easy", "app/a.py") + "## L1B. Projection\nOwns: `app/b.py`.\nForbidden: x.\nDepends: none\nDone when: one query.\nSize: easy. Small.\n"
        count, errors = self.inspect(text)
        self.assertEqual(count, 2)
        self.assertEqual(errors, ["L1B: missing difficulty label; put one of easy, easy-ui, hard, hard-ui after the id"])

    def test_missing_owns_line_is_rejected(self):
        body = contract("L1A", "easy", "app/rows.py").replace("Owns: `app/rows.py`.\n", "")
        _, errors = self.inspect(body)
        self.assertIn("L1A: missing Owns", errors)

    def test_same_layer_owns_overlap_within_one_file_is_rejected(self):
        _, errors = self.inspect(contract("L2A", "hard", "app/rows.py", "all L1 merged") + contract("L2B", "easy-ui", "app/rows.py", "all L1 merged"))
        self.assertIn("L2B overlaps L2A: app/rows.py", errors)

    def test_slices_left_skips_merged_status_rows(self):
        layers = "| Slice | Label | Status |\n|---|---|---|\n| L1A | easy | merged |\n| `L1B` | hard | planned |\n"
        with TemporaryDirectory() as directory:
            spec = Path(directory) / "spec.md"
            spec.write_text(contract("L1A", "easy", "app/a.py") + contract("L1B", "hard", "app/b.py"))
            table = Path(directory) / "layers.md"
            table.write_text(layers)
            self.assertEqual(checker.slices_left([spec, table]), 1)
            self.assertEqual(checker.slices_left([spec]), 2)

    def test_more_than_fifteen_left_runs_heavy(self):
        self.assertEqual(checker.execution_format(16), "heavy orchestrator")
        self.assertEqual(checker.execution_format(15), "light orchestrator")
        self.assertEqual(checker.execution_format(1), "light orchestrator")

    def write_alias(self, root):
        (root / "owner.swift").write_text("one")
        (root / "alias.swift").symlink_to("owner.swift")
        (root / "real").mkdir()
        (root / "real" / "child.swift").write_text("child")
        (root / "linkdir").symlink_to("real", target_is_directory=True)

    def run_alias(self, root, text):
        path = root / "spec.md"
        path.write_text(text)
        return checker.check([path], root)

    def test_alias_fixture_resolves_canonical_owners_and_keeps_parent_control(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_alias(root)
            same_layer = contract("L1A", "easy", "owner.swift") + contract("L1B", "hard", "alias.swift")
            count, errors = self.run_alias(root, same_layer)
            self.assertEqual(count, 2)
            self.assertTrue(any("resolves to owner.swift" in error for error in errors), errors)
            reversed_order = contract("L1A", "easy", "alias.swift") + contract("L1B", "hard", "owner.swift")
            _, reversed_errors = self.run_alias(root, reversed_order)
            self.assertTrue(any("resolves to owner.swift" in error for error in reversed_errors), reversed_errors)
            later = contract("L1A", "easy", "owner.swift") + contract("L2A", "hard", "alias.swift", "all L1 merged")
            self.assertEqual(self.run_alias(root, later)[1], [])
            same = contract("L1A", "easy", "owner.swift").replace("Owns: `owner.swift`.", "Owns: `owner.swift`, `alias.swift`.")
            self.assertEqual(self.run_alias(root, same)[1], [])
            marked = same + "\nparent-controlled path web/package-lock.json\n"
            marked_errors = self.run_alias(root, marked)[1]
            self.assertTrue(any("parent-controlled" in error for error in marked_errors), marked_errors)
            self.assertFalse(any("resolves to" in error for error in marked_errors), marked_errors)
            both = self.run_alias(root, same_layer + "\nparent-controlled path web/package-lock.json\n")[1]
            self.assertTrue(any("parent-controlled" in error for error in both), both)
            self.assertTrue(any("resolves to owner.swift" in error for error in both), both)
            linked = contract("L1A", "easy", "linkdir") + contract("L1B", "hard", "real/child.swift")
            linked_errors = self.run_alias(root, linked)[1]
            self.assertFalse(any("directory ownership" in error for error in linked_errors), linked_errors)
            self.assertTrue(any("ancestor ownership overlap" in error for error in linked_errors), linked_errors)

    def test_four_build_layers_in_a_row_need_a_review_layer(self):
        _, errors = self.inspect(build_layers(4))
        self.assertIn("L1-L4: 4 build layers in a row; add a review layer (Kind: review) after every two or three", errors)
        self.assertEqual(self.inspect(build_layers(3))[1], [])

    def test_review_layer_resets_the_run_and_may_overlap(self):
        layer = review("L4A", "frontend", "full-tests") + review("L4B", "frontend/src/app.tsx", "silent-failures")
        tail = contract("L5A", "easy", "app/l5.py", "all L4 merged")
        _, errors = self.inspect(build_layers(3) + layer + tail)
        self.assertEqual(errors, [])

    def test_review_layer_needs_full_tests(self):
        layer = review("L2A", "frontend", "ui-polish")
        _, errors = self.inspect(build_layers(1) + layer)
        self.assertIn("L2: review layer needs slices with Lens: full-tests", errors)

    def test_review_and_build_slices_do_not_share_a_layer(self):
        layer = review("L2A", "frontend", "full-tests") + contract("L2B", "easy", "app/b.py", "all L1 merged")
        _, errors = self.inspect(build_layers(1) + layer)
        self.assertIn("L2: mixes review and build slices; a review layer holds only review, climb and bench slices", errors)

    def test_climb_slice_needs_rubric_and_baseline(self):
        body = contract("L1A", "hard", "frontend/src/app/page.tsx") + "Kind: climb\nRubric: p75 time to interactive on /, ms, lower wins.\n"
        _, errors = self.inspect(body)
        self.assertEqual(errors, ["L1A: climb slice missing Baseline"])
        self.assertEqual(self.inspect(body + "Baseline: 1840 ms on 2026-11-12.\n")[1], [])

    def test_unknown_kind_is_rejected(self):
        _, errors = self.inspect(contract("L1A", "easy", "app/a.py") + "Kind: polish\n")
        self.assertIn("L1A: kind polish is not one of build, review, climb, bench, port", errors)

    def test_manifest_owner_states_its_dependency_change(self):
        body = contract("L1A", "easy", "frontend/package.json")
        _, errors = self.inspect(body)
        self.assertIn("L1A: owns a dependency manifest or lockfile; add 'Dependencies: <what it removes, or what it adds and why>'", errors)
        self.assertEqual(self.inspect(body + "Dependencies: removes zustand.\n")[1], [])

    def test_review_slice_names_a_known_lens(self):
        missing = contract("L2A", "hard", "frontend", "all L1 merged") + "Kind: review\n"
        _, errors = self.inspect(build_layers(1) + missing)
        self.assertTrue(any(error.startswith("L2A: review slice missing Lens") for error in errors), errors)
        _, errors = self.inspect(build_layers(1) + review("L2A", "frontend", "vibes"))
        self.assertTrue(any(error.startswith("L2A: lens vibes is not one of") for error in errors), errors)

    def test_every_lens_points_at_a_real_reference_and_is_documented(self):
        skills = Path(__file__).resolve().parents[2]
        doc = (skills / "layered-spec/references/review-and-climb-layers.md").read_text()
        for lens, reference in checker.LENSES.items():
            self.assertTrue((skills / reference).is_file(), reference)
            self.assertIn(f"`{lens}`", doc)

    def test_port_slice_needs_an_earlier_bench_slice(self):
        bench = contract("L1A", "easy", "bench/route_quotes.py") + "Kind: bench\nMeasures: p50 and p95 ms of GET /api/quotes.\n"
        port = contract("L2A", "hard", "crates/server/src/quotes.rs", "all L1 merged") + "Kind: port\nBench: L1A\n"
        self.assertEqual(self.inspect(bench + port)[1], [])
        self.assertEqual(self.inspect(bench + port.replace("Bench: L1A\n", ""))[1], ["L2A: port slice missing 'Bench: <bench slice id>' from an earlier layer"])
        same_layer = contract("L1B", "hard", "crates/server/src/quotes.rs") + "Kind: port\nBench: L1A\n"
        self.assertIn("L1B: Bench L1A must be a Kind: bench slice in an earlier layer", self.inspect(bench + same_layer)[1])
        self.assertIn("L1A: bench slice missing Measures", self.inspect(bench.replace("Measures: p50 and p95 ms of GET /api/quotes.\n", ""))[1])

    def test_bench_only_layers_do_not_count_toward_the_review_cadence(self):
        bench = contract("L3A", "easy", "bench/a.py", "all L2 merged") + "Kind: bench\nMeasures: p95 ms.\n"
        text = build_layers(2) + bench + contract("L4A", "easy", "app/l4.py", "all L3 merged")
        self.assertEqual(self.inspect(text)[1], [])


def graph_slice(slice_id, tier, owns, needs="none", extra=""):
    return f"""## {slice_id} {tier}. Job
Owns: `{owns}`.
Forbidden: everything else.
Needs: {needs}
Done when: the counted public read stays at one query.
Size: {tier}. The label matches the header.
{extra}"""


class NeedsGraphTests(unittest.TestCase):
    def inspect(self, *parts):
        marked = [parts[0] if parts[0].startswith("Schedule:") else "Schedule: needs-graph\n" + parts[0], *parts[1:]]
        with TemporaryDirectory() as directory:
            paths = []
            for index, text in enumerate(marked):
                path = Path(directory) / f"part-{index}.md"
                path.write_text(text)
                paths.append(path)
            return checker.check(paths)

    def test_needs_replaces_depends_and_allows_same_layer(self):
        text = graph_slice("L1A", "easy", "app/a.py") + graph_slice("L1B", "easy", "app/b.py", "L1A")
        self.assertEqual(self.inspect(text)[1], [])

    def test_missing_or_prose_needs_is_rejected(self):
        missing = graph_slice("L1A", "easy", "app/a.py").replace("Needs: none\n", "")
        self.assertIn("L1A: missing Needs", self.inspect(missing)[1])
        prose = graph_slice("L1A", "easy", "app/a.py", "all earlier layers merged")
        self.assertIn("L1A: Needs must be none or a comma-separated list of slice ids", self.inspect(prose)[1])

    def test_depends_must_match_needs_when_both_exist(self):
        text = graph_slice("L1A", "easy", "app/a.py").replace("Done when:", "Depends: L2A\nDone when:")
        self.assertIn("L1A: Depends and Needs must list the same slice ids", self.inspect(text)[1])
        same = graph_slice("L1A", "easy", "app/a.py", "none").replace("Done when:", "Depends: none\nDone when:")
        self.assertEqual(self.inspect(same)[1], [])

    def test_overlap_requires_a_needs_edge_across_layers_and_reviews(self):
        blocked = graph_slice("L1A", "easy", "app/rows.py") + graph_slice("L2A", "hard", "app/rows.py")
        self.assertIn("L1A overlaps L2A without a Needs edge: app/rows.py", self.inspect(blocked)[1])
        linked = graph_slice("L1A", "easy", "app/rows.py") + graph_slice("L2A", "hard", "app/rows.py", "L1A")
        self.assertEqual(self.inspect(linked)[1], [])
        chain = graph_slice("L1A", "easy", "app/rows.py") + graph_slice("L2A", "hard", "app/other.py", "L1A") + graph_slice("L3A", "hard", "app/rows.py", "L2A")
        self.assertEqual(self.inspect(chain)[1], [])
        review_block = (
            graph_slice("L2A", "hard", "app/rows.py", extra="Kind: review\nLens: full-tests\n")
            + graph_slice("L2B", "hard", "app/rows.py", extra="Kind: review\nLens: security\n")
        )
        self.assertTrue(any("without a Needs edge: app/rows.py" in error for error in self.inspect(review_block)[1]))
        review_ok = review_block.replace("Needs: none\nDone when: the counted public read stays at one query.\nSize: hard. The label matches the header.\nKind: review\nLens: security\n", "Needs: L2A\nDone when: the counted public read stays at one query.\nSize: hard. The label matches the header.\nKind: review\nLens: security\n", 1)
        self.assertEqual(self.inspect(review_ok)[1], [])

    def test_cycle_unknown_and_per_file_letter_order(self):
        cycle = graph_slice("L1A", "easy", "app/a.py", "L1B") + graph_slice("L1B", "easy", "app/b.py", "L1A")
        self.assertTrue(any(error.startswith("needs cycle:") for error in self.inspect(cycle)[1]))
        self.assertIn("L1A: Needs unknown id L9Z", self.inspect(graph_slice("L1A", "easy", "app/a.py", "L9Z"))[1])
        self.assertEqual(self.inspect(graph_slice("L1B", "easy", "app/b.py"), graph_slice("L1A", "easy", "app/a.py"))[1], [])
        swapped = graph_slice("L1B", "easy", "app/b.py") + graph_slice("L1A", "easy", "app/a.py")
        self.assertTrue(any("slice letters are not in order" in error for error in self.inspect(swapped)[1]))

    def test_marker_does_not_change_plans_that_omit_it(self):
        count, errors = SliceContractTests().inspect(contract("L1A", "easy", "app/rows.py"), contract("L2A", "hard", "app/rows.py", "all L1 merged"))
        self.assertEqual((count, errors), (2, []))


if __name__ == "__main__":
    unittest.main()

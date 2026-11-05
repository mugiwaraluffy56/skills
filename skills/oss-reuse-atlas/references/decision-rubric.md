# Reuse Decision Rubric

Use the rubric to compare candidates, NOT to manufacture false precision. Give evidence for high/low ratings and list blockers separately from the score.

| Dimension | Points | What strong evidence looks like |
|---|---:|---|
| Relevant product/workflow fit | 25 | Same actual user journey, workflow and operating assumptions |
| Proven source-level capability | 20 | D2 inspected paths, concrete behavior, relevant tests, meaningful error handling |
| Technical fit | 15 | Compatible language, APIs, runtime, security, deployment model and data ownership |
| Reuse feasibility / license clarity | 15 | Identified package/file license and use mode, manageable obligations, no license ambiguity |
| Maintenance and ecosystem | 10 | Recent meaningful upkeep or mature stable project, functioning docs/releases, responsiveness |
| Quality / test depth | 10 | Meaningful tests for actual behavior, CI/check methodology, clear boundaries and safe failure paths |
| Adoption and support cost | 5 | Small dependency surface or justified adaptation burden, sustainable updates |
| **Total** | **100** | Score is advisory; no single ranking substitutes for fit and evidence |

Rate each on documented evidence; if not inspected use `unknown` instead of awarding full points. A D0/D1 candidate can rank as a *research lead*, but not a D2 reuse selection. A candidate with `unknown` license for copied material is blocked for copying regardless of score. No stars-based shortcuts.

## Decision semantics

- **`use_dependency_or_service`:** stable public interface, maintenance acceptable, license/service terms checked, operational fit established. Record versioning and supply-chain uncertainties.
- **`copy_or_adapt`:** specific source files/modules and license obligations are known; own ongoing maintenance and upstream update burden is explicit. Do not recommend copy from source with no reuse permission.
- **`port_or_translate`:** transferable algorithm/system structure, but differences in data model, language semantics, async/concurrency, performance or license require explicit review. Translation may still be a derivative work.
- **`study_pattern_or_tests`:** architectural idea, quality strategy, navigation, visualization or test cases worth learning from; no promise to reuse implementation.
- **`defer`:** relevant but requires additional inspection, a dependency/compatibility decision or license/legal clearance.
- **`reject`:** specific evidence of poor fit, risk, license restrictions or unsuitable assumptions; include why.

## Claim and evidence hygiene

For every candidate conclusion distinguish:

1. **Repository claims:** stated by the upstream README or docs.
2. **Source confirmed:** seen in code at a specified immutable revision.
3. **Test confirmed:** tests assert that behavior; note tests are not proof of live operation.
4. **Reproduced:** actually run or observed in a controlled environment with commands, artifacts and revision.
5. **Unknown:** absence of evidence, not evidence of absence.

Use exact language such as "upstream documents", "code implements", "test asserts", or "not inspected". Avoid "battle tested", "production ready", "works with our app", and "drop in" unless supported by relevant evidence.

## Source licensing flags

Record license identifier (if verified), license document URL, per-file overrides if applicable, required notices/attribution, copyleft implications, trademark/branding constraints, and whether legal review is needed. Research is not legal advice. Do not recommend direct source copying under `unknown`, `no license`, or restricted/commercial terms without clearance.

## Evidence thresholds

- Featured direct-product examples: D1 is acceptable for *discovery*, but explicitly identify as uninspected; D2 preferred for confident comparative claims.
- `use_dependency_or_service`, `copy_or_adapt`, `port_or_translate`: D2 minimum.
- `study_pattern_or_tests`: D2 for specific source/test claims; D1 may support a tentative design inspiration lead.
- D3 is optional. A future team's actual integration must earn its own testing/evidence; atlas selection is not local adoption.

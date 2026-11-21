# AI export: what it protects, and what it doesn't

`GET /api/ai-export/?k=<int>` returns employee skill profiles for downstream AI
or analytics systems. It is the only way skill data is meant to leave the
system for model training or analysis.

## Access

The endpoint requires the dedicated permission
`skillzor.export_pseudonymized_profiles`. Read access to employees is **not**
enough. Grant it to a service account in the Django admin, not to people.

`k` defaults to `EXPORT_MIN_K` (env, default `5`). Callers may raise it, never
lower it.

## Guarantees

| Measure | What happens | Why |
| --- | --- | --- |
| Pseudonymisation | `pseudonym = HMAC-SHA256(PSEUDONYM_KEY, "employee:<id>")[:20]` | Records stay linkable across exports for longitudinal analysis, but not back to a person without the key. Rotating `PSEUDONYM_KEY` unlinks all earlier exports. |
| Data minimisation | Names, free-text `evidence` and exact dates are never exported. Certification dates are reduced to the year. | Free text is the classic PII leak; exact dates are quasi-identifiers. |
| k-anonymity on `department` × `job_title` | Rare titles are generalised to `null` within their department; small departments are suppressed. Generalised buckets that would still be smaller than `k` absorb the smallest neighbouring groups until they reach `k`. | Dropping a rare title is not enough if the person ends up alone in the "title unknown" bucket. A property test (`test_every_released_bucket_has_at_least_k_members`) checks this over 300 random org charts. |
| Rare attribute suppression | Skills and certifications held by fewer than `k` employees are dropped. | A unique skill identifies a person as well as a name does. |
| Tiny populations | If there are fewer than `k` employees in total, nothing is released (`privacy.withheld: true`). | There is no safe way to release anything. |
| Stable ordering | Records are sorted by pseudonym, not by database ID. | Row order must not leak insertion order. |

Every response carries a `privacy` block with the counts of what was
generalised, suppressed or dropped, so consumers can see the cost of
anonymisation instead of guessing.

## Known limits

Be honest about these before using the export for anything real:

* **k-anonymity is not differential privacy.** The combination of several
  common skills and their levels can still be unique. Skill *combinations* are
  not generalised; only single rare skills are dropped.
* **Attribute disclosure.** If all `k` people in a bucket share the same level
  for a skill, that level is disclosed for each of them (no l-diversity).
* **Repeated exports.** Differencing two exports taken before and after a
  single person joins can reveal that person's profile. Rate-limit and log
  exports, and rotate `PSEUDONYM_KEY` when the consumer changes.
* **The key is the boundary.** Anyone with `PSEUDONYM_KEY` and database access
  can re-identify every record.

## Example

```json
{
  "generated_at": "2026-11-22T10:00:00+00:00",
  "schema_version": 1,
  "privacy": {
    "k": 5,
    "employees": 33,
    "job_titles_generalised": 14,
    "departments_suppressed": 5,
    "rare_skills_dropped": 2,
    "rare_certifications_dropped": 1,
    "withheld": false
  },
  "records": [
    {
      "pseudonym": "012dc8230ca86a064a64",
      "department": "Data",
      "job_title": null,
      "skills": [
        {"skill_id": 3, "framework_ref": "e-CF:B.1", "level": 5},
        {"skill_id": 5, "framework_ref": "e-CF:D.7", "level": 2}
      ],
      "certifications": []
    }
  ]
}
```

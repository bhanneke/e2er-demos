# Rerunning the studies every week

Once a week, the workflow [`reproduce.yml`](../.github/workflows/reproduce.yml) downloads each study listed in [`studies.json`](studies.json) from its e2er.org address, runs its code again with the latest e2er, and compares the results with the published ones. It then writes one file, `reproduce-status.json`, and attaches it to the release [`reproduce-status`](https://github.com/bhanneke/e2er-demos/releases/tag/reproduce-status) of this repository. e2er.org reads that file and shows one line on each study's page: when the study was last rerun, with which e2er version, and what came out.

## What one run does

1. **List.** The first job tests `status.py` and reads `studies.json`. Every other job takes its list of studies from there.
2. **Rerun.** One job per study, on `ubuntu-latest` with Python 3.12, at most four at a time and at most 60 minutes each:
   - `pip install --upgrade e2er` installs the latest release; the job records its version.
   - `e2er fetch <address> -o <name>.e2er` downloads the study package from where its authors keep it and checks its size and SHA-256 against e2er.org.
   - `e2er reproduce <name>.e2er --yes --json report.json` reruns the study's steps in a Docker container. Steps that load data again from their source use the web; the other steps run without it. The workflow stops a rerun after 50 minutes.
   - `status.py entry` turns the report into the study's entry, and the job keeps the report, the logs and the entry as an artifact for 90 days (without the package itself).

   The job passes whatever the study's outcome: a study that does not reproduce is a result. A job fails only when the workflow itself breaks.
3. **Publish.** The last job collects the entries, keeps the previous entry of any study this run did not check (a run limited to one study, or a job that broke), drops studies no longer listed, checks the file against the schema below and replaces `reproduce-status.json` on the release `reproduce-status`. It creates the release on its first run. Only this job may write to the repository (`contents: write`), and only on `main`.

The workflow runs every Monday at 03:17 UTC. To run it by hand, open Actions → "Reproduce the studies" → Run workflow; the field `only` takes one project name (for example `pleiades-gaia-dr3-members`) to rerun that study alone.

## The verdicts

| verdict | when | e2er.org shows |
|---|---|---|
| `reproduced` | `e2er reproduce` exits with 0: every compared value is identical or the same at the published precision, and every table renders the same | Reproduced on 12 November 2026 with e2er 0.20.1. |
| `not-exact` | it exits with 1: values, tables or inputs differ | Reproduced with small numerical differences (only small differences), or "Not reproduced exactly" with e2er's summary |
| `source-changed` | the report says that data loaded again from their source differ from the data the study recorded | The source data changed since publication, with e2er's summary |
| `source-unavailable` | a data source did not answer (a time-out or a server error) | A data source did not answer when the study was rerun on …; the next run tries again. |
| `failed` | the package could not be fetched, the code could not run (exit 2), or the rerun did not finish in 50 minutes | Did not reproduce on …, with the reason |

The summary is e2er's own sentence from the report (`verdict`), cut to one line of at most 300 characters.

## `reproduce-status.json`

```json
{
  "schema": "e2er-reproduce-status/1",
  "repository": "bhanneke/e2er-demos",
  "generated_at": "2026-11-16T04:02:11Z",
  "run_url": "https://github.com/bhanneke/e2er-demos/actions/runs/1234567890",
  "studies": [
    {
      "address": "https://e2er.org/bhanneke/frankfurt-temperature-trend-forecasts",
      "checked_at": "2026-11-16T03:44:52Z",
      "e2er_version": "0.20.1",
      "verdict": "not-exact",
      "summary": "Not reproduced exactly: 1332 value(s) show small differences; 4 differ; 1 table(s) render differently.",
      "counts": {
        "values": 3463, "identical": 1600, "same_at_precision": 527, "small_difference": 1332, "differs": 4,
        "missing_in_rerun": 0, "only_in_rerun": 0,
        "tables_rendered": 4, "tables_identical": 3, "tables_differ": 1,
        "inputs": 1, "inputs_differ": 0
      },
      "exit_code": 1,
      "package_sha256": "64 hex digits: the SHA-256 of the .e2er file the run fetched",
      "run_url": "https://github.com/bhanneke/e2er-demos/actions/runs/1234567890"
    }
  ]
}
```

| field | type | meaning |
|---|---|---|
| `schema` | `"e2er-reproduce-status/1"` | the version of this format |
| `repository` | `owner/name` | the repository whose workflow wrote the file |
| `generated_at` | UTC time, `YYYY-MM-DDTHH:MM:SSZ` | when the file was written |
| `run_url` | `https://github.com/<repository>/actions/runs/<id>` | the run that wrote the file |
| `studies[]` | at most 200 entries, one per address | |
| `.address` | `https://e2er.org/<owner>/<project>` | the study |
| `.checked_at` | UTC time | when the rerun finished |
| `.e2er_version` | `0.20.1` | the e2er release that reran it |
| `.verdict` | `reproduced`, `not-exact`, `source-changed`, `source-unavailable` or `failed` | see above |
| `.summary` | one line of plain text, 1 to 300 characters | what e2er said |
| `.counts` | object of whole numbers, or `null` | compared values by outcome (`values`, `identical`, `same_at_precision`, `small_difference`, `differs`, `missing_in_rerun`, `only_in_rerun`), tables (`tables_rendered`, `tables_identical`, `tables_differ`) and inputs (`inputs`, `inputs_differ`); a count the report does not give is left out |
| `.exit_code` | whole number or `null` | the exit code of `e2er reproduce` (`null` when the package could not be fetched) |
| `.package_sha256` | 64 hex digits or `null` | the SHA-256 of the package the run checked |
| `.run_url` | as above | the run that checked this study (an earlier one when the entry was kept) |

No other fields are allowed. `status.py` checks every entry and the whole file before the workflow publishes it (`status_problems`).

## How e2er.org uses the file

e2er.org stores no files and no status. When a study page opens, e2er.org takes the repository of the study's package record (a release asset `https://github.com/<owner>/<repository>/releases/download/…/<name>.e2er`) and reads `https://github.com/<owner>/<repository>/releases/download/reproduce-status/reproduce-status.json` from that same repository: never from another repository, and never from another host. It keeps the answer for an hour (a failed lookup for five minutes), reads at most 256 KB, rejects a file that does not match the schema, shows every text as plain text and links only to a run in that repository. It shows the line only for the study's own address and only when `package_sha256` is the SHA-256 of the package e2er.org records for the study's current version; it does not show the status of an earlier version. Without a file, or without an entry for the study, the page shows nothing.

## The same for your own studies

Any researcher whose study packages are release assets in their own GitHub repository can publish the same status:

1. Copy `.github/workflows/reproduce.yml` and the folder `reproduce/` (`status.py`, `tests/`, `studies.json`) into the repository that holds the study packages. The tests check your own `studies.json`.
2. List your studies in `reproduce/studies.json`: `{"studies": [{"address": "https://e2er.org/<you>/<project>"}]}`. Each study's package must be a release asset of this same repository; e2er.org reads the status only from the repository the package is in.
3. If your default branch is not `main`, change `refs/heads/main` in the publish job.
4. Under Settings → Actions → General, allow GitHub Actions. The workflow needs no secret: the `GITHUB_TOKEN` of the run creates the release and replaces its file.
5. Run the workflow once by hand (Actions → Reproduce the studies → Run workflow). After it finishes, your studies' pages on e2er.org show the line within an hour.

A study whose package is on Zenodo has no repository e2er.org could read a status from, so its page shows no line.

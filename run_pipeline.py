from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    print("\n$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild the wastewater infrastructure analytics pipeline from an asset CSV."
    )
    parser.add_argument("--project", type=Path, default=Path("."))
    parser.add_argument("--input", type=Path, default=Path("data/raw/assets.csv"))
    parser.add_argument("--skip-ingest", action="store_true")
    args = parser.parse_args()

    project = args.project.resolve()
    input_path = args.input if args.input.is_absolute() else project / args.input
    database = project / "data" / "derived" / "wastewater.sqlite"
    py = sys.executable

    if not args.skip_ingest:
        run(
            [
                py,
                "src/ingest_assets.py",
                "--input",
                str(input_path),
                "--db",
                str(database),
                "--processed",
                str(project / "data" / "processed" / "assets_clean.csv"),
            ],
            project,
        )

    run([py, "src/run_sql.py", "--db", str(database), "--sql", "sql/01_quality_checks.sql"], project)
    run([py, "src/run_sql.py", "--db", str(database), "--sql", "sql/02_build_priority_views.sql"], project)
    run([py, "src/build_engineering_priority.py", "--project", str(project)], project)
    run([py, "src/lifecycle_cost_model.py", "--project", str(project)], project)
    run([py, "src/capital_allocation.py", "--project", str(project)], project)
    run([py, "src/generate_figures.py", "--project", str(project)], project)

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()

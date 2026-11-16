# Measurements

Measurements of the fabricated chip, one folder per taped-out release. `v.<VERSION>/` holds the measurements of the chip built as `release/v.<VERSION>/`, in the repository structure IHP proposes for its open MPW projects.

Inside a release folder, each measured block has a folder of its own:

| Path | Content |
| --- | --- |
| `<block>/README.md` | setup, pads, conditions, and each result next to the simulated value it is compared with and the file that value comes from |
| `<block>/data/` | raw instrument files, unchanged |
| `<block>/figures/` | plots made from `data/` |
| `<block>/scripts/` | the scripts that drive the instruments and turn `data/` into `figures/` |

Every result names the sample (package or die), the supply voltages, the temperature, and the instruments with their settings. The `.gitignore` of this repository ignores `*.raw` and `*.log` in every folder, so give raw files another extension or add them with `git add -f`.

<!-- template-only -->
## The Taped-Out Template Chip

[`v.1.0.0/`](v.1.0.0/) holds the placeholders for the chip of this branch [`IHP-TO-2026-11`](https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/tree/IHP-TO-2026-11), submitted to the IHP open MPW of November 2026 as [`SoC1693`](https://github.com/simi1505/IHP__SoC1693). Its release files are in [`release/v.1.0.0/`](../release/v.1.0.0/).
<!-- /template-only -->

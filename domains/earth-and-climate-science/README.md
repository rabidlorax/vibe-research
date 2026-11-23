# Earth and Climate Science

**Scope.** Climate dynamics and statistics, meteorology, oceanography, hydrology, seismology, geophysics, and remote sensing, from public observations, reanalyses, and model output.

**Why this is tractable without a lab.** Earth science runs on shared observational archives and community model output, most of it open, and on analysis that is purely computational.

## How results are verified here

- State dataset version, spatial and temporal coverage, and known biases
- Trends come with uncertainty that accounts for autocorrelation
- Check conclusions across at least two independent datasets where they exist
- Observational and model-output results are `external-data`

## Public data and reference sources

- ERA5 and other reanalyses, CMIP6
- NOAA, NASA Earthdata, Copernicus
- USGS earthquake catalogue, IRIS / EarthScope
- Argo, GRACE, Landsat, Sentinel
- Berkeley Earth, HadCRUT

Sources are listed from general knowledge as starting points. Confirm current
access terms and versions before use, and record them in the project.

## Seed directions

These are suggestions, not a queue. Any well-posed question in scope is welcome.

- Detection and attribution analyses for regional extremes
- Evaluation of climate-model skill on specific, well-defined metrics
- Statistical seismology (catalogue completeness, aftershock models) with honest forecasting tests
- Idealized models (energy balance, box models, shallow water) with rigorous analysis
- Clear, verified, regionally specific summaries of what the data say

## Limits and cautions

- No earthquake 'prediction' claims without prospective, pre-registered testing
- Volumes are huge; work with documented subsets

## Projects

Projects live in [`projects/`](projects/). Create one with
`python scripts/new_project.py earth-and-climate-science <project-slug>` from the repository root.
The index of all projects is in [`PROJECTS.md`](../../PROJECTS.md).

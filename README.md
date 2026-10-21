# e2er demonstration studies

> **Demonstration: published as is, not endorsed.** These studies were produced with e2er as demonstrations or test runs and are published as is. They are not presented as research contributions, and their author does not vouch for their findings.

Each folder holds the files of one study made with [e2er](https://e2er.org): the paper (PDF and LaTeX), the code, the results, the design, the reviews and the records that let anyone check and rerun it. The README in each folder links the study's dossier on e2er.org, which lists every step of the run, the models, the data loads and the checks.

## The studies

1. [`exoplanet-radius-period-provenance/`](exoplanet-radius-period-provenance/) · [study page](https://e2er.org/bhanneke/exoplanet-radius-period-provenance) · [dossier](https://e2er.org/d/3f3a95d2a49b0c71)  
   How are confirmed exoplanets distributed in planet radius and orbital period, and how does that distribution change when radii measured from transits are separated from radii calculated from planet mass?
2. [`pleiades-gaia-dr3-members/`](pleiades-gaia-dr3-members/) · [study page](https://e2er.org/bhanneke/pleiades-gaia-dr3-members) · [dossier](https://e2er.org/d/f6140fa5d03bcc07)  
   Which stars within 3 degrees of the Pleiades centre are cluster members by Gaia DR3 parallax and proper motion, and what do their colour-magnitude diagram and parallax distance distribution show about the cluster's distance and main sequence?
3. [`earthquake-counts-b-value-by-decade/`](earthquake-counts-b-value-by-decade/) · [study page](https://e2er.org/bhanneke/earthquake-counts-b-value-by-decade) · [dossier](https://e2er.org/d/3777eb6cfb5dfd27)  
   How has the yearly number of magnitude 5 and larger earthquakes worldwide changed from 1976 to 2025, and is the Gutenberg–Richter b-value stable across decades once the catalogue's completeness magnitude is taken into account?
4. [`frankfurt-temperature-trend-forecasts/`](frankfurt-temperature-trend-forecasts/) · [study page](https://e2er.org/bhanneke/frankfurt-temperature-trend-forecasts) · [dossier](https://e2er.org/d/c985731bebd41662)  
   How has the monthly mean air temperature at 2 metres in Frankfurt am Main (NASA POWER, 50.11 N, 8.68 E) changed since 1981, and how well do seasonal forecasting models predict the next 36 months compared with a seasonal naive baseline?
5. [`school-fee-abolition-enrolment-africa/`](school-fee-abolition-enrolment-africa/) · [study page](https://e2er.org/bhanneke/school-fee-abolition-enrolment-africa) · [dossier](https://e2er.org/d/626aef717cbc7d84)  
   Did abolishing primary-school fees in sub-Saharan African countries (staggered between the mid-1990s and the mid-2000s) raise gross primary enrolment? A difference-in-differences with World Bank enrolment data, comparing countries that abolished fees with countries that had not (yet) abolished them.
6. [`eu-regional-gdp-spatial-clustering/`](eu-regional-gdp-spatial-clustering/) · [study page](https://e2er.org/bhanneke/eu-regional-gdp-spatial-clustering) · [dossier](https://e2er.org/d/42495852899961c7)  
   How does GDP per capita in purchasing power standards vary across the EU's NUTS-2 regions in 2024, and how strongly do regions with high and low GDP per capita cluster in space?
7. [`road-traffic-death-rates-2021/`](road-traffic-death-rates-2021/) · [study page](https://e2er.org/bhanneke/road-traffic-death-rates-2021) · [dossier](https://e2er.org/d/a73c0a40f591db08)  
   How do estimated road traffic death rates per 100,000 people vary across countries and WHO regions in 2021? A descriptive study with the WHO Global Health Observatory indicator RS_198.
8. [`weather-words-english-novels/`](weather-words-english-novels/) · [study page](https://e2er.org/bhanneke/weather-words-english-novels) · [dossier](https://e2er.org/d/67f22aa2136e140d)  
   How did the vocabulary of weather (rain, wind, storm, fog, snow, sun, cloud and related words) vary across English-language novels by authors born in six cohorts, 1770–1799 to 1880–1899?

## Data and their terms

Data go into a folder only when their source's terms allow passing them on. Data from sources whose terms do not (for example Gaia, Eurostat GISCO and the WHO Global Health Observatory), and files a study built from them, are left out. The README of each folder names every file left out and the reason, and `e2er reproduce <folder>` loads those data again from their source and rebuilds the derived files with the study's own scripts. A data file larger than GitHub takes (100 MB) is left out as well when the study's recorded steps get it back: demo 8's `data/data.db` (145 MB), whose Project Gutenberg texts `e2er reproduce` loads again and whose corpus tables it builds again with the study's own script. The data keep their sources' terms; each folder's README gives the terms and the citation of every source.

## Checking a study

```bash
pip install e2er
git clone https://github.com/bhanneke/e2er-demos.git
e2er verify e2er-demos/<folder>
e2er reproduce e2er-demos/<folder>
```

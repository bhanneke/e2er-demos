# Literature Review: Monthly 2 m Air Temperature in Frankfurt am Main (NASA POWER, 1981-) and 36-Month Seasonal Forecasts vs. Seasonal Naive

Specialist: literature_scanner. Stage: idea.

## 0. Citation status (read first)

- `literature.bib` holds 39 keys. 11 are methods sources for this template. The other 28 are the researcher's papers, which cover crypto, NFTs, DeFi, wash trading, auctions, platforms and neuroscience. **None is relevant to climate, reanalysis or temperature forecasting.** Do not cite them. This covers `unknown2019cryptocurrencies`, `aloosh2024direct`, `lin2023crypto`, `sun2022liquidity`, `junior2024it` and the rest of that group.
- **Citable now (verified relevant methods sources):** `box2008time`, `hyndman2021forecasting`, `hyndman2008automatic`, `hyndman2006another`, `tashman2000out`, `diebold1995comparing`, `harvey1997testing`, `dickey1979distribution`, `kwiatkowski1992testing`, `mann1945nonparametric`, `sen1968estimates`.
- **Not in the bib.** No bib key exists for the climate and data literature in sections 1-2 or for the M-competition literature in section 3. These are well-known works listed from the scanner's knowledge. No search was run in this session, so bibliographic details (pages, exact figures) must be verified. Before citing, run `e2er-lit search "<title>"` to register each one. Until then, the drafter should state the claims without `\cite{}`.

## Key Findings (from the literature)

1. Germany and Central Europe have warmed faster than the global mean over land. DWD national-mean warming since 1881 is roughly 1.5-1.7 °C (verify the exact figure in the current DWD Klimareport). Most of it has occurred since about 1980, and the warmest years cluster after 2000. [Section 1]
2. MERRA-2 is a reanalysis product (1980-present) and the source of NASA POWER's daily and monthly meteorology. T2M is a model-assimilated quantity on a 0.5° x 0.625° grid, not a point station measurement. Validation studies find high correlation with stations, with biases that depend on the region, on elevation and on whether the grid cell is urban or complex terrain. [Section 2]
3. For monthly data with strong seasonality, the seasonal naive forecast (value 12 months earlier) is the standard benchmark. ETS and ARIMA are the usual competitors, and in M-competitions they are hard to beat consistently. [Section 3]
4. Methodology for comparing forecasts: scale-free errors (MASE, Hyndman & Koehler 2006), rolling-origin out-of-sample evaluation (Tashman 2000), and the Diebold-Mariano test with the Harvey-Leybourne-Newbold small-sample correction. [Section 3]

## 1. Observed warming in Central Europe and Germany since 1980

Not in the bib; to be registered.

- **DWD station network and products.** Kaspar et al. (2013), "Monitoring of climate change in Germany: data, products and services of Germany's National Climate Data Centre", *Advances in Science and Research* 10, 99-106. It documents the DWD observing network and homogenised series. DWD's annual *Nationaler Klimareport* gives the national mean temperature trend and the number of warm years. Verify the current edition and its figures before quoting.
- **National assessment.** Brasseur, Jacob & Schuck-Zöller (eds.) (2017), *Klimawandel in Deutschland*, Springer. It is a comprehensive German assessment of observed and projected change.
- **Europe-wide.** IPCC AR6 WGI (2021), Chapter 12 (regional fact sheet for Europe) and the Atlas, for the observed warming and heat-extreme increase in Europe. Citation should be "Masson-Delmotte et al. (eds.) 2021". Check the chapter authors.
- **Heat extremes.** Schär et al. (2004), *Nature* 427, 332-336. Luterbacher et al. (2004), *Science* 303, 1499-1503 (European seasonal temperature over 500 years). Rousi et al. (2022), *Nature Communications* 13, 3851, on accelerated western European heatwave trends. Verify the article number.
- **Reanalysis evidence.** Hersbach et al. (2020), "The ERA5 global reanalysis", *QJRMS* 146, 1999-2049. ERA5 and MERRA-2 both show strong warming over Europe after 1980. Cross-checking MERRA-2 against ERA5 and DWD is a possible robustness step for this paper.
- **Relevance to the paper.** The positive trend and the larger post-2000 increase are expected. This motivates a deterministic trend component, tested with Mann-Kendall (`mann1945nonparametric`) and Sen's slope (`sen1968estimates`), plus possibly an autocorrelation-corrected version (Hamed & Rao 1998, *J. Hydrology* 204, 182-196; not in bib). Unit-root and stationarity checks use `dickey1979distribution` and `kwiatkowski1992testing`.
- **Urban-effect caveat.** Frankfurt is a large urban area with an airport station. MERRA-2's grid cell mixes surfaces, so urban heat island effects are not resolved in the product. The literature on the DWD station versus reanalysis difference is not covered here.

## 2. NASA POWER / MERRA-2 and validation

Not in the bib; to be registered.

- **MERRA-2.** Gelaro et al. (2017), "The Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2)", *J. Climate* 30, 5419-5454. Coverage runs from 1980. This is why the series starts in 1981: POWER's meteorological record begins in January 1981 (verify against POWER documentation). Randles et al. (2017), *J. Climate* 30, 6823-6850, covers the aerosol assimilation. A known discontinuity concern is changes in the assimilated observing system over time, which can bias trends in reanalyses. Evaluate whether this matters for T2M.
- **NASA POWER.** The data-access project of the NASA Prediction of Worldwide Energy Resources (Stackhouse et al.). Cite the POWER documentation and data portal (power.larc.nasa.gov) with an access date. R access: Sparks (2018), "nasapower: a NASA POWER global meteorology, surface solar energy and climatology data client for R", *J. Open Source Software* 3(30), 1035.
- **Validation against stations.** The literature is mostly agronomic. Examples are Bai et al. (2010), *Agronomy Journal* 102, 9-16 (China, maize simulation), and several regional assessments in Africa, South America and Asia. The general finding is a high correlation for temperature and larger errors for precipitation and wind. I could not verify any Germany-specific POWER validation. This is a gap: the drafter should say that evidence for Central Europe is limited, and the paper may add its own comparison against DWD station data if data are provided.
- **Implication.** T2M from POWER is a gridded reanalysis estimate at 50.11 N, 8.68 E. Interpret trends as regional-scale, not station-scale. The data section should state the resolution and the daily-to-monthly aggregation.

## 3. Statistical seasonal forecasting, benchmarks and forecast comparison

### Bib-citable
- Box-Jenkins ARIMA / seasonal ARIMA: `box2008time`.
- ETS, ARIMA, seasonal naive, rolling-origin evaluation, MASE in practice: `hyndman2021forecasting`.
- `auto.arima` and `ets` automatic selection (forecast package): `hyndman2008automatic`.
- MASE and the critique of percentage errors: `hyndman2006another`. MASE scales the error by the in-sample one-step naive MAE (for seasonal data the seasonal naive MAE can be used as the scale). MASE < 1 means better than the benchmark.
- Out-of-sample evaluation design: `tashman2000out` (rolling origins, multiple forecast horizons).
- Diebold-Mariano test: `diebold1995comparing`. Small-sample correction (HLN) with t-distribution critical values: `harvey1997testing`. Use for h-step forecast errors with a Newey-West / h-1 lag variance.

### Not in bib (to be registered)
- Hyndman, Koehler, Snyder & Grose (2002), "A state space framework for automatic forecasting using exponential smoothing methods", *Int. J. Forecasting* 18, 439-454 (ETS).
- Makridakis & Hibon (2000), "The M3-Competition: results, conclusions and implications", *IJF* 16, 451-476. Makridakis, Spiliotis & Assimakopoulos (2020), "The M4 Competition: 100,000 time series and 61 forecasting methods", *IJF* 36, 54-74. Simple benchmarks (naive, seasonal naive, ETS, Theta) are hard to beat. Combinations do better than single methods.
- Diebold (2015), "Comparing predictive accuracy, twenty years later", *JBES* 33, 1-9. Giacomini & White (2006), *Econometrica* 74, 1545-1578 (conditional predictive ability). These matter because DM is for forecasts, not models, and rolling schemes.
- Cleveland et al. (1990), "STL: a seasonal-trend decomposition procedure based on loess", *J. Official Statistics* 6, 3-73.
- Gneiting & Raftery (2007), *JASA* 102, 359-378 (proper scoring rules, relevant if prediction intervals are scored).
- Taylor & Letham (2018), "Forecasting at scale" (Prophet), *The American Statistician* 72, 37-45, as an optional contender.
- Dynamical seasonal forecasting for context, e.g. Doblas-Reyes et al. (2013), *WIREs Climate Change* 4, 245-268. Skill at monthly lead times over Central Europe is modest. A 36-month horizon is beyond dynamical seasonal systems (which run about 7 months), so the statistical comparison is the relevant one here.

### Expected results from the literature (hypothesis, not finding)
- For monthly temperature, the seasonal cycle dominates the variance. Seasonal naive captures it but carries last year's anomaly noise, so it has roughly twice the error variance of a climatological-mean forecast. ETS or SARIMA with a trend should beat seasonal naive at medium horizons, mainly by averaging out the noise and extrapolating the trend. A seasonal-mean-plus-trend model would probably do as well. Gains at long horizons come from the trend and the climatology, not from dynamics.
- Add a seasonal mean (climatology) benchmark in addition to seasonal naive. Hyndman & Athanasopoulos 2021 describe the seasonal naive; the climatology benchmark is an obvious extension and the literature calls this out, because seasonal naive is a weak benchmark for noisy seasonal series.

## Methodology notes for downstream specialists

- The hold-out is the final 36 months. Compare models with MASE (scaled by in-sample seasonal naive MAE), RMSE and MAE, and with DM tests (HLN-corrected, squared or absolute loss) per horizon and pooled.
- DM with n = 36 observations at horizons 1-36 is low-powered, and the errors at adjacent horizons are correlated. The paper should say so. A rolling-origin design (`tashman2000out`) gives more forecast errors.
- The tests in `box2008time` / `dickey1979distribution` / `kwiatkowski1992testing` treat the series with a deterministic seasonal pattern. Remove or model the seasonal component first. ADF and KPSS may disagree under a trend.
- No causal claims. Describe the trend as an association and as consistent with the literature on regional warming, without attributing it.

## Gaps & Open Questions

- No bib entries for any climate or data-product paper. Register Gelaro 2017, Hersbach 2020, Kaspar 2013, IPCC AR6 and the M3 / M4 papers via `e2er-lit search` before the draft.
- No verified Germany-specific POWER validation paper was identified. If the claim is made, it must be hedged.
- DWD Frankfurt station data are not in the data available, so the validation of POWER against the station cannot be performed unless the data analyst adds it.
- Exact DWD national warming figures (1881-present and 1981-present) need checking against the current Klimareport.
- Whether the observing-system changes in MERRA-2 affect the T2M trend at this location is not addressed in the sources I know.

## Sources & References (summary list)

In bib: box2008time; hyndman2021forecasting; hyndman2008automatic; hyndman2006another; tashman2000out; diebold1995comparing; harvey1997testing; dickey1979distribution; kwiatkowski1992testing; mann1945nonparametric; sen1968estimates.

Not in bib (verify, then register): Gelaro et al. 2017 (J. Climate 30); Randles et al. 2017 (J. Climate 30); Sparks 2018 (JOSS 3(30), 1035); Bai et al. 2010 (Agron. J. 102); Hersbach et al. 2020 (QJRMS 146); Kaspar et al. 2013 (Adv. Sci. Res. 10); Brasseur et al. 2017 (Springer); IPCC AR6 WGI 2021; Schär et al. 2004 (Nature 427); Luterbacher et al. 2004 (Science 303); Rousi et al. 2022 (Nat. Commun. 13); Hamed & Rao 1998 (J. Hydrol. 204); Hyndman et al. 2002 (IJF 18); Makridakis & Hibon 2000 (IJF 16); Makridakis et al. 2020 (IJF 36); Diebold 2015 (JBES 33); Giacomini & White 2006 (Econometrica 74); Cleveland et al. 1990 (JOS 6); Gneiting & Raftery 2007 (JASA 102); Taylor & Letham 2018 (Am. Stat. 72); Doblas-Reyes et al. 2013 (WIREs Clim. Change 4).

Excluded as unrelated: all 28 researcher papers in the bib (crypto wash trading, DeFi, NFTs, stablecoins, auctions, platform economics, neuroscience).

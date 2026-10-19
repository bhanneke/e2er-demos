s = open('run_estimation.py').read()


def r(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)


r('c = df[df["mi"] >= round(th * 10)].groupby', 'c = df[df["mag"] >= th - 1e-9].groupby')
r('m5 = df[df["mi"] >= 50].copy()', 'm5 = df[df["mag"] >= 5.0 - 1e-9].copy()')
r('''"b_common_threshold": by_decade(mw_df, {d: MC_COMMON for d in mc_mw}),
                       "b_own_mc"''', '"b_own_mc"')
r('"n_events_m5plus": int((mw_df["mi"] >= 50).sum())', '"n_events_m5plus": int((mw_df["mag"] >= 5.0 - 1e-9).sum())')
r('"n_events_m5plus": int((sh_df["mi"] >= 50).sum())', '"n_events_m5plus": int((sh_df["mag"] >= 5.0 - 1e-9).sum())')
r('checks["mw_family_only"]["pair_tests_common"] = pair_tests(checks["mw_family_only"]["b_common_threshold"])\n',
  '''checks["mw_family_only"]["note"] = ("No b at the common threshold: moment magnitudes are assigned mainly to larger events, "
    "so the Mw-only sample is not complete at the common threshold; b is reported at the sample's own Mc only.")
''')
r('# ---------- schema blocks ----------', '''# Mc at the load floor (M>=4.5): estimate is censored there
FLOOR = 4.5
at_floor = {}
for rule in ("maxc", "gft90", "gft95"):
    at_floor[rule] = [d for d, v in mc_dec.items() if v[rule] is not None and abs(v[rule] - FLOOR) < 1e-9]
mc_censored = {"load_floor_magnitude": FLOOR,
               "decades_at_floor_by_rule": at_floor,
               "note": ("Mc = 4.5 equals the load floor (events with M>=4.5 only): the estimate is censored at the floor "
                        "and the true Mc may be lower. Decades listed are those where the raw rule returns 4.5; "
                        "for these decades b at Mc=4.5 uses all loaded events.")}

# ---------- schema blocks ----------''')
r('"completeness": {"per_decade": mc_dec,', '"completeness": {"per_decade": mc_dec, "mc_censored_at_load_floor": mc_censored,')
open('run_estimation.py', 'w').write(s)

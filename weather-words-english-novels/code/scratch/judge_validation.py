"""Writes text_validation.json from the hand judgments below (made by reading each passage in validation_sample.json).
Code: y = correct and literal, f = correct, figurative image whose vehicle is the weather itself, n = wrong."""
import json, collections

S = json.load(open("validation_sample.json", encoding="utf-8"))

J = {
"weather_all": [
("y","[literal] cloud crossing the moon"),("y","[literal] clouds parting before the moon"),
("y","[literal] tempest and calm among the Alpine seasons"),
("f","[figurative-right] plume likened to a cloud that emits sun rays and lightning"),
("y","[literal] mist driven by the gale at sea"),
("f","[figurative-right] 'the sun shines into his mind': sun image, mood tenor"),
("n","[figurative-wrong] 'storms and disappointments' are troubles of life"),
("y","[literal] stormy, windy night"),("y","[literal] lightning in a sea storm"),
("y","[literal] stray breeze in a summer parlour"),("y","[literal] clouds in the western sky"),
("y","[literal] wind blowing from them, carrying smoke"),
("n","[other-sense] 'hazy' conclusion = vague"),("y","[literal] gale at sea"),
("y","[literal] breeze from land on the voyage"),("y","[literal] mist shredding into clouds in a gorge"),
("y","[literal] gust of wind on the ship"),("y","[literal] hoary fog, drop on a twig"),
("y","[literal] showery days in April"),
("n","[figurative-wrong] 'gale of spears' breath' = battle, in a song"),
("y","[literal] sun on the peaks of the Rockies"),
("n","[other-sense] a song thundering forth, sound only"),
("n","[other-sense] 'misty blue' as a colour of eyes/hills, no weather"),
("y","[literal] snow-plow forcing through heavy snowfall"),("y","[literal] sunny landscape"),
("n","[other-sense] 'sun god', myth"),("n","[figurative-wrong] 'thunder of the spheres', music"),
("n","[other-sense] 'cold mists' of a cosmology, nebula"),
("y","[literal] rain-stained roof"),
("f","[figurative-right] 'breeze was sunshine in motion': sunshine image"),
],
"precipitation": [
("n","[other-sense] 'rapid showers' of arrows"),("y","[literal] rain falling on Wallace"),
("y","[literal] evening sinks into rain"),("y","[literal] it had rained every day"),
("y","[literal] shelter from a shower"),("y","[literal] rained hard in the night"),
("y","[literal] how the rain beats"),("y","[literal] 'we may have rain'"),
("y","[literal] showers curling away, sweet scents"),("y","[literal] rain in the leaves"),
("y","[literal] mild and rainy night"),("y","[literal] before the rain came"),
("n","[figurative-wrong] 'shower of buffets', memory of a quarrel"),
("y","[literal] northeasterly rain"),("y","[literal] drops of rain, then lightning"),
("f","[figurative-right] flatteries fell from him like rain"),
("n","[other-sense] 'shower on shower of stones', thrown"),
("y","[literal] out of the rain"),("y","[literal] 'looks like rain'"),
("y","[literal] out in the rain"),("y","[literal] rain shower from a bus roof"),
("y","[literal] drizzling rain"),("y","[literal] rain-drenched overall"),("y","[literal] when it rains")
],
"wind_words": [
("y","[literal] gale of wind"),
("n","[figurative-wrong] 'wind of praise', 'shifting gale' of fame (verse)"),
("y","[literal] ship before the gale"),("y","[literal] gentle breezes of evening"),
("y","[literal] 'before the wind', sailing"),("y","[literal] gust catching the sail"),
("y","[literal] a breeze (wind) bringing down on the ship, sailor's call"),
("y","[literal] not a breeze stirred"),("n","[other-sense] 'walls wind up', verb of winding"),
("y","[literal] gale at sea"),("y","[literal] gale at its height"),
("n","[figurative-wrong] 'a regular gale' of laughter"),
("f","[figurative-right] wind personified as the heath's friend, storm scene"),
("y","[literal] sea-breezes"),("y","[literal] gale from the north-east"),
("y","[literal] light breeze filling sails"),("y","[literal] rain and wind moderating"),
("y","[literal] a breeze at the window"),("y","[literal] breeze-swept mountainside"),
("y","[literal] flow of the breeze"),("y","[literal] a scream against the wind"),
("y","[literal] zephyr lashing the sage"),
("f","[figurative-right] stood as if leaning into a stiff gale"),("y","[literal] breeze whipping the curtains"),
],
"storm_words": [
("n","[figurative-wrong] storm in the citadel = political upheaval"),
("n","[figurative-wrong] 'stormy placing' of a minister = disputed"),
("f","[figurative-right] 'as the lightning scorches the bush'"),
("n","[figurative-wrong] 'domestic hurricane' = family uproar"),
("y","[literal] thunder nearing, lightning"),
("n","[figurative-wrong] 'stormy excitement' of music"),
("n","[figurative-wrong] 'lightning of conscience'"),
("y","[literal] rain and lightning in a sea storm"),
("n","[figurative-wrong] 'thunder of the sea' = surf noise, not the weather"),
("n","[figurative-wrong] eyes 'scintillated as if lightning'"),
("n","[idiom] 'pounced like lightning' = speed"),
("n","[figurative-wrong] 'let in a hurricane' = a draught, jest"),
("n","[figurative-wrong] 'thunder of waves', noise of breakers"),
("y","[literal] stormy drift of rain"),("y","[literal] sheet-lightning"),
("n","[figurative-wrong] 'like a lightning flash' for a sudden realisation"),
("y","[literal] 'had to storm', rain on a trip"),("y","[literal] lightning and thunder in the forest"),
("y","[literal] squall at sea"),("y","[literal] riding out the squall"),
("n","[idiom] 'thundering good breakfast', intensifier"),
("n","[idiom] 'lightning calculation' = speed"),
("y","[literal] hurricane, ice and fog as the sea's elements"),
("n","[other-sense] 'hurricane lantern', a lamp type"),
],
"fog_words": [
("n","[other-sense] 'standing fog' = dry rank grass, set alight on the prairie"),
("y","[literal] misty mountains"),("y","[literal] gathering mist on rocks"),
("y","[literal] nightly fog at sea"),("n","[figurative-wrong] 'as in a haze' = dazed"),
("y","[literal] foggy squall at sea"),("n","[other-sense] 'hazy scarf', fabric"),
("n","[figurative-wrong] 'chill fog between them' = estrangement"),
("y","[literal] hazy mountains in the distance"),("y","[literal] haze of the night before"),
("n","[figurative-wrong] 'mist of metaphysics'"),("y","[literal] morning haze"),
("y","[literal] dense fog-wreath"),("n","[other-sense] smoke mists from cigars"),
("y","[literal] sun flung a glittering mist over Sitka"),("y","[literal] dark blue mist of the afternoon"),
("n","[other-sense] mist from the vats of a stockyard"),("y","[literal] mist lifting"),
("y","[literal] the mist closing in"),("n","[figurative-wrong] 'blue haze round his hair', fleeing"),
("n","[figurative-wrong] 'cleared the fog from my mind'"),
("n","[other-sense] haze of gasoline fumes"),("n","[figurative-wrong] 'a mist was over all', obscurity"),
("n","[figurative-wrong] 'night of fog and questioning', mental confusion"),
],
"snow_ice_words": [
("y","[literal] icy glittering peaks"),("y","[literal] melted snow"),("y","[literal] rain and snow"),
("n","[figurative-wrong] 'blighting frosts' on thin locks = age"),("y","[literal] icy northern seas"),
("y","[literal] frost on the mountains"),("y","[literal] frosty starlight"),
("n","[idiom] 'pure as snow'"),("n","[figurative-wrong] 'icy civility'"),
("y","[literal] snowy foil under red berries"),("y","[literal] this snow, outside"),
("f","[figurative-right] icicles combed from Spring's hair, season personified"),
("y","[literal] icy grass after a frost"),("y","[literal] a rapid thaw"),
("y","[literal] two nights in the snow"),("y","[literal] country without snow, sledges"),
("y","[literal] icy spray in a gale"),("y","[literal] snow squalls"),("y","[literal] heavy snows"),
("y","[literal] snow-blind from glare"),("y","[literal] icy oak, winter woods"),
("y","[literal] snow-drifts"),("n","[name] surname: Colonel Rutherford Snow"),
("y","[literal] snow in the crevices of the bank"),
],
"sun_words": [
("y","[literal] a genial sun, climate"),("f","[figurative-right] gleam of sunshine lighting a dark dell"),
("y","[literal] sunny braes"),("y","[literal] 'my own sunny clime'"),
("y","[literal] sun-lit waves"),("n","[figurative-wrong] 'heart into the sunlight' = mood"),
("y","[literal] sunbeams through foliage"),("y","[literal] stream of sunshine from the window"),
("y","[literal] sun getting low"),("y","[literal] staring into the sunshine"),
("y","[literal] shadow black in the sunshine"),("y","[literal] sunny afternoon"),
("y","[literal] sun sinking behind a cloud-bank"),("y","[literal] death walking in the sunlight"),
("y","[literal] standing in sunlight"),("y","[literal] long sunny days"),
("n","[name] the Sun Dance, a ceremony"),("y","[literal] revolver flashed in the sunlight"),
("y","[literal] bar of sunlight"),("y","[literal] 'too sunny on this side'"),
("n","[name] the Sun, a newspaper"),("y","[literal] sunshine on brown wood"),
("y","[literal] sunlight shut out by a sandstorm"),
("n","[idiom] 'work right in the sunshine' = openly"),
],
"cloud_words": [
("n","[figurative-wrong] 'clouded every enjoyment'"),("y","[literal] heavens cloudless"),
("n","[figurative-wrong] 'brow was overcast' = anger"),("y","[literal] cloudless blue sky"),
("n","[other-sense] steam and smoke 'mimic cloud-region'"),("y","[literal] bright, cloudless day"),
("n","[figurative-wrong] countenance 'overcast' = mood"),
("n","[figurative-wrong] 'cloudless pleasure' of eyes"),
("n","[idiom] 'under a cloud' = in disgrace"),("y","[literal] cloudless day"),
("y","[literal] cloudless sky of deep blue"),("y","[literal] sky overcast with flying clouds"),
("y","[literal] moon breaking from the clouds"),("y","[literal] cloudless splendor after the storm"),
("y","[literal] cloudless August day"),("y","[literal] cloudless skies of the Nile"),
("n","[other-sense] 'cloud of water' from a blast"),("y","[literal] cloudless golden light"),
("y","[literal] cloudless blue of the heavens"),("n","[other-sense] painted clouds on a fan"),
("n","[other-sense] 'clouds of large birds'"),("y","[literal] sky cloudless, no moon"),
("y","[literal] tropically perfect cloudless sky"),("n","[other-sense] 'cloudy' blue eyes of puppies"),
],
}

out = {}
rows = []
for k, js in J.items():
    items = S[k]["items"]
    assert len(items) == len(js), (k, len(items), len(js))
    oi = []
    for it, (c, why) in zip(items, js):
        ok = c in ("y", "f")
        oi.append(dict(doc_id=it["doc_id"], term=it["term"], quote=it["quote"], correct=ok, reason=why))
        rows.append((k, it["cohort"], it["term"], c, it["doc_id"]))
    nc = sum(i["correct"] for i in oi)
    out[k] = dict(items=oi, precision=round(nc / len(oi), 4), n_checked=len(oi), n_correct=nc)
json.dump(out, open("text_validation.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

def fam(t):
    for stem, f in [("thunder","thunder"),("lightning","lightning"),("hurricane","hurricane"),("squall","squall"),("tempest","tempest"),
                    ("storm","storm"),("rain","rain"),("shower","shower"),("sleet","sleet"),("breez","breeze"),("gale","gale"),("gust","gust"),("zephyr","zephyr"),
                    ("wind","wind"),("fog","fog"),("mist","mist"),("haze","haze"),("hazy","haze"),("hailstone","hail"),("snow","snow"),("frost","frost"),("icy","icy"),("icicle","icicle"),("thaw","thaw"),
                    ("sun","sun"),("cloud","cloud"),("overcast","overcast")]:
        if t.startswith(stem):
            return f
    return t

def tab(keyf, label):
    d = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        k = keyf(r)
        d[k][0] += 1
        d[k][1] += r[3] in "yf"
        d[k][2] += r[3] == "y"
    print("##", label)
    for k in sorted(d):
        n, c, s = d[k]
        print(f"{k}\t{c}/{n}\t{c/n:.3f}\tstrict {s/n:.3f}")

tab(lambda r: r[0], "measure")
tab(lambda r: r[1], "cohort (all items)")
tab(lambda r: ("all",), "overall")
tab(lambda r: fam(r[2]), "term family")
# terms not in weather_all duplicates: overlap exists, so term tab pools all 198 items
tab(lambda r: (fam(r[2]), r[1]), "family x cohort")
tab(lambda r: r[2], "exact term")

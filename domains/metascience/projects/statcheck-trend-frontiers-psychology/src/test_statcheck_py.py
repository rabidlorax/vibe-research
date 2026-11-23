"""Hand-computed checks of the extractor and the consistency rule.
Run: python src/test_statcheck_py.py"""
from statcheck_py import extract, normalize


def one(s):
    r = list(extract(normalize(s)))
    assert len(r) == 1, (s, r)
    return r[0]


def none(s):
    assert list(extract(normalize(s))) == [], s


# t(28) = 2.20 -> two-tailed p = .0363
r = one("we found t(28) = 2.20, p = .04 here"); assert not r["error"] and abs((r["p_min"] + r["p_max"]) / 2 - .0363) < .001
r = one("t(28) = 2.20, p = .03"); assert r["error"] and not r["decision_error"]
r = one("t(28) = 2.20, p < .05"); assert not r["error"]
r = one("t(28) = 2.20, p < .01"); assert r["error"] and not r["decision_error"]
r = one("t(28) = 1.20, p < .05"); assert r["error"] and r["decision_error"]      # p = .24
r = one("t(28) = 2.20, p = .20"); assert r["error"] and r["decision_error"]
r = one("t(28) = 2.20, p > .05"); assert r["error"] and r["decision_error"]
# unicode minus, thin spaces, p with leading zero
r = one("t(28) = −2.20, p = 0.036"); assert not r["error"] and r["stat"] == "-2.20"
# rounding of the statistic: t(10) = 2.2 could be 2.15..2.25 -> p .0481...0569
r = one("t(10) = 2.2, p = .05"); assert not r["error"]
r = one("t(10) = 2.2, p = .06"); assert not r["error"]
r = one("t(10) = 2.2, p = .07"); assert r["error"]
# one-tailed: t(28) = 1.80 two-tailed .083, one-tailed .041
r = one("t(28) = 1.80, p = .04"); assert r["error"] and r["error_1t"] and r["decision_error"]
r = one("A one-tailed test gave t(28) = 1.80, p = .04"); assert r["error"] and not r["error_1t"] and not r["decision_error_1t"]
# F(2, 30) = 3.50 -> p = .0430 ; F(1, 30) = 4.00 -> .0546
r = one("F(2, 30) = 3.50, p = .043"); assert not r["error"]
r = one("F(1,30) = 4.00; p < 0.05"); assert r["error"] and r["decision_error"]
r = one("F(1.83, 54.9) = 3.50, p = .04"); assert not r["error"]
# chi-square(1) = 3.84 -> .0500 ; chi2(2, N = 120) = 10.00 -> .0067
r = one("χ2(1) = 3.84, p = .05"); assert not r["error"]
r = one("χ2 (2, N = 120) = 10.00, p = .007"); assert not r["error"] and r["kind"] == "chi2"
r = one("X2(2) = 10.00, p = .07"); assert r["error"] and r["decision_error"]
# r(48) = .30 -> p = .034
r = one("r(48) = .30, p = .034"); assert not r["error"]
r = one("r(48) = -0.30, p < .01"); assert r["error"]
# z = 1.96 -> .0500 ; Z = 2.58 -> .0099
r = one("z = 1.96, p = .05"); assert not r["error"]
r = one("Z = 2.58, p = 0.01"); assert not r["error"]
r = one("z = 1.00, p = .03"); assert r["error"] and r["decision_error"]
# p = .000 is read as "rounds to zero at three decimals"
r = one("t(50) = 6.00, p = .000"); assert not r["error"] and r["p_zero"]
r = one("t(50) = 2.00, p = .000"); assert r["error"]
# things that must not be extracted
none("Yt(28) = 2.20, p = .03"); none("t(28) = 2.20, d = 0.4, p = .03"); none("t(28) < 1, p = .5")
none("t(28) = 2.20, p = 3.1 × 10-5"); none("t(28) = 2.20, p = .03.4"); none("r(48) = 3.0, p = .03")
none("t(76) = -3.99, p = 1.00E-04"); none("t(18) = 7.04, p = 1.00 * 10-6")
# sentence-ending full stop after the p-value is accepted; ".05/3" and "0.31 · 10-3" are not
r = one("F(1, 30) = 4.50, p = .04."); assert not r["error"]
r = one("t(28) = 2.20, p = .036. Next sentence"); assert not r["error"]
none("t(28) = 2.20, p < .05/3"); none("t(28) = 5.20, p = 0.31 · 10-3"); none("t(28) = 2.20, p < .000")
none("t(0.097) = -2.734, p < .01"); none("Cohen's d-z = 0.50, p = .04")
# "directional" triggers the statcheck allowance but not the strict one
r = one("A bidirectional link. t(28) = 1.80, p = .04"); assert not r["error_1t"] and r["error_1t_strict"] and r["half_p_consistent"]
none("Wald z-score: Wz = 2.0, p = .04"); none("t(28) = 2.20, ns")
print("all tests passed")

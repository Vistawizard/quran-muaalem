from quran_muaalem.app.serve import pick_search_result
from quran_muaalem.app.types import PhonemesSearchSpanApp, SearchResultResponse


def span(sura, aya):
    return PhonemesSearchSpanApp(
        sura_idx=sura, aya_idx=aya, uthmani_word_idx=0, uthmani_char_idx=0, phonemes_idx=0
    )


def result(sura, aya_start, aya_end, end_sura=None):
    return SearchResultResponse(
        start=span(sura, aya_start), end=span(end_sura or sura, aya_end), uthmani_text=""
    )


def test_no_hint_keeps_best():
    results = [result(1, 1, 1), result(1, 3, 3)]
    assert pick_search_result(results, None, None) is results[0]


def test_hint_picks_covering_result():
    results = [result(1, 1, 1), result(1, 3, 3)]
    assert pick_search_result(results, 1, 3) is results[1]


def test_hint_inside_multi_aya_span():
    results = [result(2, 1, 1), result(2, 2, 4)]
    assert pick_search_result(results, 2, 3) is results[1]


def test_unmatched_hint_falls_back():
    results = [result(1, 1, 1)]
    assert pick_search_result(results, 2, 255) is results[0]


def test_hint_across_sura_boundary():
    results = [result(3, 1, 1), result(1, 7, 1, end_sura=2)]
    assert pick_search_result(results, 1, 7) is results[1]
    assert pick_search_result(results, 2, 1) is results[1]

from pathlib import Path
import re
import requests

def check_validity(link, readme)->bool:
    try:
        response = requests.head(link, allow_redirects=True)
        if response.status_code != 200:
            print(f'Invalid link: {link} in {readme} (Status code: {response.status_code})')
            return False
        else:
            return True
    except requests.RequestException as e:
        print(f'Error checking link: {link} in {readme} ({e})')
        return False

def main():
    link_pattern = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')

    root_dir = Path(__file__).resolve().parent.parent
    for subdir in root_dir.iterdir():
        if subdir.is_file() or not (subdir / 'readme.md').is_file():
            continue
        print("-" * 20+ f" {subdir.name} " + "-" * 20)
        readme = subdir / 'readme.md'
        content = readme.read_text(encoding='utf-8')
        links = link_pattern.findall(content)
        for link in links:
            check_validity(link, readme)

if __name__ == '__main__':
    main()

"""
-------------------- 20210225_BlenderPotatoChips --------------------
-------------------- 20210322_BlenderMaze --------------------
-------------------- 20210423_AHC001 --------------------
-------------------- 20210708_CADDi2019Visualizer --------------------
-------------------- 20210826_GenomeContestVisualizer --------------------
-------------------- 20220330_UmetaniHeuristic --------------------
Invalid link: https://www.amazon.co.jp/%E3%81%97%E3%81%A3%E3%81%8B%E3%82%8A%E5%AD%A6%E3%81%B6%E6%95%B0%E7%90%86%E6%9C%80%E9%81%A9%E5%8C%96-%E3%83%A2%E3%83%87%E3%83%AB%E3%81%8B%E3%82%89%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0%E3%81%BE%E3%81%A7-KS%E6%83%85%E5%A0%B1%E7%A7%91%E5%AD%A6%E5%B0%82%E9%96%80%E6%9B%B8-%E6%A2%85%E8%B0%B7-%E4%BF%8A%E6%B2%BB/dp/4065212707 in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 405)
Error checking link: http://coop-math.ism.ac.jp/files/4/umetani.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPConnectionPool(host='coop-math.ism.ac.jp', port=80): Max retries exceeded with url: /files/4/umetani.pdf (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x000001358D783380>: Failed to resolve 'coop-math.ism.ac.jp' ([Errno 11001] getaddrinfo failed)")))
Error checking link: http://www.orsj.or.jp/archive2/or59-10/or59_10_615.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPConnectionPool(host='www.orsj.or.jp', port=80): Max retries exceeded with url: /archive2/or59-10/or59_10_615.pdf (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001358D751F90>, 'Connection to www.orsj.or.jp timed out. (connect timeout=None)')))
Error checking link: https://www.orsj.or.jp/~archive/pdf/bul/Vol.50_05_335.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPSConnectionPool(host='www.orsj.or.jp', port=443): Max retries exceeded with url: /~archive/pdf/bul/Vol.50_05_335.pdf (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x000001358D7525D0>, 'Connection to www.orsj.or.jp timed out. (connect timeout=None)')))
Invalid link: https://www-or.amp.i.kyoto-u.ac.jp/members/yagiura/papers/tabu-kaisetsu-2008.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 404)
Error checking link: http://www.orsj.or.jp/archive2/or58-12/or58_12_695.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPConnectionPool(host='www.orsj.or.jp', port=80): Max retries exceeded with url: /archive2/or58-12/or58_12_695.pdf (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001358D751810>, 'Connection to www.orsj.or.jp timed out. (connect timeout=None)')))
Invalid link: https://www.keyence.co.jp/ss/general/iot-glossary/heuristic.jsp in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 400)
Invalid link: https://www-or.amp.i.kyoto-u.ac.jp/members/yagiura/papers/tabu-kaisetsu-2008.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 404)
Error checking link: http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=79D883C1455A0D775D781C658F770C2C?doi=10.1.1.170.689&rep=rep1&type=pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPSConnectionPool(host='citeseerx.ist.psu.edu', port=443): Max retries exceeded with url: /viewdoc/download;jsessionid=79D883C1455A0D775D781C658F770C2C?doi=10.1.1.170.689&rep=rep1&type=pdf (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1028)'))))
Invalid link: https://slideplayer.com/slide/14171683/ in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 504)
Invalid link: https://a3a6340e-a-62cb3a1a-s-sites.googlegroups.com/site/shunjiumetani/file/tsp_slide.pdf?attachauth=ANoY7cpgqG5hhus3TMXP1wPGetevlrC4QQkwd5C5DSJWMF5btSFIoXpdxyAeEaox4xfeSd2ePi30Hcf8MLpmXUWSmRV52tSSAzHqmYRJWwUidSoN8mrxqYgYGRWPpIO1o9bA41eQ5zBhd2PpOrWMx2oWmNU2It_lEeM7ACy7Md213POPZ88goYNDymhE3quLrpeZk5Go8NLinf0AlALIID2R8OhK5Wi-FD2f9VMiwpZRHl7biYogjEk%3D&attredirects=0 in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 400)
Error checking link: http://www.orsj.or.jp/archive2/or58-12/or58_12_703.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPConnectionPool(host='www.orsj.or.jp', port=80): Max retries exceeded with url: /archive2/or58-12/or58_12_703.pdf (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001358D72B490>, 'Connection to www.orsj.or.jp timed out. (connect timeout=None)')))
Invalid link: https://doi.org/10.1016/S0377-2217(98 in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 404)
Invalid link: https://a3a6340e-a-62cb3a1a-s-sites.googlegroups.com/site/shunjiumetani/file/tsp_slide.pdf?attachauth=ANoY7cpgqG5hhus3TMXP1wPGetevlrC4QQkwd5C5DSJWMF5btSFIoXpdxyAeEaox4xfeSd2ePi30Hcf8MLpmXUWSmRV52tSSAzHqmYRJWwUidSoN8mrxqYgYGRWPpIO1o9bA41eQ5zBhd2PpOrWMx2oWmNU2It_lEeM7ACy7Md213POPZ88goYNDymhE3quLrpeZk5Go8NLinf0AlALIID2R8OhK5Wi-FD2f9VMiwpZRHl7biYogjEk%3D&attredirects=0 in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 400)
Invalid link: https://www.researchgate.net/publication/227419264_An_integrated_hybrid_approach_to_the_examination_timetabling_problem in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 403)
Error checking link: https://www.orsj.or.jp/~archive/pdf/bul/Vol.50_05_335.pdf in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPSConnectionPool(host='www.orsj.or.jp', port=443): Max retries exceeded with url: /~archive/pdf/bul/Vol.50_05_335.pdf (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x000001358D753390>, 'Connection to www.orsj.or.jp timed out. (connect timeout=None)')))
Invalid link: https://a3a6340e-a-62cb3a1a-s-sites.googlegroups.com/site/shunjiumetani/file/2dspp_slide.pdf?attachauth=ANoY7coLYixz3-u_bcQ32cAQlCdigwe8wRRRwJIkHbj-hs-T_m8OD0tgUw-2IVaJFjzplpCMXpdP8B4_rxsWTbXXsC_40kRnRbM2gLAtP4mx_yx-stqp34Yi27BpkdtLccjeMzPab9MkRVL2Fcww3xWj72sro_XBfEy3pb3S10x_E4OZ5B3oeBYrQ_mQ3yJSpXudQhpJKtpvry26P1UwcbNJgzAVMcQK2tPvwwry0s999ovi-Aa00EI%3D&attredirects=0 in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 400)
Error checking link: https://gym.openai.com/ in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (HTTPSConnectionPool(host='gym.openai.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'gym.openai.com'. (_ssl.c:1028)"))))
Invalid link: https://colab.research.google.com/github/jeffheaton/t81_558_deep_learning/blob/master/t81_558_class_12_01_ai_gym.ipynb in C:\Users\hirok\Documents\QiitaArticles\20220330_UmetaniHeuristic\readme.md (Status code: 405)
-------------------- 20220906_ICFPC2022 --------------------
-------------------- 20221003_AHC014 --------------------
Invalid link: https://twitter.com/bowwowforeach/status/1576151587126640641 in C:\Users\hirok\Documents\QiitaArticles\20221003_AHC014\readme.md (Status code: 403)
Invalid link: https://twitter.com/fuppy_kyopro/status/1576161955265794049 in C:\Users\hirok\Documents\QiitaArticles\20221003_AHC014\readme.md (Status code: 403)
Invalid link: https://tc-wleite.github.io/ahc014.html in C:\Users\hirok\Documents\QiitaArticles\20221003_AHC014\readme.md (Status code: 404)
-------------------- 20221210_WatanabeConjecture --------------------
-------------------- 20230113_JavaScriptTrivia --------------------
Invalid link: https://twitter.com/chokudai/status/1595634980012847104 in C:\Users\hirok\Documents\QiitaArticles\20230113_JavaScriptTrivia\readme.md (Status code: 403)
-------------------- 20230326_TOYOTA2023Spring --------------------
Invalid link: https://twitter.com/iaNTU_ in C:\Users\hirok\Documents\QiitaArticles\20230326_TOYOTA2023Spring\readme.md (Status code: 403)
Invalid link: https://twitter.com/kuruton456/status/1636961287916896256 in C:\Users\hirok\Documents\QiitaArticles\20230326_TOYOTA2023Spring\readme.md (Status code: 403)
-------------------- 20231218_RoM --------------------
Invalid link: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.118.090501 in C:\Users\hirok\Documents\QiitaArticles\20231218_RoM\readme.md (Status code: 403)
Invalid link: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.115.070501 in C:\Users\hirok\Documents\QiitaArticles\20231218_RoM\readme.md (Status code: 403)
Invalid link: https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.2.010307 in C:\Users\hirok\Documents\QiitaArticles\20231218_RoM\readme.md (Status code: 403)
-------------------- 20240220_AHC030 --------------------
-------------------- 20240822_LaTeXColorReproduction --------------------
-------------------- 20240927_ConvexIsNotContinuous --------------------
Invalid link: https://creativecommons.org/licenses/by-sa/4.0&gt in C:\Users\hirok\Documents\QiitaArticles\20240927_ConvexIsNotContinuous\readme.md (Status code: 404)
-------------------- 20241213_ChangeMakingProblem --------------------
-------------------- 20250211_BaseOfProximalGradient --------------------
Invalid link: https://ja.wikipedia.org/wiki/%E3%82%A8%E3%83%94%E3%82%B0%E3%83%A9%E3%83%95_(%E6%95%B0%E5%AD%A6 in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 404)
Invalid link: https://ja.wikipedia.org/wiki/%E5%8B%BE%E9%85%8D_(%E3%83%99%E3%82%AF%E3%83%88%E3%83%AB%E8%A7%A3%E6%9E%90 in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 404)
Invalid link: https://en.wikipedia.org/wiki/Duality_(optimization in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 404)
Invalid link: https://www.researchgate.net/publication/279825155_Long_term_motion_analysis_for_object_level_grouping_and_nonsmooth_optimization_methods in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 403)
Invalid link: https://doi.org/10.1137/070687542 in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 403)
Invalid link: https://doi.org/10.1137/1.9781611974997 in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 403)
Invalid link: https://www.researchgate.net/figure/llustration-of-the-Moreau-envelope-f-l-f-2_fig1_381158237 in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 403)
Invalid link: https://www.researchgate.net/publication/345481682_4_Algorithms_for_Convex_Optimization in C:\Users\hirok\Documents\QiitaArticles\20250211_BaseOfProximalGradient\readme.md (Status code: 403)
-------------------- 20250501_IsotonicRegression --------------------
Invalid link: https://upload.wikimedia.org/wikipedia/commons/8/8c/Dose_response_curve_stimulation.jpg in C:\Users\hirok\Documents\QiitaArticles\20250501_IsotonicRegression\readme.md (Status code: 403)
Invalid link: https://doi.org/10.1080%2F19466315.2017.1286256 in C:\Users\hirok\Documents\QiitaArticles\20250501_IsotonicRegression\readme.md (Status code: 403)
-------------------- 20250528_LWMagicComment --------------------
-------------------- 20250603_MathEnglish --------------------
Invalid link: https://dictionary.cambridge.org/dictionary/english/scalar in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/vector in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/matrix in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/german-english/eigen in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/algebra in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/finite in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/infinite in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/infinite in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/annihilate in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://x.com/Keyneqq/status/1037263459514114048 in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/algorithm in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/anti in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/chaos in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/column in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/corollary in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/gradient in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/hull in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/image in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/pseudo in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/relative in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/remainder in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/secant in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/suffices in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/tensor in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/dimension in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/quasi in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://www.oed.com/dictionary/hermitian_adj in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/Poisson in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/Gaussian in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/Wolfram in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://en.wikipedia.org/wiki/Philip_Wolfe_(mathematician in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 404)
Invalid link: https://dictionary.cambridge.org/dictionary/english/wood in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/woman in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://www.wolframalpha.com/ in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 404)
Invalid link: https://forvo.com/search/Barzilai in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/reciprocal in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://ja.wikipedia.org/wiki/%E5%B0%84_(%E5%9C%8F%E8%AB%96 in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 404)
Invalid link: https://dictionary.cambridge.org/dictionary/english/radii in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://x.com/tenseiYN99/status/1925438036420304931 in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://dictionary.cambridge.org/dictionary/english/equal#google_vignette in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Sekai-no-gengo.png/1200px-Sekai-no-gengo.png?20081022180809 in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://academic.oup.com/imajna/article-abstract/8/1/141/802460 in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
Invalid link: https://academic.oup.com/imajna/article-abstract/13/3/321/703847?redirectedFrom=fulltext in C:\Users\hirok\Documents\QiitaArticles\20250603_MathEnglish\readme.md (Status code: 403)
-------------------- 202599999_CheckLinks --------------------
"""
"""ko_re: regex for Korean & Free from ord/chr in Hangeul analysis.

ADD 
TODO: 주석이나 re.X 고려하기

unicode order: 
ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ
ㅤㅥㅦㅧㅨㅩㅪㅫㅬㅭㅮㅯㅰㅱㅲㅳㅴㅵㅶㅷㅸㅹㅺㅻㅼㅽㅾㅿㆀㆁㆂㆃㆄㆅㆆㆇㆈㆉㆊㆋㆌㆍㆎ

초성 - first consonant letter 중성 - middle vowel letter 종성 - last consonant letter

규칙:
1. kor_re가 처리하는 항목은 [초성:중성]('가'같은 종성이 없는 글자의 경우) 또는 [초성:중성:종성]형식으로 한다.
    초성, 중성에는 모든 가능한 한 글자 조합과 0, 처음에는 ^, 그리고 .만 들어갈 수 있다.
    이외에는 일반적은 regex 구문으로 처리되고, 만약 해당 글자 조합을 만족한다면 kor_re의 문법으로 처리된다.
2. 만약 모든 것을 일치시키고 싶다면 해당 칸을 비우거나(파이썬 스타일) .을 입력(regex 스타일)한다. 두 스타일은 모두 적합하며 우열이 없다.
    하지만 섞어서 사용하는 것은 권장하지 않는다.
    예) [ㄱ:]/[ㄱ:.]: 앞글자가 ㄱ인 글자들. 이때 중성은 상관하지 않음.(=[가개갸걔거게겨계고과괘괴교구궈궤귀규그긔기])
    예2) [::ㅎ]/[.:.:ㅎ]: 종성이 ㅎ인 모든 글자. ([:.:ㄴㅇㅎ]도 가능하지만 권장하지 않는다.)
3. regex의 []구문처럼 글자를 이어서 적거나 '-'를 이용해서 작성할 수 있다.
    주의! '-'를 이용해서 연속된 문자열을 작성할 때 된소리를 유의해야 한다. 예를 들어 'ㄱ-ㄹ'은 'ㄱㄴㄷㄹ'가 아닌 'ㄱㄲㄴㄷㄸㄹ'이다.
    예) [ㄱㅎㄹ:ㅏㅓ]: 초성이 ㄱ 또는 ㅎ,ㄹ이고 중성이 ㅏ,ㅓ인 글자(=[가하라거허러])
    예2) [ㄱ-ㄹ:ㅏ]: 초성이 ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ이고 중성이 ㅏ인 글자.
4. 조합 문자는 된소리를 제외하고 ()를 이용해 표기할 수 있다.
    예) [ㄱ:ㅏ(ㅗㅏ):(ㄴㅎ)(ㄹㅂ)]: 초성이 ㄱ이고 중성이 ㅏ 또는 ㅘ이며, 종성이 ㄶ이거나 ㄼ인 문자를 의미한다.
                                    [ㄱ:ㅏㅘ:ㄶㄼ]과 완전히 동일하다.
5. 각각 맨 앞에 ^를 사용하면 그것을 제외한 문자라는 의미가 된다. 이때 ^의 범위는 한글로 한정한다.
    예) [^ㄱㄴ:ㅏ:^ㄱ-ㅂ]: 초성이 ㄱ이나 ㄴ이 아니고 중성은 ㅏ이며 종성은 ㄱ~ㅂ이 아닌 문자를 의미한다.
6. 0을 입력할 경우 그 자리에 음소가 없다는 것을 의미한다.
    예) [ㄱ:ㅏ:ㄴ0]: '간' 또는 '가'를 의미한다.
    예2) [0:ㅏ-ㅓ:0]: [ㅏㅑㅓ]를 의미한다.
    예3) [:0]: [ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ]를 의미한다.
    주의! [0:0:0], [0:*:*], [*:0:*]은 정의되지 않는다.(*는 0이 아닌 적합한 문자를 의미함.)
    주의! 초성과 중성의 0은 혼자만 사용할 수 있다. 초성과 중성에 0과 다른 것들이 들어간다면(^ 포함) 오류가 발생한다.
    참고표:
        [*:*:*0] > 일반적인 처리
        [*:0:*] > X
        [*:0:0] > CHOSUNG
        [0:*:*] > X
        [0:*:0] > JUNGSUNG
        [0:0:*] > JONGSUNG
        [0:0:0] > X
"""
import re

CHOSUNG = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ' 
CHOSUNG_WITH_ZERO = '0ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
JUNGSUNG = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
JUNGSUNG_WITH_ZERO = '0ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
JONGSUNG = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
JONGSUNG_WITH_ZERO = '0ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ' # zero stands for no final consonant

def change_order(order):
    global CHOSUNG, CHOSUNG_WITH_ZERO, JUNGSUNG, JUNGSUNG_WITH_ZERO, JONGSUNG, JONGSUNG_WITH_ZERO
    if order == 'default':
        CHOSUNG = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ' 
        CHOSUNG_WITH_ZERO = '0ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
        JUNGSUNG = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
        JUNGSUNG_WITH_ZERO = '0ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
        JONGSUNG = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
        JONGSUNG_WITH_ZERO = '0ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
    if order == 'regular_first':
        CHOSUNG = 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉ' 
        CHOSUNG_WITH_ZERO = '0ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉ'
        JUNGSUNG = 'ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖㅘㅙㅚㅝㅞㅟㅢ'
        JUNGSUNG_WITH_ZERO = '0ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖㅘㅙㅚㅝㅞㅟㅢ'
        JONGSUNG = 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄳㄵㄶㄺㄻㄼㄽㄾㄿㅀㅄㅆ'
        JONGSUNG_WITH_ZERO = '0ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄳㄵㄶㄺㄻㄼㄽㄾㄿㅀㅄㅆ'

def _subtitude(match):
    """Subtitude mathched ko_re-specific grammars."""
    def sub_nested(string):
        return (
            string
            .replace('(ㅗㅏ)', 'ㅘ')
            .replace('(ㅗㅐ)', 'ㅙ')
            .replace('(ㅗㅣ)', 'ㅚ')
            .replace('(ㅜㅓ)', 'ㅝ')
            .replace('(ㅜㅔ)', 'ㅞ')
            .replace('(ㅜㅓ)', 'ㅟ')
            .replace('(ㅡㅣ)', 'ㅢ')
            .replace('(ㄱㅅ)', 'ㄳ')
            .replace('(ㄴㅈ)', 'ㄵ')
            .replace('(ㄴㅎ)', 'ㄶ')
            .replace('(ㄹㄱ)', 'ㄺ')
            .replace('(ㄹㅁ)', 'ㄻ')
            .replace('(ㄹㅂ)', 'ㄼ')
            .replace('(ㄹㅅ)', 'ㄽ')
            .replace('(ㄹㅌ)', 'ㄾ')
            .replace('(ㄹㅎ)', 'ㅀ')
            .replace('(ㅂㅅ)', 'ㅄ')
        )
    # print(sub_nested('(ㅗㅏ)'))

    def sub_hyphen(types: str):
        def word_type_dependent(match: re.Match):
            pre, pro = match.group(1), match.group(2)
            string = ''
            assert types.index(pre) <= types.index(pro), f'bad character range {pre}-{pro}.'
            for i in range(types.index(pre), types.index(pro) + 1):
                string += types[i]
            return string
        return word_type_dependent

    def inverse(string, inverse_range):
        inverse_set = set(string)
        inverse_range = set(inverse_range)
        return ''.join(sorted(list(inverse_range - inverse_set)))
    
    # print('!', inverse('ㄱㄲ', CHOSUNG))

    def makeassert(string, assert_range):
        """반복을 제거하고 assert_range안에 포함되어 있는지 확인하며 정렬한다."""
        string_set = set(string)
        assert_set = set(assert_range)
        assert string_set <= assert_set, 'assert_set에서 포함하지 않는 string이 있음.'
        return ''.join(sorted(list(string_set)))

    def combile_hangeul(first, middle, last):
        return chr(0xAC00 + 588 * CHOSUNG.index(first) + 28 * JUNGSUNG.index(middle) + JONGSUNG_WITH_ZERO.index(last))

    first, middle, last = match.group(1), match.group(2), match.group(3)

    # .일 경우 .을 빈칸으로 만듦.
    first = first if not first == '.' else ''
    middle = middle if not middle == '.' else ''
    last = last if not last == '.' else ''

    first, middle, last = sub_nested(first), sub_nested(middle), sub_nested(last)

    # 범위문을 해결(ㄱ-ㄹ > ㄱㄲㄴㄷㄸㄹ)
    first = re.sub('(.)-(.)', sub_hyphen(CHOSUNG_WITH_ZERO), first)
    middle = re.sub('(.)-(.)', sub_hyphen(JUNGSUNG_WITH_ZERO), middle)
    last = re.sub('(.)-(.)', sub_hyphen(JONGSUNG_WITH_ZERO), last)

    # 0이 first나 middle에서 혼자 쓰였는지 확인
    if '0' in first:
        assert first == '0', '0 in first consonant letter only can used alone.'
    if '0' in middle:
        assert middle == '0', '0 in middle vowel letter only can used alone.'


    # [0:~]이나 [~:0:~]을 해결
    # to test: [0:^ㅣ:0], [0:ㅓㅐ:0]
    if first == '0':
        assert middle != '0' or last != '0', 'invaild case([0:0:0]), cannot compose this case.'
        assert not (middle != '0' and last != '0'), 'invaild case([0:*:*]), cannot compose this case.'

        if middle != '0':
            if middle == '':
                return f'[{JUNGSUNG}]'
            if middle[0] == '^':
                return f'[{inverse(middle, JUNGSUNG)}]'
            return f'[{makeassert(middle, JUNGSUNG)}]'
    else:
        if middle == '0':
            assert last == '0', 'invaild case([*:0:*]), cannot compose this case.'

            if first == '':
                return f'[{CHOSUNG}]'
            if first[0] == '^':
                return f'[{inverse(first, CHOSUNG)}]'
            return f'[{makeassert(first, CHOSUNG)}]'
    
    # 일반 구문([*:*:*0]) 분석
    if '^' if first == '' else first[0] == '^':
        first = inverse(first, CHOSUNG)
    if '^' if middle == '' else middle[0] == '^':
        middle = inverse(middle, JUNGSUNG)
    if '^' if last == '' else last[0] == '^':
        last = inverse(last, JONGSUNG_WITH_ZERO) # with_zero로 할지 아니면 그냥으로 할지 결정하기

    return_value = ''
    for first_one in makeassert(first, CHOSUNG):
        for middle_one in makeassert(middle, JUNGSUNG):
            for last_one in makeassert(last, JONGSUNG_WITH_ZERO):
                # print(first_one, middle_one, last_one)
                return_value += combile_hangeul(first_one, middle_one, last_one)

    # print(first, middle, last, sep='/')
    # return f'[{first}:{middle}:{last}]'
    return f'[{return_value}]'

def compilestr(pattern):
    """Make string to complied."""
    # Replace things like "[ㄱ:ㅣ-ㅗ]" to "[ㄱ:ㅣ-ㅗ:0]".
    pattern = re.sub(r'\[([0ㄱ-ㅎ()^-]*|\.*:[0ㅏ-ㅣ.()^-]*)\]', '[\g<1>:0]', pattern)
    # Replace things like "[ㄱ:ㅣ-ㅗ:0]" to [가개걔거게겨계고], MAIN WORKER
    pattern = re.sub(r'\[([0ㄱ-ㅎ()^-]*|\.*):([0ㅏ-ㅣ.()^-]*):([ㄱ-ㅎ0.()^-]*)\]', _subtitude, pattern)
    return pattern # Compile by re and return.

def compile(pattern, flags=0):
    """Complie ko_re by re."""
    return re.compile(compilestr(pattern), flags)
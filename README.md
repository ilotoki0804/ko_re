# korean-regex: regex for Korean - Being free from ord/chr in Hangeul analysis.

## 소개

korean-regex는 한국어(한글)을 분석하기 위해 regex(정규표현식)에 문법을 추가한 패키지입니다. korean-regex로는 한글과 관련한 많은 추가 기능을 사용할 수 있습니다.

```python
import ko_re
regex = ko_re.compile(r'\b[^ ]+(?=[::^0]).\b')
print(regex.findall('ko_re는 한국어(한글)을 분석하기 위해 regex(정규표현식)에 문법을 추가한 패키지입니다. ko_re로는 한글과 관련한 많은 추가 기능을 사용할 수 있습니다.')) # ['ko_re는', '한국어(한글)을', 'regex(정규표현식', '문법을', '추가한', 'ko_re로는', '관련한', '많은', '기능을', '사용할']
```

## 설치

korean-regex는 pip를 통해 설치하실 수 있습니다. ko_re를 설치하는 것이 **아닌** korean_regex를 설치해야 한다는 점에 주의하세요.

```python
pip install -U korean_regex
```

## 상세

기본적으로 korean-regex는 bracket expression에서 특정한 조건을 발생시켰을 때 작동하는 추가적인 기능을 가미한 것입니다. 해당 조건을 제외한 나머지 상황에서는 파이썬의 기본 re 라이브러리와 동작이 완전히 같습니다.

우선 korean-regex를 불러오려면 ko_re.compile()을 사용합니다. korean-regex는 현재로선 compile만 지원합니다. 나머지는 compile로 re 객체를 만든 뒤 사용하세요.

korean-regex에서 처리되는 구문은 다음과 같습니다: `[초성:중성]`(`가`와 같은 종성이 없는 글자의 경우) 또는 `[초성:중성:종성]`, 또한 이는 regex의 bracket expression처럼 글자를 죽 이어서 쓰거나 `-`을 처리하는 것으로 여러 음소(소리의 최소 단위로, 자음과 모음을 의미합니다.)를 선택합니다.

예를 들어 `[ㄱㄴ:ㅏ]`는 regex구문에서 `[가나]`를 의미하고, `[ㄹㅎ:ㅗ:ㄶㅈ]`은 `[롢롲혾홎]`을 의미합니다. 또한 `[ㄱ-ㄹ:ㅏ]`는 `[가까나다따라]`를 의미합니다(`[가나다라]`가 아님에 주의하세요!).

```python
# 예시 코드
import ko_re
some_regex = ko_re.compile('[ㄱㄴ:ㅏㅓㅣ:ㄶㄷㄹㅊ]')
print(some_regex) # re.compile('[갆갇갈갗걶걷걸겇긶긷길깇낞낟날낯넎넏널넟닎닏닐닟]')
print(some_regex.findall('길을 걷는 사람을 보았다. 그는 날 볼 낯이 없어서 멀리멀리 떠났다.')) # ['길', '걷', '날', '낯']
```

또한 regex구문처럼 `^`도 지원합니다. 예를 들어 `[^ㄷㄹㅉㅎ:ㅏ]`는 `[가까나따마바빠사싸아자차카타파]`(`ㅏ` 조합 중 `다,라,짜,하` 없음.)입니다.

만약 해당 자리에 모든 구문을 일치시키고 싶다면 해당 자리를 비워두거나 .으로 나타낼 수도 있습니다. 예를 들어 `[.:ㅏ]`는 가능한 모든 `ㅏ` 조합을 의미하고, `[:ㅗ:ㄴ]`은 `[곤꼰논돈똔...혼]`을 의미합니다. 비워두는 경우와 .으로 나타내는 경우는 완전히 동일하며 바꿔쓸 수 있습니다(단, 한 칸이 .으로 채워져 있다면 그 칸에는 다른 문자가 있어서는 안 됩니다.). 이를 응용하여 모든 한글 조합을 알아낼 수 있습니다. `[::]`(혹은 `[.:.:.])`이 바로 그 경우입니다.

## 고급

### 조합의 사용

된소리를 제외한 조합형 음소는 괄호를 이용해서 표현할 수 있습니다. 예를 들어 `ㅚ`는 `(ㅗㅣ)`와 완전히 같은 구문이고, `ㄶ`은 `(ㄴㅎ)`과 완전히 같습니다. 예를 들어 `[:ㅞㅢ:ㄶㄼ]`은 `[:(ㅜㅔ)ㅢ:ㄶ(ㄹㅂ)]`과 같습니다.

### `0`의 사용

`0`은 해당 자리에 음소가 없다는 의미입니다. 예를 들어 `[ㄱ:ㅏ:0ㄴㅎ]`은 `[가간갛]`와 같습니다. 초성과 중성에는 기본적으로는 `0`을 사용하는 것이 금지되지만 특별한 경우, 한 음소를 나타내고 싶을 때, 사용됩니다. 예를 들어 `[0:ㅏ-ㅜ]` 혹은 `[0:ㅏ-ㅜ:0]`은 `[ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜ]`를 의미합니다. 또한 `[ㄱ-ㄹ:0]` 또는 `[ㄱ-ㄹ:0:0]`은 `[ㄱㄲㄴㄷㄸㄹ]`를 의미합니다. 하지만 초성과 중성에 `0`이 들어가는 경우는 몇 가지 제약이 있는데요, 우선 `0`이 들어가면 그 자리에는 `0` 외에 다른 음소를 작성할 수 없습니다. 다음은 몇 가지 조합은 `0`을 사용할 수 없다는 것입니다. 예를 들어 `[ㄱ:0:ㅎ]`을 생각해 봅시다. 이런 한글은 곰곰히 생각해도 사용할 수 있는 형태는 아닙니다. 이것 뿐만 아니라 `[0:ㅏ:ㅎ]`나 `[0:0:0]`도 금지됩니다.

### compilestr 및 make_korean 사용 및 응용

기본적으로 compile은 단순히 compilestr()을 거친 문자열을 re.complie()에 감싸는 것에 불과합니다.

```python
# compile의 내부 구현
def compile(pattern, flags=0):
    return re.compile(compilestr(pattern), flags)
```

따라서 처리 전 상태의 구문을 알고 싶다면 compilestr을 사용할 수 있습니다.

만약 regex 구문이 궁금한 것이 아니라 그냥 가능한 모든 한글 조합을 알고 싶은 경우엔 make_korean의 기능을 응용할 수 있습니다.

```python
# 받침이 ㄴ인 글자 모두 뽑기
import ko_re
print(ko_re.make_korean('[::ㄴ]'))
# 간갠갼걘...휸흔흰힌
```

## 정규 음운 후행 자모순

`regular_first` 자모순('정규 음운 후행 자모순' 이하 '후행 자모순')은 된소리나 자음군, 합용자들이 뒤로 보내진 순서입니다.

비교하면 기본 순서(유니코드 순서 또는 사전순)은 다음과 같습니다:

초성: ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ

중성: ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ

종성: ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ

하지만 후행 자모순은 다음과 같습니다:

초성: ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉ

중성: ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖㅘㅙㅚㅝㅞㅟㅢ

종성: ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄳㄵㄶㄺㄻㄼㄽㄾㄿㅀㅄㅆ

이 순서는 `-`를 통해 값에 접근할 때 사용되지만, 정렬은 일반적인 유니코드 순서(사전 순서)대로 정렬됩니다.

예를 들어 `[ㄱ-ㅎ:0:0]`은 기본 순서에서는 모든 초성을 포함하는 `[ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ]`이지만, 후행 자모순에서는 `[ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ]`입니다.

다음과 같은 방식으로 후행 자모순을 사용할 수 있습니다.

```python
import ko_re
ko_re.change_order('regular_first') # 후행 자모순
ko_re.change_order('default') # 기본값(사전순)
```

이 자모순은 특히 된소리(ㄲ, ㄸ, ㅃ, ㅆ, ㅉ)가 아닌 일반적으로 알고 있는 순서를 사용하고 싶을 때 유용하게 사용할 수 있습니다.

## release note

* 0.0.5: make_korean 추가, 이름 변경, 타입 추가, 리팩토링, 검사 추가
* 0.0.4: readme 보강, 리팩토링
* 0.0.3(첫 안정화 버전): ko_re 시작.

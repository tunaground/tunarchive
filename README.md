# tunARCHIVE

참치 인터넷 어장의 구 게시판(Lightuna) 원본 데이터(JSON)를 인간친화적인 형식으로 빌드한다.

## 요구사항

- Python3
- `requirements.txt` 참고.

## 사용법

> [!WARNING]
> Windows 사용시 `--windows` 옵션을 붙여야 Surrogates 관련 오류가 발생하지 않는다.

우선 프로젝트 루트 아래에 `data` 디렉토리를 생성한 뒤 Lightuna 원본 데이터를 옮겨넣는다.

디렉토리/파일 구조는 다음과 같은 형태로 나온다.

```
.
├── data/
│   ├── tuna/
│   │   ├── data/
│   │   │   ├── image1.jpg
│   │   │   └── image2.png
│   │   ├── 1111111111.json
│   │   ├── 2222222222.json
│   │   └── index.json
│   └── situplay/
│       ├── data/
│       │   ├── image3.jpg
│       │   └── image4.png
│       ├── 3333333333.json
│       ├── 4444444444.json
│       └── index.json
├── dist
├── templates/
└── run.py
```

- `data`: 원본 데이터 디렉토리
- `dist`: 빌드 결과물 디렉토리
- `templates`: 출력 템플릿 디렉토리
- `run.py`: 빌드 프로그램

아래 커맨드로 빌드한다.

```bash
# 전체 빌드
python3 run.py BOARD_ID

# 주제글 페이지(trace)만 빌드
python3 run.py BOARD_ID --trace-only

# 목록 페이지(index)만 빌드
python3 run.py BOARD_ID --index-only
```

> [!NOTE]
> BOARD_ID는 data/ 하위의 디렉토리명과 동일하게 입력한다.
> ex) `python3 run.py situplay`

빌드 결과물은 `dist/` 디렉토리 하위에 생성된다.

### Data URI

`--data-uri` 옵션을 사용하면 빌드 과정에서 첨부파일을 Data URI로 변환하여 html 파일을 발행한다.

이 경우 별도의 첨부파일 디렉토리를 필요로 하지 않으므로 파일 생성 경로가 달라진다.

```bash
# 기본
python3 run.py BOARD_ID
# 결과물
dist/tuna/1111111111/index.html
dist/tuna/1111111111/data/some-image.png

# Data URI 활성화
python3 run.py BOARD_ID --data-uri
# 결과물
dist/tuna/1111111111.html
```

### Body AA

구 앵커판 사양에 맞춰 답글 전반에 AA 폰트 설정을 적용하려는 경우
`--body-aa` 옵션을 사용한다.

### 데이터 조작

`data/` 디렉토리 하위의 원본 데이터를 직접 수정하여 빌드 전 필요한 결과만 출력하거나
내용을 변경할 수 있다.

### Templating

이 프로그램은 Jinja2를 이용해 탬플릿으로 결과를 출력한다.

`templates/` 디렉토리 하위의 탬플릿 파일을 수정하여 간단하게 출력을 변경할 수 있다.

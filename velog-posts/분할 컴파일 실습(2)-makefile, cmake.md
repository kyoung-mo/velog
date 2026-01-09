<h3 id="my_project-예제를-makefile로-하기"><code>my_project</code> 예제를 makefile로 하기</h3>
<p>프로젝트 루트 폴더(<code>my_project</code>)에 <code>Makefile</code>이라는 이름의 파일을 만들고 아래 내용을 붙여넣으시면 됩니다.</p>
<h3 id="makefile-작성">Makefile 작성</h3>
<p>Makefile</p>
<pre><code class="language-makefile"># 1. 컴파일러 및 옵션 설정
CC = gcc
# CFLAGS: -fPIC를 여기에 넣어서 모든 .o 파일이 공유 라이브러리용으로 만들어지게 합니다.
CFLAGS = -Wall -g -I./include -fPIC
LDFLAGS = -L./lib -lmymath

# 2. 디렉토리 설정
SRC_DIR = src
APP_DIR = app
LIB_DIR = lib
BIN_DIR = bin

# --------------------------------------------------------
# [핵심 변경 1] 소스 파일 및 오브젝트 파일 목록화
# --------------------------------------------------------
# 라이브러리에 포함될 소스 파일들을 나열합니다.
LIB_SRCS = $(SRC_DIR)/add.c $(SRC_DIR)/substract.c 

# 위 소스 파일 목록에서 .c를 .o로 바꾼 목록을 자동으로 생성합니다.
# 결과: src/mymath.o src/multiply.o
LIB_OBJS = $(LIB_SRCS:.c=.o)

# 3. 최종 타겟 파일 이름
LIB_STATIC = $(LIB_DIR)/libmymath.a
LIB_SHARED = $(LIB_DIR)/libmymath.so
EXE_STATIC = $(BIN_DIR)/main_static
EXE_SHARED = $(BIN_DIR)/main_shared

# 4. 기본 타겟
all: directories $(EXE_STATIC) $(EXE_SHARED)

# 5. 디렉토리 생성
directories:
    @mkdir -p $(BIN_DIR)
    @mkdir -p $(LIB_DIR)

# --------------------------------------------------------
# 빌드 규칙
# --------------------------------------------------------

# [핵심 변경 2] 패턴 규칙 (Pattern Rule) 사용
# src 폴더의 모든 .c 파일을 .o 파일로 컴파일하는 공통 규칙입니다.
# 파일이 100개로 늘어나도 이 규칙 하나면 됩니다.
$(SRC_DIR)/%.o: $(SRC_DIR)/%.c
    $(CC) $(CFLAGS) -c $&lt; -o $@

# (1) 정적 라이브러리 (.a) 생성
# $^ : 의존성 목록 전체 (즉, src/mymath.o src/multiply.o 모두 포함)
$(LIB_STATIC): $(LIB_OBJS)
    ar rcs $@ $^

# (2) 공유 라이브러리 (.so) 생성
$(LIB_SHARED): $(LIB_OBJS)
    $(CC) -shared -o $@ $^

# (3) 실행 파일 생성 (정적 링크)
$(EXE_STATIC): $(APP_DIR)/main.c $(LIB_STATIC)
    $(CC) $(CFLAGS) $&lt; -o $@ -L$(LIB_DIR) -lmymath

# (4) 실행 파일 생성 (공유 링크)
$(EXE_SHARED): $(APP_DIR)/main.c $(LIB_SHARED)
    $(CC) $(CFLAGS) $&lt; -o $@ -L$(LIB_DIR) -lmymath

# --------------------------------------------------------
# 정리 (Clean)
# --------------------------------------------------------
clean:
    rm -f $(SRC_DIR)/*.o
    rm -f $(LIB_DIR)/*
    rm -f $(BIN_DIR)/*

.PHONY: all clean directories</code></pre>
<hr />
<h3 id="makefile-사용-방법">Makefile 사용 방법</h3>
<p>터미널에서 <code>my_project</code> 폴더로 이동한 뒤 다음 명령어들을 사용하세요.</p>
<h3 id="1-전체-빌드">1. 전체 빌드</h3>
<p>Bash</p>
<p><code>make</code></p>
<p>이 명령어를 치면:</p>
<ol>
<li><code>src/mymath.c</code>를 컴파일해 <code>src/mymath.o</code>를 만듭니다.</li>
<li><code>lib</code> 폴더에 <code>.a</code>와 <code>.so</code> 파일을 만듭니다.</li>
<li><code>bin</code> 폴더에 <code>main_static</code>과 <code>main_shared</code> 실행 파일을 만듭니다.</li>
</ol>
<h3 id="2-실행-테스트">2. 실행 테스트</h3>
<ul>
<li><p><strong>정적 링크 실행 파일:</strong>Bash</p>
<p>  <code>./bin/main_static</code></p>
</li>
<li><p><strong>공유 링크 실행 파일:</strong>
(이전과 마찬가지로 라이브러리 경로를 알려줘야 합니다)Bash</p>
<p>  <code>export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/lib
  ./bin/main_shared</code></p>
</li>
</ul>
<h3 id="3-정리-clean">3. 정리 (Clean)</h3>
<p>빌드된 파일들을 모두 지우고 싶을 때 사용합니다.</p>
<p>Bash</p>
<p><code>make clean</code></p>
<hr />
<h3 id="핵심-포인트-설명-자동-변수">핵심 포인트 설명 (자동 변수)</h3>
<p>Makefile 안에 사용된 기호들의 의미입니다. 이걸 알면 나중에 수정하기 편합니다.</p>
<ul>
<li><code>$@</code> (Target): 현재 규칙의 <strong>결과물 파일 이름</strong>입니다.<ul>
<li>예: <code>$(CC) -o $@</code> → <code>gcc -o bin/main_static</code></li>
</ul>
</li>
<li><code>$&lt;</code> (First Prerequisite): 현재 규칙의 <strong>첫 번째 재료 파일</strong>입니다.<ul>
<li>예: <code>$(CC) -c $&lt;</code> → <code>gcc -c src/mymath.c</code></li>
</ul>
</li>
<li><code>^</code> (All Prerequisites): 모든 재료 파일입니다.</li>
</ul>
<p>이 Makefile은 소스 코드가 수정되면, 변경된 부분만 알아서 다시 컴파일하도록 의존성(<code>Dependency</code>)이 설정되어 있습니다. 예를 들어 <code>src/mymath.c</code>를 고치고 <code>make</code>를 치면, 라이브러리와 실행 파일까지 싹 업데이트됩니다.</p>
<h3 id="my_project-예제를-cmake로-하기"><code>my_project</code> 예제를 cmake로 하기</h3>
<p>CMake를 사용하면 <code>gcc</code> 명령어를 직접 칠 필요 없이, 설정 파일(<code>CMakeLists.txt</code>) 하나로 복잡한 컴파일과 링크 과정을 관리할 수 있습니다.</p>
<hr />
<h3 id="1-프로젝트-구조-확인">1. 프로젝트 구조 확인</h3>
<p>먼저 파일들이 다음과 같이 위치해 있다고 가정합니다.</p>
<pre><code class="language-c">my_project/
├── CMakeLists.txt      &lt;-- (새로 만들 파일)
├── include/
│   └── mymath.h
├── src/
│   └── add.c
│   └── substract.c
└── app/
    └── main.c</code></pre>
<hr />
<h3 id="2-cmakeliststxt-작성">2. CMakeLists.txt 작성</h3>
<p>프로젝트 최상위 폴더(my_project)에 CMakeLists.txt 파일을 만들고 아래 내용을 작성하세요.</p>
<p>이 파일이 기존의 gcc, ar, -I, -L 옵션들을 대신합니다.</p>
<p>CMakeLists.txt </p>
<pre><code class="language-c"># 1. CMake 최소 버전 및 프로젝트 설정
cmake_minimum_required(VERSION 3.10)
project(MyMathProject)

# 2. 헤더 파일 경로 지정 (-I 옵션 역할)
# include 폴더를 컴파일러가 찾을 수 있게 등록합니다.
include_directories(${CMAKE_SOURCE_DIR}/include)

# 3. 출력 디렉토리 설정 (선택 사항)
# 빌드된 라이브러리는 build/lib, 실행 파일은 build/bin에 모으도록 설정
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# ==========================================
# 4. 정적 라이브러리 (.a) 생성
# ==========================================
# add_library(타겟이름 STATIC 소스파일)
add_library(mymath_static STATIC src/add.c src/substract.c)

# 실제 파일명이 libmymath.a가 되도록 이름을 지정
set_target_properties(mymath_static PROPERTIES OUTPUT_NAME &quot;mymath&quot;)

# ==========================================
# 5. 공유 라이브러리 (.so) 생성
# ==========================================
# add_library(타겟이름 SHARED 소스파일)
# CMake는 SHARED 지정 시 자동으로 -fPIC 옵션을 적용합니다.
add_library(mymath_shared SHARED src/add.c src/substract.c)

# 실제 파일명이 libmymath.so가 되도록 이름을 지정
set_target_properties(mymath_shared PROPERTIES OUTPUT_NAME &quot;mymath&quot;)

# ==========================================
# 6. 실행 파일 생성 및 링크
# ==========================================

# (1) 정적 라이브러리를 사용하는 실행 파일
add_executable(main_static_app app/main.c)
# target_link_libraries: 링커에게 라이브러리 연결 지시 (-L, -l 역할)
target_link_libraries(main_static_app mymath_static)

# (2) 공유 라이브러리를 사용하는 실행 파일
add_executable(main_shared_app app/main.c)
target_link_libraries(main_shared_app mymath_shared)</code></pre>
<hr />
<h3 id="3-빌드-실행-out-of-source-build">3. 빌드 실행 (Out-of-source Build)</h3>
<p>CMake의 장점은 소스 코드 폴더를 더럽히지 않고 별도의 <code>build</code> 폴더에서 빌드할 수 있다는 점입니다.</p>
<p>터미널에서 <code>my_project</code> 폴더로 이동한 후 아래 명령어를 순서대로 입력하세요.</p>
<pre><code class="language-c"># 1. 빌드용 폴더 생성 및 이동
mkdir build
cd build

# 2. CMake 설정 (Makefile 생성 단계)
# &quot;..&quot;은 상위 폴더의 CMakeLists.txt를 참조하라는 뜻입니다.
cmake ..

# 3. 실제 빌드 수행 (make 실행 단계)
make</code></pre>
<h3 id="4-결과-확인-및-실행">4. 결과 확인 및 실행</h3>
<p>빌드가 완료되면 <code>build</code> 폴더 내부에 우리가 설정한 대로 결과물이 생성됩니다.</p>
<h3 id="41-생성된-파일-확인">4.1 생성된 파일 확인</h3>
<p>Bash</p>
<pre><code class="language-c"># 라이브러리 파일 확인 (.a, .so)
ls -l lib/
# 실행 파일 확인
ls -l bin/</code></pre>
<h3 id="42-실행-파일-실행">4.2 실행 파일 실행</h3>
<p>① 정적 라이브러리 버전 실행</p>
<p>이건 바로 실행됩니다. 라이브러리가 안에 포함되어 있기 때문입니다.</p>
<p>Bash</p>
<pre><code class="language-c">./bin/main_static_app</code></pre>
<p>② 공유 라이브러리 버전 실행</p>
<p>공유 라이브러리(.so)는 실행 시점에 라이브러리를 찾아야 합니다.</p>
<p>CMakeLists.txt가 빌드된 위치(build/lib)를 가리키고 있지만, 배포 환경 등을 고려해 LD_LIBRARY_PATH를 지정해주는 것이 명확합니다.</p>
<p>Bash</p>
<pre><code class="language-c"># 라이브러리 경로를 지정하고 실행
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/lib
./bin/main_shared_app</code></pre>
<hr />
<h3 id="명령어-매핑-요약-manual-vs-cmake">명령어 매핑 요약 (Manual vs CMake)</h3>
<table>
<thead>
<tr>
<th><strong>수동 명령어 (GCC)</strong></th>
<th><strong>CMake 명령어</strong></th>
<th><strong>비고</strong></th>
</tr>
</thead>
<tbody><tr>
<td><code>gcc -c ... -I./include</code></td>
<td><code>include_directories(...)</code></td>
<td>헤더 경로 추가</td>
</tr>
<tr>
<td><code>gcc -fPIC</code></td>
<td><code>add_library(... SHARED ...)</code></td>
<td>SHARED 옵션 시 자동 적용</td>
</tr>
<tr>
<td><code>ar rcs libmymath.a ...</code></td>
<td><code>add_library(... STATIC ...)</code></td>
<td>정적 라이브러리 생성</td>
</tr>
<tr>
<td><code>gcc -shared ...</code></td>
<td><code>add_library(... SHARED ...)</code></td>
<td>공유 라이브러리 생성</td>
</tr>
<tr>
<td><code>gcc ... -L./lib -lmymath</code></td>
<td><code>target_link_libraries(...)</code></td>
<td>라이브러리 링크</td>
</tr>
</tbody></table>
<h3 id="tip">Tip</h3>
<p>CMake를 사용하면 <code>make clean</code> 명령어 역시 자동으로 지원되므로, <code>build</code> 폴더 안에서 <code>make clean</code>을 입력하면 빌드된 파일들을 싹 지울 수 있습니다. 혹은 그냥 <code>build</code> 폴더 전체를 삭제(<code>rm -rf build</code>)해도 소스 코드에는 아무런 영향이 없습니다.</p>
<h3 id="환경-변수와-앨리어스-export-alias">환경 변수와 앨리어스 (export, alias)</h3>
<h4 id="실습-내용">실습 내용</h4>
<ol>
<li><code>env</code> 명령어로 모든 환경변수 조회</li>
<li><code>export MY_VAR=&quot;hello&quot;</code> 설정 후 스크립트에서 사용</li>
<li><code>alias ll='ls -alF'</code> 처럼 자주 쓰는 명령어 단축키 등록</li>
<li><code>.bashrc</code> 수정하여 영구 적용</li>
</ol>
<hr />
<h3 id="export란">export란?</h3>
<p>현재 쉘에서 만든 변수를 자식 프로세스(새로 실행한 프로그램)에서도 쓸 수 있게 여권을 발급해주는 명령어입니다.</p>
<p>임베디드 개발에서 툴체인 경로 설정이나 컴파일 옵션을 지정할 때 필수적으로 사용됩니다.</p>
<h3 id="동작-원리-부모-vs-자식">동작 원리 (부모 vs 자식)</h3>
<p>리눅스에서 터미널(부모)이 스크립트나 프로그램(자식)을 실행할 때, 기본적으로 변수는 상속되지 않습니다. <code>export</code>를 붙여야만 자식에게 전달됩니다.</p>
<h3 id="상황">상황</h3>
<p><code>MY_VAR=&quot;hello&quot;</code> 라고 변수를 만들고 <code>./script.sh</code>를 실행한다면:</p>
<ul>
<li>그냥 변수 (<code>MY_VAR</code>): 스크립트 안에서는 이 변수가 비어있음 (안 보임)</li>
<li><code>export</code> 변수 (<code>export MY_VAR</code>): 스크립트 안에서도 <code>&quot;hello&quot;</code>라고 보임</li>
</ul>
<hr />
<h3 id="1-툴체인-경로-추가-path">1. 툴체인 경로 추가 (PATH)</h3>
<p>컴파일러(<code>arm-linux-gcc</code>)를 아무 곳에서나 실행하려면 경로를 등록해야 합니다.</p>
<pre><code class="language-bash"># 그냥 PATH=... 하면 make 실행할 때 적용 안 됨
# 꼭 export 해야 함
export PATH=$PATH:/opt/gcc-arm-10.2/bin</code></pre>
<h3 id="2-크로스-컴파일-설정-arch-cross_compile">2. 크로스 컴파일 설정 (ARCH, CROSS_COMPILE)</h3>
<p>리눅스 커널이나 U-Boot를 빌드할 때, Makefile에게 &quot;나 ARM용으로 빌드할 거야&quot;라고 알려줍니다.</p>
<pre><code class="language-bash">export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-

# 이제 make만 쳐도 위 설정을 알아서 가져감
make defconfig</code></pre>
<h3 id="3-라이브러리-경로-지정-ld_library_path">3. 라이브러리 경로 지정 (LD_LIBRARY_PATH)</h3>
<p>내가 직접 만든 공유 라이브러리(<code>.so</code>)를 프로그램이 못 찾을 때 사용합니다.</p>
<pre><code class="language-bash">export LD_LIBRARY_PATH=/home/pi/my_libs:$LD_LIBRARY_PATH
./my_program</code></pre>
<h3 id="주의사항-재부팅하면-사라짐">주의사항: 재부팅하면 사라짐</h3>
<p>터미널에서 친 <code>export</code> 명령어는 그 터미널 창을 끄거나 재부팅하면 사라집니다 (휘발성).</p>
<p>영구적으로 적용하려면 홈 디렉터리의 설정 파일(<code>~/.bashrc</code> 또는 <code>~/.zshrc</code>) 맨 아래에 해당 <code>export</code> 명령어를 적어두어야 합니다.</p>
<pre><code class="language-bash"># 설정 파일 열기
vi ~/.bashrc

# 맨 아래 추가
export PATH=$PATH:/opt/toolchain/bin

# 적용
source ~/.bashrc</code></pre>
<hr />
<h3 id="환경-변수-실습">환경 변수 실습</h3>
<h3 id="1-모든-환경-변수-조회">1. 모든 환경 변수 조회</h3>
<pre><code class="language-bash"># 모든 환경 변수 출력
env

# 또는
printenv</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d3ed62be-e830-4343-9ac7-699d9945c8ef/image.png" /></p>
<pre><code># 특정 환경 변수 확인
echo $PATH
echo $HOME
echo $USER</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dea6af97-4db4-439c-8ca5-ecda9dbc23b3/image.png" /></p>
<h3 id="2-환경-변수-설정-및-사용">2. 환경 변수 설정 및 사용</h3>
<pre><code class="language-bash"># 일반 변수 (현재 쉘에서만)
MY_VAR=&quot;hello&quot;
echo $MY_VAR

# 환경 변수 (자식 프로세스에게도 전달)
export MY_VAR=&quot;hello&quot;

# 스크립트에서 사용
cat &gt; test.sh &lt;&lt; 'EOF'
#!/bin/bash
echo &quot;MY_VAR의 값: $MY_VAR&quot;
EOF

chmod +x test.sh
./test.sh</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bf374481-042c-4b36-bf71-f22bda3ad467/image.png" /></p>
<h3 id="3-path-환경-변수">3. PATH 환경 변수</h3>
<pre><code class="language-bash"># 현재 PATH 확인
echo $PATH

# 새 경로 추가 (임시)
export PATH=$PATH:/home/pi/my_bin

# 확인
echo $PATH

# 영구 적용 (~/.bashrc에 추가)
echo 'export PATH=$PATH:/home/pi/my_bin' &gt;&gt; ~/.bashrc
source ~/.bashrc</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d598b386-31ce-4798-a906-e4119de45bbc/image.png" /></p>
<hr />
<h2 id="앨리어스-alias">앨리어스 (alias)</h2>
<h3 id="자주-쓰는-명령어-단축키-만들기">자주 쓰는 명령어 단축키 만들기</h3>
<pre><code class="language-bash"># 현재 세션에서만 적용
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# 사용
ll</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8cbaf477-eaab-4489-8669-aa3253c14c8a/image.png" /></p>
<pre><code># 앨리어스 목록 확인
alias

# 앨리어스 해제
unalias ll</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/91933160-ac18-4ed2-b1a2-54a0f119a9d2/image.png" /></p>
<h3 id="영구-앨리어스-설정">영구 앨리어스 설정</h3>
<pre><code class="language-bash"># .bashrc 편집
nano ~/.bashrc

# 맨 아래 추가
alias ll='ls -alF'
alias la='ls -A'
alias proj='cd ~/project'
alias gs='git status'
alias gp='git push'
alias gc='git commit'

# 저장 후 적용
source ~/.bashrc</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c02be82c-50f3-4699-a354-3b335f3e3a54/image.png" /></p>
<h3 id="유용한-앨리어스-예제">유용한 앨리어스 예제</h3>
<pre><code class="language-bash"># 디렉토리 이동
alias ..='cd ..'
alias ...='cd ../..'
alias proj='cd ~/project'

# Git 단축키
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'

# 안전한 파일 조작
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# 시스템 정보
alias temp='vcgencmd measure_temp'
alias mem='free -h'
alias disk='df -h'</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/825e2bb8-21e7-416e-9bf0-7bb64c735311/image.png" /></p>
<hr />
<h3 id="쉘-스크립트-기초-echo-variables">쉘 스크립트 기초 (echo, variables)</h3>
<h3 id="실습-내용-1">실습 내용</h3>
<ol>
<li><code>hello.sh</code> 파일 생성 및 실행 권한 부여</li>
<li>변수 선언하고 <code>echo &quot;Hello $NAME&quot;</code> 출력하기</li>
<li>사용자 입력 받기 (<code>read</code>) 기능 구현</li>
</ol>
<hr />
<h3 id="첫-번째-스크립트-hellosh">첫 번째 스크립트: hello.sh</h3>
<h3 id="스크립트-생성">스크립트 생성</h3>
<pre><code class="language-bash"># 스크립트 파일 생성
cat &gt; hello.sh &lt;&lt; 'EOF'
#!/bin/bash

# 주석: 이것은 주석입니다
echo &quot;Hello, World!&quot;
EOF

# 실행 권한 부여
chmod +x hello.sh

# 실행
./hello.sh</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8c9f4be4-ad67-48b8-8eb2-d84bfe13b9df/image.png" /></p>
<h3 id="쉐뱅shebang이란">쉐뱅(Shebang)이란?</h3>
<pre><code class="language-bash">#!/bin/bash</code></pre>
<p>스크립트 첫 줄의 <code>#!</code>은 이 파일을 어떤 인터프리터로 실행할지 지정합니다.</p>
<ul>
<li><code>#!/bin/bash</code> - Bash 쉘로 실행</li>
<li><code>#!/bin/sh</code> - POSIX 호환 쉘로 실행</li>
<li><code>#!/usr/bin/python3</code> - Python3로 실행</li>
</ul>
<hr />
<h2 id="변수-사용하기">변수 사용하기</h2>
<h3 id="기본-변수">기본 변수</h3>
<pre><code class="language-bash">#!/bin/bash

# 변수 선언 (= 앞뒤 공백 없이!)
NAME=&quot;Linux&quot;
VERSION=5.15

# 변수 사용
echo &quot;Hello, $NAME&quot;
echo &quot;Version: $VERSION&quot;

# 중괄호 사용 (권장)
echo &quot;Hello, ${NAME}!&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/949b9913-be78-4ef2-a5ae-44533212f665/image.png" /></p>
<h3 id="사용자-입력-받기-read">사용자 입력 받기 (read)</h3>
<pre><code class="language-bash">#!/bin/bash

# 사용자 이름 입력받기
echo &quot;이름을 입력하세요:&quot;
read NAME

echo &quot;안녕하세요, ${NAME}님!&quot;

# 한 줄로
read -p &quot;나이를 입력하세요: &quot; AGE
echo &quot;당신의 나이는 ${AGE}세입니다.&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d15c104d-f7a5-4533-a688-77fd19fa81ac/image.png" /></p>
<h3 id="명령어-실행-결과를-변수에-저장">명령어 실행 결과를 변수에 저장</h3>
<pre><code class="language-bash">#!/bin/bash

# 방법 1: 백틱 사용
CURRENT_DATE=`date`

# 방법 2: $() 사용 (권장)
CURRENT_USER=$(whoami)
FILE_COUNT=$(ls | wc -l)

echo &quot;현재 날짜: $CURRENT_DATE&quot;
echo &quot;현재 사용자: $CURRENT_USER&quot;
echo &quot;파일 개수: $FILE_COUNT&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7dbc1b4e-907d-4bef-96e9-84dad22cb944/image.png" /></p>
<hr />
<h2 id="실습-예제">실습 예제</h2>
<h3 id="예제-1-간단한-인사-스크립트">예제 1: 간단한 인사 스크립트</h3>
<pre><code class="language-bash">#!/bin/bash

read -p &quot;이름을 입력하세요: &quot; NAME
read -p &quot;나이를 입력하세요: &quot; AGE

echo &quot;================================&quot;
echo &quot;이름: $NAME&quot;
echo &quot;나이: $AGE&quot;
echo &quot;현재 시간: $(date)&quot;
echo &quot;================================&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/668c858f-404f-4d34-8517-5e49aa3a3cd7/image.png" /></p>
<h3 id="예제-2-시스템-정보-출력">예제 2: 시스템 정보 출력</h3>
<pre><code class="language-bash">#!/bin/bash

echo &quot;=== 시스템 정보 ===&quot;
echo &quot;호스트명: $(hostname)&quot;
echo &quot;사용자: $(whoami)&quot;
echo &quot;현재 디렉토리: $(pwd)&quot;
echo &quot;CPU 온도: $(vcgencmd measure_temp)&quot;
echo &quot;메모리 사용량:&quot;
free -h</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/16712920-7022-4dc1-95a4-adb0d30daace/image.png" /></p>
<hr />
<h3 id="쉘-스크립트-제어문-if-for">쉘 스크립트 제어문 (if, for)</h3>
<h3 id="실습-내용-2">실습 내용</h3>
<ol>
<li><code>if</code>문으로 파일이 존재하는지 체크하고, 없으면 생성</li>
<li><code>for</code>문으로 현재 폴더의 모든 파일을 순회하며 이름 출력</li>
<li>졸업 과제: 지정된 디렉터리의 로그 파일을 압축해서 백업 폴더로 옮기는 자동화 스크립트</li>
</ol>
<hr />
<h3 id="if-조건문">if 조건문</h3>
<h3 id="기본-문법">기본 문법</h3>
<pre><code class="language-bash">#!/bin/bash

if [ 조건 ]; then
    # 조건이 참일 때 실행
    echo &quot;조건 참&quot;
fi</code></pre>
<h3 id="if-else">if-else</h3>
<pre><code class="language-bash">#!/bin/bash

AGE=20

if [ $AGE -ge 18 ]; then
    echo &quot;성인입니다&quot;
else
    echo &quot;미성년자입니다&quot;
fi</code></pre>
<h3 id="if-elif-else">if-elif-else</h3>
<pre><code class="language-bash">#!/bin/bash

SCORE=85

if [ $SCORE -ge 90 ]; then
    echo &quot;A학점&quot;
elif [ $SCORE -ge 80 ]; then
    echo &quot;B학점&quot;
elif [ $SCORE -ge 70 ]; then
    echo &quot;C학점&quot;
else
    echo &quot;재수강&quot;
fi</code></pre>
<h3 id="비교-연산자">비교 연산자</h3>
<h4 id="숫자-비교">숫자 비교</h4>
<pre><code class="language-bash">-eq  # 같다 (equal)
-ne  # 다르다 (not equal)
-gt  # 크다 (greater than)
-ge  # 크거나 같다 (greater or equal)
-lt  # 작다 (less than)
-le  # 작거나 같다 (less or equal)</code></pre>
<h4 id="문자열-비교">문자열 비교</h4>
<pre><code class="language-bash">=    # 같다
!=   # 다르다
-z   # 문자열이 비어있다
-n   # 문자열이 비어있지 않다</code></pre>
<h4 id="파일-검사">파일 검사</h4>
<pre><code class="language-bash">-e   # 파일이 존재한다
-f   # 일반 파일이다
-d   # 디렉토리이다
-r   # 읽기 가능하다
-w   # 쓰기 가능하다
-x   # 실행 가능하다</code></pre>
<h3 id="파일-존재-여부-확인">파일 존재 여부 확인</h3>
<pre><code class="language-bash">#!/bin/bash

FILE=&quot;test.txt&quot;

if [ -e &quot;$FILE&quot; ]; then
    echo &quot;$FILE 파일이 존재합니다&quot;
else
    echo &quot;$FILE 파일이 없습니다. 생성합니다...&quot;
    touch &quot;$FILE&quot;
fi</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/aa8c47c1-aa2a-4de9-8fb0-8784e4700d61/image.png" /></p>
<h3 id="디렉토리-검사-및-생성">디렉토리 검사 및 생성</h3>
<pre><code class="language-bash">#!/bin/bash

DIR=&quot;backup&quot;

if [ -d &quot;$DIR&quot; ]; then
    echo &quot;$DIR 디렉토리가 이미 존재합니다&quot;
else
    echo &quot;$DIR 디렉토리를 생성합니다&quot;
    mkdir -p &quot;$DIR&quot;
fi</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b9a64cfa-48eb-43a8-999b-c90b595030e6/image.png" /></p>
<hr />
<h2 id="for-반복문">for 반복문</h2>
<h3 id="기본-문법-1">기본 문법</h3>
<pre><code class="language-bash">#!/bin/bash

# 리스트 순회
for i in 1 2 3 4 5; do
    echo &quot;숫자: $i&quot;
done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/94fd65a7-519d-4d42-9f51-7592d1c34e85/image.png" /></p>
<h3 id="범위-사용">범위 사용</h3>
<pre><code class="language-bash">#!/bin/bash

# {시작..끝} 형식
for i in {1..10}; do
    echo &quot;Number: $i&quot;
done

# 증가값 지정
for i in {0..20..2}; do
    echo &quot;짝수: $i&quot;
done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8a9ef72e-7449-4026-ac8d-fca4a7bba44a/image.png" /></p>
<h3 id="파일-순회">파일 순회</h3>
<pre><code class="language-bash">#!/bin/bash

# 현재 디렉토리의 모든 파일
for file in *; do
    echo &quot;파일: $file&quot;
done

# 특정 확장자만
for cfile in *.c; do
    echo &quot;C 파일: $cfile&quot;
done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4a6b5635-9b16-484e-83d7-1c3aec3381ed/image.png" /></p>
<h3 id="명령어-결과-순회">명령어 결과 순회</h3>
<pre><code class="language-bash">#!/bin/bash

# ls 결과를 순회
for file in $(ls); do
    if [ -f &quot;$file&quot; ]; then
        echo &quot;파일: $file&quot;
    elif [ -d &quot;$file&quot; ]; then
        echo &quot;디렉토리: $file&quot;
    fi
done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f5363d42-be7e-43ad-b79f-fe5346b48135/image.png" /></p>
<hr />
<h2 id="실습-예제-1">실습 예제</h2>
<h3 id="예제-1-파일-존재-확인-및-생성">예제 1: 파일 존재 확인 및 생성</h3>
<pre><code class="language-bash">#!/bin/bash

FILES=&quot;log1.txt log2.txt log3.txt&quot;

for file in $FILES; do
    if [ -e &quot;$file&quot; ]; then
        echo &quot;$file 존재함&quot;
    else
        echo &quot;$file 생성 중...&quot;
        touch &quot;$file&quot;
    fi
done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c56c5d18-3122-4a94-864e-9d553fa1d7b0/image.png" /></p>
<h3 id="예제-2-파일-정보-출력">예제 2: 파일 정보 출력</h3>
<pre><code class="language-bash">#!/bin/bash

echo &quot;현재 디렉토리의 파일 정보:&quot;
echo &quot;==========================&quot;

for file in *; do
    if [ -f &quot;$file&quot; ]; then
        SIZE=$(ls -lh &quot;$file&quot; | awk '{print $5}')
        echo &quot;파일: $file (크기: $SIZE)&quot;
    fi
done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/aeb15d52-c234-4987-a690-bf0f5b24e5de/image.png" /></p>
<h3 id="예제-3-조건부-파일-처리">예제 3: 조건부 파일 처리</h3>
<pre><code class="language-bash">#!/bin/bash

for file in *.txt; do
    if [ -f &quot;$file&quot; ]; then
        LINES=$(wc -l &lt; &quot;$file&quot;)

        if [ $LINES -gt 100 ]; then
            echo &quot;$file: 큰 파일 ($LINES 줄)&quot;
        else
            echo &quot;$file: 작은 파일 ($LINES 줄)&quot;
        fi
    fi
done</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c854d36b-f218-490f-881d-d08ec2694412/image.png" /></p>
<hr />
<h3 id="로그-파일-백업-스크립트">로그 파일 백업 스크립트</h3>
<h3 id="요구사항">요구사항</h3>
<p>지정된 디렉터리의 로그 파일을 압축해서 백업 폴더로 옮기는 자동화 스크립트를 작성하세요.</p>
<h3 id="기능-명세">기능 명세</h3>
<ol>
<li>로그 디렉토리 확인 (<code>/var/log</code> 또는 <code>~/logs</code>)</li>
<li><code>.log</code> 확장자 파일 찾기</li>
<li>백업 디렉토리 생성 (<code>~/backup</code>)</li>
<li>현재 날짜로 압축 파일명 생성</li>
<li>로그 파일들을 tar.gz로 압축</li>
<li>압축 파일을 백업 디렉토리로 이동</li>
<li>작업 결과 출력</li>
</ol>
<h3 id="해답-예시">해답 예시</h3>
<pre><code class="language-bash">#!/bin/bash

# 설정
LOG_DIR=&quot;$HOME/logs&quot;
BACKUP_DIR=&quot;$HOME/backup&quot;
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE=&quot;logs_backup_${DATE}.tar.gz&quot;

echo &quot;=== 로그 백업 스크립트 시작 ===&quot;

# 1. 로그 디렉토리 확인
if [ ! -d &quot;$LOG_DIR&quot; ]; then
    echo &quot;오류: 로그 디렉토리 $LOG_DIR 가 존재하지 않습니다&quot;
    exit 1
fi

# 2. 백업 디렉토리 생성
if [ ! -d &quot;$BACKUP_DIR&quot; ]; then
    echo &quot;백업 디렉토리 생성: $BACKUP_DIR&quot;
    mkdir -p &quot;$BACKUP_DIR&quot;
fi

# 3. 로그 파일 개수 확인
LOG_COUNT=$(find &quot;$LOG_DIR&quot; -name &quot;*.log&quot; | wc -l)

if [ $LOG_COUNT -eq 0 ]; then
    echo &quot;백업할 로그 파일이 없습니다&quot;
    exit 0
fi

echo &quot;백업할 로그 파일: $LOG_COUNT 개&quot;

# 4. 압축
echo &quot;압축 중...&quot;
tar -czf &quot;$BACKUP_DIR/$BACKUP_FILE&quot; -C &quot;$LOG_DIR&quot; *.log 2&gt;/dev/null

# 5. 결과 확인
if [ -f &quot;$BACKUP_DIR/$BACKUP_FILE&quot; ]; then
    SIZE=$(ls -lh &quot;$BACKUP_DIR/$BACKUP_FILE&quot; | awk '{print $5}')
    echo &quot;백업 완료: $BACKUP_FILE (크기: $SIZE)&quot;

    # 6. 선택: 원본 로그 파일 삭제
    read -p &quot;원본 로그 파일을 삭제하시겠습니까? (y/n): &quot; ANSWER
    if [ &quot;$ANSWER&quot; = &quot;y&quot; ]; then
        rm -f &quot;$LOG_DIR&quot;/*.log
        echo &quot;원본 로그 파일 삭제 완료&quot;
    fi
else
    echo &quot;오류: 백업 실패&quot;
    exit 1
fi

echo &quot;=== 백업 완료 ===&quot;</code></pre>
<h3 id="고급-버전-로그-로테이션-포함">고급 버전 (로그 로테이션 포함)</h3>
<pre><code class="language-bash">#!/bin/bash

LOG_DIR=&quot;$HOME/logs&quot;
BACKUP_DIR=&quot;$HOME/backup&quot;
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE=&quot;logs_backup_${DATE}.tar.gz&quot;
KEEP_DAYS=7  # 7일 이상 된 백업 파일 삭제

echo &quot;=== 로그 백업 스크립트 (로테이션 포함) ===&quot;

# 백업 디렉토리 생성
mkdir -p &quot;$BACKUP_DIR&quot;

# 로그 파일 확인
if [ ! -d &quot;$LOG_DIR&quot; ] || [ $(find &quot;$LOG_DIR&quot; -name &quot;*.log&quot; | wc -l) -eq 0 ]; then
    echo &quot;백업할 로그 파일이 없습니다&quot;
    exit 0
fi

# 압축
tar -czf &quot;$BACKUP_DIR/$BACKUP_FILE&quot; -C &quot;$LOG_DIR&quot; *.log 2&gt;/dev/null

if [ $? -eq 0 ]; then
    echo &quot;백업 완료: $BACKUP_FILE&quot;

    # 오래된 백업 파일 삭제 (7일 이상)
    find &quot;$BACKUP_DIR&quot; -name &quot;logs_backup_*.tar.gz&quot; -mtime +$KEEP_DAYS -delete
    echo &quot;오래된 백업 파일 정리 완료 (${KEEP_DAYS}일 이상)&quot;

    # 백업 목록 출력
    echo &quot;현재 백업 파일:&quot;
    ls -lh &quot;$BACKUP_DIR&quot;/logs_backup_*.tar.gz
else
    echo &quot;백업 실패&quot;
    exit 1
fi</code></pre>
<hr />
<h2 id="crontab과-연동">Crontab과 연동</h2>
<h3 id="자동-백업-설정">자동 백업 설정</h3>
<pre><code class="language-bash"># crontab 편집
crontab -e

# 매일 새벽 2시에 백업 실행
0 2 * * * /home/pi/scripts/log_backup.sh &gt;&gt; /home/pi/backup/backup.log 2&gt;&amp;1

# 매주 일요일 자정에 백업
0 0 * * 0 /home/pi/scripts/log_backup.sh &gt;&gt; /home/pi/backup/backup.log 2&gt;&amp;1</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1a9b2f27-dc01-4229-bc48-135ce93c2775/image.png" /></p>
<hr />
<h2 id="참고-자료">참고 자료</h2>
<ul>
<li><a href="https://mywiki.wooledge.org/BashGuide">Bash Guide</a></li>
<li><a href="https://tldp.org/LDP/abs/html/">Advanced Bash-Scripting Guide</a></li>
<li><a href="https://www.shellcheck.net/">ShellCheck</a> - 스크립트 검증 도구</li>
</ul>
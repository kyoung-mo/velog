<hr />
<h2 id="프로세스-환경-process-environment">프로세스 환경 (Process Environment)</h2>
<hr />
<h2 id="목차">목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#start-up-%EB%A3%A8%ED%8B%B4">Start-up 루틴</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%AA%85%EB%A0%B9%EC%A4%84-%EC%9D%B8%EC%88%98-argc-argv">명령줄 인수 (argc, argv)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%99%98%EA%B2%BD-%EB%B3%80%EC%88%98-environment-variables">환경 변수 (Environment Variables)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4-%EB%A9%94%EB%AA%A8%EB%A6%AC-%EA%B5%AC%EC%A1%B0">프로세스 메모리 구조</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%A4%EC%A0%84-%EC%98%88%EC%A0%9C%EC%99%80-%EC%A3%BC%EC%9D%98%EC%82%AC%ED%95%AD">실전 예제와 주의사항</a></li>
</ol>
<hr />
<h2 id="start-up-루틴">Start-up 루틴</h2>
<h3 id="프로그램-시작-과정">프로그램 시작 과정</h3>
<p>일반적으로 &quot;C 프로그램은 <code>main()</code> 함수에서 시작한다&quot;고 알고 있지만, 실제로는 그 이전에 <strong>특별한 start-up 루틴</strong>이 존재합니다.</p>
<pre><code>커널 → _start → __libc_start_main → main()</code></pre><h3 id="주요-특징">주요 특징</h3>
<ul>
<li><strong>컴파일러</strong>가 생성하는 실행 파일에는 <strong>linker</strong>가 정한 start-up 루틴의 시작 주소가 포함</li>
<li><strong>ASLR</strong>(Address Space Layout Randomization)을 사용하면 시작 주소를 예측할 수 없음</li>
<li>ASLR은 buffer overflow 같은 공격을 방어하기 위한 메모리 보호 장치</li>
</ul>
<h3 id="aslr이란">ASLR이란?</h3>
<pre><code>실행할 때마다 메모리 주소가 바뀜:
- Stack 시작 주소
- Heap 시작 주소
- 라이브러리 로드 주소

→ 공격자가 특정 주소를 예측할 수 없게 만듦</code></pre><hr />
<h2 id="명령줄-인수-argc-argv">명령줄 인수 (argc, argv)</h2>
<h3 id="함수-시그니처">함수 시그니처</h3>
<pre><code class="language-c">int main(int argc, char *argv[]);</code></pre>
<table>
<thead>
<tr>
<th>매개변수</th>
<th>타입</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td><code>argc</code></td>
<td><code>int</code></td>
<td>명령줄 인수의 개수</td>
</tr>
<tr>
<td><code>argv</code></td>
<td><code>char*[]</code></td>
<td>명령줄 인수 문자열 배열</td>
</tr>
</tbody></table>
<h3 id="특징">특징</h3>
<ul>
<li>명령줄 매개변수는 <strong>공백(space)으로 구분</strong></li>
<li><code>argv[0]</code>은 항상 <strong>프로그램 이름</strong> (실행 경로)</li>
<li><code>argv[argc]</code>는 항상 <code>NULL</code></li>
</ul>
<h3 id="예제-cli_argsc">예제: cli_args.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(int argc, char *argv[]) {
    printf(&quot;Number of Arguments Passed: %d\n&quot;, argc);

    // 모든 명령줄 인수 출력
    for(int i = 0; i &lt; argc; i++) {
        printf(&quot;argv[%d]: %s\n&quot;, i, argv[i]);
    }

    return 0;
}</code></pre>
<h3 id="실행-결과">실행 결과</h3>
<pre><code class="language-bash">$ gcc cli_args.c -o cli_args

$ ./cli_args
Number of Arguments Passed: 1
argv[0]: ./cli_args

$ ./cli_args hello world good morning
Number of Arguments Passed: 5
argv[0]: ./cli_args
argv[1]: hello
argv[2]: world
argv[3]: good
argv[4]: morning</code></pre>
<hr />
<h2 id="환경-변수-environment-variables">환경 변수 (Environment Variables)</h2>
<h3 id="환경-변수란">환경 변수란?</h3>
<p>리눅스 운영체제는 <strong>character array 포인터</strong>에 저장된 환경 변수 목록을 관리합니다.</p>
<pre><code>형식: name=value
예시: HOME=/home/pi
     PATH=/usr/bin:/bin
     LANG=en_US.UTF-8</code></pre><h3 id="environ-변수">environ 변수</h3>
<pre><code class="language-c">extern char **environ;</code></pre>
<ul>
<li>환경 변수 목록을 참조하는 포인터</li>
<li>사전 정의 변수 + 사용자 생성 변수로 구성</li>
<li>프로그램은 이 환경 변수 목록 하에서 실행됨</li>
</ul>
<h3 id="환경-변수-목록-보기">환경 변수 목록 보기</h3>
<h4 id="예제-env_listc">예제: env_list.c</h4>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main() {
    extern char **environ;
    char **env = environ;

    // 모든 환경 변수 출력
    while(*env != NULL) {
        printf(&quot;%s\n&quot;, *env);
        env++;
    }

    return 0;
}</code></pre>
<h4 id="실행-결과-1">실행 결과</h4>
<pre><code class="language-bash">$ gcc env_list.c -o env_list
$ ./env_list
SHELL=/bin/bash
PWD=/home/pi/project
LOGNAME=pi
HOME=/home/pi
LANG=C.UTF-8
PATH=/usr/local/bin:/usr/bin:/bin
...</code></pre>
<h3 id="환경-변수-접근-함수">환경 변수 접근 함수</h3>
<pre><code class="language-c">char *getenv(const char *name);
int setenv(const char *name, const char *value, int overwrite);
int unsetenv(const char *name);</code></pre>
<table>
<thead>
<tr>
<th>함수</th>
<th>기능</th>
<th>반환값</th>
</tr>
</thead>
<tbody><tr>
<td><code>getenv()</code></td>
<td>환경 변수 값 가져오기</td>
<td>값 문자열 또는 NULL</td>
</tr>
<tr>
<td><code>setenv()</code></td>
<td>환경 변수 설정/수정</td>
<td>성공 0, 실패 -1</td>
</tr>
<tr>
<td><code>unsetenv()</code></td>
<td>환경 변수 삭제</td>
<td>성공 0, 실패 -1</td>
</tr>
</tbody></table>
<h4 id="예제-env_set_get_delc">예제: env_set_get_del.c</h4>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main() {
    char env_name[15];
    char env_value[255];

    printf(&quot;Enter Variable name: &quot;);
    scanf(&quot;%s&quot;, env_name);
    printf(&quot;Enter Variable value: &quot;);
    scanf(&quot;%s&quot;, env_value);

    // 환경 변수 설정
    int status = setenv(env_name, env_value, 1);

    if(status == 0) {
        printf(&quot;Environment variable created successfully!\n&quot;);
    } else {
        printf(&quot;Environment variable creation failed!\n&quot;);
    }

    // 값 확인
    printf(&quot;%s=%s\n&quot;, env_name, getenv(env_name));

    // 삭제
    unsetenv(env_name);
    printf(&quot;After delete: %s=%s\n&quot;, env_name, getenv(env_name));

    return 0;
}</code></pre>
<h4 id="실행-결과-2">실행 결과</h4>
<pre><code class="language-bash">$ gcc env_set_get_del.c -o env_test
$ ./env_test
Enter Variable name: MY_VAR
Enter Variable value: hello
Environment variable created successfully!
MY_VAR=hello
After delete: MY_VAR=(null)

$ echo $MY_VAR
                    # 빈 값 (프로세스 내부 변경은 Shell에 영향 없음)</code></pre>
<hr />
<h2 id="환경-변수-상속-inheritance">환경 변수 상속 (Inheritance)</h2>
<h3 id="핵심-개념">핵심 개념</h3>
<blockquote>
<p><strong>자식 프로세스는 부모의 환경 변수를 물려받지만,<br />자식이 수정한 내용은 부모에게 영향을 주지 않음</strong></p>
</blockquote>
<pre><code>Shell (부모)
  └─ export MY_DATA=&quot;Parent_Value&quot;
     └─ ./program (자식)
        └─ setenv(&quot;MY_DATA&quot;, &quot;Child_Value&quot;)  ← 자식만 변경

Shell에서 확인 → 여전히 &quot;Parent_Value&quot;</code></pre><h3 id="예제-env_inheritc">예제: env_inherit.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main() {
    char *name = &quot;MY_DATA&quot;;
    char *val;

    // 1. 부모로부터 상속받은 값 확인
    val = getenv(name);
    if (val == NULL) {
        printf(&quot;[Child] '%s' 환경 변수가 없습니다.\n&quot;, name);
    } else {
        printf(&quot;[Child] 상속받은 값: %s\n&quot;, val);
    }

    // 2. 자식 프로세스 내에서 값 변경
    printf(&quot;[Child] 값을 'Child_Value'로 변경...\n&quot;);
    setenv(name, &quot;Child_Value&quot;, 1);

    // 3. 변경된 값 확인
    printf(&quot;[Child] 변경된 값: %s\n&quot;, getenv(name));
    printf(&quot;[Child] 프로세스 종료.\n&quot;);

    return 0;
}</code></pre>
<h3 id="실행-및-확인">실행 및 확인</h3>
<pre><code class="language-bash"># 1. 컴파일
$ gcc env_inherit.c -o env_inherit

# 2. 부모(Shell)에서 환경 변수 설정
$ export MY_DATA=&quot;Parent_Value&quot;
$ echo $MY_DATA
Parent_Value

# 3. 자식 프로세스 실행
$ ./env_inherit
[Child] 상속받은 값: Parent_Value
[Child] 값을 'Child_Value'로 변경...
[Child] 변경된 값: Child_Value
[Child] 프로세스 종료.

# 4. 부모(Shell) 값 재확인 → 변화 없음!
$ echo $MY_DATA
Parent_Value</code></pre>
<h3 id="결론">결론</h3>
<ul>
<li>✅ <strong>상속(Inheritance)</strong>: 부모 → 자식으로 값 전달됨</li>
<li>✅ <strong>격리(Isolation)</strong>: 자식의 변경사항은 부모에 영향 없음</li>
</ul>
<hr />
<h2 id="프로세스-메모리-구조">프로세스 메모리 구조</h2>
<h3 id="메모리-레이아웃">메모리 레이아웃</h3>
<p>리눅스 프로세스는 <strong>가상 메모리 공간</strong>을 사용하며, ELF 포맷에 따라 구획됩니다.</p>
<pre><code>높은 주소
┌─────────────────┐
│  Command Line   │  ← 명령줄 인수, 환경변수
│  &amp; Environment  │
├─────────────────┤
│     Stack       │  ← 지역변수, 함수 호출
│       ↓         │     (높은 주소 → 낮은 주소)
├─────────────────┤
│                 │
│   (Free Space)  │
│                 │
├─────────────────┤
│       ↑         │
│     Heap        │  ← 동적 할당 (malloc)
│                 │     (낮은 주소 → 높은 주소)
├─────────────────┤
│   BSS Segment   │  ← 초기화 안 된 전역변수
│                 │     (자동으로 0 초기화)
├─────────────────┤
│  Data Segment   │  ← 초기화된 전역변수
│ (Initialized)   │
├─────────────────┤
│  Text Segment   │  ← 실행 코드 + 문자열 리터럴
│    (Code)       │     (Read-Only)
└─────────────────┘
낮은 주소</code></pre><h3 id="각-영역-설명">각 영역 설명</h3>
<table>
<thead>
<tr>
<th>영역</th>
<th>내용</th>
<th>특징</th>
</tr>
</thead>
<tbody><tr>
<td><strong>Text (Code)</strong></td>
<td>실행 코드, 문자열 리터럴</td>
<td>Read-Only</td>
</tr>
<tr>
<td><strong>Data</strong></td>
<td>초기화된 전역변수 <code>int a=10;</code></td>
<td>Read-Write</td>
</tr>
<tr>
<td><strong>BSS</strong></td>
<td>초기화 안 된 전역변수 <code>int b;</code></td>
<td>자동 0 초기화</td>
</tr>
<tr>
<td><strong>Heap</strong></td>
<td>동적 할당 (<code>malloc</code>)</td>
<td>위로 성장 ↑</td>
</tr>
<tr>
<td><strong>Stack</strong></td>
<td>지역변수, 함수 인자</td>
<td>아래로 성장 ↓</td>
</tr>
</tbody></table>
<hr />
<h2 id="실전-예제와-주의사항">실전 예제와 주의사항</h2>
<h3 id="❌-잘못된-코드-예제">❌ 잘못된 코드 예제</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;

int main() {
    // 문제 1: 문자열 리터럴 (Read-Only)
    char *data = &quot;This is read-only string&quot;;

    // 문제 2: Heap 메모리 누수
    char *name = malloc(40);
    name = &quot;andrew&quot;;  // malloc 주소를 잃어버림!

    // 💥 Segmentation Fault!
    strcpy(data, &quot;hello world&quot;);  // Read-Only 메모리에 쓰기 시도

    return 0;
}</code></pre>
<h3 id="문제-분석">문제 분석</h3>
<h4 id="problem-1-segmentation-fault">Problem 1: Segmentation Fault</h4>
<pre><code class="language-c">char *data = &quot;This is...&quot;;  // data는 Stack, 문자열은 Text(Read-Only)
strcpy(data, &quot;hello&quot;);      // ❌ Read-Only 영역에 쓰기 → Crash!</code></pre>
<p><strong>해결책:</strong></p>
<pre><code class="language-c">// 방법 1: 배열로 선언 (Stack에 복사본 생성)
char data[] = &quot;This is...&quot;;

// 방법 2: Heap에 할당
char *data = malloc(50);
strcpy(data, &quot;This is...&quot;);</code></pre>
<h4 id="problem-2-memory-leak">Problem 2: Memory Leak</h4>
<pre><code class="language-c">char *name = malloc(40);    // Heap에 40바이트 할당 (주소: 0x12345678)
name = &quot;andrew&quot;;            // Text 영역 주소(0x00400500)로 덮어씀
                            // → 0x12345678은 영원히 접근 불가 (Leak!)</code></pre>
<p><strong>해결책:</strong></p>
<pre><code class="language-c">char *name = malloc(40);
strcpy(name, &quot;andrew&quot;);     // malloc 받은 메모리에 복사
// 사용 후
free(name);                 // 반드시 해제!</code></pre>
<h3 id="✅-올바른-코드">✅ 올바른 코드</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;

int main() {
    // Stack에 배열 할당 (수정 가능)
    char data[100] = &quot;Original string&quot;;

    // Heap에 메모리 할당
    char *name = malloc(40);
    if (name == NULL) {
        perror(&quot;malloc failed&quot;);
        return 1;
    }

    // 안전하게 복사
    strcpy(name, &quot;andrew&quot;);
    strcpy(data, &quot;hello world&quot;);

    printf(&quot;data: %s\n&quot;, data);
    printf(&quot;name: %s\n&quot;, name);

    // 메모리 해제
    free(name);

    return 0;
}</code></pre>
<hr />
<h2 id="메모리-영역별-변수-예제">메모리 영역별 변수 예제</h2>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

// Data Segment (초기화된 전역변수)
int global_init = 10;

// BSS Segment (초기화 안 된 전역변수)
int global_uninit;

int main() {
    // Stack (지역변수)
    int local = 20;

    // Heap (동적 할당)
    int *heap_var = malloc(sizeof(int));
    *heap_var = 30;

    // Text (문자열 리터럴)
    char *str = &quot;Hello&quot;;

    printf(&quot;=== 메모리 주소 ===\n&quot;);
    printf(&quot;Text (str):          %p\n&quot;, (void*)str);
    printf(&quot;Data (global_init):  %p\n&quot;, (void*)&amp;global_init);
    printf(&quot;BSS (global_uninit): %p\n&quot;, (void*)&amp;global_uninit);
    printf(&quot;Heap (heap_var):     %p\n&quot;, (void*)heap_var);
    printf(&quot;Stack (local):       %p\n&quot;, (void*)&amp;local);

    free(heap_var);
    return 0;
}</code></pre>
<h3 id="예상-출력-주소는-매번-다름">예상 출력 (주소는 매번 다름)</h3>
<pre><code>=== 메모리 주소 ===
Text (str):          0x0000000000400610  (낮은 주소)
Data (global_init):  0x0000000000601030
BSS (global_uninit): 0x0000000000601038
Heap (heap_var):     0x0000000001a4a010
Stack (local):       0x00007ffc8b3e2a4c  (높은 주소)</code></pre><hr />
<h2 id="핵심-정리">핵심 정리</h2>
<h3 id="start-up-루틴-1">Start-up 루틴</h3>
<pre><code>커널 → _start → __libc_start_main → main()
ASLR로 인해 주소는 실행마다 바뀜</code></pre><h3 id="명령줄-인수">명령줄 인수</h3>
<pre><code class="language-c">int main(int argc, char *argv[])
argv[0]: 프로그램 이름
argv[1~argc-1]: 실제 인수</code></pre>
<h3 id="환경-변수">환경 변수</h3>
<pre><code class="language-c">extern char **environ;  // 전체 목록
getenv(name)            // 값 가져오기
setenv(name, val, 1)    // 값 설정
unsetenv(name)          // 삭제

자식 프로세스 변경 → 부모에 영향 없음!</code></pre>
<h3 id="메모리-구조">메모리 구조</h3>
<pre><code>Text (Code) → Read-Only! 수정 시도 시 Segfault
Data        → 초기화된 전역변수
BSS         → 초기화 안 된 전역변수 (0으로 자동 초기화)
Heap        → malloc (위로 성장 ↑)
Stack       → 지역변수 (아래로 성장 ↓)</code></pre><h3 id="주의사항">주의사항</h3>
<pre><code class="language-c">❌ char *s = &quot;literal&quot;; strcpy(s, &quot;new&quot;);  // Segfault
✅ char s[] = &quot;literal&quot;; strcpy(s, &quot;new&quot;); // OK

❌ char *p = malloc(10); p = &quot;leak&quot;;       // Memory Leak
✅ char *p = malloc(10); strcpy(p, &quot;ok&quot;); free(p);</code></pre>
<hr />
<h2 id="참고-자료">참고 자료</h2>
<ul>
<li><a href="https://gabrieletolomei.wordpress.com/miscellanea/operating-systems/in-memory-layout/">Linux Memory Layout</a></li>
<li>APUE (Advanced Programming in the UNIX Environment)</li>
<li>Linux man pages: <code>man environ</code>, <code>man getenv</code></li>
</ul>
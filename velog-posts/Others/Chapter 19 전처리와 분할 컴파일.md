<h2 id="1-전처리-지시자">1. 전처리 지시자</h2>
<ul>
<li>프로그램은 컴파일환경을 바꾸거나 여러개의 모듈로 나누어 작성할때 이식성과 호환성을 고려해야한다.</li>
<li>컴파일전에 컴파일 환경에 맞게 소스코드를 편집할 수 있는 기능이 필요하고, 이를 전처리지시자로 한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f630c387-e7ee-4517-90a1-f45e4a32f8b3/image.png" /></p>
<ul>
<li>컴파일하기 좋게 다듬는 과정</li>
<li>#으로 시작하는 지시자</li>
</ul>
<h3 id="파일을-포함하는-include">파일을 포함하는 #include</h3>
<ul>
<li><p>&lt;&gt; : 컴파일러의 include디렉터리에서 헤더파일 참조 -&gt; 소스파일이 저장된 디렉터리에서 참조</p>
</li>
<li><p>&quot;&quot; : 소스파일이 저장된 디렉터리에서 참조 -&gt; 컴파일러의 include디렉터리에서 헤더파일 참조</p>
</li>
<li><p>student.h : 사용자 정의 헤더 파일을 사용하는 프로그램</p>
<pre><code class="language-c">  // 사용자 정의 헤더 파일 – student.h
  typedef struct        // student 구조체 선언
  {
      int num;          // 학번
      char name[20];    // 이름
  } Student;
</code></pre>
</li>
<li><p>main.c : 사용자 정의 헤더 파일을 사용하는 프로그램</p>
<pre><code class="language-c">  // 소스 파일 – main.c
  #include &lt;stdio.h&gt;           // 시스템 헤더 파일의 내용 복사
  #include &quot;student.h&quot;         // 사용자 정의 헤더 파일의 내용 복사

  int main(void)
  {
      Student a = { 315, &quot;홍길동&quot; };   // 구조체 변수 선언과 초기화

      printf(&quot;학번 : %d, 이름 : %s\\n&quot;, a.num, a.name);  // 구조체 멤버 출력

      return 0;
  }
</code></pre>
</li>
<li><p>전처리가 끝나면 인크루드한 파일의 내용은 복사되어 소스파일에 포함됩니다.</p>
</li>
<li><p>include는 파일의 내용을 단순히 복사하여 붙여넣는 기능을 한다.</p>
<p>  예시일뿐 이런식으로 프로그램 하지는 않느다. </p>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0ebcab46-f0f6-478a-842d-08803fa7a2de/image.png" /></p>
<h3 id="매크로명으로-만드는-define">매크로명으로 만드는 #define</h3>
<ul>
<li><p>매크로명을 정의하면 복잡한 상수나 문장을 의미 있는 단어로 쓸 수 있다.</p>
</li>
<li><p>#define 매크로명 치환될_부분</p>
</li>
<li><p>19-2.c  : 다양한 매크로명의 사용</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #define PI 3.14159                        // 상수를 매크로명으로 정의
  #define LIMIT 100.0                       // 상수를 매크로명으로 정의
  #define MSG &quot;passed!&quot;                     // 문자열을 매크로명으로 정의
  #define ERR_PRN printf(&quot;범위를 벗어났습니다!\\n&quot;)  // 출력문을 매크로명으로 정의

  int main(void)
  {
      double radius, area;                  // 반지름과 면적 변수

</code></pre>
</li>
</ul>
<pre><code>    printf(&quot;반지름을 입력하세요(100 이하) : &quot;);
    scanf(&quot;%lf&quot;, &amp;radius);                // 반지름 입력
    area = PI * radius * radius;          // 면적 계산
    if (radius &gt; LIMIT) ERR_PRN;            // 반지름이 100을 초과하면 오류 메시지 출력
    else printf(&quot;원의 면적 : %.2lf(%s)\\n&quot;, area, MSG);  // 면적과 메시지 출력

    return 0;
}
```</code></pre><ul>
<li>모든 매크로명은 전처리과정에서 치환될 부분으로 바뀝니다.</li>
<li>상수 대신해서 쓰이는 매크로를 <strong>매크로상수</strong></li>
<li>에러 메시지를 소스코드에서 즉시 확인하기 힘들어진다.</li>
<li>필요한 경우만 제한적으로 사용하자.</li>
</ul>
<h2 id="define을-사용한-매크로-함수">#define을 사용한 매크로 함수</h2>
<ul>
<li><p>#define 매크로_함수명(인수) 치환할_부분</p>
</li>
<li><p>19-3.c : 매크로 함수를 사용한 프로그램</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void func(void);

  int main(void)
  {
      printf(&quot;컴파일 날짜와 시간 : %s, %s\n\n&quot;, __DATE__, __TIME__);
      printf(&quot;파일명 : %s\n&quot;, __FILE__);
      printf(&quot;함수명 : %s\n&quot;, __FUNCTION__);
      printf(&quot;행번호 : %d\n&quot;, __LINE__);

  #line 100 &quot;macro.c&quot;   // 행 번호를 100부터 시작, 파일명은 macro.c로 표시
      func();           // 여기부터 행 번호는 100으로 시작

      return 0;
  }

  void func(void)
  {
      printf(&quot;\\n&quot;);
      printf(&quot;파일명 : %s\\n&quot;, __FILE__);
      printf(&quot;함수명 : %s\\n&quot;, __FUNCTION__);
      printf(&quot;행번호 : %d\\n&quot;, __LINE__);
  }</code></pre>
<pre><code>  a + b = 30
  x + y = 70
  res : 3
</code></pre></li>
<li><p>매크로 함수는 치환된 후의 부작용을 줄이기위해 치환될 부분에 괄호를 써서 정의 합니다.</p>
</li>
</ul>
<h3 id="이미-정의된-매크로">이미 정의된 매크로</h3>
<ul>
<li>매크로 이외에 이미 정의가 약속되어 있는 매크로명이 있다.</li>
<li>컴파일러나 버전에 다를 수 있다.</li>
<li>디버깅에 유용한 매크로</li>
</ul>
<table>
<thead>
<tr>
<th>매크로</th>
<th>기능</th>
</tr>
</thead>
<tbody><tr>
<td><strong>FILE</strong></td>
<td>전체 디렉터리 경로를 포함한 파일명</td>
</tr>
<tr>
<td><strong>FUNCTION</strong></td>
<td>매크로명이 사용된 함수 이름</td>
</tr>
<tr>
<td><strong>LINE</strong></td>
<td>매크로명이 사용된 행 번호</td>
</tr>
<tr>
<td><strong>DATE</strong></td>
<td>컴파일을 시작한 날짜</td>
</tr>
<tr>
<td><strong>TIME</strong></td>
<td>컴파일을 시작한 시간</td>
</tr>
</tbody></table>
<ul>
<li><p>19-4.c  : 이미 정의된 매크로 기능</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void func(void);

  int main(void)
  {
      printf(&quot;컴파일 날짜와 시간 : %s, %s\\n\\n&quot;, __DATE__, __TIME__);
      printf(&quot;파일명 : %s\\n&quot;, __FILE__);
      printf(&quot;함수명 : %s\\n&quot;, __FUNCTION__);
      printf(&quot;행번호 : %d\\n&quot;, __LINE__);

  #line 100 &quot;macro.c&quot;   // 행 번호를 100부터 시작, 파일명은 macro.c로 표시
      func();           // 여기부터 행 번호는 100으로 시작

      return 0;
  }

  void func(void)
  {
      printf(&quot;\\n&quot;);
      printf(&quot;파일명 : %s\\n&quot;, __FILE__);
      printf(&quot;함수명 : %s\\n&quot;, __FUNCTION__);
      printf(&quot;행번호 : %d\\n&quot;, __LINE__);
  }
</code></pre>
<pre><code>  컴파일 날짜와 시간 : Jan 22 2021, 16:36:15

  파일명 : /tmp/tmpcdx_h0jb.c
  함수명 : main
  행번호 : 10

  파일명 : macro.c
  함수명 : func
  행번호 : 110
</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b97a9b8a-0707-4767-8061-cf857d3b3d00/image.png" /></p>
<h2 id="매크로-연산자-과-">매크로 연산자 #과 <code>##</code></h2>
<ul>
<li><p>인수를 특별한 방법으로 치환</p>
</li>
<li><p>#: 매크로 함수의 인수를 문자열로 치환</p>
</li>
<li><p>'##' : 두 인수를 붙여서 치환</p>
</li>
<li><p>19-5.c  : #, ## 사용한 매크로 함수</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  #define PRINT_EXPR(x) printf(#x &quot; = %d\n&quot;, x)
  #define NAME_CAT(x, y) (x ## y)

  int main(void)
  {
      int a1, a2;

      NAME_CAT(a, 1) = 10;     // (a1) = 10;
      NAME_CAT(a, 2) = 20;     // (a2) = 20;
      PRINT_EXPR(a1 + a2);     // printf(&quot;a1 + a2&quot; &quot; = %d\\n&quot;, a1 + a2);
      PRINT_EXPR(a2 - a1);     // printf(&quot;a2 - a1&quot; &quot; = %d\\n&quot;, a2 - a1);

      return 0;
  }
</code></pre>
<pre><code>  a1 + a2 = 30
  a2 - a1 = 10
</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/620b9cc1-b4d2-45e3-a4b8-f60445bbe734/image.png" /></p>
<h3 id="조건부-컴파일-지시자">조건부 컴파일 지시자</h3>
<ul>
<li><p>소스 코드를 조건에 따라 선택적으로 컴파일</p>
</li>
<li><p>전처리 지시자를 다양한 방법으로 조합하여 사용</p>
</li>
<li><p>19-6.c  : 조건부 컴파일</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  #define VER 7          // 치환될 부분이 있는 매크로명 정의
  #define BIT16          // 치환될 부분이 없는 매크로명 정의

  int main(void)
  {
      int max;

  #if VER &gt;= 6           // 매크로명 VER이 6 이상이면
      printf(&quot;버전 %d입니다.\\n&quot;, VER);    // 이 문장 컴파일
  #endif                 // #if의 끝

  #ifdef BIT16           // 매크로명 BIT16이 정의되어 있으면
      max = 32767;       // 이 문장 컴파일
  #else                  // BIT16이 정의되어 있지 않으면
      max = 2147483647;  // 이 문장 컴파일
  #endif                 // #ifdef의 끝

      printf(&quot;int형 변수의 최댓값 : %d\\n&quot;, max);   // max 출력

      return 0;
  }
</code></pre>
<pre><code>  버전 7입니다.
  int형 변수의 최댓값 : 32767
</code></pre><ul>
<li>조건부 컴파일의 다양한 사용법
<img alt="" src="https://velog.velcdn.com/images/kym11290306/post/ba2e30ab-fc51-475b-bbda-7ecf4940e35a/image.png" /></li>
</ul>
</li>
</ul>
<pre><code>- 전처리 연산자 defined와  !defined
![](https://velog.velcdn.com/images/kym11290306/post/542ce8bb-0c3f-4a1f-9aac-79b938997e73/image.png)</code></pre><h2 id="pragma-지시자">pragma 지시자</h2>
<ul>
<li><p>컴파일러의 컴파일 방법을 세부적으로 제어할때 사용.</p>
<ul>
<li>pack : 구조체의 패딩 바이트 크기를 결정</li>
<li>warning : 경고메시지를 관리</li>
</ul>
</li>
<li><p>19-7-c : #pragma 를 사용한 바이트 얼라인먼트 변경</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  #pragma pack(push, 1)    // 바이트 얼라인먼트를 1로 바꿈
  typedef struct
  {
      char ch;
      int in;
  } Sample1;

  #pragma pack(pop)        // 바꾸기 전의 바이트 얼라인먼트 적용
  typedef struct
  {
      char ch;
      int in;
  } Sample2;

  int main(void)
  {
      printf(&quot;Sample1 구조체의 크기 : %d바이트\\n&quot;, sizeof(Sample1));
      printf(&quot;Sample2 구조체의 크기 : %d바이트\\n&quot;, sizeof(Sample2));

      return 0;
  }
</code></pre>
<pre><code>  Sample1 구조체의 크기 : 5바이트
  Sample2 구조체의 크기 : 8바이트
</code></pre></li>
<li><p>push는 바이트 얼라이먼트를 바꿀때 현재의 규칙을 기억합니다.</p>
</li>
<li><p>push,pop을 사용하지 않고 크기만 사용하는 것도 가능하다.</p>
</li>
</ul>
<blockquote>
<h1 id="pragma-warningdisable4101">pragma warning(disable:4101);</h1>
</blockquote>
<h1 id="pragma-once">pragma once</h1>
<blockquote>
</blockquote>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>#include는 지정한 파일을 소스 코드에 적절하게 포함시킨다.</li>
<li>#define은 매크로 상수와 매크로 함수를 만들 때 쓴다.</li>
<li>#if, #else, #elif, #ifdef, #ifndef, #endif는 조건부 컴파일을 위해 사용하는 조건부 컴파일 지시자다. 그 외에도 #pragma, #error, #line 등 컴파일 과정을 돕는 다양한 지시자가 있다.</li>
<li>defined, #, ##은 전처리 지시자와 함께 사용하는 전처리 연산자다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0d77f2f5-bd83-4641-a92b-119b66586db6/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/5f44bc1a-457d-4873-abc5-07cfa9a219ad/image.png" /></p>
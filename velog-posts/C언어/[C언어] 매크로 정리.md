<p>C언어 문제를 풀면서, 매크로 함수를 어떻게 구현해야할지 잘 모르겠어서 매크로에 관해 정리를 해보려합니다. 혼자 공부하는 C언어 책으로 독학을 진행하고 있기 때문에 책 내용과 인터넷을 참고하여 작성해볼 생각입니다.</p>
<hr />
<ul>
<li><code>#define</code> : 매크로명을 정의하는 전처리 지시자<blockquote>
<p>#define 매크로명 치환될_부분</p>
</blockquote>
</li>
</ul>
<p>위와 같은 형식으로 사용합니다.
<code>main()</code> 함수에서 작성한 매크로명이 컴파일 과정에서 매크로명-&gt;치환될 부분으로 자동으로 대입됩니다.</p>
<p>매크로명은 다른 변수명과 쉽게 구분할 수 있도록 관례상 대문자로 쓰며, 치환될 부분은 매크로명과 하나 이상의 빈칸을 둡니다.</p>
<hr />
<h3 id="예제-다양한-매크로-명-사용교재588p">예제) 다양한 매크로 명 사용(교재&gt;588p)</h3>
<pre><code class="language-c">#define _CRT_SECURE_NO_WARNINGS
#include &lt;stdio.h&gt;
#define PI 3.14159
#define LIMIT 10.0
#define MSG &quot;passed!&quot;
#define ERR_PRN printf(&quot;허용 범위를 벗어났습니다!\n&quot;)

int main() {
    double radius, area;
    printf(&quot;반지름을 입력하세요(10 이하) : &quot;);
    scanf(&quot;%lf&quot;, &amp;radius);
    area = PI * radius * radius;
    if (radius &gt; LIMIT) ERR_PRN;
    else printf(&quot;원의 면적 : %.2lf(%s)\n&quot;, area, MSG);

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/daa15469-5377-4a89-adfe-0f102625e9ce/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/17d4d817-ad0b-4d97-a444-6aaa5722e3b1/image.png" /></p>
<hr />
<ul>
<li>매크로명 정의<pre><code class="language-c">#define INTRO &quot;Perfect C Language \
&amp; basic Data Structure&quot;</code></pre>
</li>
<li>매크로명 사용<pre><code class="language-c">printf(&quot;%s&quot;,INTRO);
</code></pre>
</li>
</ul>
<p>// 전처리 과정 이후
printf(&quot;%s&quot;, &quot;Perfect C Language &amp; basic Data Structure&quot;);</p>
<pre><code>
---

### #define 이용한 매크로 함수

매크로 함수는 아래와 같이 정의된다.
&gt; #define 매크로함수명(인수) 치환될부분

매크로 함수도 일반 매크로(`#define`)와 똑같이 전처리 과정에서 인수에 따라 서로 다른 결과값을 갖도록 치환된다.

정확히 말하면 **매크로 함수는 함수가 아니다** 하지만 인수를 주고 함수처럼 쓸 수 있다.

매크로 함수를 만들 때는 매크로 명에 괄호를 열고 인수를 나열해야한다. 왜냐하면 사칙 연산에서는 곱하기, 나누기(`* , /`)가 더하기, 빼기(`+ , -`)보다 우선 순위를 갖기 때문에 인수 값을 그대로 전달하면 원하는 값이 출력되지 않을 수도 있기 때문이다.

---
아래는 방금 내용에 관련된 예제이다.

```c
#include &lt;stdio.h&gt;
#define SUM(a,b) ((a)+(b))
#define MUL(a,b) ((a)*(b))

int main() {
    int a = 10, b = 20;
    int x = 30, y = 40;
    int res;

    printf(&quot;a*b = %d\n&quot;, MUL(a+b, b));
    printf(&quot;x*y = %d\n&quot;, MUL(x, y));
    res = 30 / MUL(2, 5);
    printf(&quot;res : %d\n&quot;,res);

    return 0;
}</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ccccf936-eec9-4be2-9991-b81bc024de0b/image.png" /></p>
<p>만약 인수마다 괄호를 안 쳐주면?</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#define SUM(a,b) (a+b)
#define MUL(a,b) (a*b)

int main() {
    int a = 10, b = 20;
    int x = 30, y = 40;
    int res;

    printf(&quot;a*b = %d\n&quot;, MUL(a+b, b));
    printf(&quot;x*y = %d\n&quot;, MUL(x, y));
    res = 30 / MUL(2, 5);
    printf(&quot;res : %d\n&quot;,res);

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8d5bc398-da51-43a8-ab93-757de6ee8ac2/image.png" /></p>
<hr />
<p>왜 결과값의 차이가 날까?</p>
<p>방금 말했던것 처럼 사칙연산의 우선순위의 영향을 받아서 그렇다.</p>
<ol>
<li>첫 번째 코드</li>
</ol>
<pre><code class="language-c">MUL(a+b,b); 
=&gt; 전처리 과정에서 다음과 같이 변환

    ((a+b)*(b))
=    ((10+20)*(20))
=    (30*20)
=    600</code></pre>
<ol start="2">
<li>두 번째 코드</li>
</ol>
<pre><code class="language-c">MUL(a+b,b); 
=&gt; 전처리 과정에서 다음과 같이 변환

    (a+b*b)
=    (10+20*20)
=    (10+400)
=    410</code></pre>
<p>따라서 인수에는 괄호를 쳐줘야 한다.</p>
<hr />
<h3 id="매크로-연산자-과-">매크로 연산자 <code>#과 ##</code></h3>
<p>이것까지 정리할 생각은 없었지만, 매크로 관련 정리한김에 해야겠다.</p>
<p>사실 코드짤 때 이 개념은 생각나진 않을 것 같지만 개념 정도는 알고 있으면 좋을 것 같다.</p>
<ul>
<li><code>#</code> : 매크로 함수의 인수를 문자열로 치환</li>
<li><code>##</code> : 두 인수를 붙여서 치환</li>
</ul>
<hr />
<p>바로 예제로 들어가보자.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#define PRINT_EXPR(x) printf(#x &quot; = %d\n&quot;,x)
#define NAME_CAT(x,y) (x##y)

int main() {
    int a1, a2;

    NAME_CAT(a, 1) = 10;
    NAME_CAT(a, 2) = 20;
    PRINT_EXPR(a1 + a2);
    PRINT_EXPR(a1 - a2);

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d9737894-bc78-468a-b49c-30264bf1a1a1/image.png" /></p>
<p>위 예제에서, <code>#</code>은 인수를 문자열로 치환하기 때문에 컴파일 과정에서 아래와 같이 바뀐다.</p>
<pre><code class="language-c">    NAME_CAT(a, 1) = 10;
    #define NAME_CAT(x,y) (x##y)
=    a+1 =&gt; ##x = a1

    NAME_CAT(a, 2) = 20;
    #define NAME_CAT(x,y) (x##y)
=    a+2 =&gt; ##x = a2

    PRINT_EXPR(a1 + a2);
    #define PRINT_EXPR(x) printf(#x &quot; = %d\n&quot;,x)
=    #x -&gt; x=&quot;a1+a2&quot;    

    PRINT_EXPR(a1 - a2);
    #define PRINT_EXPR(x) printf(#x &quot; = %d\n&quot;,x)
=    #x -&gt; x=&quot;a1-a2&quot;    </code></pre>
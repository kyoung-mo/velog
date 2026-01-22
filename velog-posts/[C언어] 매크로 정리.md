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


</code></pre>
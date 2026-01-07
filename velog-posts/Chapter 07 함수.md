<h2 id="7-1-함수의-작성과-사용">7-1 함수의 작성과 사용</h2>
<ul>
<li><p>함수란 기능을 수행하는 코드 단위</p>
</li>
<li><p>main함수, printf, scanf함수</p>
</li>
<li><p>표준 라이브러리 함수 : 특정 기능을 미리 약속하고 프로그램에서 바로 사용할 수 있게 구현한 함수.</p>
</li>
<li><p>함수를 만들려면 3가지 요소</p>
<ul>
<li><strong>함수정의</strong> : 함수을 실제 코드로 만드는 것이며 기능을 구현합니다.</li>
<li><strong>함수호출</strong> : 함수 호출을 해야지 함수를 사용할 수 있습니다.</li>
<li><strong>함수선언</strong> : 프로그램의 상단에서 어떤 함수를 사용할 것이라고 컴파일러에 정보를 주는 역할</li>
</ul>
</li>
</ul>
<h3 id="함수-정의">함수 정의</h3>
<h3 id="3가지-질문">3가지 질문</h3>
<pre><code>- 함수의 기능에 맞는 이름?
- 함수가 기능을 수행하는데 필요한 데이터?
- 함수가 수행된 후의 결과는?</code></pre><h3 id="함수정의--함수-원형-function-prototype">함수정의 : 함수 원형 (function prototype)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/498c8586-35ab-4393-8612-0b5f2dd3866c/image.png" /></p>
<pre><code>- 함수명 : 함수의 기능에 맞는 이름
- 매개변수 : 함수가 기능을 수행하는 데 필요한 데이터
- 반환형 : 함수가 수행된 후의 결과
</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/58bfbbde-aaa6-47c7-8e92-c8326e9e92e1/image.png" /></p>
<ul>
<li><p>ex7-1.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int sum(int x, int y);       // sum 함수 선언 : 186쪽에서 설명합니다.

  int main(void)               // main 함수 시작
  {
      int a = 10, b = 20;
      int result;              // 두 정수를 더한 결과(result)를 저장할 변수

      result = sum(a, b);      // sum 함수 호출
      printf(&quot;result : %d\\n&quot;, result);

      return 0;
  }                            // main 함수의 끝

  int sum(int x, int y)        // sum 함수 정의 시작
  {
      int temp;                // 두 정수의 합을 잠시 저장할 변수

      temp = x + y;            // x와 y의 합을 temp에 보관

      return temp;             // temp의 값을 반환
  }                            // sum 함수의 끝
</code></pre>
<pre><code>  result : 30
</code></pre></li>
</ul>
<h3 id="함수속-변수명">함수속 변수명</h3>
<ul>
<li>컴파일러는 변수명의 사용범위를 선언한 블록 내부로 제한합니다</li>
</ul>
<pre><code class="language-c"> int sum(int a, int b)
 {
     int result;

     result = a + b;
     return result;

 }</code></pre>
<hr />
<h2 id="함수-호출과-반환">함수 호출과 반환</h2>
<h3 id="함수-호출">함수 호출</h3>
<ul>
<li>함수를 호출할 때 함수에 필요한 데이터를 괄호 안에 넣어주는데 이를 <strong>인수</strong>(argument)라 한다.</li>
</ul>
<pre><code class="language-c">result=sum(a,b);</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/686b030d-4871-4727-861f-345a9a71e226/image.png" /></p>
<h3 id="함수-반환">함수 반환</h3>
<ul>
<li>호출된 함수가 실행을 끝내고 반환할때 return문 사용.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b799382a-753a-4b1f-a913-c3398f074fa1/image.png" /></p>
<h3 id="함수-선언">함수 선언</h3>
<ul>
<li>컴파일러가 새로 만든 함수를 인식할 수 있도록 알리는 역할.</li>
<li>함수 원형에 세미콜론을 붙였을 뿐.</li>
<li>함수 선언은 main함수 앞에 한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8eb4f93b-5336-4c6b-ae3b-1118dc84f4c0/image.png" /></p>
<h3 id="함수정의가-있는데-왜-함수-선언이-필요할까">함수정의가 있는데 왜 함수 선언이 필요할까?</h3>
<ul>
<li>함수호출한자리에 <strong>반환값</strong>과 같은 형태의 저장 공간을 준비</li>
<li>반환형을 컴파일러에게 미리 알려주어야 한다.</li>
<li>함수호출이전에 함수를 정의해도 된다.</li>
<li>분할 컴파일하는 프로그램에서 호출하는 함수와 호출되는 함수가 서로 다른 파일에 있으면 반드시 함수선언이 필요합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/43678541-8ca5-4afd-8527-d2427f9dd4bd/image.png" /></p>
<ul>
<li>이유 2<ul>
<li>함수 호출 형식에 문제가 없는지 검사</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/00d2bc8b-796e-4877-a0eb-3def75ed387a/image.png" /></p>
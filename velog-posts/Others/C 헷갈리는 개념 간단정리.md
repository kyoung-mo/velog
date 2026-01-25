<h1 id="1장">1장</h1>
<h3 id="컴파일-과정">컴파일 과정</h3>
<ul>
<li><code>Source.c</code> --(전처리)--&gt; <code>전처리된 소스파일</code> --(컴파일)--&gt; <code>개체 파일</code> --(링크)--&gt; <code>실행 파일</code></li>
</ul>
<hr />
<h1 id="3장">3장</h1>
<h3 id="초기화">초기화</h3>
<pre><code class="language-c">// memset을 이용한 초기화
memset(ary1, 0, sizeof(ary1)); // 모든 원소를 0으로 초기화</code></pre>
<hr />
<h1 id="4장">4장</h1>
<ul>
<li>연산자(operator) , 피연산자(operand)</li>
<li>ALU(Arithmetic Logic Unit) : CPU의 산술논리 연산장치</li>
<li>레지스터(register) : CPU의 메모리, 연산할 데이터와 연산 후의 결과를 임시로 저장</li>
<li>load : 메인 메모리에서 레지스터(CPU의 메모리)로 값을 복사하는 과정</li>
<li>store : 연산 완료된 값을 레지스터(CPU의 메모리)에서 메인 메모리로 복사하는 과정</li>
</ul>
<hr />
<h1 id="5장">5장</h1>
<pre><code class="language-c">switch(ch)
{
case 'a':
case 'b':
    printf(&quot;ch는 a 혹은 b입니다.\n); // a일 경우에도 출력
    break;
case 'c':
    printf(&quot;ch는 c입니다.\n&quot;);
    break;
default:
    printf(&quot;a도 b도 c도 아닙니다.\n&quot;);
    break;
}</code></pre>
<hr />
<h1 id="16장">16장</h1>
<ul>
<li>동적 할당<pre><code class="language-c">int *arr;    // arr을 int* 형으로 선언
arr = (int *)malloc(sizeof(int)*n);    // 변수 대입을 위해 (int*)로 형변환</code></pre>
</li>
<li>명령행 인수 : 명령행에서 프로그램을 실행시킬 때 프로그램의 이름 외에 함께 주는 프로그램에 필요한 정보<pre><code class="language-c">int main(int argc, char** argv)
// argc : 명령행 인수의 개수. 프로그램 이름을 포함하므로 항상 1이상
// argv : 명령행 인수를 가진 이차원 배열. 문자열을 가진 배열이라고 생각하면 됨</code></pre>
</li>
</ul>
<hr />
<h1 id="17장">17장</h1>
<ul>
<li>structure : 형태가 서로 다른 변수를 묶는 자료형.
한번 형태가 정의되면 그 이후부터는 구조체 변수, 구조체 배열, 구조체 포인터 등으로 활용 가능</li>
<li>열거형(enumeration) : 변수에 저장할 수 있는 정수 값을 기호로 정의해 나열하는 자료형<pre><code class="language-c">enum state{FEVER, COUGH, RUNNY_NOSE};
enum season{SPRING, SUMMER, FALL, WINTER};</code></pre>
</li>
</ul>
<hr />
<h1 id="18장">18장</h1>
<ul>
<li>전처리(preprocessing) : 전처리 지시자 ( <code>#include</code> , <code>#define</code> 등)에 따라 소스파일을 가공하는 과정</li>
</ul>
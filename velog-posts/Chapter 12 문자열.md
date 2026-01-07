<h2 id="12-1-문자열과-포인터">12-1 문자열과 포인터</h2>
<h3 id="문자열-상수-구현-방법">문자열 상수 구현 방법</h3>
<ul>
<li><p>12-1.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      printf(&quot;apple이 저장된 시작 주소 값 : %p\n&quot;, &quot;apple&quot;);    // 주소 값 출력
      printf(&quot;두 번째 문자의 주소 값 : %p\n&quot;, &quot;apple&quot; + 1);     // 주소 값 출력
      printf(&quot;첫 번째 문자 : %c\n&quot;, *&quot;apple&quot;);                  // 간접 참조 연산
      printf(&quot;두 번째 문자 : %c\n&quot;, *(&quot;apple&quot; + 1));            // 포인터 연산식
      printf(&quot;배열로 표현한 세 번째 문자 : %c\n&quot;, &quot;apple&quot;[2]);  // 배열 표현식

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/1928dd0c-8b31-480d-abb7-c45dd95c22d0/image.png" /></p>
<h3 id="char-포인터로-문자열-사용">char 포인터로 문자열 사용</h3>
<ul>
<li><p>12-2.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      char* dessert = &quot;apple&quot;;                     // 포인터에 문자열 초기화

      printf(&quot;오늘 후식은 %s입니다.\n&quot;, dessert);  // 문자열 출력
      dessert = &quot;banana&quot;;                          // 새로운 문자열 대입
      printf(&quot;내일 후식은 %s입니다.\n&quot;, dessert);  // 바뀐 문자열 출력

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ece1c1df-aa90-4c17-96e1-3dbb6c5fa5be/image.png" /></p>
<h3 id="scanf-함수를-사용한-문자열-입력">scanf 함수를 사용한 문자열 입력</h3>
<ul>
<li><p>12-3.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      char str[80];

      printf(&quot;문자열 입력 : &quot;);
      scanf(&quot;%s&quot;, str);                      // %s를 사용하고 배열명을 준다.
      printf(&quot;첫 번째 단어 : %s\n&quot;, str);    // 배열에 입력된 문자열 출력
      scanf(&quot;%s&quot;, str);
      printf(&quot;버퍼에 남아 있는 두 번째 단어 : %s\n&quot;, str);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/5fe89771-15b7-40f6-9a9e-3fdaba195cd2/image.png" /></p>
<h3 id="gets-함수를-사용한-문자열-입력">gets 함수를 사용한 문자열 입력</h3>
<ul>
<li><p>12-4.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      char str[80];

      printf(&quot;공백이 포함된 문자열 입력 : &quot;);
      gets(str);                  // 배열명으로 주고 함수 호출
      printf(&quot;입력한 문자열은 %s입니다.&quot;, str);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3900670a-54d8-4002-b7b7-6c9b41826b26/image.png" /></p>
<h3 id="fgets-함수를-사용한-문자열-입력">fgets 함수를 사용한 문자열 입력</h3>
<ul>
<li><p>12-5.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  // 나중에 입력할 공간입니다. 

  int main(void)
  {
      char str[80];

      printf(&quot;공백이 포함된 문자열 입력: &quot;);
      fgets(str, sizeof(str), stdin);              // 문자열 입력
      // 나중에 입력할 공간입니다. 
      printf(&quot;입력된 문자열은 %s입니다. \n&quot;, str);   // 문자열 출력

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/63235b50-3914-45f0-8853-330ad9aeefdb/image.png" /></p>
<h3 id="표준-입력-함수의-버퍼-공유-문제">표준 입력 함수의 버퍼 공유 문제</h3>
<ul>
<li><p>12-6.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      int age;                  // 나이를 저장할 변수
      char name[20];            // 이름을 저장할 배열

      printf(&quot;나이 입력 : &quot;);
      scanf(&quot;%d&quot;, &amp;age);        // scanf 함수로 나이 입력

      printf(&quot;이름 입력 : &quot;);
      gets(name);               // gets 함수로 이름 입력
      printf(&quot;나이 : %d, 이름 : %s\n&quot;, age, name);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/028ac37d-6d07-4c9d-9b06-5be792322dca/image.png" /></p>
<ul>
<li>버퍼를 clear하는 방법<ul>
<li>scanf(&quot;%*c&quot;);</li>
<li>getchar();</li>
<li>fgetc(stdin);</li>
</ul>
</li>
</ul>
<h3 id="문자열을-출력하는-puts-fputs-함수">문자열을 출력하는 puts, fputs 함수</h3>
<ul>
<li><p>12-7.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      char str[80] = &quot;apple juice&quot;;   // 배열에 문자열 초기화
      char* ps = &quot;banana&quot;;            // 포인터에 문자열 연결

      puts(str);              // apple juice 출력하고 줄 바꿈
      fputs(ps, stdout);      // banana만 출력
      puts(&quot;milk&quot;);           // banana에 이어 milk 출력

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0abd25a5-a59d-4cbf-a141-f88d6b078025/image.png" /></p>
<h3 id="직접-구현해-보는-gets함수">직접 구현해 보는 gets함수</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
    int i = 0;
    char str[20];
    char ch;

    do
    {
        ch = getchar();
        str[i] = ch;
        i++;
    } while(ch !='\n');

    return 0;
}</code></pre>
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>문자열은 첫 번째 문자가 저장된 메모리의 주소로 바뀐다.</li>
<li>scanf 함수는 중간에 공백이 포함된 문자열을 입력할 수 없다.</li>
<li>gets 함수는 한 줄의 데이터를 char 배열에 저장한다.</li>
<li>fgets 함수는 배열의 크기를 검사하는 문자열 입력 함수다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/2fda1b7a-fbd0-4445-bf9c-a4289c16e255/image.png" /></p>
<h2 id="12-2-문자열-연산-함수">12-2 문자열 연산 함수</h2>
<p>문자열을 연산할 때는 문자열 연산에 사용하는 함수를 따로 사용해야 함</p>
<h3 id="문자열을-대입하는-strcpy-함수">문자열을 대입하는 strcpy 함수</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d656b452-5e32-422c-be88-abf3365c5033/image.png" /></p>
<ul>
<li><p>12-8.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;                        // strcpy 함수를 사용하기 위해 인클루드함

  int main(void)
  {
      char str1[6] =  &quot;apple&quot;;         // char 배열에 문자열 초기화
      char str2[11] = &quot;strawberry&quot;;             // char 배열에 문자열 초기화
      char* ps1 = &quot;banana&quot;;                  // 포인터로 문자열 상수 연결
      char* ps2 = str2;                      // 포인터로 배열 연결

      printf(&quot;최초 문자열 : %s\n&quot;, str1);
      strcpy(str1, str2);                    // 다른 char 배열의 문자열 복사
      printf(&quot;바뀐 문자열 : %s\n&quot;, str1);

      strcpy(str1, ps1);                     // 문자열 상수를 연결한 포인터 사용
      printf(&quot;바뀐 문자열 : %s\n&quot;, str1);

      strcpy(str1, ps2);                     // 배열을 연결한 포인터 사용
      printf(&quot;바뀐 문자열 : %s\n&quot;, str1);

      strcpy(str1, &quot;banana&quot;);                // 문자열 상수 사용
      printf(&quot;바뀐 문자열 : %s\n&quot;, str1);

      return 0;
  }</code></pre>
<pre><code class="language-c">  최초 문자열 : strawberry
  바뀐 문자열 : apple
  바뀐 문자열 : banana
  바뀐 문자열 : apple
  바뀐 문자열 : banana</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/58980de4-8c19-41d3-8dce-84a68604f419/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/dcb16be7-0113-4d87-924c-296abed5d68f/image.png" /></p>
<p>💡 사용하면 안됨</p>
<p>   strcpy(&quot;banana&quot;, &quot;apple&quot;) ⇒ 문자열 상수를 바꾸고자 함
   strcpy(ps1, &quot;apple&quot;) ⇒ ps1이 연결하고 있는 문자열 상수가 바뀜 ⇒ 컴파일은 되나, 실행시 에러발생</p>
<p>💡
strcpy함수를 사용할 때는 다음 2가지만 기억합니다.<br />첫 번째 인수는 char 배열이나 배열명을 저장한 포인터만 사용할 수 있다.
두 번째 인수는 문자열의 시작 위치를 알 수 있다면 어떤 것이든 사용할 수 있다.</p>
<ul>
<li><p>mystrcpy(ary1, ary2) ＝＞ strcpy사용하지 않고, max 80까지</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int my_strcpy(char* str2, char* str1)
  {
      int i = 0;
      while (1)
      {
          str2[i] = str1[i];
          if (str1[i] == '\0')
              return i;
          else
              i++;

      }

  }

  int main(void)
  {
      char str1[80] = &quot;qwgserfhtrsehr&quot;;
      char str2[80] = &quot;ffrrrrrrr&quot;;
      printf(&quot;%s %s \n&quot;, str1, str2);
      my_strcpy(str1, str2);
      printf(&quot;%s %s \n&quot;, str1, str2);


</code></pre>
</li>
</ul>
<pre><code>}

```</code></pre><h3 id="원하는-개수의-문자만을-복사하는-strncpy-함수">원하는 개수의 문자만을 복사하는 strncpy 함수</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/cb5d728d-07fc-459f-8f89-865ef1e15128/image.png" /></p>
<ul>
<li><p>12-9.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;                // strncpy 함수 사용을 위한 헤더 파일 포함

  int main(void)
  {
      char str[20] = &quot;mango tree&quot;;   // 배열 초기화

      strncpy(str, &quot;apple-pie&quot;, 5);  // &quot;apple-pie&quot;에서 다섯 문자만 복사

      printf(&quot;%s\n&quot;, str);           // 복사 받은 문자열 출력

      return 0;
  }</code></pre>
<pre><code class="language-c">  apple tree</code></pre>
</li>
</ul>
<h3 id="문자열을-붙이는-strcat-strncat-함수">문자열을 붙이는 strcat, strncat 함수</h3>
<pre><code class="language-c">char* strcat(char* destination, const char* source);
/*
문자열을 덧붙인다.
destination 끝에 source 를 더하게 된다. 
이 때, destination 의 맨 마지막 널 문자는 source 의 첫번째 문자가 덮어 씌우게 된다. 
그리고, source 의 마지막 널 문자가 destination 끝에 붙어서 새로운 문자열을 형성하게 된다.
다시말해, destination = &quot;ab&quot; 이고, source=&quot;c&quot; 였다면
strcat 후, destination 은 &quot;abc&quot; 가 된다.
*/

char* strncat(char* destination, const char* source, size_t n);
/*
문자열에 일부 문자들을 덧붙인다.
source 의 처음 num 개의 문자들을 destination 끝에 덧붙인다. 
이 때, destination 끝에는 자동으로 NULL 문자 까지 붙여진다.
만일, source 의 문자열의 길이가 num 보다 작다면, source 의 NULL 문자 까지만 붙여진다.

destination = &quot;abc&quot; source = &quot;bcdef&quot;
strncat(destination, source, 3) -&gt; destination = &quot;abcbcd&quot;
*/</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/fd00da97-51af-4aa2-ab41-bcdd6f4e3201/image.png" /></p>
<ul>
<li><p>12-10.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;      // strcat, strncat 함수 사용을 위한 헤더 파일 포함

  int main(void)
  {
      char str[80] = &quot;straw&quot;;     // 문자열 초기화

      strcat(str, &quot;berry&quot;);       // str 배열에 문자열 붙이기
      printf(&quot;%s\n&quot;, str);
      strncat(str, &quot;piece&quot;, 3);   // str 배열에 3개의 문자 붙이기
      printf(&quot;%s\n&quot;, str);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b7504af5-68c2-44dc-b384-1eddf021df75/image.png" /></p>
<aside>
💡

<ul>
<li>strcat함수 사용시 주의 사항<ol>
<li>메모리를 침범할 수 있습니다. </li>
<li>사용할 때는 배열을 초기화해야 합니다. </aside>

</li>
</ol>
</li>
</ul>
<h3 id="문자열-길이를-계산하는-strlen-함수">문자열 길이를 계산하는 strlen 함수</h3>
<pre><code class="language-c">size_t strlen(const char *str)
/*
const char* 타입의 문자열을 받아서 해당 문자열의 길이를 반환하는 함수입니다.
size_t 타입은 객체나 값이 포함 할수 있는 최대 크기의 데이터를 표현하는 데이터 타입 입니다.
즉, 0이상의 자연수를 출력하는 함수입니다.
*/</code></pre>
<ul>
<li><p>12-11.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;                            // strlen 함수 사용을 위한 헤더 파일 포함

  int main(void)
  {
      char str1[80], str2[80];                   // 두 문자열을 입력할 배열
      char* resp;                                // 문자열이 긴 배열을 선택할 포인터

      printf(&quot;2개의 과일 이름 입력 : &quot;);
      scanf(&quot;%s%s&quot;, str1, str2);                 // 2개의 문자열 입력
      if (strlen(str1) &gt; strlen(str2))           // 배열에 입력된 문자열의 길이 비교
          resp = str1;                           // 첫 번째 배열이 긴 경우 선택
      else
          resp = str2;                           // 두 번째 배열이 긴 경우 선택
      printf(&quot;이름이 긴 과일은 : %s\n&quot;, resp);   // 선택된 배열의 문자열 출력

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/04abd2d2-48ad-44d9-ad3e-b0f73026445a/image.png" /></p>
<aside>
💡

<p>sizeof연산자 Vs strlen함수</p>
<p>sizeof연산자 : 배열에  저장된 무자열 길이와 상관없이 배열 전체 크기 계산</p>
<p>strlen함수 : 배열에서 문자열만 계산</p>
</aside>

<h3 id="문자열을-비교하는-strcmp-strncmp-함수">문자열을 비교하는 strcmp, strncmp 함수</h3>
<p>strcmp 함수는 두 문자열의 사전 순서(사전에 단어가 수록되는 순서)를 판단하여 결과값을 반환. </p>
<p>아스키 코드 값으로 비교( 아스키 코드가 더 큰 쪽이 사전의 뒤에 나오는 문자열)</p>
<pre><code class="language-c">strcmp(str1, str2); ⇒ str1 &gt; str2 = 1  
                       str1 &lt; str2 = -1
                       str1 == str2 =0 </code></pre>
<ul>
<li><p>12-12.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;

  int main(void)
  {
      char str1[80] = &quot;Pear&quot;;
      char str2[80] = &quot;peach&quot;;

      printf(&quot;사전에 나중에 나오는 과일 이름 : &quot;);
      if (strcmp(str1, str2) &gt; 0)    // str1이 str2보다 크면(사전에 나중에 나오면)
          printf(&quot;%s\n&quot;, str1);      // str1 출력
      else                           // str1이 str2보다 크지 않으면
          printf(&quot;%s\n&quot;, str2);      // str2 출력

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/34d973a9-02cd-4229-9e76-9e2897c95041/image.png" /></p>
<p>strncmp(str1, str2, ) → n번째 숫자 순서까지의 단어 아스키 코드 비교</p>
<p>@ 대문자 주의!(대문자의 아스키코드가 소문자보다 작기때문)</p>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>strcpy 함수에서 문자열을 복사 받는 곳은 배열이어야 한다.</li>
<li>strcat 함수로 문자열을 최초로 붙일 때는 초기화를 해야 한다.</li>
<li>strlen 함수로 배열에 저장된 문자열의 길이를 알 수 있다.</li>
<li>strcmp 함수로 문자열의 사전 등록 순서를 확인할 수 있다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트-1">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d7740093-b4d6-4eac-bdd7-0776c9f492a7/image.png" /></p>
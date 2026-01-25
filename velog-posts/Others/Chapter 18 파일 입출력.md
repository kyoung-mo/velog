<pre><code class="language-c">#include&lt;stdio.h&gt;

int main(void)
{
int i, j, n;


printf(&quot;줄수입력 : &quot;);
scanf(&quot;%d&quot;, &amp;n);

for (i = 1; i &lt;= n; i++)
{
    for (j = 1; j &lt;= n - i; j++)
    {
        printf(&quot; &quot;);
    }
    for (j = 1; j &lt;= 2 * i - 1; j++)
    {
            printf(&quot;*&quot;);
    }
        printf(&quot;\\n&quot;);
}

return 0;
</code></pre>
<p>}</p>
<ul>
<li>하드 디스크에 데이터 저장</li>
</ul>
<h3 id="파일-개방과-폐쇄">파일 개방과 폐쇄</h3>
<ul>
<li><p>데이터를 입출력하기 전에 준비하는 과정이 파일 개방.</p>
</li>
<li><p>사용이 끝난 파일은 닫는 과정이 필요하며, 함수 호출로 수행합니다.</p>
</li>
<li><p>fopen, fclose</p>
</li>
<li><p>18-1.c : 파일을 열고 닫는 프로그램</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      FILE* fp;                   // 파일 포인터

      fp = fopen(&quot;a.txt&quot;, &quot;r&quot;);   // a.txt 파일을 읽기 전용으로 개방
      if (fp == NULL)             // fp가 널 포인터면 파일 개방 실패
      {
          printf(&quot;파일이 열리지 않았습니다.\n&quot;);   // 안내 메시지 출력
          return 1;                    // 프로그램 종료
      }
      printf(&quot;파일이 열렸습니다.\n&quot;);
      fclose(fp);                      // 파일 닫기

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d7d39bf9-1ff9-49da-b586-13a0a3f5de38/image.png" /></p>
<pre><code>- fopen 함수가 개방할 파일을 찾는 기본위치는 [현재 작업 디렉토리]이다.
- 다른곳에 있는 파일을 개방하려면 경로를 함께 적습니다.</code></pre><pre><code class="language-c">        fopen(&quot;c:\\source\\a.txt&quot;, &quot;r&quot;); //윈도우의 경우 백슬래시를 2번사용합니다. 
        fopen(&quot;./test2/a.txt&quot;, &quot;r&quot;);  //리눅스의 경우 현재 디렉터리 밑에./형식 사용</code></pre>
<ul>
<li>절대경로 상대경로<ul>
<li>현재 작업 디렉터리를 기준으로 상대경로를 지정하여 사용.</li>
<li>절대경로는 드라이브/모디렉터리에서 부터 시작.</li>
</ul>
</li>
<li>개방모드는 개방할 파일의 용도를 표시하며 기본적인 개방 모드는 다음과 같다.</li>
</ul>
<table>
<thead>
<tr>
<th>개방모드</th>
<th>의미</th>
<th>파일이 있을 때</th>
<th>파일이 없을 때</th>
</tr>
</thead>
<tbody><tr>
<td>r</td>
<td>read</td>
<td>읽기 위해 개방</td>
<td>NULL 널포인터 반환</td>
</tr>
<tr>
<td>w</td>
<td>write</td>
<td>내용을 지우고 쓰기 위해 개방</td>
<td>새로운 파일 생성</td>
</tr>
<tr>
<td>a</td>
<td>append</td>
<td>파일의 끝에 추가하기 위해 개방</td>
<td>새로운 파일 생성</td>
</tr>
</tbody></table>
<ul>
<li><p>fopen 함수가 파일을 찾아 개방하면 파일 포인터를 반환</p>
<ul>
<li><p>실제 파일이 있는 장치와 연결되어 스트림 파일을 메모리에 만듭니다.</p>
</li>
<li><p>스트림 파일에 접근할 수 있도록 파일 포인터를 반환</p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9c849ba2-e4c2-472b-ab8a-0134fa029394/image.png" /></p>
</li>
</ul>
</li>
</ul>
<ul>
<li><p>개방하지 못하면 NULL(널 포인터)을 반환</p>
<ul>
<li><p>NULL은 0번지를 이름으로 정의해서 사용하며, stdio.h에 다음과 같이 정의</p>
<pre><code class="language-c">  #define NULL ((void *)0)</code></pre>
</li>
<li><p>NULL은 포인터를 반환함수에서 예외상황을 알리기 위한 용도이므로 간접 참조 하면 안된다.</p>
</li>
<li><p>결과는 개방모드에 따라 달라짐</p>
<ul>
<li>r모드 : NULL을 반환</li>
<li>w모드 : 내용이 없는 새로운 파일을 만들어 개방, 같은 이름이 있으면 내용지우고 개방</li>
<li>a모드 : 파일 끝에 데이터를 추가</li>
</ul>
</li>
</ul>
</li>
<li><p>개방한 파일을 더 이상 사용하지 않으면 fclose함수로 닫습니다.</p>
<pre><code class="language-c">  int fclose (FILE *);</code></pre>
<ul>
<li><p>닫을 파일의 포인터를 넘겨줍니다.</p>
</li>
<li><p>성공적으로 닫으면 0을 반환, 오류발생하면 EOF을 반환</p>
</li>
<li><p>EOF : End Of FIle ⇒ 오류가 발생하거나, 파일의 데이터를 모두 읽었는지 확인</p>
<pre><code class="language-c">  #define EOF (-1)</code></pre>
</li>
</ul>
</li>
<li><p>파일 개방을 통해 만들어진 스트림 파일은 메모리를 사용합니다.</p>
<ul>
<li>파일 입출력이 끝나면 회수하여 재활용...</li>
</ul>
</li>
</ul>
<h3 id="스트림-파일과-파일-포인터">스트림 파일과 파일 포인터</h3>
<ul>
<li>스트림 파일은 프로그램과 입출력 장치 사이의 다리 역할하는 논리적인 파일.<ul>
<li>파일 입출력은 스트림 파일을 통해서 수행한다.
  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/8b1fe496-637a-496b-bff7-1621dee59842/image.png" /></li>
</ul>
</li>
</ul>
<pre><code>- 문자 배열 형태의 버퍼가 있다.
- 버퍼는 프로그램이 출력한 데이터를 모아서 한꺼번에 출력장치로 보내거나, 입력장치에서 한번에 많은 데이터를 읽어 저장해 놓고 프로그램이 필요한 데이터를 바로 꺼낼수 있도록 준비.
- 버퍼에서 데이터를 읽거나 쓸때 그 위치와 크기가 필요하다.
- 스트림 파일은 이들 정보를 구조체로 묶어 보관
    - 이때 스트림 파일이 사용하는 구조체 이름이 FILE
    - FILE 구조체 변수의 주소를 반환
        - 구현에 따라 여러가지 정보를 포함하며 컴파일러에 따라 다름.
    ![](https://velog.velcdn.com/images/kym11290306/post/dad65452-a362-4c05-a5a6-c620d29099f4/image.png)</code></pre><ul>
<li>스트림 파일 사용의 장점<ul>
<li>입출력 효율을 높이고 장치로부터 독립된 프로그램이 가능<ul>
<li>입출력함수가 장치를 직접 접근하면 입출력이 바뀔때 마다 함수를 수정해야함.</li>
<li>입출력 함수들은 표준화된 스트림 파일로 입출력하고, 장치의 연결은 하드웨어 특성에 따라 운영체제가 담당.
<img alt="" src="https://velog.velcdn.com/images/kym11290306/post/2b82c826-ce72-41f5-8192-b18fd56f7e20/image.png" /></li>
</ul>
</li>
</ul>
</li>
</ul>
<pre><code>- 프로그램과 장치의 입출력 속도 차이를 줄일 수 있다.</code></pre><h3 id="문자-입력-함수-fgetc">문자 입력 함수 fgetc</h3>
<ul>
<li><p>fgetc함수는 파일에서 하나의 문자를 입력하여 반환</p>
</li>
<li><p>a.txt파일을 만들고 안에 &quot;apple&quot;이라는 내용을 입력하고 저장한다.</p>
</li>
<li><p>18-2.c : 파일의 내용을 화면에 출력하기</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      FILE* fp;                   // 파일 포인터 선언
      int ch;                     // 입력한 문자를 저장할 변수

      fp = fopen(&quot;a.txt&quot;, &quot;r&quot;);   // 읽기 전용으로 파일 개방
      if (fp == NULL)             // 파일이 개방되었는지 확인
      {
          printf(&quot;파일이 열리지 않았습니다.\n&quot;);
          return 1;
      }

      while (1)
      {
          ch = fgetc(fp);         // 개방한 파일에서 문자 입력
          if (ch == EOF)          // 함수의 반환값이 EOF면 입력 종료
          {
              break;
          }
          putchar(ch);            // 입력한 문자를 화면에 출력
      }
      fclose(fp);                 // 파일 닫음

      return 0;
  }</code></pre>
<ul>
<li>fgetc함수는 파일 포인터와 연결된 스트림 파일의 버퍼에서 데이터를 가져옴</li>
<li>처음에는 버퍼가 비어 있어서 하드디스크에서 데이터를 가져와 버퍼를 채움
<img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3fa15bc4-6ee5-44ac-8d6e-3588bd9451fe/image.png" /></li>
</ul>
</li>
</ul>
<ul>
<li><p>스트림 파일에는 문자를 입력할 버퍼의 위치를 알려주는 지시자가 있다.</p>
<ul>
<li><p>파일이 개방되면 0으로 초기화되어 입력함수를 읽을 때 그 크기만큼 증가</p>
</li>
<li><p>버퍼의 내용을 위치 지시자가 1씩 증가하면서 차례로 가져온다.</p>
</li>
<li><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a5a42959-faf9-4493-a6cd-1039701a4a4d/image.png" /></p>
</li>
</ul>
</li>
</ul>
<ul>
<li>버퍼의 내용을 모두 읽으면 EOF(-1)를 반환한다.<ul>
<li>파일의 끝을 표시하는 어떤 정보도 있지 않다.</li>
</ul>
</li>
</ul>
<h3 id="문자-출력-함수-fputc">문자 출력 함수 fputc</h3>
<ul>
<li><p>한 문자를 파일로 출력할 때 사용한다.</p>
</li>
<li><p>출력할 문자와 파일 포인터를 인수로 주면 파일로 문자를 출력한다.</p>
</li>
<li><p>18-3.c : 문자열을 한 문자 씩 파일로 출력하기</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      FILE* fp;                    // 파일 포인터 선언
      char str[] = &quot;banana&quot;;       // 출력할 문자열
      int i;                       // 반복 제어 변수

      fp = fopen(&quot;b.txt&quot;, &quot;w&quot;);    // 쓰기 전용으로 개방
      if (fp == NULL)              // 파일 개방 확인
      {
          printf(&quot;파일을 만들지 못했습니다.\n&quot;);
          return 1;
      }

      i = 0;        // 문자 배열의 첫 번째 문자부터 출력
      while (str[i] != '\0')       // 널 문자가 아니면
      {
          fputc(str[i], fp);       // 문자를 파일에 출력
          i++;                     // 다음 문자로 이동
      }
      fputc('\n', fp);
      fclose(fp);                  // 파일 닫음

      return 0;
  }</code></pre>
<ul>
<li>문자열을 한 문자씩 디스크 파일로 출력<ul>
<li>str배열의 문자를 하나씩 개방한 파일에 반복적으로 출력</li>
<li>출력과정에서 스트림 파일의 버퍼를 사용</li>
<li>문자가 하나씩 하드디스크에 직접 저장되는 것이 아니고 버퍼에 데이터를 모은 후 한번에 출력한다.</li>
<li>버퍼의 데이터를 즉시 장치로 출력해야 한다면 fflush 함수를 사용한다.</li>
</ul>
</li>
<li><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/7c998555-5c39-467a-aafb-d669ce62072e/image.png" /></li>
</ul>
</li>
</ul>
<h3 id="기본적으로-개방되는-표준-입출력-스트림-파일">기본적으로 개방되는 표준 입출력 스트림 파일</h3>
<ul>
<li><p>운영체제는 프로그램을 실행할때 3개의 스트림파일을 만든다.</p>
</li>
<li><p>이렇게 만든 스트림은 키보드, 모니터등에 연결하여 입출력함수들이 포인터 없이 사용할 수 있도록 제공한다.</p>
</li>
<li><p>18-4.c : 표준 입출력 스트림을 사용한 문자열 입력</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int ch;                     // 입력한 문자를 저장할 변수

      while (1)
      {
          ch = getchar();         // 키보드에서 문자 입력
          if (ch == EOF)         // &lt;Ctrl&gt; + &lt;Z&gt;로 입력 종료, 리눅스는 ctrl-d
          {
              break;
          }
          putchar(ch);         // 화면에 문자 출력
      }

      return 0;
  }</code></pre>
<ul>
<li>3개의 스트림 파일</li>
<li></li>
</ul>
</li>
</ul>
<table>
<thead>
<tr>
<th>스트림 파일명</th>
<th>용도</th>
<th>연결된 입출력 장치</th>
</tr>
</thead>
<tbody><tr>
<td>stdin</td>
<td>표준 입력 스트림</td>
<td>키보드</td>
</tr>
<tr>
<td>stdout</td>
<td>표준 출력 스트림</td>
<td>모니터</td>
</tr>
<tr>
<td>stderr</td>
<td>표준 에러 스트림</td>
<td>모니터</td>
</tr>
</tbody></table>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d67b840c-fdd6-40f3-9ab1-54d510b2e1d0/image.png" /></p>
<ul>
<li><p>getchar함수는 내부적으로 stdin을 사용하므로 표준 입력 스트림 파일의 버퍼를 통해 입력한다.</p>
<ul>
<li>버퍼에서 첫번째 문자를 가져다 반환한다. 이후 차례로 다음 문자를 반환.</li>
<li>ctrl-z (윈도우), ctrl-d(리눅스)는  EOF를 반환한다.<ul>
<li>운영체제가 기본적으로 개방하는스트림 파일은 scanf, printf, getchar, putchar, gets, puts등은 표준 입출력함수들을 사용하지만 파일 포인터를 인수로 받는 함수도 사용할 수 있다.</li>
<li>18-5.c - stdin과 stdout을 사용한 문자 입출력</li>
</ul>
</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
   int ch;                        // 입력한 문자를 저장할 변수

   while (1)
   {
       ch = fgetc(stdin);        // 키보드에서 문자 입력
       if (ch == EOF)            // &lt;Ctrl&gt; + &lt;Z&gt;로 입력 종료
       {
           break;
       }
       fputc(ch, stdout);        // 화면에 문자 출력
   }

   return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/c2ad9f86-7865-4db1-a0bb-d16072176777/image.png" /></p>
</li>
</ul>
<h3 id="텍스트-파일과-바이너리-파일">텍스트 파일과 바이너리 파일</h3>
<ul>
<li>파일은 데이터의 기록 방식에 따라 텍스트 파일과 바이터리 파일로 나눕니다.<ul>
<li>텍스트파일은 아스키코드로 저장, 그 이외의 방식은 바이너리파일</li>
</ul>
</li>
<li>개방모드에 텍스트 파일은 t, 바이너리 파일은 b를 추가하여 개방합니다.</li>
</ul>
<table>
<thead>
<tr>
<th>개방모드</th>
<th>파일의 용도</th>
</tr>
</thead>
<tbody><tr>
<td>rb</td>
<td>바이너리 파일을 읽기 위해 개방</td>
</tr>
<tr>
<td>wb</td>
<td>바이너리 파일을 쓰기 위해 개방</td>
</tr>
<tr>
<td>ab</td>
<td>바이너리 파일의 끝에 추가하기 위해 개방</td>
</tr>
</tbody></table>
<ul>
<li><p>파일의 형태를 별도로 표시하지 않으면 자동으로 텍스트 파일로 개방.</p>
</li>
<li><p>18-6.c : 파일 형태와 개방 모드가 다른 경우</p>
<pre><code class="language-c">  n#define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      FILE* fp;
      int ary[10] = { 13, 10, 13, 13, 10, 26, 13, 10, 13, 10 };
      int i, res;

      fp = fopen(&quot;a.txt&quot;, &quot;wb&quot;);        // 바이너리 파일로 개방
      for (i = 0; i &lt; 10; i++)
      {
          fputc(ary[i], fp);            // 배열 요소의 각 값에 해당하는 아스키 문자 출력
      }
      fclose(fp);                        // 파일 닫음

      fp = fopen(&quot;a.txt&quot;, &quot;rt&quot;);        // 같은 파일을 텍스트 파일로 개방
      while (1)
      {
          res = fgetc(fp);            // 파일에서 한 문자 입력
          if (res == EOF) break;
          printf(&quot;%4d&quot;, res);            // 입력한 문자의 아스키 코드 값 출력
      }
      fclose(fp);                        // 파일 닫음

      return 0;
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/8c886c2e-a1f5-48d6-aba2-b203ee204623/image.png" /></p>
</li>
</ul>
<pre><code>- fgetc함수는 리턴문자 (\r)를 읽으면 버리고 다음 개행문자(\n) 하나만 입력한다.
    - 윈도우는 운영체제에서 화면에서 줄바꿈을 리턴/개행문자를 이어서 함께 사용.
- fgetc함수는 `윈도우에서ctrl+z(26)`, `리눅스에서 ctrl+d(04)`  에 대한 아스키 코드를 읽으면 파일의 끝으로 인식</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/f7c1aec7-4e58-497f-abda-b4b05ac02412/image.png" /></p>
<ul>
<li>운영체제마다 줄바꿈이 같나?<ul>
<li>운영체제에 따라 줄바꿈이 다르다.</li>
<li>리눅스 : 개행문자 (\n)만 사용</li>
<li>애플 맥OS : 리턴문자 (\r) 사용</li>
<li>윈도우 : 개행문자 (\n) 리턴문자 (\r)</li>
</ul>
</li>
</ul>
<h3 id="개방-모드-fseek-rewind-feof-함수">개방 모드, fseek, rewind, feof 함수</h3>
<ul>
<li>+를 사용하면 읽고 쓰는 작업을 함께 할 수 있다.</li>
</ul>
<table>
<thead>
<tr>
<th>개방모드</th>
<th>파일이 있을 때</th>
</tr>
</thead>
<tbody><tr>
<td>r+</td>
<td>텍스트 파일에 읽고 쓰기 위해 개방</td>
</tr>
<tr>
<td>w+</td>
<td>텍스트 파일의 내용을 지우고 읽거나 쓰기 위해 개방</td>
</tr>
<tr>
<td>a+</td>
<td>텍스트 파일을 읽거나 파일의 끝에 추가하기 위해 개방</td>
</tr>
<tr>
<td>rb+</td>
<td>바이너리 파일에 읽고 쓰기 위해 개방</td>
</tr>
<tr>
<td>wb+</td>
<td>바이너리 파일의 내용을 지우고 읽거나 쓰기 위해 개방</td>
</tr>
<tr>
<td>ab+</td>
<td>바이너리 파일을 읽거나 파일의 끝에 추가하기 위해 개방</td>
</tr>
</tbody></table>
<ul>
<li><p><del>18-7.c : a+모드로 파일의 내용을 확인하며 출력</del></p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;

  int main(void)
  {
      FILE* fp;
      char str[20];

      fp = fopen(&quot;a.txt&quot;, &quot;a+&quot;);                // 읽기 가능한 추가 모드로 개방
      if (fp == NULL)                           // 파일 개방 확인
      {
          printf(&quot;파일을 만들지 못했습니다.\n&quot;);
          return 1;
      }

      while (1)
      {
          printf(&quot;과일 이름 : &quot;);
          scanf(&quot;%s&quot;, str);                     // 키보드로 과일 이름 입력
          if (strcmp(str, &quot;end&quot;) == 0)          // end 입력 시 종료
          {
              break;
          }
          else if (strcmp(str, &quot;list&quot;) == 0)    // list를 입력하면 파일의 내용 확인
          {
              fseek(fp, 0, SEEK_SET);           // 버퍼의 위치 지시자를 맨 처음으로 이동
              while (1)
              {
                  fgets(str, sizeof(str), fp);  // 과일 이름을 읽는다.
                  if (feof(fp))                 // 파일의 내용을 모두 읽으면 종료
                  {
                      break;
                  }
                  printf(&quot;%s&quot;, str);            // 읽은 과일 이름을 화면 출력
              }
          }
          else
          {
              fprintf(fp, &quot;%s\n&quot;, str);         // 입력한 과일 이름을 파일에 출력
          }
      }
      fclose(fp);

      return 0;
  }</code></pre>
<ul>
<li>파일의 입력과 출력을 서로 전환할 때마다 fseek함수를 호출해야 한다.<ul>
<li>fprint함수는 스트림 파일의 버퍼에 데이터를 출력해놓는데, 이때 버퍼의 데이터가 있는 상태에서 하드디스크로부터 데이터를 입력하게 되면 입출력 순서가 꼬인다.</li>
<li>버퍼의 데이터를 하드디스크로 옮기고 버퍼를 읽기 위한 공간을 설정 후 하드디스크의 데이터를 처음부터 다시 읽는다.</li>
</ul>
</li>
<li>fseek 함수는 + 모드에서 읽고 쓰기를 바꿀 때 필요하다.
  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/53a15fbc-2822-4eff-97ca-8dea9a506cf6/image.png" /></li>
</ul>
</li>
</ul>
<pre><code>    - 매크로명은 값대신에 사용할 수 있는 이름으로 전처리 과정에서 약속된 정수로 변경된다.
- feof 함수는 파일의 끝이면 참(0이 아닌 값)을 반환한다.</code></pre><hr />
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>fopen 함수가 파일을 개방하면 메모리에 스트림 파일을 만든다.</li>
<li>스트림 파일은 프로그램과 장치를 연결하며 버퍼에 데이터를 저장한다.</li>
<li>파일 입출력 함수는 스트림 파일을 통해 입출력을 수행한다.</li>
<li>fclose 함수는 개방한 스트림 파일을 메모리에서 제거한다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/5bed7f36-1cab-43a9-803c-6371bd6d5907/image.png" /></p>
<hr />
<h2 id="18-2-다양한-파일-입출력-함수">18-2 다양한 파일 입출력 함수</h2>
<ul>
<li>파일의 데이터는 fgetc함수 하나로 모두 읽을 수 있고, fputc함수로 모두 출력할 수 있다.</li>
<li>한번의 함수 호출로 한 줄씩 읽거나 쓰면?</li>
</ul>
<h3 id="fgets와-fputs--한-줄씩-입출력">fgets와 fputs : 한 줄씩 입출력</h3>
<ul>
<li><p>fgets : 파일에서 데이터를 한줄씩 입력할때</p>
</li>
<li><p>fputs : 문자열을 파일에 출력할 때</p>
</li>
<li><p>18-8.c : 여러 줄의 문장을 입력하여 한 줄로 출력</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;

  int main(void)
  {
      FILE* ifp, * ofp;                  // 파일 포인터 선언
      char str[80];                      // 입력한 문자열을 저장할 배열
      char* res;                         // fgets 함수의 반환값을 저장할 변수

      ifp = fopen(&quot;a.txt&quot;, &quot;r&quot;);         // 입력 파일을 읽기 전용으로 개방
      if (ifp == NULL)                   // 개방 여부 확인  ,  
      {
          printf(&quot;입력 파일을 열지 못했습니다.\n&quot;);
          return 1;
      }

      ofp = fopen(&quot;b.txt&quot;, &quot;w&quot;);         // 출력 파일을 쓰기 전용으로 개방
      if (ofp == NULL)                   // 개방 여부 확인 EOF사용하면 계속출력, 파일사이즈 커짐
      {
          printf(&quot;출력 파일을 열지 못했습니다.\n&quot;);
          return 1;
      }

      while (1)                          // 문자열을 입력하고 출력하는 과정 반복
      {
          res = fgets(str, sizeof(str), ifp);
          if (res == NULL)               // 반환값이 널 포인터면 반복 종료
          {
              break;
          }
          str[strlen(str) - 1] = '\0';   // 개행 문자 제거
          fputs(str, ofp);
          fputs(&quot; &quot;, ofp);
      }

      fclose(ifp);        // 입력 파일 닫기
      fclose(ofp);        // 출력 파일 닫기

      return 0;
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3be5e7b6-928e-4674-87fb-032647221cba/image.png" /></p>
</li>
</ul>
<pre><code>![](https://velog.velcdn.com/images/kym11290306/post/444fbb48-4458-43e5-8148-631ce814f422/image.png)</code></pre><ul>
<li>왜 fgets, fputs를 사용해야 하나?<ul>
<li>gets,puts는 사용하기 좋으나, gets함수는 입력할 저장 공간의 크기를 인수로 줄 수 없으므로 문자열을 입력할 때 할당하지 않은 메모리 공간을 침범할 가능성이 있습니다.</li>
</ul>
</li>
</ul>
<h3 id="fscanf-fprintf--다양한-형태의-입출력">fscanf, fprintf : 다양한 형태의 입출력</h3>
<ul>
<li><p>파일에 저정된 문자열을 숫자로 변환하여 입력할때는 fscanf함수를 사용.</p>
</li>
<li><p>반대로 정수나 실수를 쉽게 파일에 출력할때는 fprintf함수를 사용</p>
</li>
<li><p>18-9.c : 다양한 자료형을 형식에 맞게 입출력</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      FILE* ifp, * ofp;                // 파일 포인터 선언
      char name[20];                    // 이름
      int kor, eng, math;                // 세 과목 점수
      int total;                        // 총점
      double avg;                        // 평균
      int res;                        // fscanf 함수의 반환값 저장

      ifp = fopen(&quot;a.txt&quot;, &quot;r&quot;);      // 입력 파일을 읽기 전용으로 개방
      if (ifp == NULL)                // 개방 여부 확인
      {
          printf(&quot;입력 파일을 열지 못했습니다.\n&quot;);
          return 1;
      }

      ofp = fopen(&quot;b.txt&quot;, &quot;w&quot;);      // 출력 파일을 쓰기 전용으로 개방
      if (ofp == NULL)                // 개방 여부 확인
      {
          printf(&quot;출력 파일을 열지 못했습니다.\n&quot;);
          return 1;
      }

      while (1)
      {
          res = fscanf(ifp, &quot;%s%d%d%d&quot;, name, &amp;kor, &amp;eng, &amp;math);  // 데이터 입력
          if (res == EOF)             // 파일의 데이터를 모두 읽으면 EOF 반환
          {
              break;
          }
          total = kor + eng + math;   // 총점 계산
          avg = total / 3.0;          // 평균 계산
          fprintf(ofp, &quot;%s%5d%7.1lf\n&quot;, name, total, avg);   // 이름, 총점, 평균 출력
      }

      fclose(ifp);                    // 입력 파일 닫기
      fclose(ofp);                    // 출력 파일 닫기

      return 0;
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e89a6023-aa77-490a-8662-f498c535e49e/image.png" /></p>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/2ead335c-5b36-472f-a738-92578d881d43/image.png" /></p>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b13cac05-86f9-4d05-9cf3-0189116647e2/image.png" /></p>
</li>
</ul>
<h3 id="스트림-파일의-버퍼-공유-문제와-fflush-함수">스트림 파일의 버퍼 공유 문제와 fflush 함수</h3>
<pre><code class="language-c">#define _CRT_SECURE_NO_WARNINGS
#include &lt;stdio.h&gt;
#include &lt;string.h&gt;

int main(void)
{
FILE* ifp, * ofp;                  // 파일 포인터 선언
char str[80];                      // 입력한 문자열을 저장할 배열
char* res;                         // fgets 함수의 반환값을 저장할 변수


ifp = fopen(&quot;a.txt&quot;, &quot;r&quot;);         // 입력 파일을 읽기 전용으로 개방
if (ifp == NULL)                   // 개방 여부 확인  ,
{
    printf(&quot;입력 파일을 열지 못했습니다.\\n&quot;);
    return 1;
}

ofp = fopen(&quot;b.txt&quot;, &quot;w&quot;);         // 출력 파일을 쓰기 전용으로 개방
if (ofp == NULL)                   // 개방 여부 확인 EOF사용하면 계속출력, 파일사이즈 커짐
{
    printf(&quot;출력 파일을 열지 못했습니다.\\n&quot;);
    return 1;
}

while (1)                          // 문자열을 입력하고 출력하는 과정 반복
{
    res = fgets(str, sizeof(str), ifp);
    if (res == NULL)               // 반환값이 널 포인터면 반복 종료
    {
        break;
    }
    str[strlen(str) - 1] = '\\0';   // 개행 문자 제거
    fputs(str, ofp);
    fputs(&quot; &quot;, ofp);
}

fclose(ifp);        // 입력 파일 닫기
fclose(ofp);        // 출력 파일 닫기

return 0;
</code></pre>
<p>}</p>
<ul>
<li><p>스트림 파일을 사용하는 입출력 함수들이  버퍼를 공유하면 예상과 다른 결과가 나온다.</p>
</li>
<li><p>18-10.c : 버퍼를 공유함으로 인해 발생하는 문제</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      FILE* fp;                       // 파일 포인터
      int age;                        // 나이 저장 변수
      char name[20];                  // 이름 저장 배열

      fp = fopen(&quot;a.txt&quot;, &quot;r&quot;);       // 파일 개방

      fscanf(fp, &quot;%d&quot;, &amp;age);         // 나이 입력
      fgets(name, sizeof(name), fp);  // 이름 입력

      printf(&quot;나이 : %d, 이름 : %s&quot;, age, name);  // 입력 데이터 출력
      fclose(fp);                     // 파일 닫음

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/fa3b4933-21ce-4032-a9a0-1e514fbd6a1e/image.png" /></p>
<ul>
<li>나이만 입력한 것처럼 보인다. fscanf함수와 fgets함수가 개행문자를 처리하는 방식이 다르다.</li>
<li>스트림 파일의 버퍼를 비우는 fflush함수로 해결!!</li>
</ul>
<h3 id="fread와-fwrite-함수">fread와 fwrite 함수</h3>
<ul>
<li><p>입출력할 데이터의 크기와 개수를 인수로 줄 수 있으므로 구조체나 배열과 같이 데이터양이 많은 경우도 파일에 쉽게 입출력 할 수 있다.</p>
</li>
<li><p>숫자,문자 사이의 변환 과정을 거치지 않으므로  입출력 효율을 높일 수 있다.</p>
</li>
<li><p>18-1.c  : fread와 fwrite 함수의 차이</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      FILE* afp, * bfp;
      int num = 10;
      int res;

      afp = fopen(&quot;a.txt&quot;, &quot;wt&quot;);         // 텍스트 모드로 출력 파일 개방
      fprintf(afp, &quot;%d&quot;, num);            // num의 값을 문자로 변환하여 출력

      bfp = fopen(&quot;b.txt&quot;, &quot;wb&quot;);         // 바이너리 모드로 출력 파일 개방
      fwrite(&amp;num, sizeof(num), 1, bfp);  // num의 값을 그대로 파일에 출력

      fclose(afp);
      fclose(bfp);

      bfp = fopen(&quot;b.txt&quot;, &quot;rb&quot;);         // 바이너리 모드로 입력 파일 개방
      fread(&amp;res, sizeof(res), 1, bfp);   // 파일의 데이터를 그대로 변수에 입력
      printf(&quot;%d&quot;, res);                  // 입력한 데이터 확인

      fclose(bfp);

      return 0;
  }</code></pre>
</li>
<li><p>fread와 fwrite 는 메모리의 데이터를 변환 없이 입출력 한다.</p>
<ul>
<li>fprintf 함수가 변환하여 파일에 출력하는 경우</li>
</ul>
</li>
</ul>
<pre><code>    ![](https://velog.velcdn.com/images/kym11290306/post/4cd72d48-66d5-4609-94da-36d3824ca66c/image.png)


- fwrite가 변환 없이 파일에 출력하는 경우

    ![](https://velog.velcdn.com/images/kym11290306/post/1a992e15-e2c7-4dfa-8f12-5388b59bc202/image.png)</code></pre><hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>fgets 함수는 한 줄씩 입력하며 데이터를 모두 읽으면 NULL을 반환한다.</li>
<li>fscanf 함수와 fprintf 함수는 scanf, printf 함수와 사용법이 비슷하다    .</li>
<li>fflush 함수는 출력할 때 사용하며 스트림 버퍼의 내용을 즉시 장치로 기록한다.</li>
<li>fread와 fwrite 함수는 데이터의 크기를 지정해 입출력할 수 있다.</li>
</ul>
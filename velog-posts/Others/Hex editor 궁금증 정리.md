<p>날짜 : 2026-01-05(월)</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(){
    int a=100;
    int b=200;
    int c=a+b;
    char d='a';
    float e= 3.14159;

    printf(&quot;%c\n&quot;,d);

    return 0;
}</code></pre>
<p>위 코드에서 gdb를 통한 디버깅을 진행해보았다.<br />vscode에서 아래와 같은 Extentions를 깔아주었다.  </p>
<img alt="image" height="400" src="https://github.com/user-attachments/assets/30ef2f0c-ee58-4faf-bea1-2588d4cc2203" width="266" />

<p>C/C++ Extention Pack을 깔고, vscode에서 c코드를 작성, 디버깅 하는 과정을 거쳤다.<br />아래와 같이 break point를 설정하고, F5 -&gt; gdb를 이용하여 디버깅을 진행하였다.  </p>
<img alt="image" height="303" src="https://github.com/user-attachments/assets/9d67c0ea-7f9d-4777-af37-d95d1fe29b97" width="685" />

<p>break point를 지날때마다, 변수가 쓰레기값에서 할당하고자 하는 값으로 넣어지며 초기화 되는  확인</p>
<img alt="image" height="195" src="https://github.com/user-attachments/assets/44d7e696-a36a-45bc-bbc0-67aa98539650" width="272" />

<p>각 변수가 저장된 주소, <code>sizeof(변수)</code> 명령어를 통해 각 변수의 크기를 확인하였다.</p>
<img alt="image" height="296" src="https://github.com/user-attachments/assets/f75d4e15-d85c-439e-8b59-52502c60fd48" width="259" />

<p>아래 사진은 변수 a가 저장된 주소 <code>&amp;a=0x7fffffffdc80</code> 를 오프셋으로 한, Hex Editor 이다.</p>
<img alt="image" height="891" src="https://github.com/user-attachments/assets/8cac580d-161f-4bb1-b7ff-38f96d6ffff2" width="800" />

<p>아래 사진은 변수 d가 저장된 주소 <code>&amp;d=0x7fffffffdc7f</code> 를 오프셋으로 한, Hex Editor 이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bc1c80d4-0b7e-4f29-bc34-5c793a75466c/image.png" /></p>
<p>여기서 들었던 의문이였던 점은, 변수는 a, b, c, d, e 순서로 저장을 했는데
주소의 시작 값은 아래와 같았다.</p>
<pre><code class="language-bash">&amp;a = 0x7fffffffdc80
&amp;b = 0x7fffffffdc84
&amp;c = 0x7fffffffdc88
&amp;d = 0x7fffffffdc7f
&amp;e = 0x7fffffffdc8c</code></pre>
<p>왜 d가 제일 먼저 저장되고, a, b, c, e 순으로 저장되었을까? 고민을 해보았다.  </p>
<p>a, b, c 는 int형 변수, d는 char형 변수, e는 float형 변수로,</p>
<p>각각의 크기는 다음과 같다.</p>
<pre><code class="language-c">sizeof(a) = 4  // 4btye
sizeof(b) = 4  // 4btye
sizeof(c) = 4  // 4btye
sizeof(d) = 1  // 1byte
sizeof(e) = 4  // 4btye</code></pre>
<p>int와 float형 변수의 경우 4byte 정렬을 맞추기 위해 연속된 4의 배수 주소에 배치되는 것이 유리하다.<br />만약 char형 변수 d가 int나 float 사이에 소스 코드 순서대로 배치된다면, 이후에 오는 4바이트 정렬이 필요한 변수의 정렬을 맞추기 위해<br />바이트 단위의 패딩이 추가될 수 있다. 그러나 본 실험에서는 컴파일러가 정렬 효율을 고려하여 char형 변수 d를 4바이트 경계 바로 앞에 배치하고,<br />int와 float형 변수들을 4바이트 정렬된 영역에 연속적으로 배치함으로써 불필요한 패딩을 최소화하였다.</p>
<ul>
<li>정렬(alignment)이란?<ul>
<li>CPU는 특정 타입을 특정 주소 배수에서 접근할 때 가장 효율적이다.</li>
<li>char형은 어디에 있어도 상관 없음</li>
<li>int/float는 주소가 4의 배수여야 효율적</li>
</ul>
</li>
</ul>
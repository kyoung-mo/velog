<blockquote>
</blockquote>
<p>/*  </p>
<ul>
<li><strong>입력:</strong> 소스 주소, 목적지 주소, 복사할 바이트 수<ul>
<li><strong>출력:</strong> 메모리 복사 후 목적지 주소의 데이터 덤프</li>
<li><strong>제약조건:</strong> <code>memcpy</code> 대신 <code>memmove</code> 동작 구현 (src와 dest 영역이 겹칠 때 데이터 오염 방지).</li>
<li><strong>실행결과:</strong> <code>Overlap handled correctly.</code><blockquote>
<p>*/</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<p>이거에 대한 과제 하다가 overlap 상황을 만들어보고 직접 터미널에서 보고 싶었다. 포인터 연산을 함께 했을때 각 변수의 주소가 어떻게 저장되는지에 대한 개념과, 리틀 앤디언의 개념에 대해 익혔다..</p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c3bd4811-2266-4d6c-a016-b6e32c71339e/image.png" /></p>
<ul>
<li><code>uint32_t</code> 자료형으로 initial_memory 변수를 선언, 값은 69999로 초기화하였다.</li>
<li><code>uint32_t*</code> 자료형으로 src, dest 포인터 변수를 선언, 값은 아래와 같이 초기화하였다.<pre><code class="language-c">uint32_t *src=&amp;initial_memory;
uint32_t *dest=(uint32_t*)((char*)src+2);</code></pre>
처음에는 <code>dest=src+1</code> 을 해주었으나, src는 4바이트 값을 기본으로 하기 때문에 
src+1을 해주어도 <code>주소값+1</code> 출력이 아닌 
<code>주소값+(1*src 기본 크기)</code>로 초기화 되면서 
<code>주소값+4byte</code> 가 출력되어 overlap이 적용되지 않는 상황이 반복되었기 때문이다.</li>
</ul>
<p>그러다가 <code>uint32_t *dest=(uint32_t*)((char*)src+2);</code> 와 같이 초기화를 해주면, dest에는 src에서 2바이트 만큼 이동하게 되어, 원래 src, dest 크기는 각각 4바이트였는데 dest가 src에 대해 2바이트 만큼 쉬프트 되었으므로, 2바이트 만큼 overlap 되는 상황이 드디어 만들어졌다. 아래와 같은 상황이다.</p>
<pre><code class="language-c">주소:     DC20  DC21  DC22  DC23  DC24  DC25
         [─────src (4바이트)─────]
                     [─────dest (4바이트)─────]
                     └─────┘
                   2바이트 겹침!</code></pre>
<hr />
<p>그리고 저장된 값을 읽어들이는 방법으로 리틀앤디언, 빅앤디언 방식이 있다. 이중 빅앤디언은 저장된 값을 순서대로 읽어들이는 방법이고, 리틀앤디언은 저장된 값을 역순으로 읽어들이는 방식이다.</p>
<p>아래 연습했던 코드의 실행 결과를 보면, <code>*src=0x0001116F</code> 라는 값이 터미널에 출력되는데, 프로그램의 메모리에는 1바이트씩 역순으로 저장되어 있기 때문에, <code>6F 11 01 00</code> 으로 메모리에 저장되어있고, <code>0x0001116F</code> 는 리틀 앤디언 방식으로 메모리에 저장된 데이터를 해석하지만 이미 메모리에서 읽어서 역순으로 조합한 후의 값이다.</p>
<hr />
<h2 id="삽질-코드">삽질 코드</h2>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdint.h&gt;
#include &lt;string.h&gt;

/*
- **입력:** 소스 주소, 목적지 주소, 복사할 바이트 수
- **출력:** 메모리 복사 후 목적지 주소의 데이터 덤프
- **제약조건:** `memcpy` 대신 `memmove` 동작 구현 (src와 dest 영역이 겹칠 때 데이터 오염 방지).
- **실행결과:** `Overlap handled correctly.`
*/

int main(){

    uint32_t initial_memory = 69999;
    uint32_t *src=&amp;initial_memory;
    uint32_t *dest=(uint32_t*)((char*)src+2);
    uint32_t byte=sizeof(*src);
    printf(&quot;initial_memory 주소 : %08x\n&quot;,&amp;initial_memory);
    printf(&quot;initial_memory = %08x\n\n&quot;,initial_memory);

    printf(&quot;\t\t\t*src = \t%08x\n&quot;,*src);
    printf(&quot;*(uint32_t*)((char*)src+2)  = \t%08x\n&quot;,*(uint32_t*)((char*)src+2));
    //printf(&quot;\t\t\tsrc = \t%x\n&quot;,src);
    //printf(&quot;(uint32_t*)((char*)src+15)= \t%x\n\n&quot;,(uint32_t*)((char*)src+15));

    memcpy(dest,src,4);

    printf(&quot;\t\t\t*src = \t%08x\n&quot;,*src);
    printf(&quot;*(uint32_t*)((char*)src+2)  = \t%08x\n&quot;,*(uint32_t*)((char*)src+2));
    //printf(&quot;\t\t\tsrc = \t%x\n&quot;,src);
    //printf(&quot;(uint32_t*)((char*)src+15)= \t%x\n\n&quot;,(uint32_t*)((char*)src+15));

    /*
    printf(&quot;src : %X\n&quot;,src);
    printf(&quot;dest : %X\n&quot;,*dest);
    printf(&quot;byte : %x&quot;,byte);
    */

    // 포인터, 메모리 관리?
    // 안전한 memcpy 구현? 
    // overlap 처리?
    // memcpy 대신 memmove 동작 구현..

    // 공부할 것 &gt; memcpy 개념, overlap 처리의 개념
    // src와 dest 영역이 겹칠 때 데이터 오염 방지?
    /*
    소스와 목적지 영역이 겹칠 때 데이터 오염 방지...?
    &gt;&gt; (소스 + 복사할 바이트 수) 범위 안에 목적지 주소가 있는지 확인

    대충 0xAAAAAAAA 가 주소 100번지에 있는데
    101번지에 memcpy를 사용하면 애매해져서 그런가
    메모리 복사 후 목적지 주소의 데이터 덤프(memmove)
    */



    src;
    dest;



    return 0;
}</code></pre>
<h2 id="실행-결과">실행 결과</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/176d636d-ddf5-4f79-9a8c-c2d4a32e1b82/image.png" /></p>
<pre><code class="language-c">initial_memory 주소 : ffffdc20
initial_memory = 0001116f

                        *src =  0001116f
*(uint32_t*)((char*)src+2)  =   00040001
                        src =   ffffdc20
(uint32_t*)((char*)src+15)=     ffffdc2f

                        *src =  116f116f
*(uint32_t*)((char*)src+2)  =   0001116f
                        src =   ffffdc20
(uint32_t*)((char*)src+15)=     ffffdc2f

[1] + Done                       &quot;/usr/bin/gdb&quot; --interpreter=mi --tty=${DbgTerm} 0&lt;&quot;/tmp/Microsoft-MIEngine-In-cezgq0mo.wzy&quot; 1&gt;&quot;/tmp/Microsoft-MIEngine-Out-ecbfkno1.vwa&quot;</code></pre>
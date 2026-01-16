<h3 id="day-4-비트-단위-reverse-mirroring">Day 4. 비트 단위 Reverse (Mirroring)</h3>
<ul>
<li><strong>입력:</strong> 8비트 정수 <code>0b11010010</code></li>
<li><strong>출력:</strong> <code>0b01001011</code> (비트 순서 반전)</li>
<li><strong>제약조건:</strong> Lookup Table(LUT)을 사용하지 않고 O(1) 비트 연산으로 구현.</li>
<li><strong>실행결과:</strong></li>
</ul>
<pre><code class="language-c">=== Day 4: Bitwise Reverse (Mirroring) ===

Case 1:
  Input : 0xD2 (1101 0010)
  Output: 0x4B (0100 1011)
  Verify: OK
------------------------
Case 2:
  Input : 0x0F (0000 1111)
  Output: 0xF0 (1111 0000)
  Verify: OK
------------------------
Case 3:
  Input : 0xAA (1010 1010)
  Output: 0x55 (0101 0101)
  Verify: OK
------------------------
Case 4:
  Input : 0x12 (0001 0010)
  Output: 0x48 (0100 1000)
  Verify: OK
------------------------</code></pre>
<hr />
<h3 id="나의-풀이-정답-x">나의 풀이 (정답 x)</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdint.h&gt;

int cnt=1;

static int verify_v(uint8_t v){
    if((v|(uint8_t)(~v))==0xFF){ 
    return 0;
    }
    else return 1;
}

static void print_bin8(uint8_t v){
    for(int i=7;i&gt;=0;--i){
        putchar((v&amp;(1u&lt;&lt;i))? '1': '0'); // unsigned int
        if(i%4 ==0 &amp;&amp; i !=0) putchar(' ');
    }
}

static void reverse_print_bin8(uint8_t v){
    for(int i=0;i&lt;=7;i++){
        putchar((v&amp;(1u&lt;&lt;i))? '1': '0');
        if((i+1)%4 ==0 &amp;&amp; (i+1) !=0) putchar(' ');
    }
}


void print_case(uint8_t v){

    int verify=0;

    printf(&quot;Case %d&quot;,cnt);
    printf(&quot;\tInput : 0x%02X (&quot;,v);
    print_bin8(v);
    printf(&quot;)\n\tOutput : 0x%02X (&quot;,v);
    reverse_print_bin8(v);
    printf(&quot;)\n&quot;);

    verify = verify_v(v);

    if(verify==0) printf(&quot;\tVerify : OK\n&quot;);
    else printf(&quot;\tVerify : ERROR\n&quot;);

    printf(&quot;------------------------\n&quot;);

    cnt++;
}
int main(){

    printf(&quot;=== Day 4: Bitwise Reverse (Mirroring) ===\n&quot;);

    print_case(0xD2);
    print_case(0x0F);
    print_case(0xAA);
    print_case(0x12);


    return 0;
}</code></pre>
<p>내 풀이에서 제일 큰 문제는 2가지였다.</p>
<ul>
<li>일단 verify 로직 잘못 생각했다.</li>
<li>Reverse 함수 로직을 잘못짰다.</li>
</ul>
<p>추가적으로, 시간 복잡도가 for문을 썼기 때문에 제약 조건에서 벗어난다. -&gt; <code>O(n)</code></p>
<ul>
<li><code>O(1)</code> 으로 구현</li>
</ul>
<p>2026-01-13 펌웨어)</p>
<h2 id="3색-rgb-led-모듈을-이용한-실습">3색 RGB LED 모듈을 이용한 실습</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/628dcf4f-82bb-46eb-a2c5-084f32098f30/image.png" /></p>
<hr />
<h3 id="회로도예시">회로도(예시)</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d2387ac3-77da-479e-a338-ac17a35805c0/image.png" /></p>
<hr />
<h3 id="코드-1-기본-예제">코드 1) 기본 예제</h3>
<pre><code class="language-c">#define RED 5   // PD5, PORTD 5 
#define GREEN 6 // PD6, PORTD 6
#define BLUE 11 // PB3, PORTB 3
#include &lt;Arduino.h&gt;

// put function declarations here:
int myFunction(int, int);

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void loop() {
  digitalWrite(RED, HIGH);
  delay(1000);
  digitalWrite(RED, LOW);

  digitalWrite(GREEN, HIGH);
  delay(1000);
  digitalWrite(GREEN, LOW);

  digitalWrite(BLUE, HIGH);
  delay(1000);
  digitalWrite(BLUE, LOW);
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}</code></pre>
<h3 id="코드-2-portb-portd---datasheet-참고해서-정의">코드 2) PORTB, PORTD -&gt; DATASHEET 참고해서 정의</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b0f5821c-fe60-450f-bdb6-7ca72d843053/image.png" /></p>
<ul>
<li>DDRB &gt; 0x24 , PORTB &gt; 0x25</li>
<li>DDRD &gt; 0x2A , PORTD -&gt; 0x2B</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dd39c82e-2639-4609-b27d-418863e3b7da/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bee80910-6a97-4d53-a8e6-1eec8993a1d8/image.png" /></p>
<pre><code class="language-c">#include &lt;Arduino.h&gt;

void setup() { //DDRB, DDRD 설정
  *((volatile unsigned int*)0x2B) |= (0x01&lt;&lt;5);
  *((volatile unsigned int*)0x2B) |= (0x01&lt;&lt;6);
  *((volatile unsigned int*)0x25) |= (0x01&lt;&lt;3);
}

void loop() { // PORTB, PORTD 설정
  *((volatile unsigned int*)0x2A) |= (0x01&lt;&lt;5);
  delay(1000);
  *((volatile unsigned int*)0x2A) &amp;= ~(0x01&lt;&lt;5);

  *((volatile unsigned int*)0x2A) |= (0x01&lt;&lt;6);
  delay(1000);
  *((volatile unsigned int*)0x2A) &amp;= ~(0x01&lt;&lt;6);

  *((volatile unsigned int*)0x24) |= (0x01&lt;&lt;3);
  delay(1000);
  *((volatile unsigned int*)0x24) &amp;= ~(0x01&lt;&lt;3);
}
</code></pre>
<h3 id="예제-2번-실습하며-깨달은-점">예제 2번 실습하며 깨달은 점</h3>
<ul>
<li><p><code>void setup()</code> 에서는 <code>DDRB</code> , <code>DDRD</code> 를 1로 설정해서 <code>PORTB</code> , <code>PORTD</code> 의 출력 값을 받아 올  준비를 해야한다.</p>
</li>
<li><p><code>void loop()</code> 에서는 <code>PORTB</code> , <code>PORTD</code> 가 <code>HIGH</code>인지, <code>LOW</code>인지를 설정해주는 역할을 한다.</p>
</li>
<li><p>?? 인줄 알았는데 <code>PINB</code>, <code>PIND</code> 까지 봐야한다고 함. 다시 정리할 것</p>
</li>
</ul>
<hr />
<h3 id="ddrb-portb-pinb-정리">DDRB, PORTB, PINB 정리</h3>
<ul>
<li>DDRB : 입력[0] / 출력[1] 결정 스위치<ul>
<li>전구 설치(쓸 건지 말 건지)</li>
</ul>
</li>
<li>PORTB : 출력 전압 ON/OFF(출력)<ul>
<li>스위치 켜기/끄기</li>
</ul>
</li>
<li>PINB : 현재 전압 읽기(입력)<ul>
<li>불이 실제로 켜졌는지 확인</li>
</ul>
</li>
</ul>
<h3 id="풀업-저항---input-핀-관련">풀업 저항 - INPUT 핀 관련</h3>
<ul>
<li><p>풀업 저항은 입력(INPUT) 상태인 핀의 기본 전압을 HIGH로 끌어올리는 용도</p>
</li>
<li><p>현재 실습에서 사용중인 <code>Atmega328P</code>는 내부 PULL-UP을 지원</p>
</li>
<li><p>사용 어떻게?</p>
<ol>
<li>핀을 INPUT으로 설정</li>
<li>PORT 레지스터를 HIGH로 설정<pre><code class="language-c">DDRB &amp;= ~(1&lt;&lt;2); // PB2 INPUT
PORTB |= (1&lt;&lt;2);</code></pre>
</li>
<li>정리 : 입력상태 + PORTB를 1로 주면 내부 풀업</li>
</ol>
</li>
<li><p>상태 요약</p>
</li>
</ul>
<table>
<thead>
<tr>
<th>DDR</th>
<th>PORT</th>
<th>상태</th>
</tr>
</thead>
<tbody><tr>
<td>0</td>
<td>0</td>
<td>입력, 풀업 없음 (떠다님)</td>
</tr>
<tr>
<td>0</td>
<td>1</td>
<td>입력, <strong>내부 풀업 ON</strong></td>
</tr>
<tr>
<td>1</td>
<td>0</td>
<td>출력 LOW</td>
</tr>
<tr>
<td>1</td>
<td>1</td>
<td>출력 HIGH</td>
</tr>
</tbody></table>
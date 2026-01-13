<p>2026-01-12(월)</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a4c17dd3-22fe-430e-b350-e91ff728c8fd/image.png" /></p>
<p>Arduino Uno R3는 <strong>ATmega328P</strong> 마이크로컨트롤러를 기반으로 한다. 아두이노의 빌트인 LED는 디지털 13번 핀에 연결되어 있으며, 이는 ATmega328P의 내부 맵핑상 <strong>Port B의 5번 비트(PB5)</strong> 에 해당한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/947976d4-6932-4090-96a3-126dc5393d23/image.png" /></p>
<p>아래는 Port Pin Configurations에 대한 정의이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/539aa147-8601-4f43-837d-c833ae9493bd/image.png" /></p>
<p><code>pinMode</code>나 <code>digitalWrite</code> 함수를 사용하지 않고, <strong>물리적인 레지스터 메모리 주소(Address)</strong> 에 직접 접근하여 LED를 제어하는 방법으로는</p>
<h3 id="1-주요-레지스터-주소-및-정보-atmega328p"><strong>1. 주요 레지스터 주소 및 정보 (ATmega328P)</strong></h3>
<p>레지스터에 접근하기 위해 다음 두 가지 주소를 사용한다.</p>
<ul>
<li><strong>DDRB (Data Direction Register B):</strong> 포트 B의 입출력 방향을 설정한다.<ul>
<li>메모리 주소: <code>0x24</code></li>
<li>설정: 5번 비트를 1로 설정하면 출력 모드가 된다.</li>
</ul>
</li>
<li><strong>PORTB (Data Register B):</strong> 포트 B의 출력 상태(High/Low)를 설정한다.<ul>
<li>메모리 주소: <code>0x25</code></li>
<li>설정: 5번 비트를 1로 하면 High(ON), 0으로 하면 Low(OFF)가 된다.</li>
</ul>
</li>
</ul>
<h3 id="2-소스-코드-주소-직접-접근-방식"><strong>2. 소스 코드 (주소 직접 접근 방식)</strong></h3>
<p>이 코드는 C언어의 포인터를 사용하여 해당 메모리 주소에 직접 값을 쓴다.</p>
<p><strong>C++</strong></p>
<pre><code class="language-c">void setup() {
  // DDRB 레지스터 주소: 0x24
  // 0x20은 2진수로 0010 0000 (5번 비트)입니다.
  // 포인터를 사용하여 0x24 주소의 값을 읽고, 5번 비트를 1(Output)로 설정합니다.
  // volatile 키워드는 컴파일러가 이 코드를 최적화하여 생략하지 않도록 강제합니다.
  *((volatile unsigned char *)0x24) |= 0x20; 
}

void loop() {
  // PORTB 레지스터 주소: 0x25

  // LED 켜기 (Turn ON)
  // 0x25 주소의 5번 비트를 1로 설정 (OR 연산)
  *((volatile unsigned char *)0x25) |= 0x20;

  delay(1000); // 1초 대기 (편의상 아두이노 내장 함수 사용)

  // LED 끄기 (Turn OFF)
  // 0x25 주소의 5번 비트를 0으로 설정 (AND 연산 + NOT 연산)
  // ~0x20은 1101 1111이므로, AND 연산을 하면 5번 비트만 0이 됩니다.
  *((volatile unsigned char *)0x25) &amp;= ~0x20;

  delay(1000); // 1초 대기
}</code></pre>
<h3 id="3-코드-상세-설명"><strong>3. 코드 상세 설명</strong></h3>
<ol>
<li><strong><code>volatile unsigned char *</code></strong>:<ul>
<li><code>0x24</code>와 <code>0x25</code>는 단순한 숫자이므로, 이를 &quot;주소&quot;로 인식시키기 위해 캐스팅(형 변환)을 합니다.</li>
<li><code>volatile</code>은 매우 중요합니다. 컴파일러에게 &quot;이 메모리 주소의 값은 언제든지 하드웨어적으로 변경될 수 있으니, 코드를 멋대로 최적화하거나 캐시하지 말고 항상 실제 메모리에 접근하라&quot;고 지시하는 것입니다.</li>
</ul>
</li>
<li><strong>비트 연산 (<code>|=</code>, <code>&amp;= ~</code>)</strong>:<ul>
<li><code>|= 0x20</code>: 기존 레지스터 값은 유지한 채 5번 비트만 1로 만듭니다. (Set Bit)</li>
<li><code>&amp;= ~0x20</code>: 기존 레지스터 값은 유지한 채 5번 비트만 0으로 만듭니다. (Clear Bit)</li>
</ul>
</li>
</ol>
<h3 id="참고-일반적인-레지스터-코딩-방식"><strong>참고: 일반적인 레지스터 코딩 방식</strong></h3>
<p>실무나 일반적인 AVR 프로그래밍에서는 주소(<code>0x24</code>)를 직접 외워서 쓰기보다는, 컴파일러(avr-libc)가 미리 정의해 둔 매크로 이름(<code>DDRB</code>, <code>PORTB</code>)을 사용하는 것이 가독성이 좋고 안전합니다.</p>
<pre><code class="language-c">// 매크로를 사용한 동일한 기능의 코드
void setup() {
  DDRB |= (1 &lt;&lt; 5); // PB5를 출력으로 설정
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  *(volatile unsigned char*)0x25 |= 0x20;
  delay(1000);
  *(volatile unsigned char*)0x25 &amp;= ~0x20; //-&gt; 의미?
  delay(1000);
  int sizeint= sizeof(int);
  Serial.println(sizeint);
}</code></pre>
<p>위의 예제, 아레 예제는 같은 의미이다.</p>
<pre><code class="language-c">void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  PORTB |= (1&lt;&lt;5);
  delay(1000);
  PORTB &amp;= ~(1&lt;&lt;5)); //-&gt; 의미?
  delay(1000);
  int sizeint= sizeof(int);
  Serial.println(sizeint);
}</code></pre>
<hr />
<h3 id="아두이노는-c언어-일종인데-main-함수는-어디에">아두이노는 C언어 일종인데 <code>main()</code> 함수는 어디에..?</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e3c58aba-cdf1-4e81-9f45-cbb1558fe10b/image.png" />
<code>void loop()</code> 함수에서     <code>main</code> 함수를 추가해주고 (VSCode 기준) F12를 누르면 <code>main</code> 함수가 어디에 정의되어있는지 확인 가능하다.</p>
<p>(확인용)
실제 코드에서 main() 함수를 사용하면 본인이 본인을 불러주는것이기 때문에 사용하면 안된다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f729eac5-00fc-48ab-9bc2-8777a8356065/image.png" /></p>
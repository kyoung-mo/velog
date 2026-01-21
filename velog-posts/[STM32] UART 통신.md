<p>2026-01-20 STM32 USART실습)</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/02f5056a-fad2-4c18-b4dd-268d79cd49c4/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e1d471b0-8424-444a-9033-acee81aeb836/image.png" /></p>
<ul>
<li>USART2를 위와 같이 설정</li>
</ul>
<hr />
<p><strong>하드웨어 설정, 소프트웨어 구현, PC 터미널 연결</strong>의 3단계가 필요합니다.</p>
<p>Nucleo-F411RE 보드는 USB 케이블을 통해 PC와 가상 시리얼 포트(VCP)로 연결되도록 설계되어 있다.</p>
<hr />
<h3 id="1-stm32cubeide-설정-ioc-파일">1. STM32CubeIDE 설정 (.ioc 파일)</h3>
<ol>
<li><strong>USART 선택:</strong> * <code>Connectivity</code> -&gt; <code>USART2</code>를 선택합니다. (Nucleo 보드는 보통 USART2가 ST-LINK를 통해 USB 시리얼로 연결되어 있습니다.)</li>
<li><strong>모드 설정:</strong> * <code>Mode</code>를 <strong>Asynchronous</strong> (비동기)로 설정합니다.</li>
<li><strong>통신 속도 설정:</strong> * 아래 <code>Configuration</code> 창의 <code>Parameter Settings</code>에서 <code>Baud Rate</code>를 확인합니다 (기본값 <strong>115200</strong>).</li>
<li><strong>저장 및 코드 생성:</strong> <code>Ctrl + S</code>를 눌러 코드를 생성합니다.</li>
</ol>
<hr />
<h3 id="2-코드-작성-mainc">2. 코드 작성 (main.c)</h3>
<p>데이터를 보내고 받는 가장 기초적인 방법은 <code>HAL_UART_Transmit</code>과 <code>HAL_UART_Receive</code>를 사용하는 것입니다.</p>
<h3 id="데이터-송신-pc로-보내기">데이터 송신 (PC로 보내기)</h3>
<p><code>while(1)</code> 루프 안에 아래 코드를 추가해 보세요.</p>
<p>C</p>
<pre><code class="language-c">char *msg = &quot;Hello STM32!\r\n&quot;;
HAL_UART_Transmit(&amp;huart2, (uint8_t*)msg, strlen(msg), 10);
HAL_Delay(1000);</code></pre>
<h3 id="printf-사용하기-추천">printf 사용하기 (추천)</h3>
<p><code>printf</code>를 사용하면 변수 출력이 훨씬 편리합니다. <code>main.c</code> 상단 <code>/* USER CODE BEGIN PFP */</code> 구역에 아래 코드를 추가하세요.</p>
<p>C</p>
<pre><code class="language-c">#ifdef __GNUC__
  #define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
  #define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif

PUTCHAR_PROTOTYPE
{
  HAL_UART_Transmit(&amp;huart2, (uint8_t *)&amp;ch, 1, 0xFFFF);
  return ch;
}</code></pre>
<p><em>이제 코드 어디에서든 <code>printf(&quot;Value: %d\r\n&quot;, value);</code>를 사용할 수 있습니다.</em></p>
<hr />
<h3 id="3-pc-터미널-프로그램-연결">3. PC 터미널 프로그램 연결</h3>
<p>보드에서 보낸 데이터를 확인하려면 PC에 터미널 프로그램이 필요합니다.</p>
<ul>
<li><strong>추천 프로그램:</strong> Hercules, Tera Term, PuTTY 또는 STM32CubeIDE 내장 <strong>Serial Monitor</strong>.</li>
<li><strong>설정값:</strong><ul>
<li><strong>Port:</strong> 장치 관리자에서 확인된 <code>STLink Virtual COM Port</code> 번호</li>
<li><strong>Baud Rate:</strong> 115200 (설정한 값과 일치해야 함)</li>
<li><strong>Data bits:</strong> 8 / <strong>Stop bits:</strong> 1 / <strong>Parity:</strong> None</li>
</ul>
</li>
</ul>
<hr />
<h3 id="4-하드웨어-연결-확인-nucleo-보드">4. 하드웨어 연결 확인 (Nucleo 보드)</h3>
<p>Nucleo 보드 사용 시 별도의 배선은 필요 없습니다. 하지만 만약 <strong>외부 시리얼 모듈(CP2102 등)</strong>을 사용한다면 다음과 같이 교차 연결해야 합니다.</p>
<ul>
<li>MCU TX -&gt; USB 모듈 RX</li>
<li>MCU RX -&gt; USB 모듈 TX</li>
<li>GND -&gt; GND</li>
</ul>
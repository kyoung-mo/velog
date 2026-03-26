<blockquote>
<p>본 글은 시리즈 2편입니다.
1편: <a href="https://velog.io/@mommers/catnip1">CAN 기반 STM32 + Raspberry Pi 분산 ECU 시스템 — 아키텍처 설계</a></p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e9db5e88-17f3-403d-9188-590bef477148/image.png" /></p>
<hr />
<h2 id="한-줄-요약">한 줄 요약</h2>
<blockquote>
<p>B-L475E-IOT01A2(STM32L4) 기반 주행 ECU를 설계하고, 모터 PWM / 엔코더 RPM / 속도 PID / CAN 통신을 단계적으로 구현했습니다.</p>
</blockquote>
<blockquote>
<p>MangoM32(STM32F103)를 활용한 CAN 통신 단계별 검증 과정도 함께 다룹니다.</p>
</blockquote>
<hr />
<h2 id="개요--주행-ecu의-역할-정의">개요 — 주행 ECU의 역할 정의</h2>
<p>1편에서 설명했듯이, 이 시스템에서 STM32 주행 ECU의 원칙은 하나입니다.</p>
<blockquote>
<p><strong>&quot;판단하지 않는다. 명령을 수행하고 데이터를 피드백할 뿐이다.&quot;</strong></p>
</blockquote>
<p>RPi1 미션 ECU가 카메라로 라인을 분석하고 방향을 결정하면, STM32는 그 명령을 CAN으로 받아 모터를 제어합니다. 동시에 엔코더로 측정한 실제 RPM을 피드백으로 돌려보냅니다.</p>
<p>개발은 처음부터 CAN을 붙이지 않고, <strong>모터 → 엔코더 → PID → CAN 순서로 나눠서</strong> 진행했습니다. 이유는 단순합니다. 한 번에 붙이면 문제가 생겼을 때 어디서 터진 건지 알 수가 없습니다. 각 단계가 완전히 동작하는 걸 눈으로 확인한 뒤에야 다음 단계로 넘어갔습니다.</p>
<hr />
<h2 id="1-초기-단계--팀-구조-정리">1. 초기 단계 — 팀 구조 정리</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c27d3074-ec85-434d-a274-759eb836041c/image.png" /></p>
<p>프로젝트 초반에는 팀 구조가 정리되지 않은 상태였습니다.</p>
<p>CAN ID, ECU 역할, 통신 흐름이 팀원마다 다르게 이해되고 있었고, 이 상태로 개발이 진행되면 나중에 통합할 때 충돌이 생길 가능성이 높았습니다.</p>
<p>그래서 PM으로서, 먼저 전체 구조를 다시 정의했습니다.</p>
<ul>
<li>CAN ID 테이블 재정리 (송신 노드 / 수신 노드 / 주기 명확화)</li>
<li>ECU 역할 경계 명확화 (STM32는 판단하지 않음, RPi1이 모든 판단 담당)</li>
<li>데이터 흐름 통일 (주문 → 출동 → 주행 → 도착 → 인증 → 귀환)</li>
</ul>
<p>이 작업 이후부터 각 ECU 개발이 충돌 없이 진행되기 시작했습니다. 코드보다 앞서 구조를 맞춰두는 것이 결과적으로 훨씬 빠른 길이었습니다.</p>
<hr />
<h2 id="2-raspberry-pi-5--mangom32-보드-교체-가능성-검증">2. Raspberry Pi 5-&gt; MangoM32 보드 교체 가능성 검증</h2>
<p>원래 화물함 ECU는 Raspberry Pi 5로 설계되어 있었습니다.
그런데 화물함 ECU가 실제로 해야 하는 일을 다시 살펴보니, CAN 수신 / 키패드 입력 / LCD 출력 / 서보 제어가 전부였습니다. 리눅스 OS에 필요한 OpenCV나 네트워크 스택이 작업이 하나도 없었습니다.</p>
<p><strong>&quot;Raspberry Pi 5를 여기에 쓰는 건 너무 과하다.&quot;</strong> </p>
<p>대신 bxCAN 내장에 GPIO, I2C, PWM을 모두 갖춘 STM32F103 기반 MangoM32 보드로 교체하는 게 훨씬 적합하다고 판단했습니다. 제가 갖고있던 보드이기도 하고, 인터럽트 기반 실시간 처리도 MCU가 훨씬 유리합니다.</p>
<p>다만 실제로 교체하려면 MangoM32에서 CAN 통신이 되는지 먼저 확인이 필요했습니다. 직접 Silent Loopback 테스트로 CAN 컨트롤러가 정상인지 확인했고, 결과는 정상이었습니다. 이후 팀원에게 CAN 구현을 넘겼는데 얼마 지나지 않아 이런 얘기가 나왔습니다.</p>
<blockquote>
<p><strong>팀원: &quot;이거 CAN 안될 것 같은데? 보드 문제 있어.&quot;</strong></p>
</blockquote>
<p>직접 확인해봤을 때는 됐는데, 이 상태에서 이유도 모른 채 포기하기는 싫었습니다.</p>
<p>다시 직접 붙잡고 시작했습니다. 외부 디버거 설정부터 배선, 트랜시버, 종단저항까지 하나씩 다시 확인했고, 여기서 2~3일이 소요됐으나, 결과적으로 CAN 통신에 성공하였습니다.</p>
<p>이 확인이 있었기에 MangoM32를 화물함 ECU로 확정할 수 있었습니다. 검증 과정의 상세한 내용은 아래 MangoM32 섹션에서 다룹니다.</p>
<hr />
<h2 id="3-보드-선정--왜-b-l475e-iot01a2인가">3. 보드 선정 — 왜 B-L475E-IOT01A2인가</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0f999e3b-917e-4e10-a6a7-c302a560635a/image.png" /></p>
<p>위 보드를 주행 ECU로 선택한 이유는 두 가지였습니다.</p>
<p>첫째, <strong>bxCAN 내장</strong>입니다. STM32L4 계열은 CAN 컨트롤러가 MCU에 내장되어 있어 MCP2515 같은 외부 컨트롤러 없이 트랜시버만 연결하면 됩니다. 배선이 단순해지고 SPI 통신 오버헤드도 없습니다.</p>
<p>둘째, <strong>제가 보유중인 보드</strong>였습니다. 학부 시절, 이 보드를 구매해서 실습을 진행하려 했으나, 실제로 써보진 못했습니다. 결국 새로 구매하지 않아도 되는 이유도 있었습니다.</p>
<p>다만 이 보드를 선택하면서 초반에 꽤 고생했는데, 그게 바로 핀 충돌 문제였습니다.</p>
<hr />
<h2 id="4-핀-충돌-이슈--baseioc가-필요한-이유">4. 핀 충돌 이슈 — base.ioc가 필요한 이유</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b1650ad3-cb6e-4d01-a13e-350349785d97/image.png" /></p>
<p>B-L475E-IOT01A2는 온보드에 WiFi, BLE, 각종 센서가 달려 있는 IoT 보드입니다. CubeMX에서 이 보드를 기본값으로 초기화하면 온보드 주변장치들이 핀을 미리 점유합니다.</p>
<p>처음에는 모터가 동작하지 않고 엔코더 카운트가 전혀 올라가지 않았는데, 코드상으로는 아무 문제가 없어 보였습니다. 코드를 여러 번 확인했지만 문제를 찾을 수 없었고, 오히려 코드가 정상이라서 더 혼란스러웠습니다.</p>
<p><strong>&quot;코드 문제가 아니면 뭐지?&quot;</strong></p>
<p>그때부터 핀맵을 하나씩 다시 들여다보기 시작했습니다. 결과적으로 온보드 주변장치가 우리가 쓰려는 핀을 이미 점유하고 있었던 것이었습니다.</p>
<table>
<thead>
<tr>
<th>온보드 주변장치</th>
<th>점유 핀</th>
<th>우리 프로젝트 용도</th>
</tr>
</thead>
<tbody><tr>
<td>UART4 (Arduino Serial)</td>
<td>PA0, PA1</td>
<td>TIM5 엔코더 (왼쪽)</td>
</tr>
<tr>
<td>SPI1 (Arduino SPI)</td>
<td>PA6, PA7</td>
<td>TIM3 엔코더 (오른쪽)</td>
</tr>
<tr>
<td>I2C1 (Arduino I2C)</td>
<td>PB8, PB9</td>
<td>CAN1 RX/TX</td>
</tr>
</tbody></table>
<p>해결 방법은 <strong>온보드 주변장치를 전부 비활성화한 <code>base.ioc</code>를 베이스로 사용</strong>하는 것이었습니다. 이후 필요한 기능만 직접 활성화하는 방식으로 진행했습니다.</p>
<hr />
<h2 id="5-핀맵-및-cubemx-설정">5. 핀맵 및 CubeMX 설정</h2>
<p>핀 충돌 이슈를 해결하고 확정한 최종 핀맵입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/91358c1c-7069-4b4f-bc79-539d06936714/image.png" /></p>
<table>
<thead>
<tr>
<th>기능</th>
<th>핀</th>
<th>CubeMX 설정</th>
<th>연결 대상</th>
</tr>
</thead>
<tbody><tr>
<td>CAN1_RX</td>
<td>PB8</td>
<td>CAN1_RX</td>
<td>SN65HVD230 RXD</td>
</tr>
<tr>
<td>CAN1_TX</td>
<td>PB9</td>
<td>CAN1_TX</td>
<td>SN65HVD230 TXD</td>
</tr>
<tr>
<td>USART1_TX</td>
<td>PB6</td>
<td>USART1_TX</td>
<td>ST-LINK VCP (디버그)</td>
</tr>
<tr>
<td>USART1_RX</td>
<td>PB7</td>
<td>USART1_RX</td>
<td>ST-LINK VCP</td>
</tr>
<tr>
<td>TIM2_CH1</td>
<td>PA15</td>
<td>PWM 1kHz</td>
<td>L298N ENA (왼쪽 모터)</td>
</tr>
<tr>
<td>TIM2_CH3</td>
<td>PA2</td>
<td>PWM 1kHz</td>
<td>L298N ENB (오른쪽 모터)</td>
</tr>
<tr>
<td>TIM5_CH1/2</td>
<td>PA0/PA1</td>
<td>Encoder Mode</td>
<td>왼쪽 엔코더 A/B</td>
</tr>
<tr>
<td>TIM3_CH1/2</td>
<td>PA6/PA7</td>
<td>Encoder Mode</td>
<td>오른쪽 엔코더 A/B</td>
</tr>
<tr>
<td>GPIO_OUT</td>
<td>PC2~PC5</td>
<td>GPIO_Output</td>
<td>L298N IN1~IN4</td>
</tr>
<tr>
<td>I2C2_SCL/SDA</td>
<td>PB10/PB11</td>
<td>I2C2</td>
<td>VL53L0X 전방 거리 센서</td>
</tr>
</tbody></table>
<blockquote>
<p>⚠️ PA15는 기본적으로 JTAG 핀으로 설정되어 있어 TIM2_CH1으로 사용하려면 CubeMX에서 <strong>SWD 모드로 변경(JTAG 해제)</strong> 이 필수입니다.</p>
</blockquote>
<p><strong>CubeMX 핵심 설정:</strong></p>
<pre><code>CAN1:   Prescaler=16, BS1=13TQ, BS2=2TQ → 250 kbps
TIM2:   Prescaler=79, Period=999 → 1 kHz PWM (PWM_MAX=999)
TIM5:   Encoder Mode TI12, Period=65535 (왼쪽 엔코더)
TIM3:   Encoder Mode TI12, Period=65535 (오른쪽 엔코더)
TIM6:   Prescaler=79, Period=9999 → 10 ms PID 인터럽트
TIM7:   HAL Timebase (SysTick 대체)
IWDG:   Prescaler=/32, Reload=300 → 300 ms Watchdog
Clock:  HSI 16MHz → PLL → SYSCLK 80MHz</code></pre><hr />
<h2 id="6-하드웨어-구성-및-배선">6. 하드웨어 구성 및 배선</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/68ff04b6-bd4d-4ac2-90dc-481252cc9af7/image.png" /></p>
<h3 id="모터-드라이버-l298n">모터 드라이버 (L298N)</h3>
<p>스키드 스티어링 방식을 채택했습니다. 서보 조향 없이 좌우 바퀴의 속도 차이로 방향을 제어하는 탱크 방식입니다. L298N 하나로 좌우 각 2개씩 총 4개 모터를 병렬로 구동합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f9257806-1738-4a08-8712-88fb0eba49c9/image.png" /></p>
<pre><code>STM32 PA15 → L298N ENA (왼쪽 PWM)
STM32 PA2  → L298N ENB (오른쪽 PWM)
STM32 PC2~PC5 → L298N IN1~IN4

L298N OUT1/OUT2 → 왼쪽 모터 2개 병렬
L298N OUT3/OUT4 → 오른쪽 모터 2개 병렬</code></pre><blockquote>
<p>ENA/ENB는 3.3V PWM 신호를 L298N이 직접 인식했습니다. 레벨시프터 없이 직결 가능합니다.</p>
</blockquote>
<h3 id="엔코더-jgb37-520">엔코더 (JGB37-520)</h3>
<p>엔코더 출력 신호는 5V입니다. STM32 GPIO는 3.3V 내성이므로 레벨시프터를 반드시 거쳐야 합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/340716f1-6f21-4973-b9e9-9500741df382/image.png" /></p>
<pre><code>왼쪽 엔코더 A/B  → 레벨시프터 → PA0/PA1 (TIM5)
오른쪽 엔코더 A/B → 레벨시프터 → PA6/PA7 (TIM3)</code></pre><h3 id="can-트랜시버-sn65hvd230">CAN 트랜시버 (SN65HVD230)</h3>
<pre><code>STM32 PB9 (CAN_TX) → SN65HVD230 TXD
SN65HVD230 RXD    → STM32 PB8 (CAN_RX)
SN65HVD230 VCC = 3.3V
SN65HVD230 GND = GND</code></pre><blockquote>
<p>VCC와 GND 핀 위치를 혼동하면 CAN 통신이 전혀 되지 않습니다. 오결선으로 배선을 전부 다시 확인하고 나서야 찾은 문제였습니다.</p>
</blockquote>
<hr />
<h2 id="7-단계별-개발">7. 단계별 개발</h2>
<h3 id="모터-동작-테스트">모터 동작 테스트</h3>
<p>처음에는 UART로 직접 명령을 입력하면서 모터 단독 동작을 테스트했습니다. CAN 없이도 보드 단독으로 검증할 수 있는 구조를 먼저 잡아둔 것이 이후 디버깅에 큰 도움이 되었습니다.</p>
<p>그런데 시작부터 UART가 아예 반응하지 않았습니다.</p>
<p>코드를 여러 번 확인했지만 문제는 없었습니다. 오히려 코드가 정상이라서 더 혼란스러웠습니다.</p>
<p>&quot;이 정도면 코드 문제는 아닌데?&quot;</p>
<p>그때부터 핀맵을 하나씩 다시 보기 시작했습니다. 결과적으로 B-L475E 보드에서 USART1의 TX/RX 핀이 PA9/PA10이 아니라 <strong>ST-LINK VCP와 연결된 PB6/PB7에 내부 연결</strong>되어 있다는 걸 뒤늦게 알게 됐습니다. 핀 설정을 수정하자마자 바로 동작했습니다.</p>
<p>UART를 해결하고 나니 이번엔 모터가 전혀 돌지 않았습니다. 코드는 정상이었는데 출력이 없었습니다. 확인해보니 <strong>ENA/ENB 점퍼캡이 빠진 상태</strong>였습니다. 점퍼를 꽂자마자 바로 동작했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bb591e32-b06d-40a3-9bff-f75568a5bc1f/image.png" /></p>
<p>이 경험 이후로 문제가 생기면 코드보다 하드웨어 상태를 먼저 확인하는 습관이 생겼습니다.</p>
<p>방향 제어는 IN1~IN4 핀 조합으로 결정됩니다.</p>
<pre><code class="language-c">// 전진
IN1=H, IN2=L / IN3=H, IN4=L

// 좌회전 (제자리)
IN1=L, IN2=H / IN3=H, IN4=L

// 정지 (브레이크 모드)
IN1=H, IN2=H / IN3=H, IN4=H</code></pre>
<blockquote>
<p>⚠️ IN 핀을 모두 LOW로 내리면 L298N이 <strong>coast(공회전) 모드</strong>로 동작해 관성 주행이 발생합니다. 브레이크를 걸려면 HIGH로 설정해야 합니다. 처음에 이걸 몰라서 정지 명령 후에도 차량이 계속 굴러가는 문제를 겪었습니다.</p>
</blockquote>
<h3 id="엔코더-rpm-측정">엔코더 RPM 측정</h3>
<p>TIM5, TIM3을 Encoder Mode로 설정하면 A/B 채널 신호로 카운트를 자동으로 쌓아줍니다. 10ms마다 TIM6 인터럽트에서 카운트 변화량을 읽어 RPM을 계산합니다.</p>
<pre><code class="language-c">#define PULSE_PER_REV   5280    // 실측 확정값

void Encoder_Update(void) {
    int16_t cnt_L = (int16_t)TIM5-&gt;CNT;
    int16_t cnt_R = (int16_t)TIM3-&gt;CNT;
    TIM5-&gt;CNT = 0;
    TIM3-&gt;CNT = 0;

    rpm_L = ((float)cnt_L / PULSE_PER_REV) * (1000.0f / PID_INTERVAL_MS) * 60.0f;
    rpm_R = ((float)cnt_R / PULSE_PER_REV) * (1000.0f / PID_INTERVAL_MS) * 60.0f;
}</code></pre>
<p>PULSE_PER_REV는 모터 스펙을 그대로 쓰다가 실측값(5280)과 차이가 있어서 직접 세서 확정했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/59ac0dce-8df5-47e8-ad87-2c54c192dce2/image.png" /></p>
<p>배선 초기에 A/B 채널을 반대로 연결해서 RPM이 음수로 나오는 문제도 있었습니다. 코드 수정 없이 배선을 교체해서 해결했고, 이후로는 엔코더 배선할 때 방향을 먼저 확인하는 습관이 생겼습니다.</p>
<blockquote>
<p>⚠️ STM32CubeIDE 기본 설정에서 <code>float</code> printf가 비활성화되어 있어 RPM 출력이 안 됩니다. 링커 플래그에 <code>-u _printf_float</code>를 추가해야 합니다.</p>
</blockquote>
<h3 id="속도-pid-제어">속도 PID 제어</h3>
<p>전진 시에만 PID를 활성화합니다. 회전, 후진, U턴은 고정 PWM으로 동작합니다.</p>
<pre><code class="language-c">#define KP              0.5f
#define KI              0.05f
#define KD              0.0f
#define INTEGRAL_LIMIT  150.0f
#define PWM_OFFSET      300.0f

float PID_Compute(float target, float current, float *integral, float *prev_error) {
    float error = target - current;
    *integral += error * (PID_INTERVAL_MS / 1000.0f);
    *integral = fmaxf(-INTEGRAL_LIMIT, fminf(INTEGRAL_LIMIT, *integral));
    float output = KP * error + KI * (*integral);
    *prev_error = error;
    return fmaxf(0, fminf(PWM_MAX, output + PWM_OFFSET));
}</code></pre>
<p>초기에 <code>KI=0.3f</code>로 설정했다가 오버슈트가 심해서 RPM이 계속 튀었습니다. 수치를 하나씩 낮춰보다가 <code>KI=0.05f</code>에서 안정적으로 수렴하는 걸 확인했습니다.</p>
<p>황당한 버그도 하나 있었습니다. <code>Motor_Forward()</code> 함수 안에 <code>pid_enable = 1</code> 설정을 빠뜨린 것이었습니다. 전진 명령을 내려도 PID가 전혀 활성화되지 않아서 속도 제어 자체가 동작하지 않았고, 코드 전체를 뒤져보고 나서야 찾은 버그였습니다.</p>
<h3 id="can-통신-추가">CAN 통신 추가</h3>
<p>CAN 명령(0x010)을 받아 방향과 RPM 목표값을 설정하고, 속도 피드백(0x100)과 Heartbeat(0x200)를 주기적으로 송신합니다.</p>
<pre><code class="language-c">// Byte[0]: 방향 (0=정지, 1=전진, 2=후진, 3=좌, 4=우, 5=U턴)
// Byte[1]: RPM×10 상위 바이트
// Byte[2]: RPM×10 하위 바이트
uint8_t dir = rx_data[0];
float target_rpm = ((rx_data[1] &lt;&lt; 8) | rx_data[2]) / 10.0f;</code></pre>
<p>CAN 타임아웃을 5초로 잡은 이유는, 일시적인 패킷 손실과 완전한 통신 단절을 구분하기 위해서였습니다. 너무 짧으면 잠깐의 지연에도 모터가 멈추고, 너무 길면 실제 장애 상황에서 대응이 늦어집니다.</p>
<pre><code class="language-c">#define CAN_CMD_TIMEOUT_MS  5000

// TIM6 인터럽트에서
can_timeout_cnt += PID_INTERVAL_MS;
if (can_timeout_cnt &gt;= CAN_CMD_TIMEOUT_MS) {
    Motor_Stop();
}
// CAN 수신 콜백에서
can_timeout_cnt = 0;</code></pre>
<p>여기서도 놓친 게 있었습니다. U턴(DIR=5) 케이스를 <code>switch</code>문에 추가하는 걸 빠뜨렸습니다. U턴 명령을 보내도 <code>default</code>(정지)로 처리돼서 차량이 전혀 반응하지 않았고, RPi1 쪽 로그를 아무리 봐도 정상으로 나와서 한참 헤맸습니다. 결국 STM32 코드를 다시 보다가 switch 케이스가 빠진 걸 발견했습니다.</p>
<hr />
<h2 id="8-mangom32-can-통신-검증-상세">8. MangoM32 CAN 통신 검증 상세</h2>
<p>앞서 간략히 언급했던 MangoM32 검증 과정을 상세히 정리합니다.</p>
<h3 id="외부-디버거-연결">외부 디버거 연결</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/03860258-0609-4fbc-8b8b-64184aeda5e9/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fab2e472-f3d6-49c5-96ee-292be6a684bf/image.png" /></p>
<p>MangoM32는 ST-Link가 내장되어 있지 않아 외부 디버거가 필요합니다. NUCLEO F411RE 보드의 상단 ST-Link 부분에서 CN2 점퍼캡을 제거해 하단 타겟 보드와의 연결을 차단한 뒤, MangoM32의 SWD 핀에 직접 연결했습니다.</p>
<pre><code>NUCLEO ST-Link → MangoM32
SWDIO → PA13 / SWCLK → PA14 / GND → GND</code></pre><p>처음 써보는 방식이라 연결 방법 자체를 파악하는 데도 시간이 걸렸습니다.</p>
<h3 id="플래시-실패--칩이-잠겼다">플래시 실패 — 칩이 잠겼다</h3>
<p>외부 디버거를 연결하고 처음 플래시를 시도했을 때, 예상치 못한 문제가 발생했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/31fa5378-f2f9-40fe-8da1-245d940e3794/image.png" /></p>
<pre><code>Error finishing flash operation
Cannot connect to access port 0
No device found on target
Could not read registers</code></pre><p>시도할 때마다 증상이 점점 악화됐습니다. 원인은 1차 플래시 실패로 칩이 HardFault 상태에 빠진 것이었습니다. ST-LINK가 레지스터 자체에 접근할 수 없는 상태가 된 것입니다.</p>
<p>해결은 STM32CubeProgrammer를 통해 강제로 칩을 초기화하는 방식으로 진행했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3c50d894-ee63-4c3f-9316-80b256a50b62/image.png" /></p>
<pre><code>① STM32CubeProgrammer 실행
② Interface: SWD / Mode: Under Reset / Reset mode: Hardware reset
③ NRST 핀 연결 (Nucleo CN4 Pin5 → MangoM32 NRST)
④ MangoM32 전원 켠 상태에서 Connect
⑤ Full chip erase 수행
⑥ STM32CubeIDE Debug Configurations → Connect under reset 설정
⑦ 재플래시 성공</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5558d9f7-e3fe-404e-b0a5-d026273d5e59/image.png" /></p>
<blockquote>
<p>Under Reset 모드는 칩이 리셋 상태를 유지하는 동안 ST-LINK가 연결을 시도하는 방식입니다. 일반 모드로는 접근조차 불가능했던 칩에 접근할 수 있었습니다.</p>
</blockquote>
<h3 id="mangom32-can-설정-주의사항">MangoM32 CAN 설정 주의사항</h3>
<p>MangoM32(STM32F103)는 CAN 핀 설정에 <strong>AFIO Remap</strong>이 필요합니다.</p>
<pre><code class="language-c">__HAL_AFIO_REMAP_CAN1_2();  // PB8(RX), PB9(TX) 사용</code></pre>
<p>MangoM32에는 HSE 크리스탈이 없어서 <strong>HSI 기반 클럭</strong>으로 변경해야 합니다.</p>
<pre><code>HSI 8MHz → PLL×6 → SYSCLK 48MHz
APB1 /2  → PCLK1 24MHz
CAN: Prescaler=6, BS1=13TQ, BS2=2TQ → 250 kbps</code></pre><h3 id="단계별-can-검증">단계별 CAN 검증</h3>
<p><strong>Phase 1 — Silent Loopback (트랜시버 없이)</strong></p>
<pre><code class="language-c">hcan.Init.Mode = CAN_MODE_SILENT_LOOPBACK;</code></pre>
<p>초기에 <code>HAL_CAN_Start()</code>가 <code>HAL_ERROR</code>를 반환했습니다. <code>CAN_MODE_LOOPBACK</code>에서 외부 ACK를 받지 못해 INAK 비트가 해제되지 않는 것이 원인이었습니다. <code>CAN_MODE_SILENT_LOOPBACK</code>으로 변경해서 해결했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5aba1e9f-d0e0-4b28-a7e1-67ac6f411f63/image.png" /></p>
<p>TX는 나오는데 RX 콜백이 전혀 호출되지 않는 문제도 있었습니다. CubeMX NVIC Settings에서 CAN RX0 인터럽트를 활성화하지 않은 것이 원인이었습니다. 설정 화면을 다시 들여다보다가 체크박스가 꺼져 있는 걸 발견했습니다.</p>
<p><strong>Phase 2 — Loopback (트랜시버 연결)</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1ba0f964-24d1-492e-8abc-df14cc72de75/image.png" /></p>
<pre><code class="language-c">hcan.Init.Mode = CAN_MODE_LOOPBACK;</code></pre>
<p>USB-CAN 어댑터와 Cangaroo 프로그램으로 실제 CAN 신호를 시각적으로 확인했습니다.</p>
<p>이 단계에서 두 가지 문제가 겹쳐 있었습니다. 첫째는 <strong>트랜시버 모듈 자체 불량</strong>이었습니다. 둘째는 <strong>종단저항 중복 구성</strong>이었습니다. 교수님께 받아 사용하던 CAN 트랜시버 모듈 내부에 이미 120Ω이 달려 있는데, 외부에도 저항을 추가로 연결하면서 병렬 합성 저항값이 너무 낮아진 것이었습니다. CAN 버스 임피던스가 맞지 않으면 신호 품질이 떨어져 통신이 불안정해집니다.
버스 끝단에만 종단저항을 두고, 중간 노드는 내장 저항을 반드시 비활성화해야 합니다.</p>
<p><strong>Phase 3 — Normal Mode (2노드 통신)</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bff4c99f-3560-4586-ba49-b7e6b3d41432/image.png" /></p>
<p>실제 통신 모드입니다. Normal 모드에서는 ACK가 반드시 필요하므로 수신 노드가 연결되어 있어야 합니다.</p>
<p>두 노드 간 실제 통신이 되는지 확인하기 위해 USB-CAN 어댑터와 Cangaroo를 활용했습니다. MangoM32에서 CAN 프레임을 송신하고, Cangaroo에서 수신되는 메시지를 실시간으로 확인하는 방식으로 진행했습니다. 화면 오른쪽에서 0x301, 0x302, 0x303 등 실제 프로젝트에서 사용할 CAN ID의 데이터가 정상적으로 수신되는 걸 확인할 수 있었습니다.</p>
<pre><code class="language-c">hcan.Init.Mode = CAN_MODE_NORMAL;</code></pre>
<p><img alt="normal mode test" src="https://velog.velcdn.com/images/mommers/post/a8f92ff2-c404-4f33-9730-a328fd5b6b7d/image.png" /></p>
<p>PB8 핀에 외부 pull-up이 없으면 Normal mode 진입에 실패하는 경우가 있었습니다. 외부 pull-up 저항을 추가하고 DBF 비트 초기화 순서를 정정해서 해결했습니다.</p>
<p>이 단계를 통과하고 나서야 비로소 3노드 통합으로 넘어갈 수 있었습니다.</p>
<hr />
<h2 id="9-fail-safe--iwdg-watchdog">9. Fail-safe — IWDG Watchdog</h2>
<p>RPi1이 완전히 다운됐을 때를 대비한 하드웨어 안전장치입니다.</p>
<pre><code>IWDG: Prescaler=/32, Reload=300 → 300ms 타임아웃</code></pre><p>소프트웨어 타임아웃(5초)과 하드웨어 Watchdog(300ms)을 함께 쓰는 이유는 역할이 다르기 때문입니다. 소프트웨어 타임아웃은 CAN 명령이 잠깐 끊겼을 때를 대응하고, IWDG는 MCU 자체가 hang 상태에 빠졌을 때를 대응합니다.</p>
<hr />
<h2 id="마치며">마치며</h2>
<p>이 과정을 거치면서 느낀 건 하나였습니다.</p>
<blockquote>
<p><strong>&quot;임베디드에서는 코드보다 하드웨어가 더 오래 걸린다.&quot;</strong></p>
</blockquote>
<p>핀 하나 잘못 잡으면 몇 시간을 날릴 수 있고, CAN 통신도 단계 없이 붙이면 어디서 막혔는지 알 수 없습니다. 덕분에 이후 개발에서는 항상 <strong>&quot;단계를 나눠서 검증하는 방식&quot;</strong> 을 먼저 고려하게 되었습니다.</p>
<p>다음 글에서는 3개 노드 통합 과정과 실제 시연 중 발생한 트러블슈팅을 다룹니다.</p>
<p><strong>🔗 GitHub</strong>
전체 구현 코드는 GitHub에 정리해두었습니다.</p>
<p><a href="https://github.com/kyoung-mo/can-based-autonomous-delivery-car"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&amp;logo=github" /></a></p>
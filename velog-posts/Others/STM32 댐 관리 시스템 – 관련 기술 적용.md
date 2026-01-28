<h2 id="🎯-mcu">🎯 MCU</h2>
<p><strong>STM32-F411RE (ARM Cortex-M4)</strong></p>
<h3 id="적용-내용">적용 내용</h3>
<ul>
<li>32비트 ARM Cortex-M4 기반 임베디드 시스템</li>
<li>최대 84MHz 클럭으로 실시간 멀티태스킹 처리</li>
<li>비밀번호 인증, 센서 모니터링, 자동 제어를 동시 수행</li>
</ul>
<h3 id="역할">역할</h3>
<ul>
<li>시스템 전체 제어의 중심</li>
<li>모든 하드웨어 모듈 통합 관리</li>
<li>사용자 인터페이스 처리</li>
</ul>
<hr />
<h2 id="📡-통신">📡 통신</h2>
<h3 id="uart-universal-asynchronous-receivertransmitter">UART (Universal Asynchronous Receiver/Transmitter)</h3>
<p><strong>적용 위치:</strong> 디버그 콘솔 출력</p>
<p><strong>기능</strong></p>
<ul>
<li>PC ↔ MCU 시리얼 통신으로 시스템 로그 전송</li>
<li>비밀번호 입력, 센서 값, 제어 명령 모니터링</li>
<li>실시간 디버깅 및 시스템 상태 확인</li>
</ul>
<p><strong>예시 출력</strong></p>
<pre><code>[LOGIN] Success! RGB LED Enabled.
[SERVO1] Angle: 90 deg
[AUTO] LOW: Servo1=90, Servo2=0</code></pre><h3 id="i2c-inter-integrated-circuit">I2C (Inter-Integrated Circuit)</h3>
<p><strong>적용 위치:</strong> LCD 디스플레이</p>
<p><strong>기능</strong></p>
<ul>
<li>16×2 LCD와 양방향 통신</li>
<li>2개 핀(SCL, SDA)만으로 데이터 전송</li>
<li>시스템 상태, 메뉴, 로그 출력</li>
</ul>
<p><strong>핀 연결 예</strong></p>
<ul>
<li>PB8 (SCL) ↔ LCD 클럭</li>
<li>PB9 (SDA) ↔ LCD 데이터</li>
</ul>
<hr />
<h2 id="🎮-제어-및-주변장치">🎮 제어 및 주변장치</h2>
<h3 id="gpio-general-purpose-inputoutput">GPIO (General Purpose Input/Output)</h3>
<p><strong>입력</strong></p>
<ul>
<li>4×4 키패드: 비밀번호 입력 및 설정 변경</li>
<li>조이스틱 버튼: 메뉴 선택 및 확인</li>
</ul>
<p><strong>출력</strong></p>
<ul>
<li>LED: 비밀번호 성공/실패 표시</li>
<li>RGB LED: 수위 상태 시각화 (LOW / OK / HIGH)</li>
<li>부저: 경고음 및 알림</li>
<li>DHT11: 온습도 센서 데이터 통신</li>
</ul>
<hr />
<h3 id="pwm-pulse-width-modulation">PWM (Pulse Width Modulation)</h3>
<p><strong>적용 위치:</strong> 서보모터 제어</p>
<p><strong>원리</strong></p>
<ul>
<li><p>TIM3 타이머 기반 50Hz PWM 생성</p>
</li>
<li><p>펄스 폭으로 서보모터 각도 제어</p>
<ul>
<li>1000µs → 0° (댐 닫힘)</li>
<li>2000µs → 90° (댐 개방)</li>
</ul>
</li>
</ul>
<p><strong>기능</strong></p>
<ul>
<li>서보모터 1: 상류댐 제어 (수위 LOW 시 개방)</li>
<li>서보모터 2: 하류댐 제어 (수위 HIGH 시 개방)</li>
</ul>
<hr />
<h3 id="adc-analog-to-digital-converter">ADC (Analog-to-Digital Converter)</h3>
<p><strong>적용 위치:</strong> 아날로그 센서 입력</p>
<p><strong>채널 구성</strong></p>
<ul>
<li>ADC1_IN0 (PA0): 조이스틱 X축 (VRx)</li>
<li>ADC1_IN1 (PA1): 수위 센서</li>
<li>ADC1_IN4 (PA4): 조이스틱 Y축 (VRy)</li>
<li>Internal Temp Sensor: MCU 내부 온도</li>
</ul>
<p><strong>동작 방식</strong></p>
<ul>
<li>DMA 기반 4채널 자동 변환</li>
<li>12비트 해상도 (0~4095)</li>
<li>수위 → 백분율 변환: <code>(ADC × 100) / 4095</code></li>
</ul>
<hr />
<h3 id="rtc-real-time-clock">RTC (Real-Time Clock)</h3>
<p><strong>적용 위치:</strong> 시간 정보 관리</p>
<p><strong>클럭 소스</strong></p>
<ul>
<li>LSI (32kHz 내부 발진기)</li>
<li>PC14/PC15를 GPIO로 활용 가능</li>
</ul>
<p><strong>기능</strong></p>
<ul>
<li>날짜/시간 표시 (YYYY-MM-DD HH:MM:SS)</li>
<li>로그 이벤트 타임스탬프 기록</li>
<li>1초 주기 자동 업데이트</li>
</ul>
<hr />
<h2 id="🛠️-개발-언어">🛠️ 개발 언어</h2>
<h3 id="embedded-c">Embedded C</h3>
<h4 id="1-하드웨어-직접-제어">1. 하드웨어 직접 제어</h4>
<ul>
<li>GPIO ON/OFF 제어</li>
<li>ADC 값 읽기</li>
<li>타이머 및 인터럽트 설정</li>
</ul>
<h4 id="2-베어메탈-프로그래밍">2. 베어메탈 프로그래밍</h4>
<ul>
<li>RTOS 미사용</li>
<li>STM32 HAL 라이브러리 활용</li>
<li>폴링 기반 입력 처리</li>
<li>타이머 기반 비동기 동작</li>
<li><code>HAL_Delay</code> 최소화</li>
</ul>
<h4 id="3-메모리-최적화">3. 메모리 최적화</h4>
<ul>
<li>Flash: 512KB</li>
<li>SRAM: 128KB</li>
<li>로그 순환 버퍼 (최대 10개)</li>
<li>전역 변수 최소화</li>
</ul>
<hr />
<h2 id="🔧-세부-기술-적용-사례">🔧 세부 기술 적용 사례</h2>
<h3 id="1-제어-보드-stm32-f411re">1. 제어 보드 (STM32-F411RE)</h3>
<p><strong>비밀번호 인증 시스템</strong></p>
<ul>
<li>GPIO 키패드 + 상태 머신</li>
<li>4자리 숫자 입력</li>
<li>5회 실패 시 60초 잠금</li>
<li>성공 시 시스템 활성화</li>
</ul>
<p><strong>백그라운드 태스킹</strong></p>
<ul>
<li>타이머 기반 비블로킹 처리</li>
<li>DHT11: 2초 주기</li>
<li>RTC: 1초 주기</li>
<li>수위 로그: 1초 주기</li>
<li>RGB LED: 실시간 상태 표시</li>
</ul>
<hr />
<h3 id="2-입력-장치">2. 입력 장치</h3>
<h4 id="4×4-매트릭스-키패드">4×4 매트릭스 키패드</h4>
<ul>
<li>행(Row): PA8~PA11 (Output)</li>
<li>열(Col): PB5, PB6, PB12, PB13 (Input Pull-up)</li>
<li>디바운싱 적용</li>
<li>비밀번호 및 기준치 설정</li>
</ul>
<h4 id="조이스틱-모듈">조이스틱 모듈</h4>
<ul>
<li>ADC 기반 방향 감지</li>
<li>임계값으로 방향 판별</li>
<li>버튼 입력으로 메뉴 선택</li>
<li>Y축: 메인 메뉴 / X축: 서브 메뉴</li>
</ul>
<hr />
<h3 id="3-출력-장치">3. 출력 장치</h3>
<h4 id="서보모터-sg90">서보모터 (SG90)</h4>
<ul>
<li>TIM3 PWM (50Hz)</li>
<li>자동/수동 제어 모드 지원</li>
</ul>
<h4 id="led">LED</h4>
<ul>
<li>적색 LED (PC13): 오류, 고온 경고</li>
<li>녹색 LED (PC3): 인증 성공</li>
<li>타이머 기반 자동 소등</li>
</ul>
<h4 id="i2c-lcd-16×2--20×4">I2C LCD (16×2 / 20×4)</h4>
<ul>
<li>PCF8574 I/O 확장 칩 사용</li>
<li>메뉴, 센서, 로그 출력</li>
<li>텍스트 레이아웃 최적화</li>
</ul>
<h4 id="rgb-led">RGB LED</h4>
<ul>
<li><p>공통 캐소드 타입</p>
</li>
<li><p>수위 상태 표시</p>
<ul>
<li>빨강: LOW</li>
<li>초록: OK</li>
<li>파랑: HIGH</li>
</ul>
</li>
<li><p>로그인 후 활성화</p>
</li>
</ul>
<h4 id="부저">부저</h4>
<ul>
<li>능동 부저</li>
<li>실패/경고 알림</li>
<li>0.3~0.5초 자동 OFF</li>
</ul>
<hr />
<h3 id="4-센서">4. 센서</h3>
<h4 id="dht11-온습도-센서">DHT11 온습도 센서</h4>
<ul>
<li>1-Wire 통신</li>
<li>10kΩ 풀업 저항 필요</li>
<li>2초 주기 측정</li>
<li>30°C 이상 시 경고</li>
</ul>
<h4 id="수위-센서">수위 센서</h4>
<ul>
<li>아날로그 입력</li>
<li>ADC 값 기반 수위 계산</li>
<li>자동 제어 및 로그 기준</li>
</ul>
<hr />
<h3 id="5-기타">5. 기타</h3>
<h4 id="rtc">RTC</h4>
<ul>
<li>내부 LSI 기반</li>
<li>외부 크리스탈 불필요</li>
<li>로그 타임스탬프 제공</li>
</ul>
<h4 id="프로토타이핑">프로토타이핑</h4>
<ul>
<li><p>브레드보드, 점퍼 케이블</p>
</li>
<li><p>저항</p>
<ul>
<li>220Ω: LED 전류 제한</li>
<li>10kΩ: DHT11, 키패드 풀업</li>
</ul>
</li>
</ul>
<hr />
<h2 id="📊-시스템-구조도">📊 시스템 구조도</h2>
<pre><code>[사용자]
   ↓
[키패드] → [비밀번호 인증] → [메인 메뉴]
[조이스틱] → [메뉴 네비게이션]
                  ↓
        ┌─────────┴─────────┐
        ↓                   ↓
   [모니터링]           [제어]
        ↓                   ↓
   - 수위 센서         - 서보모터 제어
   - DHT11 센서        - 자동/수동 모드
   - RTC 시계          - 기준치 설정
        ↓                   ↓
   [로그 기록]         [RGB LED 표시]
        ↓                   ↓
   [LCD 디스플레이] ← [I2C 통신]</code></pre><hr />
<h2 id="🎯-핵심-기술-요약">🎯 핵심 기술 요약</h2>
<table>
<thead>
<tr>
<th>기술</th>
<th>적용 위치</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td>UART</td>
<td>디버그 콘솔</td>
<td>시스템 로그 출력</td>
</tr>
<tr>
<td>I2C</td>
<td>LCD</td>
<td>메뉴/상태 표시</td>
</tr>
<tr>
<td>GPIO</td>
<td>키패드, LED, 부저</td>
<td>입출력 제어</td>
</tr>
<tr>
<td>PWM</td>
<td>서보모터</td>
<td>댐 개폐 제어</td>
</tr>
<tr>
<td>ADC</td>
<td>수위, 조이스틱</td>
<td>아날로그 센서 입력</td>
</tr>
<tr>
<td>RTC</td>
<td>시간 관리</td>
<td>날짜/시간 기록</td>
</tr>
<tr>
<td>타이머</td>
<td>백그라운드 태스크</td>
<td>비블로킹 처리</td>
</tr>
<tr>
<td>상태 머신</td>
<td>모드 제어</td>
<td>시스템 동작 관리</td>
</tr>
<tr>
<td>순환 버퍼</td>
<td>로그 저장</td>
<td>메모리 효율 관리</td>
</tr>
</tbody></table>
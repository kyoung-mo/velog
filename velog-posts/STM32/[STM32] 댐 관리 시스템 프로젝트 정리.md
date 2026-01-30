<h2 id="🌊-stm32-dam-control-system---미니프로젝트-회고">🌊 STM32 Dam Control System - 미니프로젝트 회고</h2>
<blockquote>
<p>STM32F411 기반 스마트 댐 관리 시스템 개발 과정</p>
</blockquote>
<hr />
<h2 id="📋-목차">📋 목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#1-%EA%B0%9C%EB%B0%9C-%EB%AA%A9%ED%91%9C">개발 목표</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EC%84%A4%EA%B3%84">시스템 설계</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4-%EA%B5%AC%EC%84%B1">하드웨어 구성</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84">주요 기능 구현</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-%EC%8B%9C%EC%97%B0-%EC%98%81%EC%83%81">시연 영상</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-%ED%95%B5%EC%8B%AC-%EC%BD%94%EB%93%9C">핵심 코드</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-%ED%8A%B8%EB%9F%AC%EB%B8%94-%EC%8A%88%ED%8C%85">트러블 슈팅</a></li>
<li><a href="https://api.velog.io/rss/@mommers#8-%ED%9A%8C%EA%B3%A0">회고</a></li>
</ol>
<hr />
<h2 id="1-개발-목표">1. 개발 목표</h2>
<p>실시간 수위 센서 데이터를 기반으로 상류/하류 댐을 자동 또는 수동으로 제어하며, LCD와 RGB LED를 통한 직관적인 모니터링 인터페이스를 제공하는 <strong>IoT 댐 관리 시스템</strong> 개발</p>
<h3 id="프로젝트-개요">프로젝트 개요</h3>
<p>중앙 댐의 수위를 실시간으로 모니터링하고, 상류댐/하류댐 수문을 자동 또는 수동으로 제어하여 안정적인 수위 범위를 유지하는 임베디드 제어 시스템</p>
<hr />
<h2 id="2-시스템-설계">2. 시스템 설계</h2>
<h3 id="시스템-아키텍처">시스템 아키텍처</h3>
<pre><code>┌─────────────────────────────────────┐
│     STM32F411 Main Controller    │
├─────────────────────────────────────┤
│  🔐 Security    │ 📊 Monitoring  │
│  - Password     │  - Water Level │
│  - Access Lock  │  - Temperature │
├─────────────────────────────────────┤
│  🎮 Control     │  💾 Data Logger│
│  - Auto/Manual  │  - History     │
│  - Servo Motors │  - RTC Clock   │
└─────────────────────────────────────┘</code></pre><h3 id="동작-과정">동작 과정</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/41a7140a-3035-4ee7-8b84-8eeaa367ad96/image.png" /></p>
<hr />
<h2 id="3-하드웨어-구성">3. 하드웨어 구성</h2>
<h3 id="사용-부품">사용 부품</h3>
<table>
<thead>
<tr>
<th>구성요소</th>
<th>모델/사양</th>
<th>용도</th>
</tr>
</thead>
<tbody><tr>
<td>MCU</td>
<td>STM32F411CEU6</td>
<td>메인 컨트롤러</td>
</tr>
<tr>
<td>온습도 센서</td>
<td>DHT11</td>
<td>환경 모니터링</td>
</tr>
<tr>
<td>수위 센서</td>
<td>아날로그 수위 센서</td>
<td>물 높이 측정</td>
</tr>
<tr>
<td>디스플레이</td>
<td>I2C LCD 1602</td>
<td>정보 표시</td>
</tr>
<tr>
<td>입력 장치</td>
<td>4x4 매트릭스 키패드</td>
<td>비밀번호/설정</td>
</tr>
<tr>
<td>입력 장치</td>
<td>조이스틱</td>
<td>메뉴 네비게이션</td>
</tr>
<tr>
<td>액추에이터</td>
<td>서보모터 x2</td>
<td>수문 제어</td>
</tr>
<tr>
<td>표시 장치</td>
<td>RGB LED</td>
<td>상태 표시</td>
</tr>
<tr>
<td>알림 장치</td>
<td>능동 부저</td>
<td>경고음</td>
</tr>
</tbody></table>
<h3 id="핀맵-stm32f411re">핀맵 (STM32F411RE)</h3>
<table>
<thead>
<tr>
<th>핀</th>
<th>기능</th>
<th>연결 장치</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>PA0</strong></td>
<td>ADC1_IN0</td>
<td>조이스틱 VRx</td>
<td>X축 아날로그 입력</td>
</tr>
<tr>
<td><strong>PA1</strong></td>
<td>ADC1_IN1</td>
<td>수위 센서</td>
<td>수위 아날로그 입력</td>
</tr>
<tr>
<td><strong>PA4</strong></td>
<td>ADC1_IN4</td>
<td>조이스틱 VRy</td>
<td>Y축 아날로그 입력</td>
</tr>
<tr>
<td><strong>PA6</strong></td>
<td>TIM3_CH1</td>
<td>서보모터 1</td>
<td>상류댐 PWM</td>
</tr>
<tr>
<td><strong>PA7</strong></td>
<td>TIM3_CH2</td>
<td>서보모터 2</td>
<td>하류댐 PWM</td>
</tr>
<tr>
<td><strong>PA8~11</strong></td>
<td>GPIO_Output</td>
<td>키패드 Row1~4</td>
<td>4×4 키패드 행</td>
</tr>
<tr>
<td><strong>PB0</strong></td>
<td>GPIO_Input</td>
<td>조이스틱 SW</td>
<td>버튼 (풀업)</td>
</tr>
<tr>
<td><strong>PB1</strong></td>
<td>GPIO_Output</td>
<td>DHT11 DATA</td>
<td>온습도 데이터</td>
</tr>
<tr>
<td><strong>PB5,6,12,13</strong></td>
<td>GPIO_Input</td>
<td>키패드 Col1~4</td>
<td>4×4 키패드 열 (풀업)</td>
</tr>
<tr>
<td><strong>PB8</strong></td>
<td>I2C1_SCL</td>
<td>LCD SCL</td>
<td>I2C 클럭</td>
</tr>
<tr>
<td><strong>PB9</strong></td>
<td>I2C1_SDA</td>
<td>LCD SDA</td>
<td>I2C 데이터</td>
</tr>
<tr>
<td><strong>PB10</strong></td>
<td>GPIO_Output</td>
<td>부저</td>
<td>능동 부저</td>
</tr>
<tr>
<td><strong>PC0~2</strong></td>
<td>GPIO_Output</td>
<td>RGB LED R/G/B</td>
<td>3색 LED</td>
</tr>
<tr>
<td><strong>PC3</strong></td>
<td>GPIO_Output</td>
<td>LED_GREEN</td>
<td>인증 성공 LED</td>
</tr>
<tr>
<td><strong>PC13</strong></td>
<td>GPIO_Output</td>
<td>LED_RED</td>
<td>인증 실패 LED</td>
</tr>
</tbody></table>
<h3 id="하드웨어-사진">하드웨어 사진</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1d62dbc9-8095-4c74-9492-e34d6a8966a3/image.png" /></p>
<p><img alt="전체 시스템" src="https://velog.velcdn.com/images/mommers/post/42623f10-02a1-4d4b-b8ce-84a4fc23abb0/image.png" /></p>
<p><img alt="LCD 화면" src="https://velog.velcdn.com/images/mommers/post/4d8a97bd-fa5e-4fd4-b565-8cbf109b1f55/image.png" /></p>
<p><img alt="서보모터 제어" src="https://velog.velcdn.com/images/mommers/post/e5280e3b-9bb9-42e8-8756-c61088dc456c/image.png" /></p>
<hr />
<h2 id="4-주요-기능-구현">4. 주요 기능 구현</h2>
<h3 id="🔐-보안-시스템">🔐 보안 시스템</h3>
<ul>
<li>4×4 키패드 기반 4자리 비밀번호 인증</li>
<li>초기 비밀번호: <code>1234</code></li>
<li>실시간 비밀번호 변경 기능</li>
<li>5회 오류 시 시스템 잠금</li>
</ul>
<h3 id="📊-6가지-운영-모드">📊 6가지 운영 모드</h3>
<h4 id="mode-1-water-status-수위-모니터링">MODE 1: Water Status (수위 모니터링)</h4>
<ul>
<li>실시간 수위 표시 (0~60%)</li>
<li>RGB LED 상태 표시:<ul>
<li>🔴 <strong>빨강</strong>: 수위 &lt; LOW (위험)</li>
<li>🟢 <strong>녹색</strong>: LOW ≤ 수위 ≤ HIGH (정상)</li>
<li>🔵 <strong>파랑</strong>: 수위 &gt; HIGH (범람 위험)</li>
</ul>
</li>
</ul>
<h4 id="mode-2-dam-control-댐-제어">MODE 2: Dam Control (댐 제어)</h4>
<p><strong>수동 모드 (Passive Mode)</strong></p>
<ul>
<li>서보모터 1/2 개별 제어</li>
<li>0° ↔ 90° 토글 방식</li>
</ul>
<p><strong>자동 모드 (Active Mode)</strong></p>
<ul>
<li>수위 &lt; LOW → 서보1 90° (상류댐 개방)</li>
<li>수위 &gt; HIGH → 서보2 90° (하류댐 개방)</li>
<li>정상 범위 → 둘 다 0° (폐쇄)</li>
</ul>
<h4 id="mode-3-threshold-set-임계값-설정">MODE 3: Threshold Set (임계값 설정)</h4>
<ul>
<li>HIGH/LOW 임계값 설정 (0~50%)</li>
<li>유효성 검사: LOW &lt; HIGH</li>
<li>키패드를 통한 숫자 입력</li>
</ul>
<h4 id="mode-4-environment-환경-정보">MODE 4: Environment (환경 정보)</h4>
<ul>
<li>DHT11 온습도 센서</li>
<li>시스템 온도 표시</li>
<li>온도 ≥ 30°C 시 LED 경고</li>
</ul>
<h4 id="mode-5-clock-시계">MODE 5: Clock (시계)</h4>
<ul>
<li>RTC 기반 실시간 시계</li>
<li>날짜: YYYY-MM-DD</li>
<li>시간: HH:MM:SS</li>
<li>백그라운드 자동 업데이트</li>
</ul>
<h4 id="mode-6-change-password-비밀번호-변경">MODE 6: Change Password (비밀번호 변경)</h4>
<ul>
<li>새 비밀번호 입력 (4자리)</li>
<li>변경 후 재로그인 필요</li>
</ul>
<hr />
<h2 id="5-시연-영상">5. 시연 영상</h2>
<h3 id="시스템-시작-및-로그인">시스템 시작 및 로그인</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a022e603-f429-4176-a419-4e6cb17f7135/image.gif" /></p>
<ul>
<li>✅ <strong>CORRECT</strong>: 녹색 LED 점등</li>
<li>❌ <strong>WRONG</strong>: 빨간 LED + 부저</li>
</ul>
<h3 id="모드-간-전환">모드 간 전환</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/363e6058-daa7-4421-84d0-ac38a1c7b1a4/image.gif" /></p>
<ul>
<li>조이스틱으로 모드 전환</li>
</ul>
<h3 id="mode-1-수위-모니터링">MODE 1: 수위 모니터링</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/86500441-67a2-4e5c-bd90-f8235fa89f7a/image.gif" /></p>
<h3 id="mode-2-댐-제어">MODE 2: 댐 제어</h3>
<p><strong>수동 모드</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/db191006-7aa5-4e04-8f30-32abe9dfb173/image.gif" /></p>
<p><strong>자동 모드</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6b6ac830-0581-4b55-b2d2-ccdc60d357fd/image.gif" /></p>
<h3 id="mode-3-임계값-설정">MODE 3: 임계값 설정</h3>
<p><strong>HIGH 값 설정 (50 초과 시 에러)</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f726e2f5-5d55-4886-a39f-0e791333712d/image.gif" /></p>
<p><strong>HIGH = 30 설정 성공</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b32fe031-73a9-4201-9823-620fe63b815f/image.gif" /></p>
<p><strong>LOW 값 설정 (HIGH보다 크면 에러)</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5e3b58cc-372c-4e3a-87b5-1017c3feaf19/image.gif" /></p>
<p><strong>LOW = 12 설정 성공</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f65b8808-599f-44af-b7bb-5d595f6e78a6/image.gif" /></p>
<h3 id="mode-4-환경-정보">MODE 4: 환경 정보</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6eb5f452-919e-4798-9702-3d81784aeec9/image.gif" /></p>
<h3 id="mode-5-시계">MODE 5: 시계</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a2d231c7-6cc1-47f7-98eb-dc2ef25192d9/image.gif" /></p>
<h3 id="mode-6-비밀번호-변경">MODE 6: 비밀번호 변경</h3>
<p><strong>변경 과정</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c216de60-4478-4af0-bae7-8daae5706922/image.gif" /></p>
<p><strong>이전 비밀번호로 로그인 시도</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/96e5c473-30f7-470a-b77a-c0894d92cb33/image.gif" /></p>
<p><strong>새 비밀번호로 로그인</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3300dcc8-f974-475b-8a12-5aa548985e08/image.gif" /></p>
<hr />
<h2 id="6-핵심-코드">6. 핵심 코드</h2>
<h3 id="1️⃣-상태-머신state-machine-기반-설계">1️⃣ 상태 머신(State Machine) 기반 설계</h3>
<pre><code class="language-c">// 시스템 모드 정의
volatile SystemMode_t current_mode = MODE_PASSWORD_INPUT;

// 모드 전환 로직
switch (menu_selected) {
    case 0:
        current_mode = MODE_WATER_STATUS;
        break;
    case 1:
        current_mode = MODE_DAM_CONTROL;
        break;
    case 2:
        current_mode = MODE_THRESHOLD_SET;
        break;
    case 3:
        current_mode = MODE_ENVIRONMENT;
        break;
    case 4:
        current_mode = MODE_CLOCK;
        break;
    case 5:
        current_mode = MODE_PW_CHANGE;
        pw_idx = 0;
        memset(input_pw, 0, sizeof(input_pw));
        break;
    case 6:
        current_mode = MODE_LOG;
        uint8_t cnt = WaterLog_Count(&amp;g_waterlog);
        g_waterlog.view = (cnt &gt; 0) ? (cnt - 1) : 0;
        break;
}</code></pre>
<p><strong>설계 의도:</strong></p>
<ul>
<li>각 화면을 독립적인 상태(State)로 관리</li>
<li>상태 전환 시 초기화 로직 명확화</li>
<li>유지보수 및 기능 추가 용이</li>
</ul>
<hr />
<h3 id="2️⃣-백그라운드-태스크-분리">2️⃣ 백그라운드 태스크 분리</h3>
<pre><code class="language-c">void Update_Background_Tasks(void) {
    uint32_t now = HAL_GetTick();

    // DHT11 센서 읽기 (2초 간격)
    if (now - last_dht11_time &gt;= 2000) {
        last_dht11_time = now;
        dht11_valid = DHT11_Read(&amp;global_dht11_data);
    }

    // RTC 업데이트 및 로그 기록 (1초 간격)
    if (now - last_rtc_time &gt;= 1000) {
        last_rtc_time = now;
        HAL_RTC_GetTime(&amp;hrtc, &amp;global_time, RTC_FORMAT_BIN);
        HAL_RTC_GetDate(&amp;hrtc, &amp;global_date, RTC_FORMAT_BIN);

        uint8_t current_level = (adc_values[1] * 100) / 4095;

        WaterLog_Update(&amp;g_waterlog, 
                        current_level, 
                        threshold_low, 
                        threshold_high, 
                        &amp;global_time, 
                        &amp;global_date);
    }

    // 자동 댐 제어
    if (dam_auto_mode) {
        uint8_t water_level = (adc_values[1] * 100) / 4095;
        Dam_Auto_Control(water_level);
    }
}</code></pre>
<p><strong>설계 의도:</strong></p>
<ul>
<li><code>HAL_Delay()</code> 사용 최소화 → 시스템 응답성 향상</li>
<li>센서 읽기, 시간 업데이트, 자동 제어를 독립적으로 관리</li>
<li>모든 모드에서 백그라운드 태스크 동작</li>
</ul>
<hr />
<h3 id="3️⃣-ui-네비게이션-규칙-통일">3️⃣ UI 네비게이션 규칙 통일</h3>
<pre><code class="language-c">// 조이스틱 방향을 UI 이동으로 매핑
JoyDirection_t dir = Get_Joy_Direction();

// 중복 입력 방지
static JoyDirection_t last_dir = JOY_NONE;
static uint8_t menu_locked = 0;

if (dir == JOY_NONE) {
    last_dir = JOY_NONE;
    menu_locked = 0;
}

if (dir != JOY_NONE &amp;&amp; !menu_locked) {
    if (dir == JOY_UP &amp;&amp; last_dir != JOY_UP) {
        menu_selected = (menu_selected + 1) % 7;
        menu_locked = 1;
    }
    else if (dir == JOY_DOWN &amp;&amp; last_dir != JOY_DOWN) {
        menu_selected = (menu_selected == 0) ? 6 : menu_selected - 1;
        menu_locked = 1;
    }
    last_dir = dir;
}

// 같은 규칙을 모든 화면에 재사용
if (dir == JOY_LEFT &amp;&amp; last_dir != JOY_LEFT) { ... }
else if (dir == JOY_RIGHT &amp;&amp; last_dir != JOY_RIGHT) { ... }</code></pre>
<p><strong>설계 의도:</strong></p>
<ul>
<li>조이스틱 입력을 일관된 규칙으로 처리</li>
<li>중복 입력 방지 (디바운싱 효과)</li>
<li>모든 메뉴에서 동일한 사용자 경험</li>
</ul>
<hr />
<h3 id="4️⃣-hal_delay-제거">4️⃣ HAL_Delay() 제거</h3>
<p><strong>수정 전:</strong></p>
<pre><code class="language-c">HAL_GPIO_WritePin(BUZZER_GPIO_Port, BUZZER_Pin, GPIO_PIN_SET);
HAL_Delay(500);  // ❌ 시스템 블로킹
HAL_GPIO_WritePin(BUZZER_GPIO_Port, BUZZER_Pin, GPIO_PIN_RESET);

HAL_GPIO_WritePin(LED_RED_GPIO_Port, LED_RED_Pin, GPIO_PIN_SET);
HAL_Delay(1000);  // ❌ 시스템 블로킹
HAL_GPIO_WritePin(LED_RED_GPIO_Port, LED_RED_Pin, GPIO_PIN_RESET);</code></pre>
<p><strong>수정 후:</strong></p>
<pre><code class="language-c">// 부저 ON → 0.5초 후 OFF 예약
HAL_GPIO_WritePin(BUZZER_GPIO_Port, BUZZER_Pin, GPIO_PIN_SET);
buzzer_off_time = HAL_GetTick() + 500;

// LED ON → 1초 후 OFF 예약
HAL_GPIO_WritePin(LED_RED_GPIO_Port, LED_RED_Pin, GPIO_PIN_SET);
led_off_time = HAL_GetTick() + 1000;

// 메인 루프에서 타이밍 체크
if (HAL_GetTick() &gt;= buzzer_off_time) {
    HAL_GPIO_WritePin(BUZZER_GPIO_Port, BUZZER_Pin, GPIO_PIN_RESET);
}
if (HAL_GetTick() &gt;= led_off_time) {
    HAL_GPIO_WritePin(LED_RED_GPIO_Port, LED_RED_Pin, GPIO_PIN_RESET);
}</code></pre>
<p><strong>개선 효과:</strong></p>
<ul>
<li>시스템 블로킹 제거 → 부저 울리는 동안에도 다른 작업 가능</li>
<li>사용자 입력 응답성 향상</li>
<li>멀티태스킹 구현</li>
</ul>
<hr />
<h2 id="7-트러블-슈팅">7. 트러블 슈팅</h2>
<h3 id="이슈-1-adc-채널-설정-누락-✅">이슈 1: ADC 채널 설정 누락 ✅</h3>
<p><strong>문제:</strong></p>
<ul>
<li>조이스틱 X축, Y축이 정상 작동하지 않음</li>
<li>실제 사용하는 ADC 채널은 4개인데, 1개만 설정됨</li>
</ul>
<p><strong>해결:</strong></p>
<ul>
<li>CubeMX에서 ADC1 채널 4개 모두 활성화</li>
<li>DMA 설정으로 4개 채널 동시 읽기</li>
</ul>
<p><img alt="ADC 설정" src="https://velog.velcdn.com/images/mommers/post/c1f2f564-9faa-43c0-96c1-977e4e867ad3/image.png" /></p>
<hr />
<h3 id="이슈-2-조이스틱-반대-방향-인식-✅">이슈 2: 조이스틱 반대 방향 인식 ✅</h3>
<p><strong>문제:</strong></p>
<ul>
<li>조이스틱을 중립으로 돌릴 때 반대 방향으로 잠깐 인식됨</li>
<li>원인: 중립값(2048) 근처를 지나며 반대 방향으로 튀는 현상</li>
</ul>
<p><strong>해결 1: 히스테리시스 추가</strong></p>
<pre><code class="language-c">JoyDirection_t Get_Joy_Direction(void) {
    uint16_t vrx = adc_values[0];
    uint16_t vry = adc_values[2];

    #define CENTER 2048
    #define DEADZONE 800
    #define HYSTERESIS 200  // ⭐ 히스테리시스

    static JoyDirection_t last_direction = JOY_NONE;

    // Y축 상하 이동
    if (vry &lt; (CENTER - DEADZONE - HYSTERESIS)) {
        last_direction = JOY_UP;
        return JOY_UP;
    }
    if (vry &gt; (CENTER + DEADZONE + HYSTERESIS)) {
        last_direction = JOY_DOWN;
        return JOY_DOWN;
    }

    // 데드존 안에서는 이전 방향 유지
    if (vry &gt; (CENTER - DEADZONE) &amp;&amp; vry &lt; (CENTER + DEADZONE)) {
        if (vry &gt; (CENTER - 100) &amp;&amp; vry &lt; (CENTER + 100)) {
            last_direction = JOY_NONE;  // 완전 중립
        }
        return last_direction;
    }

    return last_direction;
}</code></pre>
<hr />
<h3 id="이슈-3-조이스틱-중립값-편차-✅">이슈 3: 조이스틱 중립값 편차 ✅</h3>
<p><strong>문제:</strong></p>
<ul>
<li>이론상 중립값: 2048</li>
<li>실제 측정값: 3100 근처</li>
<li>하드웨어 개체차로 인한 편차
<img alt="" src="https://velog.velcdn.com/images/mommers/post/a50aa9d4-c0c3-4953-bfe6-6d04815ba6fa/image.png" /></li>
</ul>
<p><strong>해결: 자동 캘리브레이션</strong></p>
<pre><code class="language-c">// 전역 변수
uint16_t joy_center_x = 2048;
uint16_t joy_center_y = 2048;

// 캘리브레이션 함수
void Joystick_Calibrate(void) {
    printf(&quot;\r\n[CALIBRATION] Don't touch joystick...\r\n&quot;);
    HAL_Delay(1000);

    // 10번 측정 후 평균
    uint32_t sum_x = 0;
    uint32_t sum_y = 0;

    for (int i = 0; i &lt; 10; i++) {
        sum_x += adc_values[0];
        sum_y += adc_values[2];
        HAL_Delay(50);
    }

    joy_center_x = sum_x / 10;
    joy_center_y = sum_y / 10;

    printf(&quot;[CALIBRATION] Center - X:%u Y:%u\r\n&quot;, joy_center_x, joy_center_y);
}

// 방향 읽기 (캘리브레이션 적용)
JoyDirection_t Get_Joy_Direction(void) {
    uint16_t vrx = adc_values[0];
    uint16_t vry = adc_values[2];

    #define DEADZONE 100  // 감도 향상

    if (vry &lt; (joy_center_y - DEADZONE)) return JOY_UP;
    if (vry &gt; (joy_center_y + DEADZONE)) return JOY_DOWN;
    if (vrx &lt; (joy_center_x - DEADZONE)) return JOY_LEFT;
    if (vrx &gt; (joy_center_x + DEADZONE)) return JOY_RIGHT;

    return JOY_NONE;
}</code></pre>
<p><strong>개선 효과:</strong></p>
<ul>
<li>하드웨어 개체차 자동 보정</li>
<li>시스템 시작 시 1회 실행</li>
<li>더 정확한 방향 인식</li>
</ul>
<hr />
<h3 id="이슈-4-pc14-핀-led-미동작-✅">이슈 4: PC14 핀 LED 미동작 ✅</h3>
<p><strong>문제:</strong></p>
<ul>
<li>PC13 (빨간 LED): 정상 동작 ✅</li>
<li>PC14 (녹색 LED): 점등 안 됨 ❌</li>
<li>Configuration 설정은 동일</li>
</ul>
<p><strong>원인 분석:</strong></p>
<ul>
<li>PC14-OSC32_IN: RTC 외부 크리스탈(LSE) 입력 핀</li>
<li>RTC 기능이 핀을 점유 중</li>
</ul>
<p><strong>해결:</strong></p>
<ol>
<li>RCC 메뉴 → LSE Disable</li>
<li>PC14 → PC3으로 변경</li>
<li>정상 동작 확인 ✅</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c151dbb2-fa1b-4f59-9016-5a7c071907fa/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b4208fd1-9a67-4ae9-8599-01e9d61bc9b7/image.png" /></p>
<hr />
<h3 id="이슈-5-rgb-led-green-색상-미출력-✅">이슈 5: RGB LED Green 색상 미출력 ✅</h3>
<p><strong>문제:</strong></p>
<ul>
<li>빨강(R), 파랑(B): 정상 ✅</li>
<li>녹색(G): 점등 안 됨 ❌</li>
<li>코드는 정상</li>
</ul>
<p><strong>원인:</strong></p>
<ul>
<li>하드웨어 배선 문제</li>
<li>기존: R, G, B 각각 220Ω 저항 + 공통 GND</li>
<li>문제: GND 연결 불량</li>
</ul>
<p><strong>해결:</strong></p>
<ul>
<li>R, G, B 직접 GND 연결</li>
<li>정상 동작 확인 ✅</li>
</ul>
<hr />
<h2 id="8-회고">8. 회고</h2>
<h3 id="🎯-잘된-점">🎯 잘된 점</h3>
<h4 id="1-체계적인-설계">1. 체계적인 설계</h4>
<ul>
<li>상태 머신 패턴으로 명확한 모드 관리</li>
<li>백그라운드 태스크 분리로 멀티태스킹 구현</li>
<li>HAL_Delay() 제거로 시스템 응답성 향상</li>
</ul>
<h4 id="2-팀워크">2. 팀워크</h4>
<ul>
<li>AI를 활용한 빠른 개발 속도</li>
<li>팀원 간의 합이 잘 맞아서 구현 성공</li>
<li>기능이 예상보다 잘 동작해서 만족스러움</li>
</ul>
<h4 id="3-문제-해결">3. 문제 해결</h4>
<ul>
<li>조이스틱 캘리브레이션으로 하드웨어 편차 해결</li>
<li>핀 충돌 문제를 직접 분석하고 해결</li>
<li>각종 이슈를 체계적으로 기록하고 해결</li>
</ul>
<hr />
<h3 id="😔-아쉬운-점">😔 아쉬운 점</h3>
<h4 id="1-발표-시간-관리-실패">1. 발표 시간 관리 실패</h4>
<blockquote>
<p>10분 제한에 기능을 하나하나 다 설명하려다 시간 부족</p>
</blockquote>
<p><strong>개선할 점:</strong></p>
<ul>
<li>청중 중심의 스토리텔링 필요</li>
<li>&quot;무엇을 구현했는가&quot;보다 &quot;왜 필요한가&quot;를 먼저 설명</li>
<li>핵심 기능 위주로 압축</li>
<li>발표 시뮬레이션 필요</li>
</ul>
<h4 id="2-추가-기능-미소개">2. 추가 기능 미소개</h4>
<ul>
<li>로그 기능, 5회 잠금 기능 등을 발표 직전에 추가</li>
<li>정작 발표에서는 언급하지 못함</li>
<li>발표 준비에 시간을 투자했어야 함</li>
</ul>
<p><strong>향후 계획:</strong></p>
<ul>
<li>주말에 모듈화 작업 진행</li>
<li>함수 하나하나 뜯어보며 완전히 이해</li>
<li>리팩토링 및 문서화</li>
</ul>
<hr />
<h3 id="📝-배운-점">📝 배운 점</h3>
<ol>
<li><p><strong>임베디드 설계 패턴</strong></p>
<ul>
<li>상태 머신, 백그라운드 태스크, 이벤트 기반 프로그래밍</li>
</ul>
</li>
<li><p><strong>하드웨어 디버깅</strong></p>
<ul>
<li>핀 충돌, ADC 채널 설정, 배선 문제 해결</li>
</ul>
</li>
<li><p><strong>프로젝트 관리</strong></p>
<ul>
<li>이슈 추적, 체계적인 문제 해결, 코드 버전 관리</li>
</ul>
</li>
<li><p><strong>발표 준비의 중요성</strong></p>
<ul>
<li>기술보다 전달력이 중요함을 깨달음</li>
</ul>
</li>
</ol>
<hr />
<h3 id="🚀-향후-개선-방향">🚀 향후 개선 방향</h3>
<ol>
<li><p><strong>코드 모듈화</strong></p>
<ul>
<li>ap.c 파일이 너무 김 (1000줄 이상)</li>
<li>기능별로 분리 필요</li>
</ul>
</li>
<li><p><strong>통신 기능 추가</strong></p>
<ul>
<li>보드 2개를 UART/I2C로 연결</li>
<li>상위 시스템 ↔ 하위 시스템 통신</li>
</ul>
</li>
<li><p><strong>데이터 시각화</strong></p>
<ul>
<li>UART로 PC 연동</li>
<li>수위 그래프 실시간 표시</li>
</ul>
</li>
</ol>
<hr />
<h2 id="9-참고-자료">9. 참고 자료</h2>
<h3 id="github-저장소">GitHub 저장소</h3>
<ul>
<li><a href="https://github.com/kyoung-mo/STM32-Dam-Control-System">STM32-Dam-Control-System</a></li>
</ul>
<h3 id="사용-기술">사용 기술</h3>
<ul>
<li><strong>MCU</strong>: STM32F411CEU6</li>
<li><strong>IDE</strong>: STM32CubeIDE</li>
<li><strong>HAL Library</strong>: STM32F4xx HAL Driver</li>
<li><strong>Sensors</strong>: DHT11, Water Level Sensor</li>
<li><strong>Display</strong>: I2C LCD 1602</li>
<li><strong>Actuators</strong>: SG90 Servo Motors</li>
</ul>
<hr />
<h2 id="마치며">마치며</h2>
<p>이번 프로젝트를 통해 임베디드 시스템 설계의 전체 과정을 경험할 수 있었습니다. </p>
<p>특히 <strong>상태 머신 패턴</strong>, <strong>백그라운드 태스크</strong>, <strong>이벤트 기반 프로그래밍</strong> 등의 설계 패턴을 직접 적용해보며 임베디드 시스템의 효율적인 구조에 대해 깊이 이해하게 되었습니다.</p>
<p>하드웨어 디버깅 과정에서는 데이터시트를 읽고, 핀 충돌을 해결하며 실전 경험을 쌓았고, 발표 준비의 중요성도 깨달았습니다.</p>
<p>앞으로는 코드를 모듈화하고, RTOS를 적용하며, 더 체계적인 시스템을 만들어보고 싶습니다.</p>
<hr />
<p><strong>프로젝트 기간</strong>: 2026.01.27 ~ 2026.01.28 (2일)<br /><strong>팀</strong>: 3인<br /><strong>담당</strong>: 하드웨어 설계, 소프트웨어 개발, 디버깅</p>
<hr />
<p>읽어주셔서 감사합니다! 🙏</p>
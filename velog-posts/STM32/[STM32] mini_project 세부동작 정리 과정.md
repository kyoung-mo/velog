<h1 id="stm32-스마트-금고-시스템--구현-전-확인-사항-정리">STM32 스마트 금고 시스템 – 구현 전 확인 사항 정리</h1>
<p>본 문서는 현재 코드 구조를 기준으로, <strong>하드웨어 핀 구성 / 기능 요구사항 / 상태 머신 설계</strong>를 구현 전에 명확히 하기 위한 체크리스트입니다.</p>
<hr />
<h2 id="1-4×4-키패드-keypad">1. 4×4 키패드 (Keypad)</h2>
<h3 id="q1-핀-연결-계획">Q1. 핀 연결 계획</h3>
<ul>
<li><strong>Row (출력)</strong>: PA8, PA9, PA10, PA11</li>
<li><strong>Column (입력, Pull-up)</strong>: PB3, PB4, PB5, PB6</li>
</ul>
<blockquote>
<p>Row는 하나씩 LOW로 내리며 Column을 스캔하는 방식 권장</p>
</blockquote>
<h3 id="q2-비밀번호-길이">Q2. 비밀번호 길이</h3>
<ul>
<li>기본값 제안: <strong>4자리</strong></li>
<li>확장 가능성: 6자리까지 고려 가능</li>
</ul>
<h3 id="q3-키패드-레이아웃">Q3. 키패드 레이아웃</h3>
<pre><code>[1][2][3][A]
[4][5][6][B]
[7][8][9][C]
[*][0][#][D]</code></pre><ul>
<li>숫자 입력: 0~9</li>
<li><code>#</code> : 확인 (ENTER)</li>
<li><code>*</code> : 취소 / 지우기 (CLEAR)</li>
<li><code>A~D</code> : 확장용 (미사용 또는 관리자 기능)</li>
</ul>
<hr />
<h2 id="2-서보모터-servo-motor">2. 서보모터 (Servo Motor)</h2>
<h3 id="q4-타이머-사용-계획">Q4. 타이머 사용 계획</h3>
<ul>
<li><p><strong>TIM2는 DHT11 타이밍에 사용 중 → 서보와 공유 비권장</strong></p>
</li>
<li><p>대안:</p>
<ul>
<li>TIM3 또는 TIM4 추가 사용 (PWM 전용)</li>
</ul>
</li>
</ul>
<h3 id="q5-서보-제어-핀">Q5. 서보 제어 핀</h3>
<ul>
<li><p>예시: <strong>PA6 – TIM3_CH1</strong></p>
</li>
<li><p>PWM 조건:</p>
<ul>
<li><p>주기: 20ms (50Hz)</p>
</li>
<li><p>듀티:</p>
<ul>
<li>1.0ms → 0° (LOCK)</li>
<li>1.5ms → 90° (UNLOCK)</li>
</ul>
</li>
</ul>
</li>
</ul>
<hr />
<h2 id="3-조이스틱-joystick">3. 조이스틱 (Joystick)</h2>
<h3 id="q6-핀-구성">Q6. 핀 구성</h3>
<ul>
<li><strong>VRx (X축)</strong>: PA0 – ADC1_CH0</li>
<li><strong>VRy (Y축)</strong>: PA4 – ADC1_CH4</li>
<li><strong>SW (버튼)</strong>: PB0 – GPIO Input (Pull-up)</li>
</ul>
<h3 id="q7-adc-구성">Q7. ADC 구성</h3>
<ul>
<li><p>현재: 내부 온도센서 1채널</p>
</li>
<li><p>확장 후:</p>
<ul>
<li>내부 온도 + VRx + VRy = <strong>총 3채널</strong></li>
<li><strong>ADC + DMA (Scan mode)</strong> 사용 권장</li>
</ul>
</li>
</ul>
<hr />
<h2 id="4-수위-센서-water-level-sensor">4. 수위 센서 (Water Level Sensor)</h2>
<h3 id="q8-센서-타입">Q8. 센서 타입</h3>
<ul>
<li><p><strong>아날로그 출력형 (권장)</strong></p>
<ul>
<li>ADC 채널 1개 추가 필요</li>
<li>예: PA1 – ADC1_CH1</li>
</ul>
</li>
<li><p>디지털 출력형일 경우:</p>
<ul>
<li>GPIO Input으로 임계 수위 감지만 가능</li>
</ul>
</li>
</ul>
<hr />
<h2 id="5-rgb-led">5. RGB LED</h2>
<h3 id="q9-제어-방식">Q9. 제어 방식</h3>
<ul>
<li><p>타입: <strong>공통 캐소드 (Common Cathode)</strong></p>
</li>
<li><p>핀:</p>
<ul>
<li>R: PC0</li>
<li>G: PC1</li>
<li>B: PC2</li>
</ul>
</li>
<li><p>제어 방식:</p>
<ul>
<li><p>1단계: ON/OFF</p>
</li>
<li><p>2단계(확장): PWM으로 밝기 조절</p>
<ul>
<li>TIM4_CH1~3 활용 가능</li>
</ul>
</li>
</ul>
</li>
</ul>
<hr />
<h2 id="6-부저-buzzer">6. 부저 (Buzzer)</h2>
<h3 id="q10-부저-사양">Q10. 부저 사양</h3>
<ul>
<li><p>핀: PB10</p>
</li>
<li><p>타입:</p>
<ul>
<li><strong>Active Buzzer (권장)</strong> → GPIO 토글</li>
<li>Passive Buzzer 사용 시 PWM 필요</li>
</ul>
</li>
</ul>
<hr />
<h2 id="7-상태-표시-led">7. 상태 표시 LED</h2>
<h3 id="q11-led-핀">Q11. LED 핀</h3>
<ul>
<li>빨강 LED (LOCK / ERROR): PC13</li>
<li>초록 LED (UNLOCK): PC14</li>
</ul>
<hr />
<h2 id="8-시스템-모드-설계-state-machine">8. 시스템 모드 설계 (State Machine)</h2>
<pre><code class="language-c">typedef enum {
    MODE_PASSWORD_INPUT,   // 비밀번호 입력 (초기)
    MODE_MENU_SELECT,      // 메뉴 선택
    MODE_CLOCK,            // 시계
    MODE_DHT11,            // 온습도
    MODE_WATER_LEVEL,      // 수위
    MODE_RGB_LED,          // RGB LED 제어
    MODE_PASSWORD_CHANGE   // 비밀번호 변경
} SystemMode_t;</code></pre>
<hr />
<h2 id="9-전체-동작-흐름">9. 전체 동작 흐름</h2>
<pre><code>[START]
  ↓
[MODE_PASSWORD_INPUT]
  ├─ 성공 → Servo UNLOCK + Green LED + &quot;UNLOCKED&quot;
  │          ↓ (2초)
  │       [MODE_MENU_SELECT]
  │          ├─ 조이스틱 ↑↓ : 메뉴 이동
  │          ├─ 클릭 : 모드 진입
  │          └─ BACK 선택 : 메뉴 복귀
  │
  └─ 실패 → Buzzer + Red LED + &quot;ACCESS DENIED&quot;
             ↓ (3초)
          MODE_PASSWORD_INPUT</code></pre><hr />
<h2 id="10-추가-설계-결정-사항">10. 추가 설계 결정 사항</h2>
<h3 id="q12-재잠금-방식">Q12. 재잠금 방식</h3>
<ul>
<li>선택지 1: <strong>자동 잠금</strong> (예: 30초 후)</li>
<li>선택지 2: 메뉴에서 <code>LOCK</code> 수동 선택</li>
<li>권장: <strong>자동 + 수동 병행</strong></li>
</ul>
<h3 id="q13-비밀번호-저장-방식">Q13. 비밀번호 저장 방식</h3>
<ul>
<li><p>STM32F411: EEPROM 없음</p>
</li>
<li><p>대안:</p>
<ul>
<li><strong>Internal Flash 저장 (Sector 단위)</strong></li>
<li>전원 OFF 후에도 유지 가능</li>
</ul>
</li>
</ul>
<h3 id="q14-lcd-사양">Q14. LCD 사양</h3>
<ul>
<li><p>16×2: 기본 정보 표시 가능</p>
</li>
<li><p>20×4 (권장):</p>
<ul>
<li>메뉴 스크롤 최소화</li>
<li>상태 메시지 가독성 향상</li>
</ul>
</li>
</ul>
<hr />
<h2 id="11-다음-단계-제안">11. 다음 단계 제안</h2>
<ol>
<li>핀맵 최종 확정 → CubeMX 반영</li>
<li>Driver 레벨 분리 (Keypad / Servo / Joystick / LCD)</li>
<li>Mode별 handler 함수 분리</li>
<li>Flash 비밀번호 저장 로직 구현</li>
</ol>
<hr />
<p>※ 본 문서는 구현 전 설계 합의를 위한 기준 문서로 사용됨</p>
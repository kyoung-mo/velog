<h1 id="stm32-댐-관리-시스템-dam-management-system">STM32 댐 관리 시스템 (Dam Management System)</h1>
<h2 id="1-시스템-컨셉">1. 시스템 컨셉</h2>
<p>중앙 댐의 수위를 실시간으로 모니터링하고, <strong>상류댐 / 하류댐 수문을 자동 또는 수동으로 제어</strong>하여
안정적인 수위 범위를 유지하는 임베디드 제어 시스템</p>
<hr />
<h2 id="2-하드웨어-구성">2. 하드웨어 구성</h2>
<h3 id="2-1-센서-sensors">2-1. 센서 (Sensors)</h3>
<ul>
<li><p><strong>수위 센서</strong></p>
<ul>
<li>기능: 중앙 댐 현재 수위 측정</li>
<li>핀: PA1 – ADC</li>
</ul>
</li>
<li><p><strong>DHT11</strong></p>
<ul>
<li>기능: 댐 주변 온습도 측정 (환경 모니터링)</li>
</ul>
</li>
<li><p><strong>내부 온도 센서</strong></p>
<ul>
<li>기능: MCU 시스템 온도 모니터링</li>
</ul>
</li>
</ul>
<hr />
<h3 id="2-2-액추에이터-actuators">2-2. 액추에이터 (Actuators)</h3>
<ul>
<li><p><strong>서보모터 2개 (TIM3 PWM)</strong></p>
<ul>
<li><p>서보 1 (상류댐): PA6 – TIM3_CH1</p>
<ul>
<li>0°: 닫힘</li>
<li>90°: 열림</li>
</ul>
</li>
<li><p>서보 2 (하류댐): PA7 – TIM3_CH2</p>
<ul>
<li>0°: 닫힘</li>
<li>90°: 열림</li>
</ul>
</li>
</ul>
</li>
<li><p><strong>RGB LED (상태 표시)</strong></p>
<ul>
<li><p>핀: PC0 (R), PC1 (G), PC2 (B)</p>
</li>
<li><p>색상 의미:</p>
<ul>
<li>청색: 정상 수위</li>
<li>적색: 수위 부족 (상류댐 개방 필요)</li>
<li>녹색: 수위 과다 (하류댐 개방 필요)</li>
</ul>
</li>
</ul>
</li>
<li><p><strong>부저 (Buzzer)</strong></p>
<ul>
<li>핀: PB10</li>
<li>기능: 수위 임계치 초과 시 경고음 출력</li>
</ul>
</li>
<li><p><strong>상태 LED</strong></p>
<ul>
<li>녹색 LED: PC14 (시스템 정상 / 인증 성공)</li>
<li>적색 LED: PC13 (경고 / 인증 실패)</li>
</ul>
</li>
</ul>
<hr />
<h3 id="2-3-입력-장치-input-devices">2-3. 입력 장치 (Input Devices)</h3>
<ul>
<li><p><strong>4×4 키패드</strong></p>
<ul>
<li>용도: 비밀번호 입력, 수치 설정</li>
</ul>
</li>
<li><p><strong>조이스틱</strong></p>
<ul>
<li>VRx: PA0 – ADC</li>
<li>VRy: PA4 – ADC</li>
<li>SW: PB0 – GPIO Input</li>
<li>용도: 메뉴 네비게이션, 수동 제어</li>
</ul>
</li>
</ul>
<hr />
<h2 id="3-시스템-모드-구조">3. 시스템 모드 구조</h2>
<pre><code class="language-c">typedef enum {
    MODE_PASSWORD_INPUT,    // 초기 인증
    MODE_MENU_SELECT,       // 메뉴 선택
    MODE_WATER_STATUS,      // 현재 수위 상태
    MODE_DAM_CONTROL,       // 댐 제어 (자동/수동)
    MODE_THRESHOLD_SET,     // 기준 수위 설정
    MODE_ENVIRONMENT,       // 환경 정보
    MODE_CLOCK,             // 시스템 시간
    MODE_PASSWORD_CHANGE    // 비밀번호 변경
} SystemMode_t;</code></pre>
<hr />
<h2 id="4-동작-시나리오">4. 동작 시나리오</h2>
<h3 id="phase-1-인증">Phase 1. 인증</h3>
<pre><code>[시스템 시작]
  ↓
[비밀번호 입력]
  ├─ 성공 → 녹색 LED + &quot;ACCESS GRANTED&quot; (2초)
  │          ↓
  │       [메뉴 선택 모드]
  │
  └─ 실패 → 적색 LED + 부저 + &quot;ACCESS DENIED&quot; (3초)
             ↓
          [비밀번호 재입력]</code></pre><hr />
<h3 id="phase-2-메뉴-네비게이션">Phase 2. 메뉴 네비게이션</h3>
<pre><code>[메뉴 선택] (조이스틱)
 1. 현재 수위 상태
 2. 댐 제어
 3. 기준 수위 설정
 4. 환경 정보
 5. 시스템 시간
 6. 비밀번호 변경
 7. 시스템 잠금</code></pre><hr />
<h2 id="5-모드별-상세-설계">5. 모드별 상세 설계</h2>
<h3 id="5-1-현재-수위-상태-mode_water_status">5-1. 현재 수위 상태 (MODE_WATER_STATUS)</h3>
<pre><code>===================
Current Level: 65%
Status: NORMAL
Upper Gate: CLOSED
Lower Gate: CLOSED
===================</code></pre><ul>
<li><p>RGB LED 동작:</p>
<ul>
<li>정상 (40~80%): 청색</li>
<li>부족 (&lt;40%): 적색 점멸</li>
<li>과다 (&gt;80%): 녹색 점멸</li>
</ul>
</li>
</ul>
<hr />
<h3 id="5-2-댐-제어-mode_dam_control">5-2. 댐 제어 (MODE_DAM_CONTROL)</h3>
<h4 id="자동-제어-로직-제안">자동 제어 로직 (제안)</h4>
<ul>
<li>수위 &lt; 40% → 상류댐 개방</li>
<li>수위 &gt; 80% → 하류댐 개방</li>
<li>40~80% → 모든 수문 닫힘</li>
</ul>
<p><strong>히스테리시스 적용</strong></p>
<ul>
<li>상류댐: 35% 개방 → 45% 닫힘</li>
<li>하류댐: 85% 개방 → 75% 닫힘</li>
</ul>
<h4 id="수동-제어-방식-선택-필요">수동 제어 방식 (선택 필요)</h4>
<ul>
<li><p>옵션 A: 조이스틱</p>
<ul>
<li>UP: 상류댐 토글</li>
<li>DOWN: 하류댐 토글</li>
</ul>
</li>
<li><p>옵션 B: 키패드</p>
<ul>
<li>1: 상류댐 개방</li>
<li>2: 상류댐 닫힘</li>
<li>3: 하류댐 개방</li>
<li>4: 하류댐 닫힘</li>
</ul>
</li>
</ul>
<pre><code>===================
Mode: AUTO / MANUAL
Upper: OPEN / CLOSE
Lower: OPEN / CLOSE
Level: 65%
===================</code></pre><hr />
<h3 id="5-3-기준-수위-설정-mode_threshold_set">5-3. 기준 수위 설정 (MODE_THRESHOLD_SET)</h3>
<h4 id="설정-방식-선택-필요">설정 방식 (선택 필요)</h4>
<ul>
<li>방법 1: 키패드 직접 입력</li>
<li>방법 2: 조이스틱 증감 (5% 단위)</li>
</ul>
<pre><code>===================
Threshold Setting
Lower Limit: 40%
Upper Limit: 80%
Press # to Save
===================</code></pre><hr />
<h3 id="5-4-환경-정보-mode_environment">5-4. 환경 정보 (MODE_ENVIRONMENT)</h3>
<pre><code>===================
Temperature: 24.5°C
Humidity: 55%
System Temp: 42°C
Time: 14:35:22
===================</code></pre><hr />
<h3 id="5-5-시스템-시간-mode_clock">5-5. 시스템 시간 (MODE_CLOCK)</h3>
<ul>
<li>옵션 A: 시간 표시만 (RTC, 컴파일 시간 초기값)</li>
<li>옵션 B: 키패드로 시간 설정 가능</li>
</ul>
<hr />
<h3 id="5-6-비밀번호-변경-mode_password_change">5-6. 비밀번호 변경 (MODE_PASSWORD_CHANGE)</h3>
<pre><code>===================
Old PW: ____
New PW: ____
Confirm: ____
===================</code></pre><hr />
<h2 id="6-추가-확인-사항">6. 추가 확인 사항</h2>
<h3 id="q5-비밀번호-길이">Q5. 비밀번호 길이</h3>
<ul>
<li>4자리 고정</li>
<li>또는 4~6자리 가변</li>
</ul>
<h3 id="q6-긴급-상황-처리">Q6. 긴급 상황 처리</h3>
<ul>
<li>옵션 A: 경고만 (부저 + LED)</li>
<li>옵션 B: 강제 자동모드 전환 + 수문 개방</li>
</ul>
<h3 id="q7-flash-저장-데이터">Q7. Flash 저장 데이터</h3>
<ul>
<li>비밀번호</li>
<li>수위 기준값 (상/하한)</li>
<li>마지막 제어 모드 (AUTO/MANUAL)</li>
</ul>
<h3 id="q8-lcd-사양">Q8. LCD 사양</h3>
<ul>
<li>16×2: 제한적</li>
<li><strong>20×4: 권장</strong></li>
</ul>
<hr />
<h2 id="7-다음-단계">7. 다음 단계</h2>
<ol>
<li>최종 설계 결정 사항 확정</li>
<li>핀맵 최종 확정</li>
<li>CubeMX 설정 가이드 작성</li>
<li>모듈별 드라이버 구조 설계</li>
<li>main.c 전체 로직 구현</li>
</ol>
<hr />
<p>※ 본 문서는 STM32 기반 댐 관리 시스템 프로젝트의 설계 기준 문서로 사용됨</p>
<p>인사이드 임베디드님의 유튜브를 토대로 정리한 내용입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7860f46c-9977-4c02-8381-92d022a2b5e8/image.png" /></p>
<hr />
<h3 id="자동차의-진화">자동차의 진화</h3>
<p>내연기관 자동차에서 소프트웨어 중심의 자동차(SDV; Software Defined Vegicle)로 진화하고 있다.</p>
<p>단순 인포테인먼트 발달만이 아닌, 차량의 주행, 제어 그리고 안전을 책임지는 임베디드 소프트웨어의 복잡도 증가가 자리잡고 있다.</p>
<hr />
<h3 id="왜-자동차-업계는-규칙이-많을까">왜 자동차 업계는 규칙이 많을까?</h3>
<ul>
<li>MISRA</li>
<li>ISO26262</li>
<li>ASPICE</li>
<li>AUTOSAR</li>
<li>MBD (모델 기반 개발)</li>
</ul>
<p>결론적으로, 모두 따로 노는 지식이 아닌 
<strong>절대적 안전(Absolute Safty)</strong>와 <strong>재현 가능한 품질(Reproducible Quality)</strong>을 위해서 한 덩어리로 묶여있다.</p>
<hr />
<h3 id="2009년-도요타-급발진unintended-acceleration-논란">2009년 도요타 급발진(Unintended Acceleration) 논란</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3f0f8a8b-8398-4016-9c61-90d41fe0af0d/image.png" /></p>
<p>소프트웨어 품질이 곧 안전이라는 산업적 각성의 계기.
코드의 복잡도, 예측 불가능성이 리스크로 직결될 수 있다는 가성성이 제기됌.</p>
<p>초기에는 매트 발걸림 등의 하드웨어 요인이 원인으로 지속되었지만, '혹시 소프트웨어 결함 가능성이 있는 것 아니냐'라는 의혹이 제기되며 업계 전반이 긴장하게 되었다.</p>
<hr />
<h3 id="misra-c--코드의-규율">MISRA C : 코드의 규율</h3>
<p>C언어의 자유도가 안전에는 리스크를 미칠 수 있다.</p>
<p>대표적인 제한 항목)</p>
<ul>
<li>동적 메모리 할당(malloc, free) 금지.</li>
<li>재귀 호출(Recursion) 금지</li>
</ul>
<blockquote>
<p>메모리 누수, 단편화 리스크 차단하기 위해
목표는 예측 가능성(Predictability) 확보</p>
</blockquote>
<p>Polyspace라는 소프트웨어 테스트 및 코드 분석을 위한 체크 도구가 있어, 코드를 관리하며 모니터링 할 수 있다.</p>
<p>하지만 코드만 MISRA-C를 만족한다고 해서 안전하게 동작한다는 보장이 없다.</p>
<p>설계 자체가 잘못되었다면, 잘못된 코드를 더욱 확실하게 실행해서 오히려 더 확실하게 사고를 내는 상황이 생길 수 있다.</p>
<p>-&gt;</p>
<hr />
<h3 id="iso26262--시스템의-안전">ISO26262 : 시스템의 안전</h3>
<blockquote>
<p>기능 안전(Functional Safety) 프레임워크
<strong>시스템 설계 단계부터 안전을 구조적으로 고려</strong></p>
</blockquote>
<p>ISO26262는 전기 및 전자(E/E) 시스템의 일반 기능 안전 표준인 IEC61508에서 파생되었다. (하지만 자동차 특성상 고려할게 많기 때문에 따로 제작? 확인 필요)</p>
<ul>
<li>시스템 설계 단계부터 안전을 구조적으로 고려한다는 말이 무슨 의미인가?</li>
</ul>
<blockquote>
<p>제어기가 고장 나더라도 차가 갑자기 위험한 동작을 하지 않도록, <strong>시스템이 허용 가능한 위험수준으로 관리되도록</strong> 설계, 검증하라는 자동차 기능 안전 국제 표준</p>
</blockquote>
<p>사고방식 3가지</p>
<ol>
<li><p>심각도(Severity)
고장이 나면 어떠한 피해가 생기는지?</p>
</li>
<li><p>노출도(Exposure)
그 위험한 상황에 얼마나 자주 노출되는가?</p>
</li>
<li><p>제어 가능성(Controllability)
실제 그 위험 상황이 발생했을 때 운전자가 회피, 또는 제어를 해서 사고를 피할 수 있는지?</p>
</li>
</ol>
<p>이러한 3가지 조합으로 부터 QM ~ ASIL A~D 등급까지 평가를 하게 되고, 조향 또는 제동처럼 안전과 직접 연결된 기능일수록 높은 등급이 요구되는 경우가 많다.</p>
<p>등급이 올라갈 수록 설계, 제약, 분석, 검증 그리고 테스트, 문서 요구사항이 굉장히 빠르게 증가한다.</p>
<p>또한 중요한것으로 <strong>안전 상태</strong>가 있다.</p>
<p>제어기가 그냥 꺼진다가 항상 안전한 것이 아니다. 오히려 기능을 안전하게 축소하고 운전자 또는 상위 시스템이 통제 가능한 상태로 유도하는 설계가 필요하다.</p>
<hr />
<h3 id="aspice--프로세스의-품질">ASPICE : 프로세스의 품질</h3>
<blockquote>
<p>재현 가능한 결과물을 만드는 프로세스 역량 모델</p>
</blockquote>
<p>맛있는 요리가 나왔다! 라는 결과물만으로는 부족하다.</p>
<p>다음번에도, 다른 사람이 해도 똑같이 맛있는 요리를 만들 수 있는 체계가 갖춰져 있는가? 를 묻는 것</p>
<p>실제로 유럽의 OEM 업체들은 부품 공급사 선정을 할 때  ASPICE 레벨 2 또는 3 달성을 필수 조건으로 요구하는 경우가 많다.</p>
<ul>
<li>Level 0 : 자취방 요리(감으로 하는 요리)<ul>
<li>배고플 때마다 맛이 다르고, 실패해서 태우기도 함</li>
<li>사실상 프로세스가 존재하지 않음</li>
</ul>
</li>
<li>Level 1 : 동네 맛집(레시피 없는 성공)<ul>
<li>맛있는 요리를 만들어서 손님에게 내놓는데에는 성공</li>
<li>주방장이 바뀌거나, 컨디션이 달라지면 맛이 변함</li>
<li>목표 달성은 했으나 체계가 부족한 상황</li>
</ul>
</li>
<li>Level 2 : 체계적인 레스토랑(프로젝트 단위 관리)<ul>
<li>레시피 = 문서화된 계획이 있다.</li>
<li>재료 재고 관리 = 형상 관리</li>
<li>지배인(PM)이 요리 시간을 체크</li>
<li>누가 요리를 하던 일정한 퀄리티를 낼 수 있다.</li>
</ul>
</li>
<li>Level 3 : 글로벌 프랜차이즈(조직 표준화)<ul>
<li>조직 전체의 표준이 되는 프로세스가 정립</li>
<li>지속적인 개선이 이루어짐</li>
<li>고객 요구사항, 시스템 설계, 소프트웨어 설계, 코드 구현, 테스트 결과가 끊임없이 연결되어야 함</li>
<li>고객이 요구한 모든 사항이 코드에 구현이 되었는가?를 문서와 산출물로 보증할 수 있어야 함</li>
</ul>
</li>
</ul>
<hr />
<h3 id="autosar--아키텍처의-표준화">AUTOSAR : 아키텍처의 표준화</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5e58f974-3b5d-411d-b7a5-da1cdf785106/image.png" /></p>
<p>표준에는 협력하되, 구현에서는 경쟁한다는 슬로건아래 탄생하였다.</p>
<p>부품사(Bosch, Continental, 현대모비스) 각각이 독자적인 소프트웨어 구조를 사용하였는데, 
그러다보니 OEM에서 부품사 변경을 하려면 소프트웨어까지 처음부터 다시 개발해야하는 문제가 있었고, 이는 곧 막대한 비용, 시간 낭비로 이어졌다.</p>
<p>AUTOSAR는 총 3계층으로 나누어지는데,</p>
<ul>
<li>ASW(Application Software) : 두뇌 / 로직</li>
<li>RTE(Runtime Environment) : 통역사 / 미들웨어</li>
<li>BSW(Basic Software) : 기초 공사 / 하드웨어 제어</li>
</ul>
<p>이를 통해 하드웨어 의존성을 줄이고, 재사용성과 교체 용이성을 높였다.</p>
<hr />
<h3 id="mbd--모델-기반-개발model-based-design">MBD : 모델 기반 개발(Model-Based Design)</h3>
<p>원래는 사람이 직접 C코드로 타이핑을 했으나, 오타나 논리적인 오류가 발생하기 쉬웠고, 변경 사항을 반영할 때도 누락이나 불일치가 생기기 쉽다는 문제.</p>
<p>따라서 MATLAB/Simulink와 같은 도구를 사용해서 시뮬레이션을 통한 사전 검증, 자동 코드 생성이 가능한 모델 기반 개발로 넘어오게 되었다.</p>
<hr />
<p><strong>V-사이클 : 개발은 어떤 순서로 굴러가나요?</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d434f0b7-9acf-4bad-b7ff-9192cea111a2/image.png" /></p>
<ul>
<li>왼쪽은 설계 과정 : SWE1, SWE2, SWE3<ul>
<li>고객의 요구 사항</li>
<li>시스템 설계</li>
<li>소프트웨어 아키텍처</li>
<li>유닛 설계 등</li>
</ul>
</li>
<li>오른쪽은 검증 과정 : SWE4, SWE5, SWE6<ul>
<li>유닛 테스트</li>
<li>통합 테스트</li>
<li>시스템 테스트
다시 위로 올라오면서 설계한게 정말 맞는지를 단계별로 확인</li>
</ul>
</li>
</ul>
<blockquote>
<p>왼쪽의 산출물 하나하나가 오른쪽의 테스트 항목과 일대일로 연결돼야 한다.</p>
</blockquote>
<blockquote>
<p><strong>추적성(Traceability)</strong> : 모든 개발 산출물의 논리적 연결 증명</p>
</blockquote>
<ul>
<li>고객 요구사항 - 시스템설계 - 소프트웨어 설계 - 코드 구현 - 테스트 결과</li>
</ul>
<hr />
<p><strong>MBD 워크플로우 : V-Model</strong></p>
<ol>
<li><p>모델링(Modeling)
Simulink의 블록을 연결해서 제어 로직을 시각적으로 구현할 수 있다.</p>
</li>
<li><p>코드 자동 생성</p>
</li>
<li><p>모델 검증(MIL : Model-in-the-Loop)
코드를 짜기 전에 PC 상에서 모델을 실행을 해서 논리가 맞는지를 검증한다.</p>
</li>
<li><p>코드 검증(SIL : Software-in-the-Loop)
툴 체인 설정과 코딩 규칙, 모델링 규칙에 맞게 자동으로 코드를 생성한다.</p>
</li>
<li><p>하드웨어 환경 검증(HIL : Hardware-in-the-Loop)
유사한 환경에서 최종 테스트를 할 수 있게된다.</p>
</li>
</ol>
<hr />
<h2 id="정리">정리</h2>
<p>ISO 26262라는 안전 목표를 위해서 
ASPICE라는 절차를 밟으며,
AUTOSAR라는 표준 플랫폼 위에서,
MBD라는 도구를 활용해서 개발을 하고,
그 과정에서 MISRA C 규칙을 기반으로 코드의 예측 가능성과 품질을 관리한다!</p>
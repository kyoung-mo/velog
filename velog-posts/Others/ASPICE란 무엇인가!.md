<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/46aa54af-b82b-4101-a53a-e2777b6fe39a/image.png" /></p>
<hr />
<h3 id="0-aspice프로세스-참조-모델란">0. ASPICE(프로세스 참조 모델)란?</h3>
<p>ASPICE(Automotive Software Process Improvement and Capability dEtermination - 차량용 소프트웨어 프로세스 심사 표준) : 소프트웨어 개발 프로세스를 평가하기 위한 업계 표준 지침이다.</p>
<p>목적 : 자동차 소프트웨어 개발의 프로세스를 체계적으로 평가하고 개선하여 품질 및 성능을 향상하는 것</p>
<p>자동차 SPICE 표준을 바탕으로 자동차 개발 기업들은 소프트웨어 개발 프로세스의 성숙도를 평가하고, 소프트웨어 정의 차량(SDV)읜 강점과 약점을 파악하여 필요에 따라 개선 조치를 직시에 갖출 수 있다.</p>
<hr />
<h3 id="1-v-모델과-aspice">1. V-모델과 ASPICE</h3>
<p>자동차 소프트웨어를 개발할 때, 가장 대표적으로 쓰이는 절차 모델이 바로 V-모델이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/20d5320d-3bd2-4351-97fb-90a3d16fca88/image.png" /></p>
<p>왼쪽(요구사항, 설계) &lt;-&gt; 오른쪽(테스트,  검증)을 시각적으로 연결해, 어떤 요구사항이 어떤 테스트로 확인되는지 추적하기 쉽다는 특징을 가진다.</p>
<p>ASPICE(Automotive SPICE)도 이 V-모델을 바탕으로, 각 단계마다 필요한 프로세스와 산출물을 정리해둔 표준이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6be6df66-fe48-45d7-b9a6-28ebd46dd634/image.png" /></p>
<blockquote>
<p>왼쪽 : 무엇을 만들건지 구체화(요구사항 -&gt; 설계)
오른쪽 : 잘 만들었는지 검증(테스트)</p>
</blockquote>
<hr />
<h3 id="2-aspice-주-프로세스-그룹">2. ASPICE 주 프로세스 그룹</h3>
<h3 id="2-1-sys-프로세스-그룹시스템">2-1) SYS 프로세스 그룹(시스템)</h3>
<p>시스템 요구사항 정의, 시스템 아키텍처 설계 등에 해당하는 프로세스이다. &quot;차량 전체적으로 어떤 기능이 필요하고, 하드웨어, 소프트웨어는 어떻게 결합해야 하는지&quot; 큰 그림을 그린다.
V-모델 왼쪽 위(상위 요구사항)부터 오른쪽 위(시스템 테스트)까지를 커버한다.</p>
<h3 id="2-2-swe-프로세스-그룹소프트웨어">2-2) SWE 프로세스 그룹(소프트웨어)</h3>
<p>SWE.1 ~ SWE.6으로 나뉘고, 실제 코딩, 단위 테스트, 통합 테스트 등 소프트웨어 개발 전반을 다룬다.
V-모델 중간 ~ 하단 부분에서 이 요구사항이 코드로 어떻게 구현되고, 해당 코드가 어떻게 테스트되는지가 주 내용인 그룹이다.</p>
<h3 id="2-3-man-프로세스-그룹프로젝트-관리">2-3) MAN 프로세스 그룹(프로젝트 관리)</h3>
<p>프로젝트 일정, 비용, 인력, 리스크 등을 관리하고, 전체 프로세스를 계획하고 통제하는 역할을 한다. V-모델 어느 단계든 다음 리뷰는 언제 할지? , 예산 초과되면 어떻게 대처할지? 같은 프로젝트 매니지먼트 업무가 필요하기 때문이다.</p>
<h3 id="2-4-sup-프로세스-그룹support-지원">2-4) SUP 프로세스 그룹(Support, 지원)</h3>
<p>SUP 영역은 V-모델 좌우(개발 단계)와 직접적으로 1:1 매칭되기보다는, 개발 전체를 가로지르는 지원 기능을 담당한다. 예를 들어, 형상 관리(SUP.8 : Configuration Management), 문제 해결(SUP.9 : Process for Problem Resolution), 변경 관리(SUP.10 : Change Request Management), 문서 관리, 품질 보증(Quality Assurance) 등이 여기에 포함된다.
개발자들끼리 코드를 짜고 테스트 하는것도 중요하지만, 실제 제품 수준으로 완성하려면 형상관리 및 이슈 추적 및 품질 점검 등이 꼭 함께 이루어져야 하기 때문에 이 그룹이 필요하다.</p>
<blockquote>
<ul>
<li>형상 관리 : 버전이 언제, 어떻게 바뀌었는지에 대해 추적 가능하게 만들어주는 것</li>
<li>변경 관리 : 시스템 요구사항이나 설계 등에 변경 요청이 들어왔을때, 해당 요청을 접수 및 평가, 프로젝트 전체 일정과 리소스에 영향을 조정하는 절차이다.</li>
<li>품질 보증 : 우리가 정의한 프로세스를 제대로 지키고 있나? 를 독립적으로 검증한다. 부실한 문서나 테스트 누락을 미리 잡아내 품질을 안정적으로 유지시켜준다. </li>
</ul>
</blockquote>
<hr />
<h3 id="3-vda-scope란">3. VDA SCOPE란?</h3>
<p>독일 자동차 협회 산하라는 독일 자동차산업협회 내 품질관리센터가 중심이 되어 자동차 산업 관점에서 이 프로세스들은 꼭 평가해야한다! 라고 정해주었다. 즉, 자동차 산업에서 특히 중요하게 여기는 항목만 집중적으로 관리하고 싶었기 때문이다.</p>
<p>주로 시스템(SYS), 소프트웨어(SWE), 지원(SUP), 관리(MAN) 프로세스 그룹의 16개 프로세스가 핵심으로 꼽히며, 이를 &quot;VDA Scope&quot;라고 부른다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/03fa984e-e51a-4c7e-9629-84c92fa72a28/image.png" /></p>
<hr />
<h3 id="v-모델--aspice-프로세스-전체-흐름-예시">V-모델 + ASPICE 프로세스: 전체 흐름 예시</h3>
<p>SYS와 SWE 그룹의 과정이 진행되는 과정에서 SUP 그룹과 MAN 그룹이 작동한다는 것을 알 수 있다.</p>
<ul>
<li><p>SYS.2(시스템 요구사항) -&gt; SYS.3(시스템 설계)</p>
<ul>
<li>차 전체의 큰 기능 정의와 아키텍처 잡기.</li>
<li>SUP 영역 중 형상관리, 문서관리 등으로 요구사항 문서를 체계적으로 버전 관리.</li>
</ul>
</li>
<li><p>SWE.1(소프트웨어 요구사항) -&gt; SWE.2(SW 아키텍처) -&gt; SWE.3(상세설계, 구현)</p>
<ul>
<li>실제 소프트웨어 기능 구현</li>
<li>SUP 영역에서 품질 보증(QA) 담당이 설계 리뷰 제대로 했는지? 등을 체크</li>
<li>동시에 MAN 팀이 프로젝트 일정, 예산, 리스크 모니터링</li>
</ul>
</li>
<li><p>SWE.5(통합 테스트)~SWE.6(검증) + SYS.4(시스템 검증)</p>
<ul>
<li>기능을 통합, 검증하고, 최종적으로 시스템 레벨까지 테스트 진행</li>
<li>문제 발견 시, SUP 문제 해결 프로세스가 작동해 어디서 발생했는지 추적, 어떻게 해결할지를 체계적으로 기록</li>
</ul>
</li>
</ul>
<hr />
<h3 id="왜-이렇게-프로세스를-나누는-걸까">왜 이렇게 프로세스를 나누는 걸까?</h3>
<p>** 1. 역할, 책임(R&amp;R) 명확화 **
시스템 레벨 요구사항은 누가?
소프트웨어 레벨 설계는 누가?
프로젝트 관리 문서는 누가?
각자 맡은 프로세스를 명확히 구분함으로써 협업이 쉬워진다.</p>
<p>** 2. 추적성(Traceability) 확보 **
V-모델 형태로, 이 요구사항은 어느 설계와 연결돼 있고, 이 설계는 어느 테스트 케이스로 검증 되는지까지 한 눈에 파악이 가능하다.</p>
<p>** 3. 품질 보장 **
왼쪽(요구사항, 설계) &lt;-&gt; 오른쪽(테스트, 검증) 연결 덕분에, 처음에 정의한 기능이 실제 잘 구현됐는가를 빠짐없이 체크 가능하다.</p>
<hr />
<blockquote>
<p><strong>Reference</strong></p>
<ol>
<li><a href="https://geonwoo.com/documents/?bmode=view&amp;idx=157150964">https://geonwoo.com/documents/?bmode=view&amp;idx=157150964</a></li>
<li><a href="https://ltsgroup.tech/kr/blog/what-is-automotive-spice/">https://ltsgroup.tech/kr/blog/what-is-automotive-spice/</a></li>
</ol>
</blockquote>
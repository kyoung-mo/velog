<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/32ea1489-c22d-4437-82d1-5b4c112d2fc9/image.png" /></p>
<hr />
<h3 id="c-라이브러리c-libraries">C 라이브러리(C Libraries)</h3>
<p>리눅스 어플리케이션이 커널과 대화하기 위한 표준 통역사 (<code>glibc</code>)</p>
<hr />
<h3 id="1-정의-및-역할">1. 정의 및 역할</h3>
<ul>
<li><strong>정체:</strong> 리눅스 시스템의 <strong>표준 C 라이브러리 (GNU libc = <code>glibc</code>)</strong>.</li>
<li><strong>위치:</strong> 어플리케이션(User)과 커널(Kernel) 사이의 <strong>중간 계층</strong>.</li>
<li><strong>목표:</strong> 커널의 복잡한 내부 동작을 <strong>고수준 API</strong>로 추상화하여 개발 편의성 제공.</li>
</ul>
<hr />
<h3 id="2-glibc의-3대-핵심-기능">2. <code>glibc</code>의 3대 핵심 기능</h3>
<h3 id="①-system-call-wrapper-래퍼">① System Call Wrapper (래퍼)</h3>
<ul>
<li><strong>기능:</strong> 복잡한 어셈블리 명령(<code>int 0x80</code>, <code>syscall</code>)이나 레지스터 설정을 대신 처리.</li>
<li><strong>효과:</strong> 개발자는 하드웨어 아키텍처를 몰라도 <code>open()</code>, <code>write()</code> 같은 표준 함수만 호출하면 됨.</li>
</ul>
<h3 id="②-표준-c-라이브러리-구현-iso-c">② 표준 C 라이브러리 구현 (ISO C)</h3>
<ul>
<li><strong>기능:</strong> 문자열 처리(<code>strcpy</code>), 입출력(<code>printf</code>), 메모리 할당(<code>malloc</code>) 등.</li>
<li><strong>효과:</strong> C언어 표준 규격을 준수하여 코드의 이식성 보장.</li>
</ul>
<h3 id="③-인프라-지원-infrastructure">③ 인프라 지원 (Infrastructure)</h3>
<ul>
<li><strong>스레딩:</strong> POSIX 스레드(<code>pthread</code>) 지원.</li>
<li><strong>런타임:</strong> 프로그램 시작(<code>_start</code>)과 종료, 동적 링킹 등 기본 실행 환경 제공.</li>
<li>전형적인 시스템 프로그래밍 모델</li>
</ul>
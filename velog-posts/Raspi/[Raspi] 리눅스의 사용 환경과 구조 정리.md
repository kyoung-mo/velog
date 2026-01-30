<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/64977141-413a-4aba-a77a-399c8148c394/image.png" /></p>
<h3 id="1-리눅스의-탄생과-역사">1. 리눅스의 탄생과 역사</h3>
<ul>
<li><strong>리눅스(Linux)의 시작:</strong><ul>
<li>1991년 9월 17일, 핀란드 헬싱키 대학의 <strong>리누스 토발즈(Linus Torvalds)</strong>가 버전 0.1 공개함.</li>
<li>초기에는 앤드루 타넨바움 교수의 교육용 OS인 <strong>미닉스(MINIX)</strong>를 기반으로 개발됨.</li>
<li>인터넷 공개 후 전 세계 해커들의 자발적 참여로 급격히 발전함.</li>
<li>1994년 커널 1.0 발표, 1996년 커널 2.0 발표하며 멀티 프로세서 지원 시작함.</li>
</ul>
</li>
<li><strong>성장과 확장:</strong><ul>
<li>IBM, 오라클 등 거대 IT 기업의 지원으로 서버 시장 진입함.</li>
<li><strong>임베디드 리눅스:</strong> 1998년 이후 µClinux 프로젝트 등을 통해 MMU가 없는 소형 기기 지원 시작함.</li>
<li><strong>안드로이드(Android):</strong> 리눅스 커널 기반의 모바일 OS로 스마트폰 시장 석권함.</li>
</ul>
</li>
</ul>
<h3 id="2-리눅스의-주요-특징">2. 리눅스의 주요 특징</h3>
<ul>
<li><strong>다중 사용자(Multi-user) &amp; 다중 작업(Multi-tasking):</strong><ul>
<li>여러 사용자가 동시에 시스템에 접속 가능함.</li>
<li>여러 개의 프로그램(프로세스)을 동시에 실행 가능함.</li>
</ul>
</li>
<li><strong>오픈 소스(Open Source):</strong><ul>
<li>소스 코드가 완전 공개되어 누구나 수정, 배포 가능함(GPL 라이선스).</li>
<li>특정 벤더에 종속되지 않고 다양한 배포판 존재함.</li>
</ul>
</li>
<li><strong>이식성(Portability):</strong><ul>
<li>C언어로 작성되어 다양한 하드웨어 아키텍처(x86, ARM, MIPS 등)에 쉽게 이식됨.</li>
</ul>
</li>
<li><strong>표준 준수:</strong><ul>
<li><strong>POSIX(Portable Operating System Interface):</strong> 유닉스 시스템 간의 호환성을 위한 표준 인터페이스 지원함.</li>
<li><strong>단일 유닉스 규격(SUS):</strong> 다른 유닉스 시스템의 애플리케이션을 쉽게 포팅 가능함.</li>
</ul>
</li>
<li><strong>계층적 파일 시스템:</strong><ul>
<li>트리(Tree) 구조의 디렉터리 시스템을 가짐.</li>
<li>모든 하드웨어 장치(마우스, 키보드, 디스크 등)를 <strong>파일</strong>로 취급하여 관리함.</li>
</ul>
</li>
</ul>
<h3 id="3-리눅스의-구조-architecture">3. 리눅스의 구조 (Architecture)</h3>
<p>리눅스 시스템은 크게 커널, 셸, 유틸리티, 응용 프로그램으로 구성됨.</p>
<ul>
<li><strong>커널(Kernel):</strong><ul>
<li>운영체제의 핵심 심장부. 메모리에 상주함.</li>
<li><strong>역할:</strong> 하드웨어(CPU, 메모리, 디스크 등) 관리, 프로세스 스케줄링, 메모리 관리, 파일 시스템 관리 등.</li>
<li>하드웨어 제어를 위해 <strong>디바이스 드라이버</strong>를 포함함.</li>
<li>사용자 프로그램과 하드웨어 사이의 인터페이스인 <strong>시스템 호출(System Call)</strong> 제공함.</li>
</ul>
</li>
<li><strong>셸(Shell):</strong><ul>
<li>사용자와 커널 사이의 <strong>명령어 해석기(Interpreter)</strong>.</li>
<li>사용자가 입력한 명령어를 해석하여 커널에 전달하고 결과를 사용자에게 보여줌.</li>
<li>종류: bash(표준), sh, csh, ksh, zsh 등.</li>
</ul>
</li>
<li><strong>유틸리티(Utility):</strong><ul>
<li>사용자가 운영체제의 기능을 활용할 수 있도록 도와주는 각종 프로그램.</li>
<li>파일 조작(cp, mv), 에디터(vi), 컴파일러(gcc) 등이 포함됨.</li>
</ul>
</li>
<li><strong>응용 프로그램(Application):</strong><ul>
<li>웹 브라우저, 데이터베이스, 게임 등 사용자 업무를 수행하는 소프트웨어.</li>
<li><strong>X 윈도 시스템:</strong> 리눅스의 GUI 환경을 제공하는 윈도우 시스템.</li>
</ul>
</li>
</ul>
<p>2026-01-19 STM32 복습)</p>
<h2 id="-stm32cubemx-stm32cubeide-정리"># STM32CubeMX, STM32CubeIDE 정리</h2>
<hr />
<h3 id="1-stm32cubemx">1. <a href="https://www.st.com/en/development-tools/stm32cubemx.html">STM32CubeMX</a></h3>
<ul>
<li>STM32 관련 MCU, Board를 선택하여 선택한 칩과 관련된 데이터 시트에 맞게 핀 / 클럭 / 주변장치 설정을 자동으로 도와준다.</li>
<li>프로젝트 생성 시 초기화 코드를 자동으로 생성해준다.</li>
<li>프로젝트 생성 시 STM32CubeIDE를 tool로 선택하여 STM32CubeIDE에서 코드 수정이 가능하다</li>
</ul>
<h3 id="mcu-mpu-선택">[MCU, MPU 선택]</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/556b5864-0172-425d-a7a7-7955597eebff/image.png" /></p>
<h3 id="board-selector-선택">[Board Selector 선택]</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d71a881c-327f-485e-b91e-56f68e966b9d/image.png" /></p>
<h3 id="메인-화면">[메인 화면]</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7683295d-7cb5-4f2b-a742-3910382f7558/image.png" /></p>
<h3 id="2-stm32cubeide">2. <a href="https://www.st.com/en/development-tools/stm32cubeide.html">STM32CubeIDE</a></h3>
<ul>
<li>통합 개발 환경(IDE)로, STM32CubeMX로 프로젝트를 생성하면, 코드 편집기, 컴파일, 다운로드, 디버깅, 시리얼 콘솔 출력 확인 등이 가능하다.</li>
</ul>
<h3 id="메인-화면-1">[메인 화면]</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/63e77699-5e5b-4882-abe4-7dc35483df47/image.png" /></p>
<h3 id="3-cubemx---cubeide-관계">3. CubeMX &lt;-&gt; CubeIDE 관계</h3>
<ul>
<li>CubeMX는 IDE가 없어도 단독 실행 가능하다.</li>
<li>CubeIDE 안에도 CubeMX 기능이 내장되어 있다.<ul>
<li><code>.ioc</code> 파일 더블 클릭</li>
<li>GUI 설정 가능  </li>
</ul>
</li>
</ul>
<blockquote>
<p>CuveMX 에서 tool로 CubeIDE 선택 -&gt; CubeIDE에서 수정</p>
</blockquote>
<ul>
<li>정리하면,<ul>
<li>CubeMX -&gt; 설정툴</li>
<li>CubeIDE -&gt; 개발툴</li>
</ul>
</li>
</ul>
<hr />
<h1 id="datasheet">DataSheet</h1>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/91120046-29e7-405b-b915-b0dd1207e356/image.png" /></p>
<ul>
<li><a href="https://www.st.com/resource/en/data_brief/nucleo-f411re.pdf">NUCLEO-xxxxRx.pdf</a></li>
<li><a href="https://file.notion.so/f/f/6d8dfb15-0001-489c-860f-715cf05a57d7/1a05b4e4-963f-4989-9140-2a66d849444a/stm32f411ce.pdf?table=block&amp;id=2edc5962-3e61-8075-93bd-e75721c72b16&amp;spaceId=6d8dfb15-0001-489c-860f-715cf05a57d7&amp;expirationTimestamp=1768953600000&amp;signature=OYFBXTUotVdjEiYVxaMNU7xzEkCTTTow4FpcgPDYhW8&amp;downloadName=stm32f411ce.pdf">STM32F411xC STM32F411xE.pdf</a></li>
<li><a href="file://C:/Users/KCCISTC/Desktop/NUCLEO-XXXXRX.pdf">NUCLEO-XXXXRX.pdf</a></li>
</ul>
<hr />
<h1 id="stm32f423-block-diagram">STM32F423 BLOCK DIAGRAM</h1>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/10aa745b-9e1b-4ac8-9d5a-2509a949f9ee/image.png" /></p>
<hr />
<h1 id="board-layout">Board Layout</h1>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d112d240-95f2-428a-a3be-720f24a1d6de/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2c1ebd19-4da7-47ca-8749-51d24522c0c8/image.png" /></p>
<hr />
<h3 id="table-1-stm32f411xce-register-boundary-addresses">Table 1. STM32F411xC/E register boundary addresses</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f89c78c4-f548-4982-a8d2-2c87f9d64167/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/31b7ebb3-eab4-4a0d-9767-c75f6939cd02/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f336b335-76e6-40f0-80fa-a84011e8c250/image.png" /></p>
<hr />
<h3 id="table-26-gpio-register-map-and-reset-values">Table 26. GPIO register map and reset values</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1711df86-50f4-4d2e-a5dd-fbdd84b12e6c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7525504c-dcd8-4da6-b00c-459c7896a67a/image.png" /></p>
<hr />
<h3 id="예제---레지스터로만-이용해서-blink">예제 - 레지스터로만 이용해서 blink</h3>
<pre><code class="language-c">int main(){

    *(volatile unsigned int*)0x40023830 |= 1U&lt;&lt;0; //portA enable

    //GPIOA M  

    //ODR

    while(1){
        *(volatile unsigned int*)0x40020014 ^=(1u&lt;&lt;5);

        volatile int delay_count=1000000;
        while(delay_count--){}
    }

}</code></pre>
<hr />
<h2 id="port-configuration">Port Configuration</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/994f5ead-6d78-4c64-b39b-b8988d012d41/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7737539d-7803-4ca6-8d74-ce05ae68f33d/image.png" /></p>
<hr />
<h3 id="figure-29-external-interruptevent-controller-block-diagram">Figure 29. External interrupt/event controller block diagram</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/385ec62e-32c8-440f-adcd-121a183dbf26/image.png" /></p>
<hr />
<h3 id="figure-30-external-interruptevent-gpio-mapping">Figure 30. External interrupt/event GPIO mapping</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bc276321-83a0-4185-b24d-b043054ea081/image.png" /></p>
<hr />
<h3 id="table-38-external-interruptevent-controller-register-map-and-reset-values">Table 38. External interrupt/event controller register map and reset values</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2fffac9b-5833-4186-b9a2-c50307ea7573/image.png" /></p>
<hr />
<h3 id="table-37-vector-table-for-stm32f411xce">Table 37. Vector table for STM32F411xC/E</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cc1d5a19-b295-4a71-a7b8-6038af517c4d/image.png" /></p>
<hr />
<h2 id="dcd와-reset_handler의-의미">DCD와 Reset_Handler의 의미</h2>
<h2 id="1-dcd란">1. DCD란?</h2>
<ul>
<li><p>DCD(Define Constant Doubleword)는 ARM 어셈블리 언어에서 사용하는 디렉티브(지시어)로, 32비트(워드) 단위의 값을 메모리에 저장 및 초기화할 때 사용</p>
</li>
<li><p>쉽게 말해, DCD는 지정된 메모리(주로 벡터 테이블)에 함수 포인터, 상수, 주소 등 4바이트 값을 순차적으로 배치하는 역할을 합니다.</p>
</li>
<li><p>ARM의 공식 DCD 설명:</p>
<blockquote>
<p>DCD 지시문은 하나 이상의 워드(4바이트) 단위 메모리를 할당하고, 그 위치에 초기값을 지정</p>
</blockquote>
</li>
</ul>
<h2 id="2-reset_handler와-dcd의-관계">2. Reset_Handler와 DCD의 관계</h2>
<ul>
<li>ARM Cortex-M, STM32 등 초기화 과정에서 <strong>Vector Table(인터럽트 벡터 테이블)</strong>은 어셈블리로 다음처럼 정의됩니다:</li>
</ul>
<pre><code class="language-nasm">textDCD __initial_sp         ; 초기 스택 포인터
DCD Reset_Handler        ; 리셋 핸들러(초기 진입 지점)
DCD NMI_Handler          ; NMI 핸들러
DCD HardFault_Handler    ; 하드폴트 핸들러
    ...
</code></pre>
<pre><code class="language-nasm">; Reset handler
Reset_Handler    PROC
                 EXPORT  Reset_Handler             [WEAK]
        IMPORT  SystemInit
        IMPORT  __main

                 LDR     R0, =SystemInit
                 BLX     R0
                 LDR     R0, =__main
                 BX      R0
                 ENDP</code></pre>
<ul>
<li>여기서 각 DCD 줄은 해당 핸들러의 '주소값'(함수 포인터)를 4바이트씩 저장하는 역할</li>
<li>CPU가 리셋 등 예외(Interrupt)가 발생했을 때 벡터 테이블의 해당 항목 값을 읽고 그 주소로 점프 </li>
<li>DCD Reset_Handler 부분은 리셋 상황에 진입하면 Reset_Handler 함수의 주소로 점프하라는 뜻</li>
</ul>
<hr />
<h1 id="핵심-정리">핵심 정리</h1>
<ul>
<li><p>DCD는 4바이트 데이터(주로 함수 주소 등)를 메모리에 배치하는 어셈블리 지시어(디렉티브)이다.</p>
</li>
<li><p>Reset_Handler는 리셋 시 CPU가 가장 먼저 실행할 함수(=엔트리 포인트)이다.</p>
</li>
<li><p>DCD Reset_Handler는 벡터 테이블에서 &quot;리셋 시 이 함수로 점프하라&quot;는 의미</p>
</li>
<li><p>DCD는 벡터 테이블 또는 데이터 섹션에 32비트 값을 저장하는 어셈블리 디렉티브</p>
</li>
<li><p>DCD Reset_Handler : 벡터 테이블 내에 Reset_Handler 함수의 주소를 저장하여 리셋 후 가장 먼저 해당 함수가 실행되도록 한다.</p>
</li>
</ul>
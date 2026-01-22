<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a0e5b73b-a867-497c-808f-bb85ee32027d/image.png" /></p>
<ul>
<li><p>DMA란?
cpu의 개입 없이 메모리와 주변장치 간, 또는 메모리 간 데이터를 직접 전송하는 하드웨어 기능
CPU의 부하를 줄이고, 고속 데이터 전송을 가능하게 한다.</p>
</li>
<li><p>STM32 DMA 특징
STM32 MCU는 보통 DMA1, DMA2 두 개의 DMA 컨트롤러를 갖고 있으며, 각각 7~8개의 스트림(stream)과 채널(channel)을 지원</p>
</li>
</ul>
<p>전송 모드</p>
<ul>
<li>정방향(one-shot)</li>
<li>순환(circular) : 버퍼 끝에 도달하면 처음으로 돌아가 계속 전송</li>
<li>인터럽트 발생 : 전송을 다 완료 했을 때, 반전송(데이터 10개를 보내야 할 때 5개쯤 보냈을 경우에 인터럽트 발생하는 경우), 에러 시 인터럽트 발생이 가능하다.</li>
</ul>
<p>주소 증가 모드
우선 순위 설정</p>
<ul>
<li>우선 순위가 높은 인터럽트가 지속해서 발생한다면, 우선 순위가 상대적으로 낮은 다른 인터럽트들이 아무 동작도 안 할수도 있으므로, 우선 순위 설정에는 신중해야 한다.</li>
<li>우선순위가 높더라도 CPU 점유 시간을 일정 시간 정해두는 것도 방법이다.</li>
<li>점유 시간(cnt)가 지나다 보면 우선 순위가 낮아지게 만들어서, 시간적으로 한참 뒤에 동작하게 하는 방법이 있다.</li>
<li>동시 요청시에만 고려</li>
</ul>
<h3 id="dma-구성-요소">DMA 구성 요소</h3>
<p>컨트롤러 : DMA1, DMA2 (각각 독립적)
레지스터 : 전송할 데이터 개수.. 주변장치 주소.. 메모리0, 1 등의 주소.. 등등</p>
<p>DMA 설정 순서(예시)</p>
<ul>
<li>클럭이 들어가지 않으면 동작하지 않는다.</li>
<li>DMA 관련 구조체(핸들 구조체) 초기화</li>
</ul>
<p>DMA 인터럽트 이벤트</p>
<ul>
<li>인터럽트 전송 중 에러가 발생하면..</li>
<li>FIFO 관련 에러..</li>
</ul>
<h3 id="dma-활용-예시">DMA 활용 예시</h3>
<ul>
<li>ADC 데이터 자동 수집</li>
<li>UART, SPI, O2C 통신 데이터 전송/수신</li>
<li>메모리 간 대용량 데이터 복사</li>
<li>오디오, 영상 처리 버퍼 관리 등</li>
</ul>
<hr />
<p>Reference</p>
<ol>
<li><a href="https://www.st.com/resource/en/application_note/an2548-introduction-to-dma-controller-for-stm32-mcus-stmicroelectronics.pdf">Introduction to DMA controller for STM32 MCUs</a></li>
<li><a href="https://deepbluembedded.com/stm32-dma-tutorial-using-direct-memory-access-dma-in-stm32/">STM32 DMA Tutorial – Using Direct Memory Access (DMA) In STM32</a></li>
<li><a href="https://civilpedia.org/p/?t=STM32-DMA-Cheat-Sheet&amp;pid=315">STM32 DMA Cheat Sheet</a></li>
</ol>
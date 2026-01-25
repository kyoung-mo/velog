<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7f53154b-3cc6-4b7c-9de1-acc58f5023b1/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/95150fc4-56db-4800-a541-7f8a8eb866ea/image.png" /></p>
<p>통신관련 alternative? 는 없음</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a67364d8-6d95-4826-97cb-7d0540d6ad07/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/28441b6f-1db1-4ddb-b936-6b7b3c0fed72/image.png" /></p>
<p><code>__weak</code> 있으면 함수 두개일때 컴파일시 <code>__weak</code> 있는게 우선권에서 빠진다.(main에서 작성한 함수가 실행된다.)</p>
<ul>
<li>대부분 콜백함수는 <code>__weak</code>로 되어있음.</li>
<li>main에서 재정의해서 실행</li>
</ul>
<p>PA10~15 하나로 묶였다?</p>
<h4 id="figure-30-external-interruptevent-gpio-mapping">Figure 30. External interrupt/event GPIO mapping</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/32bb95fa-7dea-4e6c-b6a3-bb3ccafa2656/image.png" /></p>
<h4 id="table-38-external-interruptevent-controller-register-map-and-reset-values">Table 38. External interrupt/event controller register map and reset values</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/711b69d8-035f-4a03-8f30-46f563a1a32f/image.png" /></p>
<h4 id="table-37-vector-table-for-stm32f411xce">Table 37. Vector table for STM32F411xC/E</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a4c98994-59db-40f5-9847-28520e6b6cb7/image.png" /></p>
<hr />
<h1 id="polling-vs-interrupt-차이">Polling vs Interrupt 차이</h1>
<h3 id="1-polling">1. Polling</h3>
<ul>
<li>CPU가 반복적으로 확인하다보니 부하가 꽤 큰편</li>
<li>time slice를 만들어줘야함. 이때는 읽고, 이때는 쓰고.. </li>
<li>실시간성이 중요하지 않을 때 사용</li>
</ul>
<h3 id="2-interrupt">2. Interrupt</h3>
<ul>
<li>주변 장치에 변화(이벤트)가 생겼을 때 하드웨어/MCU가 스스로 메인 루프 실행을 멈추고 즉시 미리 정해놓은 인터럽트 서비스 루틴을 실행(아까 재작성했던 콜백함수)</li>
<li>실시간 반응 속도가 매우 우수</li>
<li>코드가 복잡해질 수 있지만, 정교한 실시간 제어가 가능</li>
<li>인터럽트 내에서는 HAL_Delay등 시간 소요되는 부분 최소화.
<code>HAL_Delay(1000);</code> &gt; 함수가 들어오면 Main(CPU)도 못돌고, 인터럽트 처리도 못하기 때문</li>
<li>최대한 빠르게 인터럽트 처리하고 다른 일 다시 시작하는게 좋다.</li>
</ul>
<table>
<thead>
<tr>
<th>구분</th>
<th>Polling(폴링)</th>
<th>Interrupt(인터럽트)</th>
</tr>
</thead>
<tbody><tr>
<td>동작 방식</td>
<td>루프에서 직접 상태 계속 확인</td>
<td>이벤트 발생 시 MCU가 자동으로 반응</td>
</tr>
<tr>
<td>CPU 사용</td>
<td>상태 변화 없을 때도 계속 점유</td>
<td>이벤트 있을 때만 점유, 나머진 다른 일 가능</td>
</tr>
<tr>
<td>실시간성</td>
<td>낮음(지연 발생할 수 있음)</td>
<td>높음(즉각 반응)</td>
</tr>
<tr>
<td>코드 구조</td>
<td>단순, 초보자 구현 용이</td>
<td>다소 복잡, ISR 등 별도 관리 필요</td>
</tr>
<tr>
<td>활용 상황</td>
<td>비중요/단순한 이벤트, 빠른 반응 불필요</td>
<td>중요한 이벤트 즉시 처리, 전력 최적화 원할 때</td>
</tr>
</tbody></table>
<ul>
<li><p><strong>Polling 예시:</strong></p>
<p>  메인 루프에서 반복적으로 <code>HAL_GPIO_ReadPin</code>으로 버튼 상태 확인</p>
</li>
<li><p><strong>Interrupt 예시:</strong></p>
<p>  PC13에 외부 인터럽트(EXTI) 연동, 사용자가 버튼을 누르면 <code>HAL_GPIO_EXTI_Callback</code>이 자동 실행</p>
</li>
</ul>
<hr />
<h3 id="is_gpio_pin-함수"><code>IS_GPIO_PIN()</code> 함수</h3>
<ul>
<li><code>IS_GPIO_PIN()</code> 함수는 요청하려 하는 핀이 GPIO 핀인지 확인하는 형태로 사용한다.</li>
<li>IS_GPIO_PIN은 HAL 함수 내부에서 입력된 핀 번호/비트마스크가 STM32에서 사용 가능한 0~15번 핀에 해당하는지 사전 확인하는 매크로이다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6409ede0-4790-408c-a4fa-d1557c9b1150/image.png" /></p>
<ul>
<li>디버깅 팁 : <code>__disable_irq();</code> 에 break point 잡아본다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4606a2af-434a-4ba9-8f26-a65ae27a390e/image.png" /></p>
<p>PA5 : GPIOA의 5번 핀?</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cc47f4d1-a120-4e1a-ad7a-fc6031e6428c/image.png" /></p>
<ul>
<li>디버그 상태에서 오른쪽 메뉴( <code>SFRs</code> )를 통해 어떤 레지스터를 사용중인지 확인 가능하다.</li>
</ul>
<hr />
<h3 id="stm32cube-펌웨어-구성도">STM32Cube 펌웨어 구성도</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a8e863e7-e6bd-4a9f-8864-cf4855dccc96/image.png" /></p>
<h3 id="폴링-방식-예제">폴링 방식 예제</h3>
<pre><code class="language-c">#ifdef __GNUC__
  #define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
  #define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif

PUTCHAR_PROTOTYPE
{
  HAL_UART_Transmit(&amp;huart2, (uint8_t *)&amp;ch, 1, 0xFFFF);
  return ch;
}
---
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {

      //char *msg = &quot;Hello STM32!\r\n&quot;;
      // HAL_UART_Transmit(&amp;huart2, (uint8_t*)msg, strlen(msg), 10);
      printf(&quot;Hello STM32 printf%d\r\n&quot;,10);
      HAL_Delay(1000);

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cfe00dc3-49bb-42c3-867d-89b6bada6d97/image.png" /></p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cd6cdd1f-818b-4cbb-a1dd-8ab68e4a4c5d/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/105c0601-ebb3-4820-b60a-717029b2096d/image.png" /></p>
<h3 id="인터럽트-방식-예제">인터럽트 방식 예제</h3>
<p>main.c</p>
<pre><code class="language-c">/* USER CODE BEGIN Includes */
#include &lt;stdio.h&gt;
/* USER CODE END Includes */
---
/* USER CODE BEGIN PFP */
#ifdef __GNUC__
  #define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
  #define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif

PUTCHAR_PROTOTYPE
{
  HAL_UART_Transmit(&amp;huart2, (uint8_t *)&amp;ch, 1, 0xFFFF);
  return ch;
}
/* USER CODE END PFP */

---
/* USER CODE BEGIN 0 */
uint8_t rxData;
uint8_t txData[] = &quot;UART Interrupt Started!\r\n&quot;;
/* USER CODE END 0 */
---
/* USER CODE BEGIN 2 */
HAL_UART_Transmit_IT(&amp;huart2,txData,sizeof(txData));
HAL_UART_Receive_IT(&amp;huart2, &amp;rxData, 1);
/* USER CODE END 2 */
---
/* USER CODE BEGIN 4 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
    printf(&quot;received : %s \r\n&quot;,&amp;rxData);

    if(huart-&gt;Instance == USART2){
        HAL_UART_Receive_IT(huart, &amp;rxData, 1);}
}

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart){

}
/* USER CODE END 4 */</code></pre>
<p>stm32f4xx_it.c</p>
<pre><code class="language-c">/**
  * @brief This function handles Memory management fault.
  */
void MemManage_Handler(void)
{
  /* USER CODE BEGIN MemoryManagement_IRQn 0 */

  /* USER CODE END MemoryManagement_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_MemoryManagement_IRQn 0 */
      HAL_UART_IRQHandler(&amp;huart2);
    /* USER CODE END W1_MemoryManagement_IRQn 0 */
  }
}
</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ec9580c1-4db6-4054-af9e-d9b9313b92ca/image.png" /></p>
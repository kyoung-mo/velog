<p>아두이노에서 사용하던 함수는 STM32에서는 그대로 사용하지 못한다.
STM32 HAL의 <code>GPIO HAL API</code> 를 사용하면 된다.</p>
<table>
<thead>
<tr>
<th>Arduino</th>
<th>STM32 HAL</th>
</tr>
</thead>
<tbody><tr>
<td><code>pinMode(pin, OUTPUT)</code></td>
<td><code>HAL_GPIO_Init()</code></td>
</tr>
<tr>
<td><code>digitalWrite(pin, HIGH/LOW)</code></td>
<td><code>HAL_GPIO_WritePin()</code></td>
</tr>
<tr>
<td><code>digitalRead(pin)</code></td>
<td><code>HAL_GPIO_ReadPin()</code></td>
</tr>
<tr>
<td><code>delay(ms)</code></td>
<td><code>HAL_Delay(ms)</code></td>
</tr>
</tbody></table>
<ul>
<li>미들웨어</li>
<li>유틸리티</li>
<li>HAL 레벨 : 하드웨어 구동 위한 소프트웨어(BSP)를 받아야함</li>
</ul>
<p>HAL 드라이버는 여러가지 주변 장치 설정을 위한 데이터 구조체와 주변 장치의 구동을 위한 API 함수가 포함되어 있는 여러 개의 파일로 구성</p>
<h3 id="대표적인-hal-드라이버-종류">대표적인 HAL 드라이버 종류</h3>
<ul>
<li>RCC 중요 ★ : 클럭을 넣어줘야 동작하기 때문</li>
<li>DMA : 직접 메모리 접근(버스 기반 데이터 전송)</li>
<li>USART/UART 직렬 통신(동기 / 비동기)<ul>
<li>S가 붙으면 동기</li>
<li>UART는 비동기</li>
</ul>
</li>
<li>SPI : 직렬 주변장치 인터페이스</li>
<li>I2C : 인터-IC 통신(풀업방식)</li>
<li>CAN : 자동차에서 내부의 네트워크 연결을 할 때 가장 많이 사용, 제어 장치가 있을때 장비와 장비 사이의 통신에 사용</li>
</ul>
<h3 id="hal-드라이버용-데이터-구조체">HAL 드라이버용 데이터 구조체</h3>
<h4 id="stm32fxx_hal_timh">stm32fxx_hal_tim.h</h4>
<pre><code class="language-c">/** 
  * @brief  TIM Time Base Handle Structure definition  
  */ 
typedef struct
{
  TIM_TypeDef                 *Instance;     /*!&lt; Register base address             */
  TIM_Base_InitTypeDef        Init;          /*!&lt; TIM Time Base required parameters */
  HAL_TIM_ActiveChannel       Channel;       /*!&lt; Active channel                    */
  DMA_HandleTypeDef           *hdma[7];      /*!&lt; DMA Handlers array
                                             This array is accessed by a @ref DMA_Handle_index */
  HAL_LockTypeDef             Lock;          /*!&lt; Locking object                    */
  __IO HAL_TIM_StateTypeDef   State;         /*!&lt; TIM operation state               */
}TIM_HandleTypeDef;</code></pre>
<ul>
<li>소프트웨어가 동시에 접속하면 안되므로, 확인하는 용으로 Lock 사용</li>
<li>실제 메모리 상에서 쓰는건 <code>*Instance</code> ~ <code>*hdmap[7]</code> 까지</li>
</ul>
<h4 id="stmstm32fxx_hal_uarth">stmstm32fxx_hal_uart.h</h4>
<pre><code class="language-c">/** 
  * @brief  UART handle Structure definition  
  */  
typedef struct
{
  USART_TypeDef                 *Instance;        /*!&lt; UART registers base address        */

  UART_InitTypeDef              Init;             /*!&lt; UART communication parameters      */

  uint8_t                       *pTxBuffPtr;      /*!&lt; Pointer to UART Tx transfer Buffer */

  uint16_t                      TxXferSize;       /*!&lt; UART Tx Transfer size              */

  uint16_t                      TxXferCount;      /*!&lt; UART Tx Transfer Counter           */

  uint8_t                       *pRxBuffPtr;      /*!&lt; Pointer to UART Rx transfer Buffer */

  uint16_t                      RxXferSize;       /*!&lt; UART Rx Transfer size              */

  uint16_t                      RxXferCount;      /*!&lt; UART Rx Transfer Counter           */  

  DMA_HandleTypeDef             *hdmatx;          /*!&lt; UART Tx DMA Handle parameters      */

  DMA_HandleTypeDef             *hdmarx;          /*!&lt; UART Rx DMA Handle parameters      */

  HAL_LockTypeDef               Lock;             /*!&lt; Locking object                     */

  __IO HAL_UART_StateTypeDef    gState;           /*!&lt; UART state information related to global Handle management 
                                                       and also related to Tx operations.
                                                       This parameter can be a value of @ref HAL_UART_StateTypeDef */

  __IO HAL_UART_StateTypeDef    RxState;          /*!&lt; UART state information related to Rx operations.
                                                       This parameter can be a value of @ref HAL_UART_StateTypeDef */

  __IO uint32_t                 ErrorCode;        /*!&lt; UART Error code                    */

}UART_HandleTypeDef;</code></pre>
<ul>
<li>GPIO, SYSTICK, NVIC 등은 핸들 구조체를 사용하지 않는다.</li>
</ul>
<h4 id="gpio_inittype_def">GPIO_InitType_def</h4>
<pre><code class="language-c">/** 
  * @brief GPIO Init structure definition  
  */ 
typedef struct
{
  uint32_t Pin;       /*!&lt; Specifies the GPIO pins to be configured.
                           This parameter can be any value of @ref GPIO_pins_define */

  uint32_t Mode;      /*!&lt; Specifies the operating mode for the selected pins.
                           This parameter can be a value of @ref GPIO_mode_define */

  uint32_t Pull;      /*!&lt; Specifies the Pull-up or Pull-Down activation for the selected pins.
                           This parameter can be a value of @ref GPIO_pull_define */

  uint32_t Speed;     /*!&lt; Specifies the speed for the selected pins.
                           This parameter can be a value of @ref GPIO_speed_define */

  uint32_t Alternate;  /*!&lt; Peripheral to be connected to the selected pins. 
                            This parameter can be a value of @ref GPIO_Alternate_function_selection */
}GPIO_InitTypeDef;</code></pre>
<p>Alternate : GPIO긴 한데 통신 등 다른쪽으로 사용할지 말지 정함</p>
<ul>
<li>작업행용 구조체 : 특정한 작업을 수행하기 위해 API 함수 내에서 사용되는 구조체</li>
<li><code>HAR_PPP_Process</code> 구조와 동작 방식</li>
</ul>
<pre><code class="language-c">HAL_StatusTypeDef;
AL_PPP_Process(PPP_HandleTypeDef *hppp, PPP_ProcessConfigTypeDef *sConfig);</code></pre>
<p>PPP_HandleTypeEdf * hpp : 객체 handle</p>
<ul>
<li>해당 주변 장치의 핸들 구조체(상태, 설정 등 보유)</li>
</ul>
<p>동작 흐름</p>
<ol>
<li>함수 호출</li>
<li>인터럽트 핸들러 등록 <code>HAL_PPP_IRQHandler()</code> 호출</li>
<li>콜백 함수 동작 <ul>
<li>작업 완료 시 <code>__weak void</code></li>
<li>에러 발생 시 <code>__weake void</code></li>
</ul>
</li>
</ol>
<h3 id="hal-api-이름-규칙">HAL API 이름 규칙</h3>
<ul>
<li>형식<ul>
<li>`HAL  </li>
</ul>
</li>
<li>확장(Extension) 함수 규칙<ul>
<li>예시) <code>HAL_ADCEx_InjectedStart()</code></li>
</ul>
</li>
</ul>
<p>2026-01-19(월) stm32) 실습 과정 정리</p>
<h3 id="datasheet">DataSheet</h3>
<ul>
<li><p><a href="https://www.st.com/resource/en/data_brief/nucleo-f411re.pdf">NUCLEO-xxxxRx.pdf</a></p>
</li>
<li><p><a href="file://C:/Users/KCCISTC/Desktop/stm32f411ce.pdf">STM32F411xC STM32F411xE.pdf</a></p>
</li>
</ul>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/eed95ec3-5230-4481-b7dc-c93e1b2667ed/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a04c91d9-ff4f-4463-b8c2-b6befd046a9e/image.png" /></p>
<p>chip이 103, F4 이렇게 두 개 있는데,
103같은 경우 Window와 연결하면 메모리의 일부가 하드웨어로 잡힌다.
컴퓨터에서 stm32 하드웨어 부분으로 펌웨어 실행 파일 <code>.bin</code> 을 넣어주면 자동으로 <code>103 -&gt; F4</code> 칩으로 전송된다. 하지만 일반적인 방법은 아님.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bcd23870-0ef1-450d-a246-fac22831516b/image.png" /></p>
<p><a href="file://C:/Users/KCCISTC/STM32Cube/Repository/19168.pdf">MB1136-DEFAULT-C04 Board schematic.pdf</a>
X3 저거 중요하댔는데.. 왜?
<img alt="" src="https://velog.velcdn.com/images/mommers/post/b2aa5b83-9b3a-4a54-adf3-5ebe9f0cd961/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1e16a9c8-7d0e-434e-a315-fb8449531fc5/image.png" /></p>
<ul>
<li>vcc, ground는 노란색 , 바꿀 수 없음</li>
<li>연두색은 reset, boot 등 바꿀수있나..?</li>
</ul>
<hr />
<ol>
<li>공통 Collector, 공통 Drain </li>
</ol>
<ul>
<li>풀업 저항 역할 (풀업 돼있다는 조건하에)</li>
</ul>
<ol start="2">
<li>push, pull</li>
</ol>
<ul>
<li>올라가고 내려오는 속도 좀 더 빠르게(고속)</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0c01c2d6-f21e-444c-bab2-3092214fe763/image.png" /></p>
<p>핀 읽는법</p>
<ul>
<li>polling -&gt; 1ms check -&gt; cpu 바쁨</li>
<li>interrupt : 엣지가 발생할 때 인터럽트 관련 함수 등록하면 발생시켜줘 -&gt; cpu는 동작을 안함.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9c0fbd96-cf15-4d27-bd6a-4ede6921c14b/image.png" /></p>
<p>인풋 인터럽트, 아웃풋 인터럽트 혹은 인풋일때, 아웃풋일때마다 이런 식으로 선택 가능하다. (GPIO mode)
default는 falling edge 일때를 많이 사용한다.</p>
<p>아웃풋은 큰 의미 없고, pin Name Input일때
통신 관련해서는 us까지 내려가나, LED(gpio?)의 경우에는 속도가 어느정도 정해져있음.</p>
<p>PA 5번 핀이다, PC13번 핀이다 라고 나와있지만 User Label의 값으로도 사용 가능.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7a16b9b6-7efc-4889-a476-3c22c0efbe4a/image.png" /></p>
<p>통신 관련해서는 GPIO mode를 <code>Alternate Function Push Pull</code>로 설정해야함.
통신 관련해서는 고속으로 동작해야하기 때문</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/86fbb307-7b13-41ff-afd2-2b4aa4d0c5fa/image.png" /></p>
<ul>
<li>Interrupt 관련된 부분. NVIC 메뉴에서.
15~10번 핀에서 인터럽트 걸렸을때 동작(?)</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ecf9c835-fcb1-45df-b721-482bfc8d8ef1/image.png" /></p>
<ul>
<li>?? 뭔가 뚝딱뚝딱 하심.
datasheet에 공식 같이 정리되어있다고 합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dd6fb6d5-9256-4d1d-9e3a-7fea01de4181/image.png" /></p>
<p>맘대로 설정했다가 빨간색 표시 나오면 위의 Resolve Clock Issues 클릭하면 어느정도 재설정을 해주나, 동작 안 할수도 있음.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fa6c91dc-5688-4ff8-8f38-aa258f0e7962/image.png" /></p>
<p>설계가 잘 되어있으면 Max_Speed로 동작할 것</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7530eb9a-88cd-4d5b-ada2-7c8695a0c04b/image.png" /></p>
<p>코어마다 두 번째 줄의 버전이 다르다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0e99802f-605e-4055-aa4c-580e542268ef/image.png" /></p>
<ul>
<li>ToolChain : <del>MDK 위주로 실습할예정</del></li>
<li>오류로 인해 STM32CubeIDE로 설정 후, STM32IDE로 실습 예정</li>
</ul>
<hr />
<h2 id="stm32---led-실습">STM32 - LED 실습)</h2>
<pre><code class="language-c">/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include &quot;main.h&quot;

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
    *(volatile unsigned int*)0x40023830 |= 1U&lt;&lt;0; //portA enable

    //GPIOA M

    //ODR

    while(1){
        *(volatile unsigned int*)0x40020014 ^=(1u&lt;&lt;5);

        volatile int delay_count=10000000;
        while(delay_count--){}
    }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&amp;RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&amp;RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&amp;huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &amp;GPIO_InitStruct);

  /*Configure GPIO pin : LD2_Pin */
  GPIO_InitStruct.Pin = LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LD2_GPIO_Port, &amp;GPIO_InitStruct);

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if(GPIO_Pin == GPIO_PIN_13)
    {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf(&quot;Wrong parameters value: file %s on line %d\r\n&quot;, file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */</code></pre>
<h2 id="주의할-점">주의할 점</h2>
<ul>
<li>코드에 보면 아래처럼 생긴 주석이 있다.<pre><code class="language-c">/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
  if(GPIO_Pin == GPIO_PIN_13)
  {
      HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  }
}

</code></pre>
</li>
</ul>
<p>/* USER CODE END 4 */</p>
<p>```</p>
<ul>
<li><code>BEGIN</code> ~ <code>END</code> 사이에 코드를 작성해야만 한다.</li>
<li>위 범위를 벗어나서 코드를 작성하면, CUBE MX 사용하여 코드 재생성( <code>Generate Code</code> )시 코드 유실 위험이 있다.</li>
</ul>
<hr />
<h2 id="이해-x-해결해야할-것">이해 x) 해결해야할 것</h2>
<ol>
<li>짜여져 있는 코드를 통해 결과는 나왔으나, 이 코드가 왜 LED를 동작시킬 때 저 주소가 GPIO 13번 핀에 해당하는지에 대해 이해 못했다.</li>
<li>GPIO 13번 핀에 대해 아두이노 처럼 동작하는(지금 예제처럼 직접 주소로 접근하는것이 아닌.. ) 과정도 작성 못해봤다.</li>
<li>해당 주소를 찾으려면 DataSheet에서 어떻게 찾아야 하는지 파악을 못했다.</li>
<li>주석이면 상관 없겠지 ~ 했던 부분에서 코드 유실되는게 놀라웠다.
주석 부분 신경 쓸 것. 그리고 전체적으로 CUBE MX를 통해 프로젝트를 작성했을 때, 주석이 큰 틀로 봤을 때 어떻게 구성되어있는지 정리할 것.</li>
</ol>
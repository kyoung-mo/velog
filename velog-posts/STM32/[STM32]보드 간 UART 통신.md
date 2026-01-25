<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b69c04f2-6f26-47ec-82e6-d90c514b42d8/image.png" /></p>
<p>아악 성공했다!!</p>
<p>물론 CLAUDE AI의 도움을 받았습니다.</p>
<p><del>GPT는 계속 빙빙 돌았는데.. 역시 코드는 claude</del></p>
<p>하드웨어 배선, CubeMX를 통해 핀 설정을 해주는것까지는 진행했는데 STM32 관련 코드는 익숙하지 않아 AI를 사용했습니다.</p>
<p>이제 내걸로 만들기 위해 개념 정리를 해봅시다..</p>
<p>사용 보드 :  STM32F411RET6U (?) F4 시리즈 뉴클레어 보드를 사용했습니다.</p>
<hr />
<h2 id="1-하드웨어-구성">1. 하드웨어 구성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/98ae3610-dcb6-42b5-8018-5ce467dc56de/image.png" /></p>
<p>위 사진과 같습니다.</p>
<ul>
<li>보드A <code>USART2_TX(PA9)</code> &lt;-&gt; 보드B <code>USART2_RX(PA10)</code></li>
<li>보드B <code>USART2_TX(PA9)</code> &lt;-&gt; 보드A <code>USART2_RX(PA10)</code></li>
<li>공통 <code>GND</code> (각 보드의 그라운드끼리 연결)</li>
</ul>
<p>USART1 ~ USART6과 관련된 핀이 있으나 USART2번 핀을 사용한 이유는 상대방에게 데이터를 송신 및 수신 하는 USART와 수신받은 데이터를 내 컴퓨터랑 USART 통신을 통해 화면에 띄우는 과정을 나누고 싶었기 때문입니다.</p>
<p>그래서 USART1(PA2번 핀, PA3번 핀)은 상대방으로부터 수신받은 데이터를 본인 컴퓨터의 시리얼모니터에 띄우는 용도, USART2(PA9번 핀, PA10번 핀)은 내가 입력한 데이터를 상대방에게 송신, 상대방이 입력한 데이터를 수신하기 위해 역할을 나누었습니다.</p>
<p>아래 그림을 참조하여 하드웨어 배선을 했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4d4fe186-9211-46a4-9d8b-4aa3deffc588/image.png" /></p>
<hr />
<h2 id="2-핀-배치">2. 핀 배치</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/47a8da6d-b6e3-4efb-a475-d97ef3448eee/image.png" /></p>
<hr />
<ul>
<li><ol>
<li>USART2 CUBEMX 설정</li>
</ol>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c55e7227-ae7c-4a55-bd81-5a2b680a2105/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9ecc9659-cf30-40fd-8c4a-fecb28026b9b/image.png" /></p>
<ul>
<li><ol start="2">
<li>USART1 CUBEMX 설정</li>
</ol>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/00b37e0a-c37b-4a0d-9217-4e8d9648a157/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b0bd6465-7312-420d-afbd-cb0d969d1d9a/image.png" /></p>
<ul>
<li>이후 <code>GENERATE CODE</code> 를 하면 <code>stm32f4xx_it.c</code> 코드 상에 아래처럼 추가된 모습을 확인할 수 있다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8360c9ae-78d3-4013-a40d-90fcab014e03/image.png" /></p>
<hr />
<h3 id="3-coresrcmainc-코드">3. ./Core/Src/main.c 코드</h3>
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
#include &lt;stdio.h&gt;
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
UART_HandleTypeDef huart1;
UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_USART2_UART_Init(void);
/* USER CODE BEGIN PFP */
#ifdef __GNUC__
  #define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
  #define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif

PUTCHAR_PROTOTYPE
{
  HAL_UART_Transmit(&amp;huart2, (uint8_t *)&amp;ch, 1, HAL_MAX_DELAY);
  return ch;
}
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
uint8_t rxDataFromBoard;  // 상대 보드로부터 받은 데이터 (USART1)
uint8_t rxDataFromPC;     // PC로부터 받은 데이터 (USART2)
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
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */
  // USART2 (PA2, PA3): PC와 통신 (ST-Link Virtual COM Port)
  HAL_UART_Receive_IT(&amp;huart2, &amp;rxDataFromPC, 1);

  // USART1 (PA9, PA10): 상대 보드와 통신
  HAL_UART_Receive_IT(&amp;huart1, &amp;rxDataFromBoard, 1);

  printf(&quot;UART Communication Started!\r\n&quot;);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
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
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&amp;huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

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

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &amp;GPIO_InitStruct);

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart-&gt;Instance == USART2)
    {
        // PC로부터 데이터 수신 → 상대 보드로 전송 (USART1 사용)
        HAL_UART_Transmit(&amp;huart1, &amp;rxDataFromPC, 1, 100);
        HAL_UART_Receive_IT(&amp;huart2, &amp;rxDataFromPC, 1);
    }
    else if (huart-&gt;Instance == USART1)
    {
        // 상대 보드로부터 데이터 수신 → PC로 전송
        HAL_UART_Transmit(&amp;huart2, &amp;rxDataFromBoard, 1, 100);
        HAL_UART_Receive_IT(&amp;huart1, &amp;rxDataFromBoard, 1);
    }
}

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
    // 전송 완료 콜백 (필요시 사용)
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
<hr />
<p>각 보드에 같은 코드를 넣고, 각자 컴퓨터로 시리얼 모니터를 실행했을 때, 다음과 같이 통신이 가능하다.(상대방이 입력한 글자)</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c74aae7a-2ea8-4e5a-aab8-8874b4d6070b/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b69c04f2-6f26-47ec-82e6-d90c514b42d8/image.png" /></p>
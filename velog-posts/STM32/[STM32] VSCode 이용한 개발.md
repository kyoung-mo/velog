<p>CubeMX, CubeIDE 등의 툴을 사용해서 프로젝트를 진행하는 방식 외에, VSCode를 이용해서 프로젝트를 진행할 수 있다.</p>
<hr />
<ol>
<li>profile 생성</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/56b4d458-6753-4aaa-b2ba-7eb27aa19ff6/image.png" /></p>
<ol start="2">
<li>extensions 설치 : 사진에 있는 STM32CubeIDE for Visual Studio Code 를 설치해주면 왼쪽에 있는 관련 extension이 전부 설치된다.</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3b9f273a-6f15-4e7b-9687-1e7ee9840e9a/image.png" /></p>
<ol start="3">
<li>extensions 사용 : 왼쪽에 새로 생긴 stm32 extension에 들어가면 Launch~~ 가 나온다.</li>
</ol>
<p>기존에 STM32CubeMX는 설치되어 있었기 때문에 바로 실행이 되고,</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b3cf7217-9839-48f7-87fc-9a21b2af9c6e/image.png" /></p>
<p>STMCUFinder 같은 경우는 설치가 안되어 있어서, 파일을 찾거나 다운로드 가능했다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/4c2470de-4efe-4437-bf8e-a1dba8407468/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/31f6a778-aada-41fd-a2cc-debf4458a65c/image.png" /></p>
<hr />
<p>vscode에서 cudemx를 이용해 프로젝트를 만들어주자. 프로젝트 ToolChain/IDE는 CMake로 설정해준다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0cfc1006-26e3-41c0-9425-7daef63939b2/image.png" /></p>
<p>ADC1 -&gt; IN0 IN1 체크 후 Generate Code</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3530d5a1-9a35-4390-baa7-07123c7f67a4/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ed1a75a9-85b4-4184-92c5-f8da606dc170/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/91a0a371-777b-4869-be27-a270d41032f2/image.png" /></p>
<ul>
<li>ADC 프로젝트가 생성된 것을 확인할 수 있다(CMake).</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/31f4e72d-b992-4b9e-85fe-f39cf4ca3d48/image.png" /></p>
<ul>
<li>VSCode 상에서 open Folder -&gt; 아까 만든 프로젝트 디렉토리로 설정</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ee92a852-cedc-4397-9224-1b3fbeafbe38/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e847dfd7-f790-42b1-bf2d-db422b085d4b/image.png" /></p>
<p>VSCode 상에 추가된 것을 확인할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/da4b3517-4cfa-45a9-baeb-215291b4fe24/image.png" /></p>
<p>extention 관련 오류인지, 계속 이것저것 설치가 안되어 있는거 같아서 Claude에게 물어봐서 해결했다.. 수업 진도 속도가 빠르다보니 수업 따라가다가 캡쳐를 못했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/70d58ee1-7614-44e8-acb0-e83d9de578ed/image.png" /></p>
<p>무료 요금제 다 써서 결제해주고</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d890dc96-700c-49b8-b2e7-84ceacbcc508/image.png" /></p>
<p>Project Manager에서 Code Generator -&gt; 두번째 칸의 <code>Generate peripheral initialization as a pair of '.c/.h' files per peripheral</code> 을 체크해줘야 내가 따로 프로젝트에 추가한 APP 파일 관련 코드들()이 생성된다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a34f57a1-443c-45d0-9f90-63247a1c50e1/image.png" /></p>
<p>다시 한번 DMA 세팅을 정리하면 아래와 같다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/068068cc-5df7-4f9a-bc10-f3c216e62882/image.png" /></p>
<p>Parameter Settings</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4d565d9c-9ba4-4a74-bb0d-13fd1b15c332/image.png" /></p>
<p>DMA Settings</p>
<hr />
<p>CubeMX에서는 이렇게 설정하고 코드는 아래와 같이 설정해주었다.</p>
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
#include &quot;adc.h&quot;
#include &quot;dma.h&quot;
#include &quot;usart.h&quot;
#include &quot;gpio.h&quot;

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include &quot;ap.h&quot;
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

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
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
  MX_DMA_Init();
  MX_USART2_UART_Init();
  MX_ADC1_Init();
  /* USER CODE BEGIN 2 */
  //hwInit();
  apInit();
  apMain();
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
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 100;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
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

  if (HAL_RCC_ClockConfig(&amp;RCC_ClkInitStruct, FLASH_LATENCY_3) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

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
<p>저번에 설치했던 Teleplot을 사용해서 시리얼 통신을 해주면, 조이스틱 x축, y축을 조정해줄때마다 값이 바뀌는 것을 확인할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/76676b3f-01d2-4dcf-b7df-73a907795581/image.png" /></p>
<hr />
<p>추가로 프로젝트 위치에 추가할 APP 파일, 수정해야할 CMAKE 전체 파일을 압축 파일로 올려두겠습니다.</p>
<ol>
<li>APP -&gt; 프로젝트 디렉터리</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d33df5d7-aa75-4b29-9c36-52af6e009e56/image.png" /></p>
<ol start="2">
<li>CMakeList.txt</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/320744a4-4e1f-4dfc-9ee4-607248a47416/image.png" /></p>
<pre><code class="language-c">cmake_minimum_required(VERSION 3.22)

#
# This file is generated only once,
# and is not re-generated if converter is called multiple times.
#
# User is free to modify the file as much as necessary
#

# Setup compiler settings
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)


# Define the build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE &quot;Debug&quot;)
endif()

# Set the project name
set(CMAKE_PROJECT_NAME ADC)

# Enable compile command to ease indexing with e.g. clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

# Core project settings
project(${CMAKE_PROJECT_NAME})
message(&quot;Build type: &quot; ${CMAKE_BUILD_TYPE})

# Enable CMake support for ASM and C languages
enable_language(C ASM)

# Create an executable object type
add_executable(${CMAKE_PROJECT_NAME})

# Add STM32CubeMX generated sources
add_subdirectory(cmake/stm32cubemx)

# Link directories setup
target_link_directories(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined library search paths
)
file(GLOB SRC_FILES CONFIGURE_DEPENDS
  App/ap/*.c
  App/common/src/*.c
  App/hw/*.c
  App/hw/src/*.c   
)

# Add sources to executable
target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user sources here
    ${SRC_FILES}
)

# Add include paths
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined include paths
    App/ap
    App/common
    App/common/include
    App/hw
    App/hw/include
)
# Add project symbols (macros)
target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE
#     # Add user defined symbols
)

target_compile_options(${CMAKE_PROJECT_NAME}  PRIVATE
  -Wno-expansion-to-defined
  -Os
)

add_custom_command(TARGET ${CMAKE_PROJECT_NAME} 
  POST_BUILD
  COMMAND ${CMAKE_OBJCOPY} ARGS -O binary ${CMAKE_PROJECT_NAME}.elf ${CMAKE_PROJECT_NAME}.bin
  COMMENT &quot;Invoking: Make Binary&quot;
  )  

add_custom_command(TARGET ${CMAKE_PROJECT_NAME} 
  POST_BUILD
  COMMAND ${CMAKE_OBJCOPY} ARGS -O ihex ${CMAKE_PROJECT_NAME}.elf ${CMAKE_PROJECT_NAME}.hex
  COMMENT &quot;Invoking: Make Hex&quot;
  )    


# Remove wrong libob.a library dependency when using cpp files
list(REMOVE_ITEM CMAKE_C_IMPLICIT_LINK_LIBRARIES ob)

# Add linked libraries
target_link_libraries(${CMAKE_PROJECT_NAME}
    stm32cubemx

    # Add user defined libraries
)
</code></pre>
<p>2) 내장 온도 감지 센서 이용 -&gt; t값 그래프로 출력</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/85cb53b8-0bfb-4806-b433-c80ddae7dc7b/image.png" /></p>
<p>CubeMX에서 위쪽 <code>Temperature Sensor Channel</code> 체크, 아래쪽에서는 ADC_Regular_ConversionMode -&gt; Number Of Conversion : 3으로 수정,</p>
<pre><code>Rank 3 설정)
    Channel -&gt; Channel Temperature Sensor
    Sampling Time -&gt; 480 Cycles</code></pre><p>Channel Temperature Sensor는 위에 Mode에서 Temperature Sensor Channel 체크를 안 하면 안 뜬다!</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/92a35354-f868-468d-89cf-48c82e5bd0e7/image.png" /></p>
<p>정리하면, Mode &gt; IN0, IN1, Temperature Sensor Channel 체크, Configuration은 아래와 같이 설정(다른 설정은 이전 예제와 똑같이)</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/23cd2f95-b629-4007-89db-1ca76f5cc190/image.png" /></p>
<hr />
<h4 id="코드--위-예제와-동일">코드 : 위 예제와 동일</h4>
<h4 id="실행-결과">실행 결과)</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/80a6974c-0e35-4a0d-bb91-c067ac4b55c7/image.png" /></p>
<pre><code class="language-c"></code></pre>
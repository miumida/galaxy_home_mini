# Galaxy Cloud Speak Notify

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.0.0][version-shield]

Smartthings API를 이용한 Galaxy Cloud Speak Notify for Homeassistant입니다.<br>
Smartthings API token을 발급받아야 사용가능합니다. 갤럭시 홈 또는 갤럭시 홈 미니 디바이스도 필요합니다.<br>
TTS와는 다르며, cache 파일이 생성되지 않습니다. 네트워크가 끊어진 상태에서는 사용할 수 없습니다.<br>

- 개발자도구 > 서비스<br>
![screenshot_1](https://github.com/miumida/galaxy_cloud_speak/blob/master/images/ha_dev_tool.png?raw=true)<br>
message 길이는 최대 1000자 입니다.(한글 기준인지는 잘 모르겠습니다. Max Length 1000 이라고만 되어 있어서...)<br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2020.08.26  | First version  |

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/galaxy_cloud_speak/__init__.py`<br>
  `<config directory>/custom_components/galaxy_cloud_speak/manifest.json`<br>
  `<config directory>/custom_components/galaxy_cloud_speak/notify.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/miumida/galaxy_cloud_speak' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, galaxy_cloud_speak 검색하여 설치

<br>

## Usage
### configuration
- HA 설정에 galaxy_cloud_speak notify를 추가합니다.<br>
```yaml
notify:
  - platform: galaxy_cloud_speak
    name: galaxy_cloud_speak
    token: [Smartthings API token]
    device_id: [galaxy home mini deviceId]
```

<br>

## Smartthings API Token
'<https://account.smartthings.com/tokens>' 사이트로 접속하여 로그인합니다.<br>
'새 토큰 만들기'를 눌러서 토큰을 생성합니다.<br>
![smartthings_token_1](https://github.com/miumida/galaxy_cloud_speak/blob/master/images/smartthings_token_1.png?raw=true)<br>
토큰 이름을 입력하고, 권한 범위에서 `장치를 전체 체크`하고 저장하면 토큰이 생성됩니다.<br>
![smartthings_token_2](https://github.com/miumida/galaxy_cloud_speak/blob/master/images/smartthings_token_2.png?raw=true)<br>
생성된 토큰은 잘 복사해 둡니다.<br>

<br>

## Device ID
생성한 token으로 갤럭시 홈 또는 갤럭시 홈 미니의 Device ID를 확인합니다.<br>
'smartthins_devices.py'를 다운로드 받아 실행하여 device 목록을 확인한다.<br>
```python
python3 smartthins_devices.py {발급받은 토큰}
```

<br>

## 참고사이트
[1] In development | 갤럭시 홈 미니 API로 말 시키기 (<https://5mango.com/speak-on-galaxy-home-mini-using-api/>)<br>

[version-shield]: https://img.shields.io/badge/version-v1.0.0-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg

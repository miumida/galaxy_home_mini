# Galaxy Cloud Speak Notify

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.0.0][version-shield]

Smartthings API를 이용한 Galaxy Cloud Speak Notify for Homeassistant입니다.<br>
Smartthings API token을 발급받아야 사용가능합니다. 갤럭시 홈 또는 갤럭시 홈 미니 디바이스도 필요합니다.<br>

- 개발자도구 > 서비스<br>
![screenshot_1](https://github.com/miumida/galaxy_cloud_speak/blob/master/images/ha_dev_tool.png?raw=true)<br>

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
- 'https://github.com/miumida/galaxy_cloud_notify' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, galaxy_cloud_speak 검색하여 설치

<br>

## Usage
### configuration
- HA 설정에 galaxy_cloud_speak notify를 추가합니다.<br>
```yaml
notify:
  - platform: galaxy_cloud_speak
    name: galmini
    token: [Smartthings API token]
```

<br>

## Smartthings API Token
'<https://account.smartthings.com/tokens>' 사이트로 접속하여 token을 발급받습니다.<br>

<br>

## 참고사이트
[1] In development | 갤럭시 홈 미니 API로 말 시키기 (<https://5mango.com/speak-on-galaxy-home-mini-using-api/>)<br>

[version-shield]: https://img.shields.io/badge/version-v1.0.0-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg

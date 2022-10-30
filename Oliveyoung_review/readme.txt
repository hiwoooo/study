1. 프로그램 개요 (요청사항)
 - 올리브영 제품 리뷰 크롤링

2. 사용법 (CMD)

파일 실행 전 설치파일
python -m pip install chromedriver_autoinstaller
python -m pip install git+https://github.com/GNuSeekK/Keesung_logging.git

필요시 추가 설치
python -m pip install selenium
python -m pip install subprocess


파일 실행 : python main"N".py "csv파일"
    (1) cmd창을 통해 main"N" (1~4) 파일을 실행한다
    (2) chrome 창이 뜨면 원하는 만큼 창을 띄우고 엔터를 누른다
        4개의 창을 띄우는 것을 기본으로, main1 ~ main4를 순서대로 실행한다.
        main1을 실행할 때 4개의 창을 띄우고
        main2 ~ main4를 실행할 때 뜨는 창은 끄고 난 뒤 enter를 누른다
    (3) 창을 어느정도 정리하여 크롤링이 실행되는 것을 확인한다.

3. 저장되는 파일 명

main.py와 같은 폴더의 Result에 저장된다
"제품명".csv
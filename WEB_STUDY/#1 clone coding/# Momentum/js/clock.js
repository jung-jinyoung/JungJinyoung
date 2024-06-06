const clock = document.querySelector("#clock")

function getClock(){
    const date = new Date()
    // String 타입에서 사용할 수 있는 padStart,padEnd 
    // 문자열의 길이가 주어진 값보다 작을 때, 앞 또는 뒤에 해당 문자를 부족한 수 만큼 채운다.
    const hours = String(date.getHours()).padStart(2,"0")
    const minutes = String(date.getMinutes()).padStart(2,"0")
    const seconds = String(date.getSeconds()).padStart(2,"0")

    clock.textContent = `${hours}:${minutes}:${seconds}`
}

// setInterval(getClock,2000) // => 정해진 매초 마다 함수 실행
// setTimeout(sayHello,5000) => 정해진 초 뒤에 함수 실행 

// 순서 : 페이지가 로드 되자마자 시계 출력
getClock()
setInterval(getClock,1000)
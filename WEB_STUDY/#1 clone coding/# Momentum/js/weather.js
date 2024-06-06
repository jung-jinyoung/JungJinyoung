function onGeoOk(position){
    // 현재 위도와 경도 불러오기 
    const lat = position.coords.latitude
    const lon = position.coords.longitude
    const API_Key = '188ebc00b2781481d8232ca896dc564e'
    let url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_Key}`
    console.log(url)
    
    // 비동기적 처리 
    fetch(url)
        .then((response)=> {
            response.json()
            .then( (data)=> {
                const city = document.querySelector('#weather span:first-child')
                const weather = document.querySelector('#weather span:last-child')
                
                city.textContent =  data.name + '  : '

                const temp = Math.round(((data.main.temp - 273.15) * 5 / 9)+32)
                weather.textContent = `${temp}° / ${data.weather[0].main}`
            })
        })
}

function onGeoError(){
    alert('Can\'nt find you..!') 
}

// 현재 위치에 대한 정보를 알려주는 내장 함수
navigator.geolocation.getCurrentPosition(onGeoOk, onGeoError)
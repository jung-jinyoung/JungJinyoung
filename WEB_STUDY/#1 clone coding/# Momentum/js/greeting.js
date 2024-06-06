const loginForm = document.querySelector('#login-form')
const loginInput = document.querySelector('#login-form input')
const greetingTag = document.querySelector('#greeting')

// 이전에 로그인을 했을 경우 (localStorage에 저장된 데이터를 활용)
// 함수 작성
function paintGreetings(username){
    greetingTag.textContent = `Hello, ${username} 🤗`
    greetingTag.classList.remove("hidden")
}

// 로그인을 하지 않았을 경우
// login form에 대한 이벤트 함수 작성 
function onLoginSubmit(event){
    event.preventDefault()
    loginForm.classList.add("hidden")
    const username = loginInput.value
    localStorage.setItem("username",username)
    paintGreetings(username)
}


// 저장된 데이터 가져오기 (없다면 null)
const savedUsername = localStorage.getItem("username")
if (savedUsername === null) {
    // 로그인 하지 않았으면 로그인 이벤트 함수 
    // 로그인 폼 보이고 이벤트 함수 
    loginForm.classList.remove("hidden")
    loginForm.addEventListener("submit",onLoginSubmit)

} else {
    // 로그인한 데이터가 있다면 "환영" 텍스트 출력 
    paintGreetings(savedUsername)
}
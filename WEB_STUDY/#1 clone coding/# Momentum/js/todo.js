const todoForm = document.querySelector('#todo-form')
const todoInput = todoForm.querySelector('input')
const todoList = document.querySelector('#todo-list')
const boxTag = document.querySelector('.box')


// 로컬 저장소에 저장하기
// 계속 추가 삭제 하기 위해 배열 생성
let toDos = []
function saveTodos() {
    
    // 배열 전체로 저장하기 위한 문자열 변환 
    localStorage.setItem("todos",JSON.stringify(toDos)) 
}


function deleteTodo(event){
    // 삭제 
    const li = event.target.parentElement
    // 삭제할 요소를 제외한 Element 그대로 반환 (filter)
    // localStorage에서도 업데이트
    toDos = toDos.filter( (todo) => todo.id!== parseInt(li.id))
    li.remove()
    // 업데이트 후 저장
    saveTodos()
    // todoList.removeChild(event.target.parentElement)
    
}

// todo 항목 추가하기
function paintTodo(newTodo){
    const liTag = document.createElement('li')
    
    const spanTag = document.createElement('span')
    // id 속성으로 제공
    liTag.id = newTodo.id
    spanTag.textContent = newTodo.text +'    '
    
    const button = document.createElement('button')
    button.textContent = "x"
    button.addEventListener('click',deleteTodo)
    
    liTag.appendChild(spanTag)
    liTag.appendChild(button)
    todoList.appendChild(liTag)
    boxTag.classList.remove('hidden')
    
}


// 새로운 todo 받기
function handleTodoSubmit(event) {
    event.preventDefault()
    const newTodo = todoInput.value // 저장 
    todoInput.value = "" //초기화 
    
    // CRUD를 위한 id 설정 후 객체 저장 
    const newTodoObj = {
        text:newTodo,
        id : Date.now()
    }
    toDos.push(newTodoObj)
    paintTodo(newTodoObj) // 항목에 추가해서 조회하기
    
    // 로컬 저장소에 저장하기 
    saveTodos()
    
}
todoForm.addEventListener('submit',handleTodoSubmit)
// 저장된 todos를 parse => 다시 객체 형태로 변환
const savedTodos = localStorage.getItem("todos")
if (savedTodos) {
    const parsedTodos = JSON.parse(savedTodos)
    toDos = parsedTodos // 다시 배열로 저장해주기 
    parsedTodos.forEach(paintTodo)
}
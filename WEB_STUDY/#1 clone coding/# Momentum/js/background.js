// unsplash 랜덤 이미지 가져오기

const imgUrl = 'https://source.unsplash.com/random/?nature/1024x768'
const bgImg = document.createElement('img')
// bgImg.setAttribute('src',imgUrl)
bgImg.src = imgUrl
bgImg.classList.add('bgImg')

document.body.appendChild(bgImg)
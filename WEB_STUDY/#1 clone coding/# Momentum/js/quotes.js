const quotes = [
    {
        quote : 'What would life be if we had no courage to attempt anything?',
        author : 'Vincent Van Gogh '
    },
    {
        quote: 'Reading is to the mind what exercise is to the body. ',
        author: 'Joseph Addison '
    },
    {
        quote:'Change your life today. Don\'t gamble on the future, act now, without delay.',
        author:'Simone de Beauvoir'
    },
    {
        quote:'No matter what people tell you, words and ideas can change the world. ',
        author:'Robin Williams '
    },
    {
        quote:'Innovation distinguishes between a leader and a follower.',
        author:' Steve Jobs'
    },
    {
        quote:'All change is not growth, as all movement is not forward.',
        author:'Ellen Glasgow'
    },
    {
        quote: 'If you\'re going through hell, keep going.',
        author: 'Winston Churchill '
    },
    {
        quote: 'A rebirth out of spiritual adversity causes us to become new creatures.',
        author: 'James E. Faust '
    },
    {
        quote: 'Where there is great love, there are always wishes.',
        author: 'Willa Cather'
    },
    {
        quote: 'Anyone who has never made a mistake has never tried anything new. ',
        author: 'Albert Einstein '
    }
]

// 해당 자식 태그 요소들을 불러오는 방법 : 태그명: first-child ...
const quote =  document.querySelector("#quote span:first-child")
const author =  document.querySelector("#quote span:last-child")

// 랜덤 인덱스를 가져와서 출력
// Math.random() * N => 0~N-1 까지의 수를 가져옴
// 내림 숫자로 가져오기 


const todayQuote =  quotes[Math.floor(Math.random()*quotes.length)]
quote.textContent = todayQuote.quote
author.textContent = '-'+todayQuote.author

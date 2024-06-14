import { createRouter, createWebHistory } from 'vue-router'
import HomePageView from '@/views/HomePageView.vue'
import Recommend from '@/components/Recommend.vue'
import BookPageView from '@/views/BookPageView.vue'
import MoviePageView from '@/views/MoviePageView.vue'
import SelectMood from '@/components/SelectMood.vue'
import Modal from '@/components/Modal.vue'

// 회원가입 및 로그인 관련 불러오기 
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import { useAuthStore } from '@/stores/counter'

// 커뮤티니 + 유저 페이지 관련 불러오기
import UserPageView from '@/views/UserPageView.vue'
import RankingView from '@/views/RankingView.vue'
import Review from '@/components/Review.vue'
import ReviewContent from '@/components/ReviewContent.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePageView
    },
    {
      path: '/selectmood',
      name: 'selectmood',
      component: SelectMood
    },
    {
      path : '/signup',
      name : 'SignUpView',
      component: SignUpView
    },
    {
      path : '/login',
      name : 'LogInView',
      component: LogInView
    },
    {
      path: '/greeting',
      name: 'Modal',
      component: Modal
    },
    {
      path: '/recommend/:mood',
      name: 'recommend',
      component: Recommend
    },
    {
      path: '/recommend/book/:bookIsbn/:mood',
      name: 'bookpage',
      component: BookPageView
    },
    {
      path: '/recommend/movie/:movie_id',
      name: 'moviepage',
      component: MoviePageView
    },
    {
      path : '/profile/:username',
      name : 'Profile',
      component : UserPageView,
    },
    {
      path : '/review',
      name : 'review',
      component : Review,
      children : [
        {
          path: ':review_id',
          name : 'ReviewContent',
          component : ReviewContent
        }
      ]
    }
    ,

    { 
      path : '/ranking',
      name : 'Ranking',
      component : RankingView
    }
  ]
})


router.beforeEach((to, from) => {
  const store = useAuthStore()
  // 인증되지 않은 사용자는 유저 페이지에 접근 할 수 없음 (추후 작성 예정)
  
  // 인증된 사용자는 회원가입과 로그인 페이지에 접근 할 수 없음
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin === true)) {
    window.alert('You’re already signed in 😓')
    return { name: 'home' }
  }
})

export default router
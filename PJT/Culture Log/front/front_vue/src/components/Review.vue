<template>
  <div class="review_container">
    <h2 style="margin-bottom: 0;">📁</h2>
    <h3>{{ username }}님의 기록 페이지</h3>
    <div class="review_list">
      <div v-if="!props.reviews || paginatedReviews">
        <div v-for="review in paginatedReviews" :key="review.id">
          <p @click="openReview(review?.id) " class="review-item">
            🔸 {{ review.created_at }}
            </p>
            <hr>
        </div>
      </div>
      <div v-else style="margin-top:150px">
        <p>{{ username }}님의 기록을 기다리는 중. . .</p>
      </div>
      
      <div class="pagination_controls">
        <button @click="prevPage" :disabled="currentPage === 1">◀</button>
        <button @click="nextPage" :disabled="currentPage === totalPages">▶</button>
      </div>
    </div>
  
   <!-- 모달 -->
   <div v-if="is_choiced" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <ReviewContent 
          :review="choicedReview"
          :is_choiced="is_choiced"
          @update ="updateReview"
          @delete = "deleteReview"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, computed } from 'vue';
import ReviewContent from './ReviewContent.vue';
import { useUsersStore } from "@/stores/users";

const props = defineProps({
  reviews: Array,
  username: String
});

const is_choiced = ref(false);
const current =ref(null)
const choicedReview = computed(()=>{
  return props.reviews.find((review) => review.id === current.value )
})

// 리뷰 삭제 시 해당 뷰 끄기
const deleteReview = function() {
  is_choiced.value =false

}

// 리뷰 선택시 해당 리뷰 보여주기 : 수정된 리뷰를 조회하기 위해 새로 작성 

const openReview = (id) => {
  current.value = id
  is_choiced.value =true
}

// 일주일 단위로 리뷰 보여주기
const currentPage = ref(1);
const reviewsPerPage = 5;

const totalPages = computed(() => Math.ceil(props.reviews.length / reviewsPerPage));

// 페이지 넘기기 
const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * reviewsPerPage;
  const end = start + reviewsPerPage;
  return props.reviews.slice(start, end);
});


// 모달 닫기 기능
const closeModal = () => {
  is_choiced.value = false;
};


const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
  }
};

const userStore = useUsersStore();
const updateReview = function() {
  userStore.user_detail(props.username)
  const userId = userStore.user.userId
  userStore.get_reviews(userId)
  console.log('done!')
}

</script>

<style scoped>

  .review-item {
    cursor: pointer; /* 커서를 손 모양으로 변경 */
  }

  .review-item:hover {
    background: rgba(140, 140, 140, 0.423);
    color: #fbfbfb;
    text-shadow: 0 0 5px white;
    padding : 5px 0
  }
.review_container {
  display: flex;
  text-align: center;
  flex-direction: column;
  padding: 10px 15px;
  min-height: 530px;
}
 
.review_list {
  flex: 3;
  padding-top: 30px;
  padding-left: 20px;
  padding-right: 20px;
  margin-bottom: 20px;
  align-items: center;
  background-color: rgba(229, 229, 229, 0.542);
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 400px;
  position: relative;
}

.pagination_controls {
  display: flex;
  justify-content: center;
  position: absolute;
  bottom: 0;
  width: 100%;
  background-color: rgba(229, 229, 229, 0.542);
  padding: 10px 0;
  margin-top:20px
}

.pagination_controls button {
  margin: 0 5px;
}

.content {
  margin-top: 5px;
  text-align: center;
  overflow-y: auto;
}

/* 모달 스타일 */
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 5% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 25px;
  color: #aaa;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>

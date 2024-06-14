import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useUsersStore = defineStore('Users', () => {
  const user = ref({
    username: null,
    userImg: null,
    userId: null,
    reviews: [],
    followers: 0,
    followings: 0,
    followers_list: []
  });

  const getUserId = () => {
    return user.value.userId;
  };

  const user_detail = (username) => {
    axios.get(`http://127.0.0.1:8000/api/v1/users/${username}/`)
      .then((response) => {
        user.value.username = username;
        user.value.followers_list = response.data.followers;
        user.value.userImg = `/profile_images/${response.data.profileImg}`;
        user.value.userId = response.data.id;

        get_reviews(user.value.userId);
        get_info_follow(user.value.userId);
      })
      .catch((error) => { console.log(error); });
  };

  const get_reviews = (userId) => {
    axios.get(`http://127.0.0.1:8000/api/v1/cultures/reviews/user/${userId}/`)
      .then((response) => {
        user.value.reviews = response.data;
      })
      .catch((error) => { console.log(error); });
  };

  const get_info_follow = (userId) => {
    axios.get(`http://127.0.0.1:8000/api/v1/users/${userId}/follow-stats/`)
      .then((response) => {
        user.value.followers = response.data.followers_count;
        user.value.followings = response.data.following_count;
      })
      .catch((error) => { console.log(error); });
  };

  const updateFollowCounts = () => {
    axios.get(`http://127.0.0.1:8000/api/v1/users/${user.value.userId}/follow-stats/`)
      .then((response) => {
        user.value.followers = response.data.followers_count;
        user.value.followings = response.data.following_count;
      })
      .catch((error) => { console.log(error); });
  };

  const isFollowing = computed(() => {
    return user.value.followers_list.some(follower => follower.username === now_user.value);
  });

  const followUser = (userId, token) => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/users/${userId}/follow/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then(() => {
        updateFollowCounts();
      })
      .catch((error) => { console.log(error); });
  };

  const users = ref(null)

  const get_users = function(){
    axios({
      method : 'get',
      url : 'http://127.0.0.1:8000/api/v1/users/',
    })
      .then((response) => {
      users.value = response.data
    })
      .catch((error)=>{console.log(error)})
  }

  return {
    user,
    getUserId, // 추가된 부분
    user_detail,
    get_reviews,
    get_info_follow,
    updateFollowCounts,
    isFollowing,
    followUser,
    get_users,
    users
  };
}, { persist: true });

import { ref } from 'vue'

export function useGeolocation() {
  const lat = ref(null)
  const lon = ref(null)
  const isPositionReady = ref(false)

  function getCurrentPosition() {
    if (!navigator.geolocation) {
      setAlert('위치 정보를 찾을 수 없습니다.')
    } else {
      navigator.geolocation.getCurrentPosition(getPositionValue, geolocationError)
    }
  }

  function getPositionValue(val) {
    lat.value = val.coords.latitude
    lon.value = val.coords.longitude
    isPositionReady.value = true
  }

  function geolocationError() {
    setAlert('위치 정보를 찾을 수 없습니다.')
  }

  function setAlert(text) {
    alert(text)
  }

  return { lat, lon, isPositionReady, getCurrentPosition }
}

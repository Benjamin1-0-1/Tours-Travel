import axios from 'axios';

const BASE_URL = '/api'; // Nginx proxies /api to Flask backend

export function getAllTours() {
  return axios.get(`${BASE_URL}/tours`);
}

export function getTourDetail(tourId) {
  return axios.get(`${BASE_URL}/tours/${tourId}`);
}

// Auth
export function registerUser({ email, password, fullName }) {
  return axios.post(`${BASE_URL}/auth/register`, { email, password, fullName });
}

export function loginUser({ email, password }) {
  return axios.post(`${BASE_URL}/auth/login`, { email, password });
}

// Reviews
export function getReviews(tourId) {
  return axios.get(`${BASE_URL}/tours/${tourId}/reviews`);
}

export function postReview(tourId, reviewData) {
  return axios.post(`${BASE_URL}/tours/${tourId}/reviews`, reviewData);
}

// Bookings
export function bookTour(data, token) {
  return axios.post(`${BASE_URL}/bookings`, data, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
}

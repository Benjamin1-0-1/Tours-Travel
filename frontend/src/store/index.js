// src/store/index.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import toursReducer from './slices/toursSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    tours: toursReducer
  }
});

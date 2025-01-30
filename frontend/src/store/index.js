// frontend/src/store/index.js
import { configureStore } from '@reduxjs/toolkit';
import toursReducer from './slices/toursSlice';
import userReducer from './slices/userSlice';

export const store = configureStore({
  reducer: {
    tours: toursReducer,
    user: userReducer
  }
});

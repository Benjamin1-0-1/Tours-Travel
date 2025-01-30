// frontend/src/store/slices/userSlice.js
import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    token: null,
    email: null
  },
  reducers: {
    setCredentials: (state, action) => {
      const { token, email } = action.payload;
      state.token = token;
      state.email = email;
    },
    logout: (state) => {
      state.token = null;
      state.email = null;
    }
  }
});

export const { setCredentials, logout } = userSlice.actions;
export default userSlice.reducer;

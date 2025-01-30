// frontend/src/store/slices/toursSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Example fetch tours from Flask
export const fetchTours = createAsyncThunk(
  'tours/fetchTours',
  async () => {
    const response = await axios.get('http://localhost:5500/apis/tours/v1/tours');
    return response.data.tours; // based on your API response
  }
);

const toursSlice = createSlice({
  name: 'tours',
  initialState: {
    tours: [],
    status: 'idle',
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTours.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTours.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.tours = action.payload; // array of tours
      })
      .addCase(fetchTours.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export default toursSlice.reducer;

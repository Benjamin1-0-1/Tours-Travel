// src/store/slices/toursSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// If your route is "http://localhost:5500/apis/tours/v1/tours"
const TOURS_LIST_URL = 'http://localhost:5500/apis/tours/v1/tours';

export const fetchTours = createAsyncThunk(
  'tours/fetchTours',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get(TOURS_LIST_URL);
      // Suppose response is { "tours": [ { ... }, ... ] }
      return response.data.tours;
    } catch (err) {
      return rejectWithValue('Failed to fetch tours');
    }
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
        state.tours = action.payload;
      })
      .addCase(fetchTours.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  },
});

export default toursSlice.reducer;

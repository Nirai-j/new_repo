// File structure outline for the Travel Agency Enterprise React Application

/**
 * Project Structure:
 * 
 * /src
 *   /assets
 *   /components
 *     /common
 *     /layout
 *     /features
 *   /config
 *   /context
 *   /hooks
 *   /pages
 *   /services
 *   /state
 *   /types
 *   /utils
 */

// App.tsx - Main application entry point
import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import { LoadingSpinner } from './components/common/LoadingSpinner';
import { ToastContainer } from './components/common/ToastContainer';
import { MainLayout } from './components/layout/MainLayout';
import { ProtectedRoute } from './components/common/ProtectedRoute';

// Lazy-loaded pages for code splitting
const HomePage = React.lazy(() => import('./pages/HomePage'));
const LoginPage = React.lazy(() => import('./pages/auth/LoginPage'));
const RegisterPage = React.lazy(() => import('./pages/auth/RegisterPage'));
const DashboardPage = React.lazy(() => import('./pages/dashboard/DashboardPage'));
const SearchPage = React.lazy(() => import('./pages/search/SearchPage'));
const BookingPage = React.lazy(() => import('./pages/booking/BookingPage'));
const PaymentPage = React.lazy(() => import('./pages/payment/PaymentPage'));
const ProfilePage = React.lazy(() => import('./pages/profile/ProfilePage'));
const AdminDashboard = React.lazy(() => import('./pages/admin/AdminDashboard'));
const NotFoundPage = React.lazy(() => import('./pages/NotFoundPage'));

// Create React Query client with configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <ThemeProvider>
            <BrowserRouter>
              <ToastContainer />
              <Suspense fallback={<LoadingSpinner />}>
                <Routes>
                  {/* Public routes */}
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  
                  {/* Routes within main layout */}
                  <Route path="/" element={<MainLayout />}>
                    <Route index element={<HomePage />} />
                    <Route path="search" element={<SearchPage />} />
                    
                    {/* Protected routes requiring authentication */}
                    <Route element={<ProtectedRoute />}>
                      <Route path="dashboard" element={<DashboardPage />} />
                      <Route path="booking/:id" element={<BookingPage />} />
                      <Route path="payment/:bookingId" element={<PaymentPage />} />
                      <Route path="profile" element={<ProfilePage />} />
                    </Route>
                    
                    {/* Admin routes requiring admin role */}
                    <Route element={<ProtectedRoute requiredRole="admin" />}>
                      <Route path="admin/*" element={<AdminDashboard />} />
                    </Route>
                  </Route>
                  
                  {/* 404 and fallback routes */}
                  <Route path="/404" element={<NotFoundPage />} />
                  <Route path="*" element={<Navigate to="/404" replace />} />
                </Routes>
              </Suspense>
            </BrowserRouter>
          </ThemeProvider>
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;

// src/components/layout/MainLayout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Footer } from './Footer';
import { Sidebar } from './Sidebar';
import { useAuth } from '../../hooks/useAuth';

export const MainLayout = () => {
  const { isAuthenticated } = useAuth();
  
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-grow">
        {isAuthenticated && <Sidebar />}
        <main className="flex-grow p-4">
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  );
};

// src/context/AuthContext.tsx
import React, { createContext, useReducer, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { authService } from '../services/authService';
import { User } from '../types/user';

type AuthState = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
};

type AuthAction =
  | { type: 'LOGIN_REQUEST' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'REFRESH_TOKEN_SUCCESS'; payload: User };

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

const AuthContext = createContext<{
  state: AuthState;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}>({
  state: initialState,
  login: async () => {},
  logout: () => {},
  refreshToken: async () => {},
});

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN_REQUEST':
      return { ...state, isLoading: true, error: null };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: true,
        user: action.payload,
        error: null,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: false,
        user: null,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
      };
    case 'REFRESH_TOKEN_SUCCESS':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: true,
        user: action.payload,
      };
    default:
      return state;
  }
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for token on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        dispatch({ type: 'LOGIN_FAILURE', payload: 'No token found' });
        return;
      }
      
      try {
        // Verify token validity
        const decoded = jwtDecode<{ exp: number }>(token);
        if (decoded.exp * 1000 < Date.now()) {
          await refreshToken();
        } else {
          const user = await authService.getCurrentUser();
          dispatch({ type: 'LOGIN_SUCCESS', payload: user });
        }
      } catch (error) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        dispatch({ type: 'LOGIN_FAILURE', payload: 'Invalid token' });
      }
    };
    
    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_REQUEST' });
    try {
      const { accessToken, refreshToken, user } = await authService.login(email, password);
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', refreshToken);
      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE', payload: (error as Error).message });
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    dispatch({ type: 'LOGOUT' });
  };

  const refreshToken = async () => {
    const refreshTokenValue = localStorage.getItem('refreshToken');
    if (!refreshTokenValue) {
      dispatch({ type: 'LOGIN_FAILURE', payload: 'No refresh token' });
      return;
    }
    
    try {
      const { accessToken, refreshToken: newRefreshToken, user } = 
        await authService.refreshToken(refreshTokenValue);
      
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', newRefreshToken);
      dispatch({ type: 'REFRESH_TOKEN_SUCCESS', payload: user });
    } catch (error) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      dispatch({ type: 'LOGIN_FAILURE', payload: 'Failed to refresh token' });
    }
  };

  return (
    <AuthContext.Provider value={{ state, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// src/services/api.ts
import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';

// Create API service with interceptors for authentication and error handling
class Api {
  private axiosInstance: AxiosInstance;
  private refreshingPromise: Promise<string> | null = null;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: process.env.REACT_APP_API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.axiosInstance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('accessToken');
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for token refresh
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
        
        // If error is 401 and we haven't tried to refresh the token yet
        if (
          error.response?.status === 401 &&
          !originalRequest._retry &&
          localStorage.getItem('refreshToken')
        ) {
          if (!this.refreshingPromise) {
            // Create a promise to refresh the token
            this.refreshingPromise = this.refreshToken();
          }

          try {
            // Wait for the token refresh to complete
            const newToken = await this.refreshingPromise;
            this.refreshingPromise = null;
            
            // Retry the original request
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${newToken}`;
            }
            originalRequest._retry = true;
            return this.axiosInstance(originalRequest);
          } catch (refreshError) {
            this.refreshingPromise = null;
            // If refresh fails, log out
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );
  }

  private async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/auth/refresh`,
        { refreshToken }
      );
      
      const { accessToken, refreshToken: newRefreshToken } = response.data;
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', newRefreshToken);
      
      return accessToken;
    } catch (error) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      throw error;
    }
  }

  // Generic request methods
  async get<T>(url: string, config?: AxiosRequestConfig) {
    const response = await this.axiosInstance.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig) {
    const response = await this.axiosInstance.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig) {
    const response = await this.axiosInstance.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig) {
    const response = await this.axiosInstance.delete<T>(url, config);
    return response.data;
  }
}

export const api = new Api();

// src/services/travelService.ts
import { api } from './api';
import { SearchParams, SearchResults, Destination, Package, Booking } from '../types/travel';

export const travelService = {
  // Search functionality
  async searchDestinations(params: SearchParams): Promise<SearchResults> {
    return api.get('/destinations/search', { params });
  },
  
  // Destination details
  async getDestination(id: string): Promise<Destination> {
    return api.get(`/destinations/${id}`);
  },
  
  // Travel packages
  async getPackages(destinationId?: string): Promise<Package[]> {
    return api.get('/packages', { params: { destinationId } });
  },
  
  async getPackageDetails(id: string): Promise<Package> {
    return api.get(`/packages/${id}`);
  },
  
  // Bookings
  async createBooking(bookingData: Partial<Booking>): Promise<Booking> {
    return api.post('/bookings', bookingData);
  },
  
  async getUserBookings(): Promise<Booking[]> {
    return api.get('/bookings/user');
  },
  
  async getBookingDetails(id: string): Promise<Booking> {
    return api.get(`/bookings/${id}`);
  },
  
  async cancelBooking(id: string): Promise<{ success: boolean }> {
    return api.put(`/bookings/${id}/cancel`);
  },
  
  // Reviews and ratings
  async submitReview(packageId: string, rating: number, comment: string) {
    return api.post(`/reviews`, { packageId, rating, comment });
  },
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { REFRESH_TOKEN, ACCESS_TOKEN } from '../constants';

export async function refreshToken() {
  const refreshToken = localStorage.getItem(REFRESH_TOKEN);
  if (!refreshToken) return false;

  try {
    const response = await axios.post('/api/token/refresh/', { refresh: refreshToken });
    if (response.status === 200) {
      localStorage.setItem(ACCESS_TOKEN, response.data.access);
      return true;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
  }

  return false;
}

export function isAuthenticated() {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (!token) return false;

  try {
    const decoded = jwtDecode(token);
    const tokenExpiration = decoded.exp;
    const now = Date.now() / 1000;

    return tokenExpiration > now;
  } catch (error) {
    console.error('Error decoding token:', error);
    return false;
  }
}

export function isSuperuser() {
  const user = JSON.parse(localStorage.getItem('user'));
  return user && user.is_superuser === true;
}
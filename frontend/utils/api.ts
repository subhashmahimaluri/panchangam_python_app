/**
 * API client functions for Panchangam backend
 */

import {
  ApiError,
  PanchangamRequest,
  PanchangamResponse,
} from "../types/panchangam";

const API_BASE_URL = "http://localhost:8000/api";

/**
 * Fetch Panchangam data from the backend API
 */
export async function fetchPanchangamData(
  request: PanchangamRequest
): Promise<PanchangamResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/panchangam`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData: ApiError = await response.json();
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching Panchangam data:", error);
    throw error;
  }
}

/**
 * Fetch supported cities from the backend API
 */
export async function fetchSupportedCities() {
  try {
    const response = await fetch(`${API_BASE_URL}/cities`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching supported cities:", error);
    throw error;
  }
}

/**
 * Check if the API is healthy
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL.replace("/api", "")}/health`);
    return response.ok;
  } catch (error) {
    console.error("API health check failed:", error);
    return false;
  }
}
